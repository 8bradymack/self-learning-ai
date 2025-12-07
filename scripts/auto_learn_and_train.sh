#!/bin/bash

# AUTO LEARN AND TRAIN
# Continuously learns and auto-trains when enough knowledge is accumulated

cd ~/self-learning-ai
source venv/bin/activate

echo "🚀 AUTO LEARN & TRAIN MODE"
echo "This will:"
echo "  1. Run mega learning (50 iterations)"
echo "  2. Auto-train when ready"
echo "  3. Repeat forever"
echo ""
echo "Press Ctrl+C to stop"
echo ""

cycle=1

while true; do
    echo ""
    echo "======================================================================"
    echo "CYCLE $cycle - MEGA LEARNING"
    echo "======================================================================"

    # Run mega learning
    python scripts/mega_learn.py --iterations 50

    # Check knowledge count
    knowledge_count=$(python -c "
from src.memory.vector_store import VectorMemory
memory = VectorMemory()
print(memory.get_stats()['total_items'])
")

    echo ""
    echo "📊 Current knowledge: $knowledge_count items"

    # If we have enough knowledge, train!
    if [ "$knowledge_count" -ge 500 ]; then
        echo ""
        echo "======================================================================"
        echo "CYCLE $cycle - AUTO TRAINING ($knowledge_count items)"
        echo "======================================================================"
        echo ""

        # Prepare training data
        python scripts/auto_prepare_training.py

        # Train the model
        python scripts/train_local.py

        echo ""
        echo "✅ Training complete! Your AI is smarter now."
        echo "   Continuing to learn more..."
    fi

    ((cycle++))
    sleep 5
done
