"""
Reasoning Engine
Makes the AI actually THINK, not just memorize
"""

import logging
from typing import List, Dict, Any
import random

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ReasoningEngine:
    """Teaches the AI to reason, not just recall facts"""

    def __init__(self, apis):
        self.apis = apis

    def generate_reasoning_problems(self, n: int = 50) -> List[Dict[str, str]]:
        """Generate problems that require actual reasoning"""

        problem_types = [
            # Logical reasoning
            {
                "type": "logic",
                "prompt": "If all A are B, and all B are C, what can we conclude about A and C? Explain your reasoning step by step.",
                "requires": "deductive reasoning"
            },
            {
                "type": "logic",
                "prompt": "A says B is lying. B says C is lying. C says A and B are both lying. Who is telling the truth? Think through this carefully.",
                "requires": "logical deduction"
            },

            # Mathematical reasoning
            {
                "type": "math",
                "prompt": "If you have 3 apples and buy 2 more, then give away half, how many do you have? Show your work.",
                "requires": "arithmetic reasoning"
            },
            {
                "type": "math",
                "prompt": "What is the pattern in this sequence: 2, 4, 8, 16, ...? Explain the pattern and predict the next number.",
                "requires": "pattern recognition"
            },

            # Causal reasoning
            {
                "type": "causal",
                "prompt": "If it rains, the ground gets wet. The ground is wet. Does that mean it rained? Explain why or why not.",
                "requires": "causal reasoning"
            },
            {
                "type": "causal",
                "prompt": "Why does ice float on water? Think about the underlying physical principles.",
                "requires": "scientific reasoning"
            },

            # Problem decomposition
            {
                "type": "decomposition",
                "prompt": "How would you measure the height of a building using only a barometer? Think of multiple creative solutions.",
                "requires": "creative problem solving"
            },
            {
                "type": "decomposition",
                "prompt": "Break down the problem of 'teaching a computer to recognize cats' into smaller sub-problems.",
                "requires": "problem decomposition"
            },

            # Abstract reasoning
            {
                "type": "abstract",
                "prompt": "What do democracy and a marketplace have in common? Think abstractly about their fundamental principles.",
                "requires": "abstract reasoning"
            },
            {
                "type": "abstract",
                "prompt": "Explain the concept of 'emergence' using 3 different examples from different domains.",
                "requires": "conceptual understanding"
            },
        ]

        problems = []
        for _ in range(n):
            problem = random.choice(problem_types)
            problems.append(problem)

        return problems

    def learn_chain_of_thought(self, memory, n_examples: int = 100) -> int:
        """Learn to think step-by-step using chain-of-thought reasoning"""

        logger.info(f"\n🧠 Teaching AI to reason step-by-step ({n_examples} examples)...")

        cot_prompts = [
            "Solve this step-by-step: What is 15% of 80?",
            "Think through this: Why do we have seasons on Earth?",
            "Reason carefully: Can a computer be conscious? What evidence supports your view?",
            "Analyze this: What makes a good scientific theory?",
            "Break this down: How does the internet work?",
            "Think logically: Is it possible to prove a negative? Explain.",
            "Reason about this: What is the relationship between correlation and causation?",
            "Analyze step-by-step: Why is the sky blue?",
            "Think critically: Can AI be creative? Define creativity first, then analyze.",
            "Reason through this: What is consciousness and how would we test for it?",
        ]

        learned = 0
        for prompt in cot_prompts[:n_examples]:
            try:
                # Add explicit instruction for step-by-step reasoning
                full_prompt = f"Think step-by-step and show your reasoning:\n\n{prompt}"

                result = self.apis.query_any(full_prompt)

                if result['response']:
                    # Store with metadata indicating this is reasoning training
                    memory.add_knowledge(
                        text=f"Q: {prompt}\nReasoning: {result['response']}",
                        source=f"reasoning_{result['source']}",
                        metadata={
                            "type": "reasoning",
                            "chain_of_thought": True,
                            "prompt": prompt
                        }
                    )
                    learned += 1
                    logger.info(f"✓ Learned reasoning: {prompt[:60]}...")

            except Exception as e:
                logger.error(f"Error in reasoning training: {e}")

        logger.info(f"✓ Taught {learned} reasoning patterns")
        return learned

    def self_critique_loop(self, memory, topic: str) -> Dict[str, Any]:
        """Make the AI critique its own understanding"""

        logger.info(f"\n🔍 Self-critique on topic: {topic}")

        # Step 1: Generate initial answer
        initial_prompt = f"Explain {topic} in detail."
        initial_result = self.apis.query_any(initial_prompt)

        if not initial_result['response']:
            return {"success": False, "reason": "No initial response"}

        initial_answer = initial_result['response']
        logger.info(f"✓ Generated initial answer")

        # Step 2: Critique the answer
        critique_prompt = f"""Here is an explanation of {topic}:

{initial_answer}

Critique this explanation:
1. What did it get right?
2. What did it miss or get wrong?
3. How could it be improved?
4. What deeper questions does this raise?

Be thorough and critical."""

        critique_result = self.apis.query_any(critique_prompt)

        if not critique_result['response']:
            return {"success": False, "reason": "No critique"}

        critique = critique_result['response']
        logger.info(f"✓ Generated self-critique")

        # Step 3: Generate improved answer based on critique
        improved_prompt = f"""Original question: Explain {topic}

Original answer:
{initial_answer}

Critique of original answer:
{critique}

Based on this critique, provide an improved, more accurate explanation of {topic}."""

        improved_result = self.apis.query_any(improved_prompt)

        if improved_result['response']:
            # Store the improved understanding
            memory.add_knowledge(
                text=f"Q: {topic}\nImproved Answer: {improved_result['response']}\n\nSelf-Critique Process:\n{critique}",
                source=f"self_critique_{improved_result['source']}",
                metadata={
                    "type": "self_critique",
                    "topic": topic,
                    "iterations": 1
                }
            )
            logger.info(f"✓ Stored improved understanding")

            return {
                "success": True,
                "initial": initial_answer,
                "critique": critique,
                "improved": improved_result['response']
            }

        return {"success": False, "reason": "Could not generate improvement"}

    def problem_solving_training(self, memory, n_problems: int = 20) -> int:
        """Train on actual problem solving"""

        logger.info(f"\n🎯 Problem-solving training ({n_problems} problems)...")

        problem_templates = [
            "Design an algorithm to {task}. Explain your approach step-by-step.",
            "How would you solve this problem: {task}? What strategies would you use?",
            "What are three different approaches to {task}? Compare their trade-offs.",
            "If you had to {task}, what would be your systematic approach? Break it down.",
        ]

        tasks = [
            "find the shortest path between two points in a graph",
            "sort a list of numbers efficiently",
            "detect patterns in data",
            "compress data without losing information",
            "search through a large dataset quickly",
            "optimize a complex function",
            "balance competing objectives",
            "learn from limited examples",
            "generalize from specific cases",
            "handle uncertainty in predictions",
        ]

        solved = 0
        for _ in range(n_problems):
            template = random.choice(problem_templates)
            task = random.choice(tasks)
            prompt = template.format(task=task)

            try:
                result = self.apis.query_any(prompt)

                if result['response']:
                    memory.add_knowledge(
                        text=f"Problem: {prompt}\nSolution: {result['response']}",
                        source=f"problem_solving_{result['source']}",
                        metadata={
                            "type": "problem_solving",
                            "task": task
                        }
                    )
                    solved += 1
                    logger.info(f"✓ Solved: {task}")

            except Exception as e:
                logger.error(f"Error in problem solving: {e}")

        logger.info(f"✓ Solved {solved}/{n_problems} problems")
        return solved


if __name__ == "__main__":
    # Test the reasoning engine
    print("Reasoning Engine initialized")
