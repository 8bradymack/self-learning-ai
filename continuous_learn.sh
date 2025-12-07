#!/bin/bash

# Continuous Learning Script
# Runs the AI in learning mode indefinitely

echo "🚀 CONTINUOUS LEARNING MODE"
echo "This will run indefinitely, learning 24/7"
echo "Press Ctrl+C to stop"
echo ""

cd ~/self-learning-ai
source venv/bin/activate

# Keep learning forever in batches of 50
while true; do
    echo ""
    echo "================================"
    echo "Starting new learning batch..."
    echo "================================"

    # Run 50 learning cycles
    python main.py --mode learn --iterations 50

    # Show stats
    echo ""
    echo "Batch complete! Checking knowledge..."
    python -c "
from src.memory.vector_store import VectorMemory
memory = VectorMemory()
stats = memory.get_stats()
print(f'\n📊 KNOWLEDGE BASE: {stats[\"total_items\"]} items')
print(f'📁 Sources: {stats[\"sources\"]}')
    "

    # Brief pause
    sleep 5
done
