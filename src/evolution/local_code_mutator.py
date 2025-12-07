"""
Local Code Mutator - NO API LIMITS
Uses local GPT2 model for unlimited evolution attempts
This is the KEY to massive-scale evolution (100k+ attempts)
"""

import logging
import torch
from pathlib import Path
from typing import Dict, Optional, Tuple
import shutil
import random
from transformers import AutoModelForCausalLM, AutoTokenizer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LocalCodeMutator:
    """
    Code mutator that uses LOCAL model only - NO API LIMITS!
    This enables true massive-scale evolution (100k+ attempts)
    """

    def __init__(self, project_root: str = "/Users/bradymackintosh/self-learning-ai"):
        self.project_root = Path(project_root)
        self.modifiable_files = [
            "src/learning/learning_loop.py",
            "src/reasoning/reasoning_engine.py",
            "src/memory/vector_store.py",
            "src/self_improvement/recursive_improver.py",
        ]

        # Load local model
        logger.info("Loading local model for evolution...")
        try:
            model_path = self.project_root / "models" / "finetuned_model"
            if model_path.exists():
                logger.info(f"Loading fine-tuned model from {model_path}")
                self.tokenizer = AutoTokenizer.from_pretrained(str(model_path))
                self.model = AutoModelForCausalLM.from_pretrained(str(model_path))
            else:
                logger.info("Fine-tuned model not found, using base GPT2")
                self.tokenizer = AutoTokenizer.from_pretrained("gpt2")
                self.model = AutoModelForCausalLM.from_pretrained("gpt2")

            # Set device
            self.device = "mps" if torch.backends.mps.is_available() else "cpu"
            self.model = self.model.to(self.device)
            logger.info(f"Model loaded on {self.device}")

        except Exception as e:
            logger.error(f"Error loading model: {e}")
            logger.info("Using simple rule-based mutation instead")
            self.model = None
            self.tokenizer = None

    def read_code_file(self, filepath: str) -> str:
        """Read a Python file"""
        full_path = self.project_root / filepath
        with open(full_path, 'r') as f:
            return f.read()

    def create_backup(self, filepath: str) -> str:
        """Create backup before modification"""
        full_path = self.project_root / filepath
        backup_path = full_path.with_suffix('.py.backup')
        shutil.copy2(full_path, backup_path)
        return str(backup_path)

    def generate_mutation_idea_local(self, filepath: str) -> Optional[Dict]:
        """
        Generate mutation idea using LOCAL model - NO API CALLS!
        This is the breakthrough for unlimited evolution attempts
        """

        code = self.read_code_file(filepath)

        if self.model is not None:
            # Use local model to generate improvement idea
            prompt = f"""Improve this Python code to make it smarter:

{code[:1000]}

MODIFICATION: """

            try:
                inputs = self.tokenizer(prompt, return_tensors="pt", truncation=True, max_length=512)
                inputs = {k: v.to(self.device) for k, v in inputs.items()}

                with torch.no_grad():
                    outputs = self.model.generate(
                        **inputs,
                        max_new_tokens=200,
                        temperature=0.8,
                        do_sample=True,
                        top_p=0.9
                    )

                generated_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

                # Extract the generated part (after the prompt)
                mutation_idea = generated_text[len(prompt):].strip()

                return {
                    'filepath': filepath,
                    'original_code': code,
                    'mutation_idea': f"LOCAL MODEL SUGGESTION:\n{mutation_idea}",
                    'source': 'local_model'
                }

            except Exception as e:
                logger.error(f"Error with local model: {e}")
                # Fall through to rule-based

        # Rule-based mutation ideas (when model unavailable)
        return self.generate_rule_based_mutation(filepath, code)

    def generate_rule_based_mutation(self, filepath: str, code: str) -> Dict:
        """
        Simple rule-based mutation ideas
        These are generic improvements that could help
        """

        mutation_ideas = [
            {
                'name': 'Add caching layer',
                'reason': 'Reduces redundant computation, improves speed',
                'modification': 'Add @lru_cache decorator to frequently called functions'
            },
            {
                'name': 'Increase batch size',
                'reason': 'Better GPU utilization, faster learning',
                'modification': 'Increase batch_size parameter in learning loops'
            },
            {
                'name': 'Add early stopping',
                'reason': 'Prevents overfitting, saves computation',
                'modification': 'Add early stopping logic based on validation performance'
            },
            {
                'name': 'Improve context retrieval',
                'reason': 'Better relevant knowledge retrieval',
                'modification': 'Increase k in top_k retrieval from vector store'
            },
            {
                'name': 'Add diversity to questions',
                'reason': 'Broader knowledge coverage',
                'modification': 'Add randomization to question generation'
            },
            {
                'name': 'Optimize embedding size',
                'reason': 'Better semantic understanding',
                'modification': 'Use larger embedding model (384d instead of current)'
            },
            {
                'name': 'Add multi-hop reasoning',
                'reason': 'Deeper logical connections',
                'modification': 'Chain multiple reasoning steps before answering'
            },
            {
                'name': 'Increase learning rate',
                'reason': 'Faster convergence during training',
                'modification': 'Increase learning_rate by 20% in training config'
            },
            {
                'name': 'Add memory consolidation',
                'reason': 'Strengthen important knowledge',
                'modification': 'Periodically review and reinforce high-value memories'
            },
            {
                'name': 'Implement active learning',
                'reason': 'Focus on uncertain/valuable knowledge',
                'modification': 'Prioritize learning questions where AI is least confident'
            }
        ]

        # Pick random mutation
        idea = random.choice(mutation_ideas)

        mutation_text = f"""MODIFICATION: {idea['name']}
REASON: {idea['reason']}
IMPLEMENTATION: {idea['modification']}

TARGET FILE: {filepath}

This modification could improve the AI's intelligence by {idea['reason'].lower()}.
"""

        return {
            'filepath': filepath,
            'original_code': code,
            'mutation_idea': mutation_text,
            'source': 'rule_based'
        }

    def attempt_mutation(self, filepath: str) -> Dict:
        """
        Try to mutate code once - LOCALLY, NO API CALLS
        Returns: Dict with success status and details
        """

        logger.info(f"Attempting local mutation: {filepath}")

        # Generate mutation idea using local resources
        mutation = self.generate_mutation_idea_local(filepath)

        if not mutation:
            return {
                'success': False,
                'reason': 'Failed to generate mutation idea',
                'filepath': filepath
            }

        # Create backup
        backup_path = self.create_backup(filepath)

        # For now, we store the mutation idea
        # Real implementation would parse and apply it
        # But storing ideas builds knowledge for future training

        return {
            'success': True,
            'mutation': mutation,
            'filepath': filepath,
            'implemented': False,
            'backup_path': backup_path
        }


if __name__ == "__main__":
    print("Local Code Mutator - Unlimited Evolution (No API Limits!)")
