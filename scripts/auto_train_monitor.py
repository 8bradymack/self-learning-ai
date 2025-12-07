#!/usr/bin/env python3
"""
Auto-Training Monitor
Watches knowledge base and auto-trains when ready
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from src.memory.vector_store import VectorMemory
import subprocess
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def check_and_train(min_items: int = 1000, check_interval: int = 60):
    """
    Monitor knowledge base and auto-train when ready
    """

    print("\n" + "="*80)
    print("🤖 AUTO-TRAINING MONITOR ACTIVATED")
    print("="*80)
    print(f"\nMonitoring knowledge base...")
    print(f"Will auto-train when: {min_items}+ items")
    print(f"Check interval: {check_interval} seconds")
    print("\nPress Ctrl+C to stop monitoring")
    print("="*80 + "\n")

    last_trained_count = 0
    check_count = 0

    while True:
        try:
            check_count += 1
            memory = VectorMemory()
            stats = memory.get_stats()
            current_items = stats['total_items']

            print(f"\n[Check #{check_count}] Knowledge: {current_items} items", end="")

            # Check if ready for training
            if current_items >= min_items and current_items > last_trained_count:
                print("\n")
                print("="*80)
                print("🚀 TRAINING THRESHOLD REACHED!")
                print("="*80)
                print(f"\nKnowledge items: {current_items}")
                print(f"Triggering automatic training...\n")

                # Step 1: Prepare training data
                print("STEP 1: Preparing training data...")
                subprocess.run([
                    "python", "scripts/auto_prepare_training.py"
                ], cwd="/Users/bradymackintosh/self-learning-ai")
                print("✓ Training data prepared\n")

                # Step 2: Train the model
                print("STEP 2: Training model (this takes ~5 minutes)...")
                print("-" * 80)
                result = subprocess.run([
                    "python", "scripts/train_local.py"
                ], cwd="/Users/bradymackintosh/self-learning-ai")

                if result.returncode == 0:
                    print("\n" + "="*80)
                    print("✅ TRAINING COMPLETE!")
                    print("="*80)
                    print(f"\nYour AI just got smarter!")
                    print(f"Trained on {current_items} knowledge items")
                    print("\nThe model will be used automatically on next run.")
                    print("="*80 + "\n")

                    last_trained_count = current_items

                    # Update config to use trained model
                    import yaml
                    config_path = "/Users/bradymackintosh/self-learning-ai/configs/config.yaml"
                    with open(config_path, 'r') as f:
                        config = yaml.safe_load(f)

                    config['model']['base_model'] = 'data/models/trained_model'

                    with open(config_path, 'w') as f:
                        yaml.dump(config, f, default_flow_style=False)

                    print("✓ Config updated to use trained model\n")

                else:
                    print("\n⚠️ Training failed, will retry on next check\n")

            else:
                if current_items < min_items:
                    needed = min_items - current_items
                    print(f" (need {needed} more)")
                else:
                    print(f" (already trained)")

            # Wait before next check
            time.sleep(check_interval)

        except KeyboardInterrupt:
            print("\n\n" + "="*80)
            print("🛑 AUTO-TRAINING MONITOR STOPPED")
            print("="*80)
            break
        except Exception as e:
            logger.error(f"Error in monitoring: {e}")
            time.sleep(check_interval)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Auto-training monitor')
    parser.add_argument('--min-items', type=int, default=1000,
                       help='Minimum items before training')
    parser.add_argument('--interval', type=int, default=60,
                       help='Check interval in seconds')
    args = parser.parse_args()

    check_and_train(min_items=args.min_items, check_interval=args.interval)
