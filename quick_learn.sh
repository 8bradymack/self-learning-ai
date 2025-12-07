#!/bin/bash

# Quick Learning Script
# Run this anytime to learn more!

cd ~/self-learning-ai
source venv/bin/activate

echo "🚀 Starting learning session..."
echo "Run this script anytime your computer is awake!"
echo ""

# Learn 10 cycles (100 Q&A pairs) - takes about 20-30 minutes
python main.py --mode learn --iterations 10

echo ""
echo "✅ Learning session complete!"
echo ""

# Show stats
python -c "
from src.memory.vector_store import VectorMemory
memory = VectorMemory()
stats = memory.get_stats()
print('📊 Total Knowledge:', stats['total_items'], 'items')
print('🎯 Run this script again anytime to keep learning!')
"
