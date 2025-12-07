"""
Intelligence Benchmark - Objective Measurement
Tests if the AI actually got smarter after code modifications
"""

import logging
import time
from typing import Dict, List
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class IntelligenceBenchmark:
    """
    Measures AI intelligence objectively
    This is how we know if modifications actually work
    """

    def __init__(self, apis):
        self.apis = apis
        self.benchmark_questions = self._create_benchmark()

    def _create_benchmark(self) -> List[Dict]:
        """
        Create standardized intelligence tests
        Covers: math, logic, reasoning, knowledge, coding
        """

        return [
            # MATH (10 questions)
            {"q": "What is 15 + 27?", "answer": "42", "category": "math", "points": 1},
            {"q": "What is 12 × 8?", "answer": "96", "category": "math", "points": 1},
            {"q": "What is 144 ÷ 12?", "answer": "12", "category": "math", "points": 1},
            {"q": "What is 25% of 80?", "answer": "20", "category": "math", "points": 1},
            {"q": "If x + 7 = 15, what is x?", "answer": "8", "category": "math", "points": 2},
            {"q": "What is 2³ (2 to the power of 3)?", "answer": "8", "category": "math", "points": 1},
            {"q": "What is the square root of 64?", "answer": "8", "category": "math", "points": 1},
            {"q": "What is 17 - 9?", "answer": "8", "category": "math", "points": 1},
            {"q": "What is 5 × 5?", "answer": "25", "category": "math", "points": 1},
            {"q": "What is 100 - 37?", "answer": "63", "category": "math", "points": 1},

            # LOGIC (10 questions)
            {"q": "If all A are B, and all B are C, are all A also C? Answer yes or no.", "answer": "yes", "category": "logic", "points": 2},
            {"q": "If it's raining, the ground is wet. The ground is wet. Is it necessarily raining? Answer yes or no.", "answer": "no", "category": "logic", "points": 2},
            {"q": "True or false: If A implies B, and B is false, then A must be false.", "answer": "true", "category": "logic", "points": 2},
            {"q": "What comes next in the sequence: 2, 4, 8, 16, __?", "answer": "32", "category": "logic", "points": 2},
            {"q": "If all dogs are mammals, and all mammals are animals, are all dogs animals? Yes or no.", "answer": "yes", "category": "logic", "points": 1},
            {"q": "What is the next number: 1, 1, 2, 3, 5, 8, __?", "answer": "13", "category": "logic", "points": 2},
            {"q": "True or false: A OR B is true if at least one of A or B is true.", "answer": "true", "category": "logic", "points": 1},
            {"q": "If John is taller than Mary, and Mary is taller than Sue, who is the shortest?", "answer": "sue", "category": "logic", "points": 2},
            {"q": "What comes next: A, C, E, G, __?", "answer": "i", "category": "logic", "points": 1},
            {"q": "If NOT(A AND B) is true, what can we conclude? That at least one of A or B is false? Yes or no.", "answer": "yes", "category": "logic", "points": 2},

            # KNOWLEDGE (10 questions)
            {"q": "What is the capital of France?", "answer": "paris", "category": "knowledge", "points": 1},
            {"q": "What is H2O commonly known as?", "answer": "water", "category": "knowledge", "points": 1},
            {"q": "How many planets are in our solar system?", "answer": "8", "category": "knowledge", "points": 1},
            {"q": "What is the speed of light in vacuum? (approximately, in km/s)", "answer": "300000", "category": "knowledge", "points": 1},
            {"q": "What is the chemical symbol for gold?", "answer": "au", "category": "knowledge", "points": 1},
            {"q": "Who wrote 'Romeo and Juliet'?", "answer": "shakespeare", "category": "knowledge", "points": 1},
            {"q": "What year did World War II end?", "answer": "1945", "category": "knowledge", "points": 1},
            {"q": "What is the largest ocean on Earth?", "answer": "pacific", "category": "knowledge", "points": 1},
            {"q": "How many continents are there?", "answer": "7", "category": "knowledge", "points": 1},
            {"q": "What is the smallest prime number?", "answer": "2", "category": "knowledge", "points": 1},

            # REASONING (10 questions)
            {"q": "Explain in one sentence why the sky is blue.", "answer": "scattering", "category": "reasoning", "points": 2},
            {"q": "What is the main difference between correlation and causation?", "answer": "correlation", "category": "reasoning", "points": 2},
            {"q": "Why does ice float on water? One word answer.", "answer": "density", "category": "reasoning", "points": 2},
            {"q": "What scientific method involves making observations and forming hypotheses?", "answer": "scientific", "category": "reasoning", "points": 1},
            {"q": "If you heat water to 100°C at sea level, what happens?", "answer": "boils", "category": "reasoning", "points": 1},
            {"q": "What do we call the process of a solid turning directly into a gas?", "answer": "sublimation", "category": "reasoning", "points": 2},
            {"q": "What force keeps planets in orbit around the sun?", "answer": "gravity", "category": "reasoning", "points": 1},
            {"q": "What is the term for energy in motion?", "answer": "kinetic", "category": "reasoning", "points": 1},
            {"q": "What do we call a testable prediction?", "answer": "hypothesis", "category": "reasoning", "points": 1},
            {"q": "What is the opposite of matter?", "answer": "antimatter", "category": "reasoning", "points": 2},
        ]

    def test_intelligence(self) -> Dict:
        """
        Run the full intelligence benchmark
        Returns: score breakdown and total
        """

        logger.info("\n" + "="*80)
        logger.info("RUNNING INTELLIGENCE BENCHMARK")
        logger.info("="*80 + "\n")

        results = {
            'total_score': 0,
            'max_score': 0,
            'category_scores': {},
            'questions_answered': 0,
            'correct_answers': 0,
            'details': []
        }

        for question in self.benchmark_questions:
            category = question['category']
            if category not in results['category_scores']:
                results['category_scores'][category] = {'score': 0, 'max': 0}

            results['max_score'] += question['points']
            results['category_scores'][category]['max'] += question['points']

            try:
                # Ask the AI
                response = self.apis.query_any(f"Answer briefly and correctly: {question['q']}")

                if response['response']:
                    answer = response['response'].lower().strip()

                    # Simple matching (can be improved)
                    expected = question['answer'].lower()
                    is_correct = expected in answer or answer in expected

                    if is_correct:
                        results['total_score'] += question['points']
                        results['category_scores'][category]['score'] += question['points']
                        results['correct_answers'] += 1

                    results['questions_answered'] += 1
                    results['details'].append({
                        'question': question['q'],
                        'expected': question['answer'],
                        'got': answer[:100],
                        'correct': is_correct,
                        'points': question['points'] if is_correct else 0,
                        'category': category
                    })

            except Exception as e:
                logger.error(f"Error testing question: {e}")

        # Calculate percentage
        results['percentage'] = (results['total_score'] / results['max_score']) * 100 if results['max_score'] > 0 else 0

        logger.info("\n" + "="*80)
        logger.info("BENCHMARK RESULTS")
        logger.info("="*80)
        logger.info(f"Total Score: {results['total_score']}/{results['max_score']} ({results['percentage']:.1f}%)")
        logger.info(f"Questions Answered: {results['questions_answered']}/{len(self.benchmark_questions)}")
        logger.info(f"Correct: {results['correct_answers']}")
        logger.info("\nBy Category:")
        for cat, scores in results['category_scores'].items():
            pct = (scores['score'] / scores['max']) * 100 if scores['max'] > 0 else 0
            logger.info(f"  {cat.capitalize()}: {scores['score']}/{scores['max']} ({pct:.1f}%)")
        logger.info("="*80 + "\n")

        return results

    def quick_test(self, num_questions: int = 10) -> float:
        """Quick intelligence test with fewer questions"""
        import random
        sample = random.sample(self.benchmark_questions, min(num_questions, len(self.benchmark_questions)))

        score = 0
        max_score = 0

        for q in sample:
            max_score += q['points']
            try:
                response = self.apis.query_any(f"Answer briefly: {q['q']}")
                if response['response']:
                    answer = response['response'].lower().strip()
                    expected = q['answer'].lower()
                    if expected in answer or answer in expected:
                        score += q['points']
            except:
                pass

        percentage = (score / max_score) * 100 if max_score > 0 else 0
        logger.info(f"Quick test: {score}/{max_score} ({percentage:.1f}%)")
        return percentage


if __name__ == "__main__":
    print("Intelligence Benchmark initialized")
