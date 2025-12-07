#!/usr/bin/env python3
"""
EVOLUTION WITH REAL TESTING

This is the breakthrough version:
- Takes best mutation ideas from previous runs
- Actually tests if they improve intelligence
- Keeps winners, discards losers
- REAL evolution with selection pressure

Success odds: 10-20% (vs 1% without testing)
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from src.evolution.tested_evolution import TestedEvolution
from src.memory.vector_store import VectorMemory
import logging
import json
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    handlers=[
        logging.FileHandler('data/logs/tested_evolution.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def get_best_mutations(memory: VectorMemory, n: int = 50) -> list:
    """
    Retrieve the best mutation ideas from previous evolution runs

    Args:
        memory: Vector memory containing evolution ideas
        n: Number of mutations to retrieve

    Returns:
        List of (mutation_text, filepath) tuples
    """

    logger.info(f"Retrieving top {n} mutation ideas from knowledge base...")

    # Search for evolution-related mutations
    queries = [
        "improve learning efficiency code",
        "optimize reasoning performance",
        "enhance memory retrieval",
        "faster training better results",
        "smarter question generation"
    ]

    mutations = []
    seen = set()

    for query in queries:
        results = memory.search(query, n_results=n)

        for result in results:
            doc = result['text']
            meta = result['metadata']

            # Only include evolution mutations
            if meta.get('source') in ['unlimited_evolution', 'evolution', 'massive_evolution', 'local_model']:
                if meta.get('file'):
                    filepath = meta['file']
                else:
                    # Try to extract filepath from document
                    if 'learning_loop' in doc:
                        filepath = 'src/learning/learning_loop.py'
                    elif 'reasoning_engine' in doc:
                        filepath = 'src/reasoning/reasoning_engine.py'
                    elif 'vector_store' in doc:
                        filepath = 'src/memory/vector_store.py'
                    elif 'recursive_improver' in doc:
                        filepath = 'src/self_improvement/recursive_improver.py'
                    else:
                        continue

                # Avoid duplicates
                doc_hash = hash(doc[:100])
                if doc_hash not in seen:
                    mutations.append((doc, filepath))
                    seen.add(doc_hash)

                if len(mutations) >= n:
                    break

        if len(mutations) >= n:
            break

    logger.info(f"✓ Retrieved {len(mutations)} unique mutations")
    return mutations[:n]


def main(num_mutations: int = 20, questions_per_test: int = 5):
    """
    Run tested evolution on best mutations from knowledge base

    Args:
        num_mutations: How many mutations to test
        questions_per_test: Questions per intelligence test (5 = faster, 10 = more accurate)
    """

    print("\n" + "="*80)
    print("🧬 EVOLUTION WITH REAL TESTING")
    print("="*80)
    print("\nThis version actually:")
    print("  ✅ Applies code changes")
    print("  ✅ Tests intelligence before/after")
    print("  ✅ Keeps improvements")
    print("  ✅ Discards failures")
    print("\n⚡ This is REAL evolution with selection pressure!")
    print(f"Testing: {num_mutations} mutations")
    print(f"Questions per test: {questions_per_test}")
    print("="*80 + "\n")

    # Initialize
    memory = VectorMemory()
    evolution = TestedEvolution()

    # Get best mutations from knowledge base
    mutations = get_best_mutations(memory, n=num_mutations)

    if not mutations:
        logger.error("No mutations found in knowledge base!")
        logger.info("Run evolve_unlimited.py first to generate mutations")
        return

    # Run tested evolution
    results = evolution.evolve_with_testing(mutations, num_questions=questions_per_test)

    # Save results
    output_file = f"data/results/tested_evolution_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    Path(output_file).parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, 'w') as f:
        json.dump({
            'timestamp': datetime.now().isoformat(),
            'num_mutations_tested': num_mutations,
            'questions_per_test': questions_per_test,
            'results': results
        }, f, indent=2)

    logger.info(f"\n✓ Results saved to: {output_file}")

    # Print summary
    print("\n" + "="*80)
    print("🎯 FINAL RESULTS")
    print("="*80)

    if results['improvements_found'] > 0:
        print(f"\n🎉 SUCCESS! Found {results['improvements_found']} improvement(s)!")
        print(f"Intelligence improved: {results['baseline_score']:.1f}% → {results['final_score']:.1f}%")
        print(f"Total gain: +{results['improvement']:.1f}%\n")

        print("Improvements found:")
        for i, imp in enumerate(results['improvements'], 1):
            print(f"\n{i}. File: {imp['filepath']}")
            print(f"   Improvement: +{imp['improvement']:.1f}%")
            print(f"   What: {imp['mutation'].get('modification', 'N/A')[:100]}")

        print("\n🚀 RECURSIVE LOOP CAN BEGIN!")
        print("These improvements prove the concept works.")
        print("Train on successful patterns and run evolution again!")

    else:
        print(f"\n📊 No improvements found in this batch")
        print(f"Tested: {num_mutations} mutations")
        print(f"Intelligence: {results['baseline_score']:.1f}% (unchanged)")
        print("\nNext steps:")
        print("  1. Test more mutations (run with --mutations 100)")
        print("  2. Use better base model (Llama 3.3 70B)")
        print("  3. Generate more diverse mutations")

    print("="*80 + "\n")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Evolution with Real Testing')
    parser.add_argument('--mutations', type=int, default=20,
                       help='Number of mutations to test (default: 20)')
    parser.add_argument('--questions', type=int, default=5,
                       help='Questions per intelligence test (default: 5)')
    args = parser.parse_args()

    try:
        main(num_mutations=args.mutations, questions_per_test=args.questions)
    except KeyboardInterrupt:
        print("\n\n⚠️  Testing interrupted by user")
    except Exception as e:
        logger.error(f"Error: {e}")
        import traceback
        traceback.print_exc()
