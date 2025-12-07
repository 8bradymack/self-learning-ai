#!/bin/bash

# Quick Start Script for Self-Learning AI

echo "🚀 Starting Self-Learning AI..."
echo ""

# Activate virtual environment
source venv/bin/activate

# Check if .env has API keys
if grep -q "GROQ_API_KEY=$" .env; then
    echo "⚠️  WARNING: No API keys found in .env file!"
    echo ""
    echo "Please add your API keys to .env file:"
    echo "  1. Get free Groq API key: https://console.groq.com"
    echo "  2. Edit .env file and paste your key"
    echo ""
    echo "After adding keys, run: ./start.sh"
    exit 1
fi

echo "✓ API keys configured"
echo ""

# Run the system
python main.py --mode interactive
