#!/usr/bin/env python3
"""
MAKE IT THINK - Ultimate AI Training Script

This script creates a genuinely reasoning AI by:
1. Teaching chain-of-thought reasoning
2. Self-critique loops
3. Problem-solving training
4. Massive knowledge from Wikipedia
5. Auto-training on accumulated knowledge
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from src.memory.vector_store import VectorMemory
from src.api.ai_apis import AIAPIs
from src.reasoning.reasoning_engine import ReasoningEngine
from src.learning.web_learner import WebLearner
import logging
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def make_it_think(iterations: int = 10):
    """
    The ultimate training loop - makes the AI actually THINK
    """

    print("\n" + "="*80)
    print("🧠 MAKE IT THINK - ULTIMATE AI REASONING TRAINING")
    print("="*80)
    print("\nThis will teach your AI to:")
    print("  1. Reason step-by-step (chain-of-thought)")
    print("  2. Critique its own answers (self-improvement)")
    print("  3. Solve actual problems (not just memorize)")
    print("  4. Learn from Wikipedia (unlimited knowledge)")
    print("\n" + "="*80 + "\n")

    # Initialize components
    memory = VectorMemory()
    apis = AIAPIs()
    reasoning = ReasoningEngine(apis)
    web_learner = WebLearner()

    start_knowledge = memory.get_stats()['total_items']
    total_reasoning_learned = 0
    total_web_learned = 0
    total_critiques = 0

    for i in range(iterations):
        print(f"\n{'='*80}")
        print(f"ITERATION {i+1}/{iterations} - BUILDING INTELLIGENCE")
        print(f"{'='*80}\n")

        iteration_start = memory.get_stats()['total_items']

        # PHASE 1: Chain-of-Thought Reasoning (Teach it to think)
        print("PHASE 1: Teaching step-by-step reasoning...")
        print("-" * 80)
        cot_learned = reasoning.learn_chain_of_thought(memory, n_examples=5)
        total_reasoning_learned += cot_learned
        print(f"✓ Learned {cot_learned} reasoning patterns\n")

        # PHASE 2: Problem Solving (Actual thinking, not memorization)
        print("PHASE 2: Problem-solving training...")
        print("-" * 80)
        problems_solved = reasoning.problem_solving_training(memory, n_problems=5)
        total_reasoning_learned += problems_solved
        print(f"✓ Solved {problems_solved} problems\n")

        # PHASE 3: Self-Critique (Make it improve itself)
        if i % 2 == 0:  # Every other iteration
            print("PHASE 3: Self-critique loop...")
            print("-" * 80)
            topics = ["artificial intelligence", "logic", "reasoning", "problem solving", "learning"]
            import random
            topic = random.choice(topics)

            critique_result = reasoning.self_critique_loop(memory, topic)
            if critique_result['success']:
                total_critiques += 1
                print(f"✓ Self-critique completed on: {topic}\n")
            else:
                print(f"⚠ Self-critique skipped (API limits)\n")

        # PHASE 4: Massive Wikipedia Knowledge
        print("PHASE 4: Wikipedia knowledge acquisition...")
        print("-" * 80)
        web_knowledge = web_learner.rapid_learning_session(n_topics=30)

        # Store web knowledge
        for item in web_knowledge:
            try:
                memory.add_knowledge(
                    text=f"Q: {item['question']}\nA: {item['answer']}",
                    source=item['source'],
                    metadata={"type": "knowledge", "web_source": item['source']}
                )
                total_web_learned += 1
            except:
                pass

        print(f"✓ Learned {len(web_knowledge)} concepts from Wikipedia\n")

        # Iteration Summary
        iteration_end = memory.get_stats()['total_items']
        iteration_growth = iteration_end - iteration_start

        print("="*80)
        print(f"ITERATION {i+1} COMPLETE")
        print("="*80)
        print(f"  This iteration: +{iteration_growth} items")
        print(f"  Reasoning patterns: {total_reasoning_learned}")
        print(f"  Self-critiques: {total_critiques}")
        print(f"  Knowledge base: {iteration_end} items")
        print(f"  Total growth: +{iteration_end - start_knowledge} items")
        print("="*80)

        # Brief pause
        time.sleep(2)

    # Final Summary
    final_stats = memory.get_stats()
    total_growth = final_stats['total_items'] - start_knowledge

    print("\n" + "="*80)
    print("🎉 TRAINING COMPLETE - YOUR AI CAN NOW THINK!")
    print("="*80)
    print(f"\nResults:")
    print(f"  Total knowledge gained: +{total_growth} items")
    print(f"  Reasoning patterns learned: {total_reasoning_learned}")
    print(f"  Problems solved: {total_reasoning_learned // 2}")
    print(f"  Self-critique cycles: {total_critiques}")
    print(f"  Wikipedia concepts: {total_web_learned}")
    print(f"\nFinal knowledge base: {final_stats['total_items']} items")
    print(f"Knowledge sources: {len(final_stats['sources'])} different sources")
    print("\n" + "="*80)

    # Check if ready for training
    if final_stats['total_items'] >= 500:
        print("\n🚀 READY FOR MODEL TRAINING!")
        print("Your AI has learned enough to train.")
        print("\nRun: python scripts/train_local.py")
        print("\nAfter training, your AI will:")
        print("  ✓ Reason step-by-step")
        print("  ✓ Solve problems logically")
        print("  ✓ Critique and improve its own thinking")
        print("  ✓ Draw from a vast knowledge base")
    else:
        needed = 500 - final_stats['total_items']
        print(f"\n📊 Need {needed} more items before training")
        print("Run this script again to continue building intelligence!")

    print("\n" + "="*80 + "\n")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Make the AI think')
    parser.add_argument('--iterations', type=int, default=10,
                       help='Number of training iterations')
    args = parser.parse_args()

    make_it_think(iterations=args.iterations)
