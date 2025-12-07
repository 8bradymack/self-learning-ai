"""
Mutation Parser - Extracts and applies code changes from AI-generated text

This is THE critical component that makes evolution real:
- Parses AI-generated mutation ideas
- Extracts actual code changes
- Applies them safely in sandbox
- Enables real testing and selection
"""

import re
import ast
import logging
from typing import Dict, Optional, List, Tuple
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MutationParser:
    """
    Parses AI-generated mutation text and extracts actionable code changes
    """

    def __init__(self):
        self.code_pattern = re.compile(r'```python\n(.*?)```', re.DOTALL)
        self.modification_pattern = re.compile(r'MODIFICATION:\s*(.*?)(?=REASON:|CODE:|$)', re.DOTALL)
        self.reason_pattern = re.compile(r'REASON:\s*(.*?)(?=MODIFICATION:|CODE:|$)', re.DOTALL)

    def parse_mutation(self, mutation_text: str) -> Optional[Dict]:
        """
        Parse mutation text and extract structured information

        Returns:
            {
                'modification': 'description of change',
                'reason': 'why this improves intelligence',
                'code_snippets': ['code1', 'code2', ...],
                'has_code': bool
            }
        """

        result = {
            'modification': None,
            'reason': None,
            'code_snippets': [],
            'has_code': False
        }

        # Extract modification description
        mod_match = self.modification_pattern.search(mutation_text)
        if mod_match:
            result['modification'] = mod_match.group(1).strip()

        # Extract reason
        reason_match = self.reason_pattern.search(mutation_text)
        if reason_match:
            result['reason'] = reason_match.group(1).strip()

        # Extract code blocks
        code_matches = self.code_pattern.findall(mutation_text)
        if code_matches:
            result['code_snippets'] = [code.strip() for code in code_matches]
            result['has_code'] = True

        # Also look for CODE: section without markdown
        if 'CODE:' in mutation_text:
            code_section = mutation_text.split('CODE:')[1].split('\n\n')[0]
            if code_section.strip() and not result['code_snippets']:
                result['code_snippets'].append(code_section.strip())
                result['has_code'] = True

        return result

    def extract_function_changes(self, code_snippet: str) -> List[Dict]:
        """
        Extract individual function definitions from code snippet

        Returns list of:
            {
                'type': 'function' | 'class' | 'import' | 'other',
                'name': 'function_name',
                'code': 'actual code'
            }
        """
        changes = []

        try:
            tree = ast.parse(code_snippet)

            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    changes.append({
                        'type': 'function',
                        'name': node.name,
                        'code': ast.unparse(node),
                        'lineno': node.lineno
                    })
                elif isinstance(node, ast.ClassDef):
                    changes.append({
                        'type': 'class',
                        'name': node.name,
                        'code': ast.unparse(node),
                        'lineno': node.lineno
                    })
                elif isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom):
                    changes.append({
                        'type': 'import',
                        'name': ast.unparse(node),
                        'code': ast.unparse(node),
                        'lineno': node.lineno
                    })

        except SyntaxError as e:
            logger.warning(f"Could not parse code snippet: {e}")
            # Fall back to treating whole snippet as one change
            changes.append({
                'type': 'other',
                'name': 'unparseable',
                'code': code_snippet,
                'lineno': 0
            })

        return changes

    def is_valid_python(self, code: str) -> Tuple[bool, Optional[str]]:
        """
        Check if code is syntactically valid Python

        Returns: (is_valid, error_message)
        """
        try:
            ast.parse(code)
            return True, None
        except SyntaxError as e:
            return False, str(e)

    def estimate_safety(self, code: str) -> Dict:
        """
        Estimate if code change is safe to apply

        Returns:
            {
                'safe': bool,
                'warnings': [list of concerns],
                'risk_level': 'low' | 'medium' | 'high'
            }
        """
        warnings = []
        risk_level = 'low'

        # Check for dangerous operations
        dangerous_patterns = [
            (r'\bos\.system\b', 'Executes shell commands'),
            (r'\beval\b', 'Evaluates arbitrary code'),
            (r'\bexec\b', 'Executes arbitrary code'),
            (r'\b__import__\b', 'Dynamic imports'),
            (r'\bopen\(.+[\'"]w[\'"]\)', 'File writing'),
            (r'\brmdir\b|\bunlink\b|\bremove\b', 'File deletion'),
            (r'\bsubprocess\b', 'Subprocess execution'),
        ]

        for pattern, description in dangerous_patterns:
            if re.search(pattern, code):
                warnings.append(f"Contains {description}")
                risk_level = 'high'

        # Check for network operations
        network_patterns = [
            (r'\brequests\b', 'HTTP requests'),
            (r'\burllib\b', 'URL operations'),
            (r'\bsocket\b', 'Socket operations'),
        ]

        for pattern, description in network_patterns:
            if re.search(pattern, code):
                warnings.append(f"Contains {description}")
                if risk_level == 'low':
                    risk_level = 'medium'

        safe = risk_level == 'low'

        return {
            'safe': safe,
            'warnings': warnings,
            'risk_level': risk_level
        }

    def categorize_mutation(self, mutation_text: str) -> str:
        """
        Categorize what type of improvement this mutation attempts
        """
        text_lower = mutation_text.lower()

        categories = {
            'caching': ['cache', 'memoize', 'lru_cache'],
            'optimization': ['optimize', 'faster', 'speed', 'efficiency', 'performance'],
            'learning': ['learn', 'training', 'knowledge', 'memory'],
            'reasoning': ['reason', 'logic', 'think', 'inference'],
            'context': ['context', 'retrieval', 'search', 'embedding'],
            'architecture': ['architecture', 'structure', 'design', 'refactor'],
            'parameters': ['parameter', 'hyperparameter', 'config', 'setting'],
        }

        for category, keywords in categories.items():
            if any(keyword in text_lower for keyword in keywords):
                return category

        return 'other'


