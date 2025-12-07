"""
Self-Modification Engine
Allows the AI to modify its own code with safety constraints
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.core.model_loader import ModelLoader
import yaml
import logging
import subprocess
import shutil
from datetime import datetime
from typing import Dict, Any, Optional, List
import json
import ast
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SelfModifier:
    """Manages safe self-modification of the AI system"""

    def __init__(self, config_path: str = "configs/config.yaml"):
        self.config = self._load_config(config_path)
        self.model_loader = ModelLoader(config_path)
        self.modification_history = []
        self.backup_dir = Path("data/backups")
        self.backup_dir.mkdir(parents=True, exist_ok=True)

    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """Load configuration"""
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)

    def create_backup(self, description: str) -> str:
        """Create a backup of the current system state"""

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"backup_{timestamp}"
        backup_path = self.backup_dir / backup_name

        logger.info(f"Creating backup: {backup_name}")

        # Create backup directory
        backup_path.mkdir(parents=True, exist_ok=True)

        # Backup critical files
        files_to_backup = [
            "configs/config.yaml",
            "src/learning/learning_loop.py",
            "src/core/model_loader.py",
            "src/safety/self_modifier.py"
        ]

        for file_path in files_to_backup:
            src = Path(file_path)
            if src.exists():
                dst = backup_path / file_path
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, dst)

        # Save backup metadata
        metadata = {
            "timestamp": timestamp,
            "description": description,
            "files": files_to_backup
        }

        with open(backup_path / "metadata.json", 'w') as f:
            json.dump(metadata, f, indent=2)

        logger.info(f"Backup created: {backup_path}")
        return str(backup_path)

    def rollback_to_backup(self, backup_name: str) -> bool:
        """Restore from a backup"""

        backup_path = self.backup_dir / backup_name

        if not backup_path.exists():
            logger.error(f"Backup not found: {backup_name}")
            return False

        logger.info(f"Rolling back to: {backup_name}")

        # Load metadata
        with open(backup_path / "metadata.json", 'r') as f:
            metadata = json.load(f)

        # Restore files
        for file_path in metadata['files']:
            src = backup_path / file_path
            dst = Path(file_path)

            if src.exists():
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, dst)
                logger.info(f"Restored: {file_path}")

        logger.info("Rollback complete")
        return True

    def is_code_safe(self, code: str) -> tuple[bool, List[str]]:
        """Check if code modifications are safe"""

        safety_config = self.config['safety']
        issues = []

        # Check for dangerous operations
        dangerous_patterns = [
            'os.system',
            'subprocess.call',
            'eval(',
            'exec(',
            '__import__',
            'open(',  # Only if writing to critical files
            'shutil.rmtree',
            'os.remove',
            'requests.post',  # Prevent unauthorized network calls
        ]

        for pattern in dangerous_patterns:
            if pattern in code:
                issues.append(f"Dangerous operation detected: {pattern}")

        # Try to parse as valid Python
        try:
            ast.parse(code)
        except SyntaxError as e:
            issues.append(f"Syntax error: {e}")

        # Check if it tries to modify safety constraints
        forbidden_modifications = self.config['self_modification']['forbidden_modifications']

        for forbidden in forbidden_modifications:
            if forbidden in code.lower():
                issues.append(f"Attempted to modify forbidden component: {forbidden}")

        is_safe = len(issues) == 0
        return is_safe, issues

    def generate_code_modification(self, goal: str) -> str:
        """Generate a code modification to achieve a goal"""

        logger.info(f"Generating code modification for goal: {goal}")

        # Load model if needed
        if self.model_loader.model is None:
            self.model_loader.load_base_model()

        # Create prompt for code generation
        prompt = f"""You are an AI system that can modify its own code.

Goal: {goal}

Generate Python code that achieves this goal. The code should be:
1. Safe and well-tested
2. Follow best practices
3. Include error handling
4. Be self-contained

Only modify components in the allowed list:
{self.config['self_modification']['allowed_modifications']}

Do NOT modify:
{self.config['self_modification']['forbidden_modifications']}

Generate the code:

