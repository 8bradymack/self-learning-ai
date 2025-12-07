#!/usr/bin/env python3
"""
WIKIPEDIA BLITZ - Rapid Knowledge Acquisition
Learn 1000+ concepts in under an hour, NO rate limits
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from src.memory.vector_store import VectorMemory
from src.learning.web_learner import WebLearner
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def wikipedia_blitz(target_items: int = 1000):
    """
    Rapid Wikipedia learning - no API limits!
    """

    print("\n" + "="*80)
    print("🌐 WIKIPEDIA BLITZ - UNLIMITED LEARNING MODE")
    print("="*80)
    print(f"\nTarget: {target_items} knowledge items")
    print("Source: Wikipedia (NO rate limits!)")
    print("Strategy: Learn EVERYTHING, FAST")
    print("\n" + "="*80 + "\n")

    memory = VectorMemory()
    web_learner = WebLearner()

    start_knowledge = memory.get_stats()['total_items']
    learned = 0
    iteration = 1

    # Massive topic list
    all_topics = web_learner.generate_topic_list()

    # Keep going until we hit target
    while (memory.get_stats()['total_items'] - start_knowledge) < target_items:
        print(f"\n{'='*80}")
        print(f"BLITZ ITERATION {iteration}")
        print(f"{'='*80}\n")

        # Learn 50 topics at once
        knowledge = web_learner.rapid_learning_session(n_topics=50)

        # Store all knowledge
        for item in knowledge:
            try:
                memory.add_knowledge(
                    text=f"Q: {item['question']}\nA: {item['answer']}",
                    source=item['source'],
                    metadata={"type": "wikipedia_blitz", "iteration": iteration}
                )
                learned += 1
            except Exception as e:
                logger.error(f"Error storing: {e}")

        current = memory.get_stats()['total_items']
        progress = current - start_knowledge

        print(f"\n✓ Iteration {iteration} complete")
        print(f"  This iteration: +{len(knowledge)} items")
        print(f"  Total learned: {progress} items")
        print(f"  Knowledge base: {current} items")
        print(f"  Progress: {(progress/target_items)*100:.1f}%")

        iteration += 1

    # Final stats
    final_stats = memory.get_stats()
    total_learned = final_stats['total_items'] - start_knowledge

    print("\n" + "="*80)
    print("🎉 WIKIPEDIA BLITZ COMPLETE!")
    print("="*80)
    print(f"\nResults:")
    print(f"  Knowledge learned: {total_learned} items")
    print(f"  Iterations: {iteration - 1}")
    print(f"  Final database: {final_stats['total_items']} items")
    print(f"  Sources: {len(final_stats['sources'])}")
    print("\n" + "="*80)
    print("\n🚀 READY TO TRAIN!")
    print("\nRun: python scripts/train_local.py")
    print("\nYour AI will learn:")
    print("  ✓ " + str(total_learned) + " concepts across all domains")
    print("  ✓ Pattern recognition from massive knowledge")
    print("  ✓ Cross-domain understanding")
    print("\n" + "="*80 + "\n")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Wikipedia Blitz')
    parser.add_argument('--target', type=int, default=1000,
                       help='Target number of items to learn')
    args = parser.parse_args()

    wikipedia_blitz(target_items=args.target)
