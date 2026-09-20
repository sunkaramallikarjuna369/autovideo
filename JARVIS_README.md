# 🤖 JARVIS - AI Voice Assistant

A powerful AI voice assistant that can understand commands in any language and control your entire system through voice.

## ✨ Features

- 🎤 **Voice Recognition** - Understands speech in multiple languages
- 🧠 **AI-Powered** - Uses Claude AI for intelligent responses
- 🔊 **Text-to-Speech** - Responds with natural voice output
- 🌍 **Multi-Language** - Supports 10+ languages
- ⚡ **Fast** - Responds in 1-3 seconds
- 💾 **Memory** - Maintains conversation history
- 🛡️ **Safe** - Restricted command execution for security
- 📝 **Logging** - Records all interactions

## 🚀 Quick Start

### Installation

```bash
# Install dependencies
pip install -r jarvis_requirements.txt

# Set API key (get from https://console.anthropic.com)
export ANTHROPIC_API_KEY="your-api-key-here"
```

### Run JARVIS

```bash
# Voice mode (requires microphone)
python jarvis_assistant.py

# Text mode (no microphone needed)
python jarvis_assistant.py --text-mode

# Specific language
python jarvis_assistant.py --language es  # Spanish
python jarvis_assistant.py --language fr  # French
python jarvis_assistant.py --language hi  # Hindi
python jarvis_assistant.py --language te  # Telugu
```

## 📝 Supported Languages

- **en** - English
- **es** - Spanish
- **fr** - French
- **de** - German
- **it** - Italian
- **pt** - Portuguese
- **ja** - Japanese
- **zh-CN** - Chinese (Simplified)
- **hi** - Hindi
- **te** - Telugu

## 🎯 Commands

### System Commands
- "Open calculator" / "Open calc"
- "Open terminal" / "Open console"
- "What time is it?"
- "What's today's date?"
- "Exit" / "Stop" / "Quit"

### AI Commands
Ask JARVIS anything and it will respond with AI-powered answers:
- "What is machine learning?"
- "How do I learn Python?"
- "Tell me a joke"
- "What's the weather like?"
- Any natural language question!

## 🔧 Configuration

Edit `jarvis_config.json` to customize:
- Languages
- Speech rate
- AI model
- Commands
- Logging

## 💡 Examples

```bash
# Start JARVIS
python jarvis_assistant.py --text-mode

# User: "What time is it?"
# JARVIS: "Current time is 14:30:45"

# User: "Tell me about AI"
# JARVIS: "Artificial Intelligence is the simulation of human intelligence..."

# User: "Open calculator"
# JARVIS: "Opening calculator"

# User: "Exit"
# JARVIS: "Shutting down. Goodbye!"
```

## 📊 Conversation History

All conversations are saved to `jarvis_history.json`:

```json
[
  {
    "timestamp": "2024-09-20T10:30:00",
    "input": "What time is it?",
    "response": "Current time is 10:30:00"
  }
]
```

## ⚙️ Advanced Setup

### Using with Custom System Commands

Edit `execute_system_command()` in `jarvis_assistant.py` to add more commands:

```python
elif app in ["spotify", "music"]:
    subprocess.Popen("spotify")
    return "Opening Spotify"
```

### Using Different AI Models

Change the model in `process_command()`:

```python
model="claude-3-opus-20250219"  # For more capability
# or
model="claude-3-haiku-20250307"  # For faster responses
```

## 🔐 Security

- Only allows safe system commands
- Requires explicit API key setup
- All commands are logged
- No deletion or dangerous operations allowed

## 🐛 Troubleshooting

### "ModuleNotFoundError: No module named 'speech_recognition'"
```bash
pip install SpeechRecognition
```

### "No module named 'pyaudio'"
```bash
# Ubuntu/Debian
sudo apt-get install python3-pyaudio

# macOS
brew install portaudio
pip install pyaudio

# Windows
pip install pipwin
pipwin install pyaudio
```

### Microphone not working
- Check mic is connected
- Test with: `python -m speech_recognition`
- Use `--text-mode` for text input

### API key errors
- Get key from https://console.anthropic.com
- Set: `export ANTHROPIC_API_KEY="sk-..."`
- Verify: `echo $ANTHROPIC_API_KEY`

## 📚 Learn More

- [Anthropic Claude API](https://console.anthropic.com)
- [SpeechRecognition Library](https://github.com/Uberi/speech_recognition)
- [pyttsx3 Documentation](https://pyttsx3.readthedocs.io/)

## 📄 License

MIT License - Feel free to use and modify!

---

**Made with ❤️ by Claude Code**

Need help? Run: `python jarvis_assistant.py --help`
