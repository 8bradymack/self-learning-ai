#!/bin/bash

# Self-Learning AI Setup Script

echo "=========================================="
echo "Self-Learning AI - Setup"
echo "=========================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.9 or higher."
    exit 1
fi

echo "✓ Python 3 found: $(python3 --version)"
echo ""

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "Installing dependencies..."
echo "This may take several minutes..."
pip install -r requirements.txt

echo ""
echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Copy .env.example to .env and add your API keys:"
echo "   cp .env.example .env"
echo ""
echo "2. Edit .env and add your API keys (get free keys from):"
echo "   - Groq: https://console.groq.com"
echo "   - HuggingFace: https://huggingface.co/settings/tokens"
echo ""
echo "3. Activate the virtual environment:"
echo "   source venv/bin/activate"
echo ""
echo "4. Run the system:"
echo "   python main.py --mode interactive"
echo ""
echo "For more information, see README.md"
echo ""