class MutationApplicator:
    """
    Safely applies parsed mutations to actual code files
    """

    def __init__(self, project_root: str = "/Users/bradymackintosh/self-learning-ai"):
        self.project_root = Path(project_root)
        self.parser = MutationParser()

    def create_sandbox_copy(self, filepath: str) -> Path:
        """
        Create a sandbox copy of the file for testing
        """
        original = self.project_root / filepath
        sandbox_dir = self.project_root / "sandbox"
        sandbox_dir.mkdir(exist_ok=True)

        # Preserve directory structure in sandbox
        relative_path = Path(filepath)
        sandbox_file = sandbox_dir / relative_path
        sandbox_file.parent.mkdir(parents=True, exist_ok=True)

        # Copy file
        import shutil
        shutil.copy2(original, sandbox_file)

        return sandbox_file

    def apply_simple_replacement(self, filepath: str, old_code: str, new_code: str) -> bool:
        """
        Simple find-and-replace mutation application

        Returns: True if applied successfully
        """
        try:
            full_path = self.project_root / filepath

            with open(full_path, 'r') as f:
                content = f.read()

            if old_code not in content:
                logger.warning(f"Old code not found in {filepath}")
                return False

            new_content = content.replace(old_code, new_code)

            # Validate new code is still valid Python
            is_valid, error = self.parser.is_valid_python(new_content)
            if not is_valid:
                logger.error(f"New code would create syntax error: {error}")
                return False

            # Write the change
            with open(full_path, 'w') as f:
                f.write(new_content)

            logger.info(f"✓ Applied mutation to {filepath}")
            return True

        except Exception as e:
            logger.error(f"Failed to apply mutation: {e}")
            return False


if __name__ == "__main__":
    # Test the parser
    parser = MutationParser()

    sample_mutation = """
    MODIFICATION: Add caching to improve performance
    REASON: Reduces redundant computation
    CODE:
    ```python
    from functools import lru_cache

    @lru_cache(maxsize=128)
    def expensive_function(x):
        return x * 2
    ```
    """

    result = parser.parse_mutation(sample_mutation)
    print("Parsed mutation:", result)
    print("Category:", parser.categorize_mutation(sample_mutation))