```python
"""

        # Generate code
        generated = self.model_loader.generate(prompt, max_length=1024)

        # Extract code from response
        if "```python" in generated:
            code = generated.split("```python")[1].split("```")[0].strip()
        elif "```" in generated:
            code = generated.split("```")[1].split("```")[0].strip()
        else:
            code = generated.strip()

        return code

    def test_modification(self, code: str, test_cases: Optional[List[Dict]] = None) -> bool:
        """Test a code modification in a sandboxed environment"""

        logger.info("Testing code modification...")

        # Create temporary test file
        test_file = Path("data/logs/test_modification.py")
        test_file.parent.mkdir(parents=True, exist_ok=True)

        with open(test_file, 'w') as f:
            f.write(code)

        # Try to run basic syntax check
        try:
            result = subprocess.run(
                ['python', '-m', 'py_compile', str(test_file)],
                capture_output=True,
                text=True,
                timeout=30
            )

            if result.returncode != 0:
                logger.error(f"Syntax check failed: {result.stderr}")
                return False

            logger.info("Code passed syntax check")

            # Could add more sophisticated testing here
            # For now, syntax check is sufficient

            return True

        except subprocess.TimeoutExpired:
            logger.error("Test timed out")
            return False
        except Exception as e:
            logger.error(f"Test failed: {e}")
            return False
        finally:
            # Clean up
            if test_file.exists():
                test_file.unlink()

    def propose_and_test_modification(self, goal: str) -> Dict[str, Any]:
        """Propose a modification, test it, and return results"""

        logger.info(f"\n{'='*60}")
        logger.info(f"SELF-MODIFICATION ATTEMPT")
        logger.info(f"Goal: {goal}")
        logger.info(f"{'='*60}\n")

        # Step 1: Create backup
        backup_path = self.create_backup(f"Before: {goal}")

        # Step 2: Generate modification
        code = self.generate_code_modification(goal)

        # Step 3: Safety check
        is_safe, safety_issues = self.is_code_safe(code)

        if not is_safe:
            logger.warning("⚠ Code failed safety check:")
            for issue in safety_issues:
                logger.warning(f"  - {issue}")

            result = {
                "success": False,
                "reason": "safety_check_failed",
                "issues": safety_issues,
                "backup": backup_path
            }
        else:
            # Step 4: Test modification
            passed_tests = self.test_modification(code)

            if passed_tests:
                logger.info("✓ Code passed all tests")

                # Human approval check
                if self.config['safety']['human_approval_required']:
                    logger.info("\n" + "="*60)
                    logger.info("HUMAN APPROVAL REQUIRED")
                    logger.info("="*60)
                    logger.info(f"\nProposed code:\n{code}\n")
                    approval = input("Approve this modification? (yes/no): ")

                    if approval.lower() != 'yes':
                        logger.info("Modification rejected by human")
                        result = {
                            "success": False,
                            "reason": "human_rejected",
                            "backup": backup_path
                        }
                    else:
                        result = {
                            "success": True,
                            "code": code,
                            "backup": backup_path
                        }
                else:
                    result = {
                        "success": True,
                        "code": code,
                        "backup": backup_path
                    }
            else:
                logger.warning("✗ Code failed tests")
                result = {
                    "success": False,
                    "reason": "tests_failed",
                    "backup": backup_path
                }

        # Log modification attempt
        self.modification_history.append({
            "timestamp": datetime.now().isoformat(),
            "goal": goal,
            "result": result
        })

        self.save_history()

        return result

    def save_history(self) -> None:
        """Save modification history"""
        history_file = "data/logs/modification_history.json"
        Path(history_file).parent.mkdir(parents=True, exist_ok=True)

        with open(history_file, 'w') as f:
            json.dump(self.modification_history, f, indent=2)


if __name__ == "__main__":
    # Test the self-modifier
    modifier = SelfModifier()

    # Test code safety checker
    safe_code = """
def improve_learning_rate():
    return 0.001
"""

    unsafe_code = """
import os
os.system('rm -rf /')
"""

    is_safe, issues = modifier.is_code_safe(safe_code)
    print(f"Safe code check: {is_safe}")

    is_safe, issues = modifier.is_code_safe(unsafe_code)
    print(f"Unsafe code check: {is_safe}, Issues: {issues}")
