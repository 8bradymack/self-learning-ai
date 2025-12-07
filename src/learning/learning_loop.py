"""
Learning Loop Orchestrator
Manages the continuous learning process
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.core.model_loader import ModelLoader
from src.memory.vector_store import VectorMemory
from src.api.ai_apis import AIAPIs
from typing import List, Dict, Any, Optional
import yaml
import logging
from datetime import datetime
import json
import random

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LearningLoop:
    """Orchestrates the continuous learning process"""

    def __init__(self, config_path: str = "configs/config.yaml"):
        self.config = self._load_config(config_path)
        self.model_loader = ModelLoader(config_path)
        self.memory = VectorMemory(config_path)
        self.apis = AIAPIs(config_path)
        self.learning_history = []

    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """Load configuration"""
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)

    def generate_learning_questions(self, topic: Optional[str] = None, n: int = 10) -> List[str]:
        """Generate questions to ask other AIs"""

        if topic:
            base_questions = [
                f"Explain the fundamentals of {topic}",
                f"What are the key concepts in {topic}?",
                f"What are common challenges in {topic}?",
                f"What are best practices for {topic}?",
                f"How does {topic} relate to other fields?",
            ]
        else:
            # General knowledge acquisition
            topics = [
                "machine learning", "natural language processing", "mathematics",
                "physics", "computer science", "philosophy", "logic",
                "problem solving", "reasoning", "creativity", "optimization",
                "algorithms", "data structures", "software engineering"
            ]

            base_questions = []
            for selected_topic in random.sample(topics, min(n, len(topics))):
                base_questions.extend([
                    f"What are the core principles of {selected_topic}?",
                    f"Explain advanced concepts in {selected_topic}",
                ])

        return base_questions[:n]

    def learn_from_apis(self, questions: Optional[List[str]] = None, n_questions: int = 5) -> int:
        """Learn by querying external AIs"""

        if questions is None:
            questions = self.generate_learning_questions(n=n_questions)

        logger.info(f"Learning from {n_questions} questions...")

        learned_count = 0

        for question in questions:
            try:
                result = self.apis.query_any(question)

                if result['response']:
                    # Store in memory
                    self.memory.add_knowledge(
                        text=f"Q: {question}\nA: {result['response']}",
                        source=f"api_{result['source']}",
                        metadata={
                            "type": "qa_pair",
                            "question": question,
                            "api_source": result['source']
                        }
                    )

                    learned_count += 1
                    logger.info(f"✓ Learned from {result['source']}: {question[:50]}...")

            except Exception as e:
                logger.error(f"Error learning from question '{question}': {e}")

        logger.info(f"Learned {learned_count}/{len(questions)} items")
        return learned_count

    def learn_from_web(self, urls: List[str]) -> int:
        """Learn from web content (placeholder for future implementation)"""
        logger.info("Web learning not yet implemented")
        return 0

    def generate_training_data(self, n_examples: int = 100) -> List[Dict[str, str]]:
        """Generate training examples from stored knowledge"""

        logger.info(f"Generating {n_examples} training examples from memory...")

        # Get recent knowledge
        stats = self.memory.get_stats()
        total_items = stats['total_items']

        if total_items == 0:
            logger.warning("No knowledge in memory yet")
            return []

        # Sample from memory
        sample_size = min(n_examples, total_items)
        all_items = self.memory.collection.get(limit=sample_size)

        training_data = []

        for doc, metadata in zip(all_items['documents'], all_items['metadatas']):
            # Parse Q&A pairs
            if 'Q:' in doc and 'A:' in doc:
                parts = doc.split('\nA:', 1)
                if len(parts) == 2:
                    question = parts[0].replace('Q:', '').strip()
                    answer = parts[1].strip()

                    training_data.append({
                        "prompt": question,
                        "completion": answer
                    })

        logger.info(f"Generated {len(training_data)} training examples")
        return training_data

    def evaluate_knowledge(self, test_questions: List[str]) -> Dict[str, Any]:
        """Evaluate current knowledge by answering test questions"""

        logger.info("Evaluating knowledge...")

        results = {
            "total": len(test_questions),
            "answered": 0,
            "avg_confidence": 0.0,
            "responses": []
        }

        for question in test_questions:
            # Retrieve relevant context from memory
            context = self.memory.retrieve_context(question)

            # Generate answer using model
            prompt = f"Context:\n{context}\n\nQuestion: {question}\nAnswer:"

            try:
                if self.model_loader.model is None:
                    logger.warning("Model not loaded, loading now...")
                    self.model_loader.load_base_model()

                response = self.model_loader.generate(prompt, max_length=512)

                results["answered"] += 1
                results["responses"].append({
                    "question": question,
                    "answer": response,
                    "had_context": bool(context)
                })

            except Exception as e:
                logger.error(f"Error evaluating question '{question}': {e}")

        if results["answered"] > 0:
            # Calculate confidence based on context availability
            with_context = sum(1 for r in results["responses"] if r["had_context"])
            results["avg_confidence"] = with_context / results["answered"]

        return results

    def run_learning_cycle(self, n_iterations: int = 1) -> None:
        """Run one or more learning cycles"""

        for i in range(n_iterations):
            logger.info(f"\n{'='*60}")
            logger.info(f"LEARNING CYCLE {i+1}/{n_iterations}")
            logger.info(f"{'='*60}\n")

            # Step 1: Learn from APIs
            questions = self.generate_learning_questions(n=10)
            learned = self.learn_from_apis(questions)

            # Step 2: Get stats
            stats = self.memory.get_stats()
            logger.info(f"\nMemory Stats: {stats['total_items']} total items")

            # Step 3: Self-evaluation
            test_questions = [
                "What is machine learning?",
                "Explain neural networks",
                "What is the purpose of optimization?"
            ]

            eval_results = self.evaluate_knowledge(test_questions)
            logger.info(f"Evaluation: Answered {eval_results['answered']}/{eval_results['total']}")

            # Log cycle
            cycle_log = {
                "iteration": i + 1,
                "timestamp": datetime.now().isoformat(),
                "learned_items": learned,
                "total_knowledge": stats['total_items'],
                "evaluation": eval_results
            }

            self.learning_history.append(cycle_log)

            # Save progress
            self.save_progress()

    def save_progress(self) -> None:
        """Save learning history"""
        progress_file = "data/logs/learning_history.json"
        Path(progress_file).parent.mkdir(parents=True, exist_ok=True)

        with open(progress_file, 'w') as f:
            json.dump(self.learning_history, f, indent=2)

        logger.info(f"Progress saved to {progress_file}")


if __name__ == "__main__":
    # Run a test learning cycle
    logger.info("Starting Learning Loop Test\n")

    loop = LearningLoop()

    # Run one learning cycle
    loop.run_learning_cycle(n_iterations=1)

    print("\n" + "="*60)
    print("LEARNING CYCLE COMPLETE")
    print("="*60)
