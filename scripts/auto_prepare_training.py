#!/usr/bin/env python3
"""
Automatic Training Preparation
Checks knowledge base and prepares training data when ready
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from src.memory.vector_store import VectorMemory
import json
from datetime import datetime

def check_and_prepare_training(min_items=100):
    """Check if we have enough data and prepare for training"""

    print("\n" + "="*60)
    print("AUTO TRAINING PREPARATION")
    print("="*60 + "\n")

    memory = VectorMemory()
    stats = memory.get_stats()

    total_items = stats['total_items']
    print(f"📊 Knowledge Base: {total_items} items")

    if total_items < min_items:
        print(f"\n⏳ Not ready yet. Need {min_items} items minimum.")
        print(f"   Currently have: {total_items}")
        print(f"   Still need: {min_items - total_items} more")
        print(f"\n💡 Tip: Run more learning cycles!")
        return False

    print(f"\n✅ Ready for training! ({total_items} items)")
    print(f"\nExporting training data...")

    # Get all items
    all_items = memory.collection.get(limit=total_items)

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
                    "completion": answer,
                    "source": metadata.get('source', 'unknown')
                })

    # Save to file
    output_file = "training_data.json"
    with open(output_file, 'w') as f:
        json.dump(training_data, f, indent=2)

    print(f"✅ Exported {len(training_data)} training examples")
    print(f"📁 Saved to: {output_file}")

    print("\n" + "="*60)
    print("NEXT STEPS FOR TRAINING:")
    print("="*60)
    print("\n1. Go to: https://colab.research.google.com")
    print("2. Upload notebooks/cloud_training.ipynb")
    print("3. Upload training_data.json")
    print("4. Run the notebook cells")
    print("5. Download the trained model")
    print("6. Extract to data/models/")
    print("\n🚀 Your AI will be smarter after training!")

    return True

if __name__ == "__main__":
    # Check every time, prepare if ready
    check_and_prepare_training(min_items=50)
