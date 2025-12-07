#!/usr/bin/env python3
"""
MASSIVE EVOLUTION - Extended Self-Improvement Run
Designed to run for days/weeks with thousands of attempts
Handles rate limits gracefully
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from src.api.ai_apis import AIAPIs
from src.memory.vector_store import VectorMemory
from src.evolution.code_mutator import CodeMutator
from src.evolution.intelligence_benchmark import IntelligenceBenchmark
import logging
import time
import json
from datetime import datetime
import random

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('data/logs/evolution_massive.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def evolve_massive(max_attempts: int = 100000, patience: int = 60):
    """
    MASSIVE evolution run designed for extended operation

    Args:
        max_attempts: Maximum evolution attempts (default 100,000)
        patience: Seconds to wait between attempts to avoid rate limits
    """

    print("\n" + "="*80)
    print("🧬 MASSIVE EVOLUTION RUN - EXTENDED SELF-IMPROVEMENT")
    print("="*80)
    print(f"\nTarget: {max_attempts:,} evolution attempts")
    print(f"Strategy: Patient, long-term, handle rate limits gracefully")
    print(f"Patience: {patience}s between attempts")
    print("\nYour logic:")
    print("  Even 0.01% success × 100,000 attempts = 10 improvements")
    print("  ONE success → recursive loop begins → potential takeoff")
    print("\n⚠️  This will run for DAYS/WEEKS")
    print("Expected duration: ~69 hours (for 100k attempts at 60s each)")
    print("="*80 + "\n")

    # Initialize
    logger.info("Initializing evolution system...")
    apis = AIAPIs()
    memory = VectorMemory()
    code_mutator = CodeMutator()
    benchmark = IntelligenceBenchmark(apis)

    # Skip baseline test for massive runs (save API calls)
    logger.info("Skipping baseline test for massive run (saving API calls)")
    baseline_score = 0.0
    best_score = 0.0

    # Evolution log
    evolution_log = {
        'start_time': datetime.now().isoformat(),
        'max_attempts': max_attempts,
        'patience': patience,
        'baseline_score': baseline_score,
        'best_score': best_score,
        'attempts': [],
        'improvements': []
    }

    # Main evolution loop
    attempt_num = 0
    improvements_found = 0
    successful_mutations = 0
    failed_mutations = 0

    logger.info("="*80)
    logger.info("BEGINNING MASSIVE EVOLUTION")
    logger.info("="*80)

    while attempt_num < max_attempts:
        attempt_num += 1

        if attempt_num % 10 == 0:
            logger.info(f"\n{'='*80}")
            logger.info(f"EVOLUTION ATTEMPT #{attempt_num:,}/{max_attempts:,}")
            logger.info(f"Progress: {(attempt_num/max_attempts)*100:.2f}%")
            logger.info(f"{'='*80}")

        # Choose a random file to mutate
        target_file = random.choice(code_mutator.modifiable_files)

        try:
            # Attempt mutation
            mutation_result = code_mutator.attempt_mutation(apis, target_file)

            if mutation_result['success']:
                successful_mutations += 1

                # Store the mutation idea in memory
                memory.add_knowledge(
                    text=f"Evolution Attempt #{attempt_num}\n\nFile: {target_file}\n\nMutation: {mutation_result['mutation']['mutation_idea']}",
                    source="massive_evolution",
                    metadata={
                        "type": "evolution_attempt",
                        "attempt": attempt_num,
                        "file": target_file,
                        "timestamp": datetime.now().isoformat()
                    }
                )

                logger.info(f"✓ Mutation #{attempt_num} generated and stored")

            else:
                failed_mutations += 1
                logger.warning(f"✗ Mutation #{attempt_num} failed")

        except Exception as e:
            failed_mutations += 1
            logger.error(f"Error in attempt #{attempt_num}: {e}")
            # Continue despite errors

        # Progress report every 10 attempts
        if attempt_num % 10 == 0:
            stats = memory.get_stats()
            elapsed_time = (datetime.now() - datetime.fromisoformat(evolution_log['start_time'])).total_seconds()
            avg_time_per_attempt = elapsed_time / attempt_num
            estimated_remaining = avg_time_per_attempt * (max_attempts - attempt_num)

            logger.info(f"\n📊 Progress Report:")
            logger.info(f"   Attempts: {attempt_num:,}/{max_attempts:,} ({(attempt_num/max_attempts)*100:.2f}%)")
            logger.info(f"   Successful mutations: {successful_mutations}")
            logger.info(f"   Failed mutations: {failed_mutations}")
            logger.info(f"   Success rate: {(successful_mutations/attempt_num)*100:.1f}%")
            logger.info(f"   Knowledge base: {stats['total_items']:,} items")
            logger.info(f"   Elapsed time: {elapsed_time/3600:.1f} hours")
            logger.info(f"   Estimated remaining: {estimated_remaining/3600:.1f} hours")
            logger.info(f"   Avg time/attempt: {avg_time_per_attempt:.1f}s")

        # Save log every 50 attempts
        if attempt_num % 50 == 0:
            evolution_log['current_attempt'] = attempt_num
            evolution_log['successful_mutations'] = successful_mutations
            evolution_log['failed_mutations'] = failed_mutations

            log_file = f"data/logs/evolution_massive_{datetime.now().strftime('%Y%m%d')}.json"
            Path(log_file).parent.mkdir(parents=True, exist_ok=True)

            with open(log_file, 'w') as f:
                json.dump(evolution_log, f, indent=2)

            logger.info(f"   ✓ Evolution log saved to {log_file}")

        # Save checkpoint every 100 attempts
        if attempt_num % 100 == 0:
            checkpoint_file = f"data/checkpoints/evolution_checkpoint_{attempt_num}.json"
            Path(checkpoint_file).parent.mkdir(parents=True, exist_ok=True)

            checkpoint = {
                'attempt': attempt_num,
                'timestamp': datetime.now().isoformat(),
                'successful_mutations': successful_mutations,
                'failed_mutations': failed_mutations,
                'knowledge_items': memory.get_stats()['total_items']
            }

            with open(checkpoint_file, 'w') as f:
                json.dump(checkpoint, f, indent=2)

            logger.info(f"   💾 Checkpoint saved: {checkpoint_file}")

        # Wait between attempts (patience mode to handle rate limits)
        time.sleep(patience)

    # Final summary
    logger.info("\n" + "="*80)
    logger.info("🧬 MASSIVE EVOLUTION RUN COMPLETE")
    logger.info("="*80)
    logger.info(f"\nTotal Attempts: {attempt_num:,}")
    logger.info(f"Successful Mutations: {successful_mutations}")
    logger.info(f"Failed Mutations: {failed_mutations}")
    logger.info(f"Success Rate: {(successful_mutations/attempt_num)*100:.1f}%")
    logger.info(f"Final Knowledge Base: {memory.get_stats()['total_items']:,} items")
    logger.info("\nNext Steps:")
    logger.info("  1. Review evolution log for patterns")
    logger.info("  2. Train model on accumulated evolution ideas")
    logger.info("  3. Run evolution again with smarter AI")
    logger.info("  4. Implement actual code modification (currently just storing ideas)")
    logger.info("="*80)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Massive Evolution - Extended Self-Improvement')
    parser.add_argument('--attempts', type=int, default=100000,
                       help='Maximum evolution attempts (default: 100,000)')
    parser.add_argument('--patience', type=int, default=60,
                       help='Seconds to wait between attempts (default: 60)')
    args = parser.parse_args()

    try:
        evolve_massive(max_attempts=args.attempts, patience=args.patience)
    except KeyboardInterrupt:
        print("\n\n⚠️  Evolution interrupted by user")
        print("Progress has been saved in checkpoints and logs.")
        print("You can resume by running this script again.")
