#!/usr/bin/env python3
"""
UNLIMITED EVOLUTION - No API Rate Limits!

Uses LOCAL model only for generating mutations
This enables TRUE massive-scale evolution (100k+ attempts)

Key insight: External APIs have rate limits
Solution: Use local model for everything
Result: UNLIMITED evolution attempts
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from src.memory.vector_store import VectorMemory
from src.evolution.local_code_mutator import LocalCodeMutator
import logging
import time
import json
from datetime import datetime
import random

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    handlers=[
        logging.FileHandler('data/logs/evolution_unlimited.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def evolve_unlimited(max_attempts: int = 100000, delay: float = 1.0):
    """
    UNLIMITED evolution - no API rate limits!

    Uses only local resources:
    - Local GPT2 model for mutation ideas
    - Local vector store for knowledge
    - No external API calls = no rate limits

    This is the REAL massive-scale evolution
    """

    print("\n" + "="*80)
    print("🧬 UNLIMITED EVOLUTION - NO API RATE LIMITS")
    print("="*80)
    print("\nStrategy: 100% LOCAL - No external APIs")
    print(f"Target: {max_attempts:,} evolution attempts")
    print(f"Delay: {delay}s between attempts")
    print("\nYour logic:")
    print("  Even 0.01% success × 100,000 attempts = 10 improvements")
    print("  ONE success → recursive loop begins")
    print("\n✓ No rate limits = TRUE unlimited evolution")
    print(f"✓ Estimated duration: {(max_attempts * delay) / 3600:.1f} hours")
    print("="*80 + "\n")

    # Initialize LOCAL resources only
    memory = VectorMemory()
    code_mutator = LocalCodeMutator()

    logger.info("🚀 Starting unlimited evolution with LOCAL resources only")

    # Evolution stats
    stats = {
        'start_time': datetime.now().isoformat(),
        'max_attempts': max_attempts,
        'successful_mutations': 0,
        'failed_mutations': 0,
        'total_attempts': 0
    }

    attempt_num = 0

    while attempt_num < max_attempts:
        attempt_num += 1
        stats['total_attempts'] = attempt_num

        # Choose random file
        target_file = random.choice(code_mutator.modifiable_files)

        try:
            # Attempt mutation (LOCAL only, no API calls!)
            mutation_result = code_mutator.attempt_mutation(target_file)

            if mutation_result['success']:
                stats['successful_mutations'] += 1

                # Store in local memory
                memory.add_knowledge(
                    text=f"Evolution #{attempt_num}\n\nFile: {target_file}\n\n{mutation_result['mutation']['mutation_idea']}",
                    source="unlimited_evolution",
                    metadata={
                        "type": "evolution_unlimited",
                        "attempt": attempt_num,
                        "file": target_file,
                        "source": mutation_result['mutation']['source']
                    }
                )

                logger.info(f"✓ Mutation #{attempt_num:,} stored (source: {mutation_result['mutation']['source']})")

            else:
                stats['failed_mutations'] += 1
                logger.warning(f"✗ Mutation #{attempt_num:,} failed")

        except Exception as e:
            stats['failed_mutations'] += 1
            logger.error(f"Error in attempt #{attempt_num:,}: {e}")

        # Progress report every 10 attempts
        if attempt_num % 10 == 0:
            memory_stats = memory.get_stats()
            elapsed = (datetime.now() - datetime.fromisoformat(stats['start_time'])).total_seconds()
            rate = attempt_num / elapsed if elapsed > 0 else 0
            eta = (max_attempts - attempt_num) / rate if rate > 0 else 0

            logger.info(f"\n{'='*60}")
            logger.info(f"Progress: {attempt_num:,}/{max_attempts:,} ({attempt_num/max_attempts*100:.2f}%)")
            logger.info(f"Successful: {stats['successful_mutations']:,}")
            logger.info(f"Failed: {stats['failed_mutations']:,}")
            logger.info(f"Success rate: {stats['successful_mutations']/attempt_num*100:.1f}%")
            logger.info(f"Knowledge: {memory_stats['total_items']:,} items")
            logger.info(f"Rate: {rate:.1f} attempts/sec")
            logger.info(f"ETA: {eta/3600:.1f} hours")
            logger.info(f"{'='*60}")

        # Checkpoint every 100 attempts
        if attempt_num % 100 == 0:
            checkpoint = {
                **stats,
                'current_attempt': attempt_num,
                'timestamp': datetime.now().isoformat(),
                'knowledge_items': memory.get_stats()['total_items']
            }

            checkpoint_file = f"data/checkpoints/unlimited_{attempt_num}.json"
            Path(checkpoint_file).parent.mkdir(parents=True, exist_ok=True)

            with open(checkpoint_file, 'w') as f:
                json.dump(checkpoint, f, indent=2)

            logger.info(f"💾 Checkpoint saved: {checkpoint_file}")

        # Brief delay (adjustable for speed)
        time.sleep(delay)

    # Final summary
    logger.info("\n" + "="*80)
    logger.info("🧬 UNLIMITED EVOLUTION COMPLETE")
    logger.info("="*80)
    logger.info(f"Total Attempts: {attempt_num:,}")
    logger.info(f"Successful: {stats['successful_mutations']:,}")
    logger.info(f"Failed: {stats['failed_mutations']:,}")
    logger.info(f"Success Rate: {stats['successful_mutations']/attempt_num*100:.1f}%")
    logger.info(f"Final Knowledge: {memory.get_stats()['total_items']:,} items")
    logger.info("\nNext: Train on accumulated evolution ideas")
    logger.info("="*80)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Unlimited Evolution - No API Limits')
    parser.add_argument('--attempts', type=int, default=100000,
                       help='Evolution attempts (default: 100,000)')
    parser.add_argument('--delay', type=float, default=1.0,
                       help='Delay between attempts in seconds (default: 1.0)')
    args = parser.parse_args()

    try:
        evolve_unlimited(max_attempts=args.attempts, delay=args.delay)
    except KeyboardInterrupt:
        print("\n\n⚠️  Evolution interrupted - progress saved")
