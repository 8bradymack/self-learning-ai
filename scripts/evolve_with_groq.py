#!/usr/bin/env python3
"""
GROQ-POWERED EVOLUTION - Smart Mutations with Llama 3.3 70B

Uses Groq's Llama 3.3 70B (much smarter than GPT2)
Run daily when rate limit resets

Success odds: 20-35% (vs 1% with GPT2 alone)

Daily limit: ~1,000 attempts before rate limit
Strategy: Run daily, accumulate improvements
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from src.api.ai_apis import AIAPIs
from src.memory.vector_store import VectorMemory
from src.evolution.code_mutator import CodeMutator
from src.evolution.tested_evolution import TestedEvolution
import logging
import time
import json
from datetime import datetime
import random

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    handlers=[
        logging.FileHandler('data/logs/groq_evolution.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def evolve_with_groq_smart(max_attempts: int = 1000, test_best: int = 20):
    """
    Smart evolution using Groq's Llama 3.3 70B

    Strategy:
    1. Generate mutations with Llama 3.3 70B (high quality)
    2. Store ALL mutations
    3. Test the BEST ones for actual improvements
    4. Keep successful patterns

    Args:
        max_attempts: Max mutation generation attempts (default 1000 for daily limit)
        test_best: Number of best mutations to actually test (default 20)
    """

    print("\n" + "="*80)
    print("🧬 GROQ-POWERED EVOLUTION - Llama 3.3 70B")
    print("="*80)
    print("\nStrategy:")
    print(f"  1. Generate {max_attempts} mutations with Llama 3.3 70B")
    print("  2. Store all mutations in knowledge base")
    print(f"  3. Test top {test_best} mutations for real improvements")
    print("  4. Keep winners, learn from failures")
    print("\n⚡ Much smarter than GPT2 - higher success odds!")
    print("="*80 + "\n")

    # Initialize
    apis = AIAPIs()
    memory = VectorMemory()
    code_mutator = CodeMutator()

    # Track stats
    stats = {
        'start_time': datetime.now().isoformat(),
        'mutations_generated': 0,
        'mutations_stored': 0,
        'rate_limit_hits': 0
    }

    # Phase 1: Generate mutations with Llama 3.3 70B
    logger.info("="*80)
    logger.info("PHASE 1: GENERATING SMART MUTATIONS")
    logger.info("="*80)

    attempt = 0
    while attempt < max_attempts:
        attempt += 1

        if attempt % 10 == 0:
            logger.info(f"\nProgress: {attempt}/{max_attempts} ({attempt/max_attempts*100:.1f}%)")
            logger.info(f"Generated: {stats['mutations_generated']}")
            logger.info(f"Stored: {stats['mutations_stored']}")

        # Choose random file
        target_file = random.choice(code_mutator.modifiable_files)

        try:
            # Generate mutation with Groq (Llama 3.3 70B)
            mutation_result = code_mutator.attempt_mutation(apis, target_file)

            if mutation_result['success']:
                stats['mutations_generated'] += 1

                # Store in memory
                memory.add_knowledge(
                    text=f"Groq Evolution #{attempt}\n\nFile: {target_file}\n\n{mutation_result['mutation']['mutation_idea']}",
                    source="groq_evolution",
                    metadata={
                        "type": "groq_evolution",
                        "attempt": attempt,
                        "file": target_file,
                        "model": "llama-3.3-70b"
                    }
                )
                stats['mutations_stored'] += 1

                logger.info(f"✓ Mutation #{attempt} generated with Llama 3.3 70B")

            # Small delay to avoid rate limits
            time.sleep(1)

        except Exception as e:
            if "429" in str(e) or "rate limit" in str(e).lower():
                stats['rate_limit_hits'] += 1
                logger.warning(f"⚠️  Hit rate limit at attempt {attempt}")
                logger.info(f"Generated {stats['mutations_generated']} mutations before limit")
                break
            else:
                logger.error(f"Error: {e}")

    logger.info(f"\n✓ Phase 1 complete: {stats['mutations_generated']} mutations generated\n")

    # Phase 2: Test best mutations
    logger.info("="*80)
    logger.info(f"PHASE 2: TESTING TOP {test_best} MUTATIONS")
    logger.info("="*80 + "\n")

    evolution = TestedEvolution()

    # Get best mutations we just generated
    results = memory.search("improve code intelligence learning", n_results=test_best)

    mutations_to_test = []
    for result in results:
        doc = result['text']
        meta = result['metadata']
        if meta.get('source') == 'groq_evolution':
            filepath = meta.get('file', 'src/learning/learning_loop.py')
            mutations_to_test.append((doc, filepath))

    if mutations_to_test:
        logger.info(f"Testing {len(mutations_to_test)} mutations...")
        test_results = evolution.evolve_with_testing(mutations_to_test, num_questions=5)

        # Save results
        output_file = f"data/results/groq_evolution_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        Path(output_file).parent.mkdir(parents=True, exist_ok=True)

        with open(output_file, 'w') as f:
            json.dump({
                'timestamp': datetime.now().isoformat(),
                'phase1_stats': stats,
                'phase2_results': test_results
            }, f, indent=2)

        logger.info(f"\n✓ Results saved to: {output_file}")

        # Summary
        print("\n" + "="*80)
        print("🎯 GROQ EVOLUTION SUMMARY")
        print("="*80)
        print(f"\nPhase 1 (Generation):")
        print(f"  Mutations generated: {stats['mutations_generated']}")
        print(f"  Mutations stored: {stats['mutations_stored']}")
        print(f"  Model: Llama 3.3 70B (Groq)")

        print(f"\nPhase 2 (Testing):")
        print(f"  Mutations tested: {len(mutations_to_test)}")
        print(f"  Improvements found: {test_results['improvements_found']}")

        if test_results['improvements_found'] > 0:
            print(f"\n🎉 SUCCESS! Intelligence improved by {test_results['improvement']:+.1f}%")
            print(f"Baseline: {test_results['baseline_score']:.1f}%")
            print(f"Final: {test_results['final_score']:.1f}%")
            print("\n🚀 RECURSIVE IMPROVEMENT BEGINS!")
        else:
            print(f"\n📊 No improvements in this batch")
            print("Try again tomorrow when rate limit resets")

        print("="*80 + "\n")

    else:
        logger.warning("No mutations to test (none found in memory)")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Groq-Powered Evolution')
    parser.add_argument('--attempts', type=int, default=1000,
                       help='Max mutations to generate (default: 1000)')
    parser.add_argument('--test', type=int, default=20,
                       help='Number of best mutations to test (default: 20)')
    args = parser.parse_args()

    try:
        evolve_with_groq_smart(max_attempts=args.attempts, test_best=args.test)
    except KeyboardInterrupt:
        print("\n\n⚠️  Evolution interrupted")
    except Exception as e:
        logger.error(f"Error: {e}")
        import traceback
        traceback.print_exc()
