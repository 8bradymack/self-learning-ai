#!/usr/bin/env python3
"""
Export Training Data
Exports knowledge from vector DB to training format for cloud GPUs
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from src.memory.vector_store import VectorMemory
import json
from datetime import datetime

def export_training_data(output_file: str = "training_data.json", max_examples: int = 1000):
    """Export training data from vector memory"""

    print("Exporting training data...")

    memory = VectorMemory()
    stats = memory.get_stats()

    print(f"Total knowledge items: {stats['total_items']}")

    # Get all items
    sample_size = min(max_examples, stats['total_items'])

    if sample_size == 0:
        print("No data to export. Run some learning cycles first!")
        return

    all_items = memory.collection.get(limit=sample_size)

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
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w') as f:
        json.dump(training_data, f, indent=2)

    print(f"\n✓ Exported {len(training_data)} training examples to {output_file}")
    print(f"\nUpload this file to Google Colab for training!")

if __name__ == "__main__":
    export_training_data()
