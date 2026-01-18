#!/bin/bash

# YouTube Faceless Video Generator - One Click Automation (Linux/Mac)

echo "============================================================"
echo "  YOUTUBE FACELESS VIDEO GENERATOR - ONE CLICK AUTOMATION"
echo "============================================================"
echo ""

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed!"
    echo "Please install Python 3.8+ first."
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "[SETUP] Creating virtual environment..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to create virtual environment!"
        exit 1
    fi
    echo "[SETUP] Virtual environment created successfully!"
fi

# Activate virtual environment
echo "[SETUP] Activating virtual environment..."
source venv/bin/activate

# Install/upgrade dependencies
echo "[SETUP] Installing dependencies..."
pip install --upgrade pip -q
pip install -r requirements.txt -q

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo ""
    echo "============================================================"
    echo "  API KEYS CONFIGURATION REQUIRED"
    echo "============================================================"
    echo ""
    
    if [ -f ".env.example" ]; then
        cp ".env.example" ".env"
        echo "IMPORTANT: Please edit the .env file with your API keys:"
        echo "  - GEMINI_API_KEY (Google Gemini for AI script generation)"
        echo "  - GROQ_API_KEY (Groq for faster AI script generation)"
        echo "  - PEXELS_API_KEY (Pexels for stock video footage)"
        echo "  - PIXABAY_API_KEY (Pixabay for additional stock footage)"
        echo ""
        echo "Get your free API keys from:"
        echo "  - Gemini: https://makersuite.google.com/app/apikey"
        echo "  - Groq: https://console.groq.com/keys"
        echo "  - Pexels: https://www.pexels.com/api/"
        echo "  - Pixabay: https://pixabay.com/api/docs/"
        echo ""
        echo "Edit .env file and run this script again."
        exit 0
    else
        echo "ERROR: .env.example not found!"
        exit 1
    fi
fi

# Function to show menu
show_menu() {
    clear
    echo "============================================================"
    echo "  YOUTUBE FACELESS VIDEO GENERATOR"
    echo "============================================================"
    echo ""
    echo "  1. Generate Video (Enter topic manually)"
    echo "  2. Show Trending Topics (Monetization Focused)"
    echo "  3. Interactive Mode (Step-by-step prompts)"
    echo "  4. Quick Generate (Use suggested topic)"
    echo "  5. Exit"
    echo ""
    read -p "Enter your choice (1-5): " choice
}

# Function for manual video generation
manual_generate() {
    echo ""
    read -p "Enter video topic: " topic
    if [ -z "$topic" ]; then
        echo "ERROR: Topic cannot be empty!"
        read -p "Press Enter to continue..."
        return
    fi
    
    read -p "Enter video length in minutes (default: 8): " length
    length=${length:-8}
    
    read -p "Choose AI provider (auto/groq/gemini/ollama, default: auto): " ai
    ai=${ai:-auto}
    
    echo ""
    echo "============================================================"
    echo "  GENERATING VIDEO"
    echo "============================================================"
    echo "  Topic: $topic"
    echo "  Length: $length minutes"
    echo "  AI Provider: $ai"
    echo "============================================================"
    echo ""
    
    python3 autovideo.py --topic "$topic" --length "$length" --ai "$ai"
    
    echo ""
    echo "============================================================"
    echo "  VIDEO GENERATION COMPLETE!"
    echo "============================================================"
    echo ""
    echo "Your video files are in the projects folder."
    echo ""
    read -p "Press Enter to continue..."
}

# Function to show trending topics
show_trends() {
    echo ""
    echo "============================================================"
    echo "  FETCHING TRENDING TOPICS..."
    echo "============================================================"
    echo ""
    python3 autovideo.py --suggest-topics
    echo ""
    read -p "Press Enter to continue..."
}

# Function for interactive mode
interactive_mode() {
    echo ""
    python3 autovideo.py --interactive
    echo ""
    read -p "Press Enter to continue..."
}

# Function for quick generate
quick_generate() {
    echo ""
    echo "============================================================"
    echo "  QUICK GENERATE - HIGH CPM TOPICS"
    echo "============================================================"
    echo ""
    echo "Select a topic category:"
    echo "  1. Finance (CPM: \$15-\$50)"
    echo "  2. Technology (CPM: \$10-\$30)"
    echo "  3. Business (CPM: \$12-\$35)"
    echo "  4. Health (CPM: \$10-\$25)"
    echo "  5. Education (CPM: \$8-\$20)"
    echo ""
    read -p "Enter category (1-5): " cat
    
    case $cat in
        1) topic="5 Investment Mistakes That Cost You Thousands" ;;
        2) topic="AI Tools That Will Change Your Life" ;;
        3) topic="Business Ideas You Can Start Today" ;;
        4) topic="Morning Habits of Successful People" ;;
        5) topic="Skills That Will Make You Rich" ;;
        *) echo "Invalid selection!"; read -p "Press Enter to continue..."; return ;;
    esac
    
    echo ""
    echo "Selected topic: $topic"
    echo ""
    read -p "Generate video with this topic? (y/n): " confirm
    
    if [ "$confirm" != "y" ] && [ "$confirm" != "Y" ]; then
        return
    fi
    
    echo ""
    echo "============================================================"
    echo "  GENERATING VIDEO"
    echo "============================================================"
    echo "  Topic: $topic"
    echo "  Length: 8 minutes"
    echo "  AI Provider: auto"
    echo "============================================================"
    echo ""
    
    python3 autovideo.py --topic "$topic" --length 8 --ai auto
    
    echo ""
    echo "============================================================"
    echo "  VIDEO GENERATION COMPLETE!"
    echo "============================================================"
    echo ""
    read -p "Press Enter to continue..."
}

# Main loop
while true; do
    show_menu
    case $choice in
        1) manual_generate ;;
        2) show_trends ;;
        3) interactive_mode ;;
        4) quick_generate ;;
        5) echo ""; echo "Thank you for using YouTube Faceless Video Generator!"; deactivate 2>/dev/null; exit 0 ;;
        *) echo "Invalid choice!"; read -p "Press Enter to continue..." ;;
    esac
done
