#!/bin/bash

echo "🤖 JARVIS Setup Script"
echo "======================="
echo ""

# Check Python version
echo "📌 Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python $python_version found"

# Install dependencies
echo ""
echo "📦 Installing dependencies..."
pip install -r jarvis_requirements.txt

# Check API key
echo ""
echo "🔑 Checking ANTHROPIC_API_KEY..."
if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo "⚠️  ANTHROPIC_API_KEY not set!"
    echo ""
    echo "To get your API key:"
    echo "1. Go to https://console.anthropic.com"
    echo "2. Create an account (if needed)"
    echo "3. Copy your API key"
    echo "4. Run: export ANTHROPIC_API_KEY='your-key-here'"
    echo ""
    read -p "Enter your API key (or press Enter to skip): " api_key
    if [ ! -z "$api_key" ]; then
        export ANTHROPIC_API_KEY="$api_key"
        echo "✓ API key set!"
    fi
else
    echo "✓ API key already configured"
fi

# Make script executable
chmod +x jarvis_assistant.py

echo ""
echo "✅ Setup complete!"
echo ""
echo "🚀 Quick Start:"
echo "   • Text mode: python jarvis_assistant.py --text-mode"
echo "   • Voice mode: python jarvis_assistant.py"
echo "   • Spanish: python jarvis_assistant.py --language es"
echo ""
echo "📚 For more info, see JARVIS_README.md"
echo ""

# Offer to run
read -p "Would you like to start JARVIS now? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    python jarvis_assistant.py --text-mode
fi
