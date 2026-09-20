# 🎤 Dynamic Island - AI Assistant Popup

A beautiful floating notification popup (like Apple's Dynamic Island) that integrates with OpenRouter AI for intelligent responses.

## ✨ Features

- 📱 **Dynamic Island UI** - Beautiful Apple-inspired popup design
- 🤖 **OpenRouter API** - Access 50+ AI models
- 💬 **Multi-turn Conversations** - Maintain context across messages
- ⚡ **Fast Responses** - Quick, lightweight interactions
- 🎨 **Smooth Animations** - Expand/collapse with beautiful transitions
- 🌙 **Dark Mode** - Eye-friendly gradient background
- 📝 **Model Selection** - Choose from gpt-3.5, gpt-4, Claude, Mistral, etc.

## 🚀 Quick Start

### Option 1: Web Version (No installation needed)

1. Open `dynamic_island.html` in your browser
2. Click the "JARVIS AI" island at the top
3. Enter your OpenRouter API key
4. Start asking questions!

### Option 2: Python CLI

```bash
# Interactive mode
python openrouter_island.py -i

# Send a message
python openrouter_island.py -m "What is machine learning?"

# With specific model
python openrouter_island.py -m "Hello" --model gpt-4
```

## 🔑 Get OpenRouter API Key

1. Go to https://openrouter.ai
2. Sign up (free)
3. Create API key in dashboard
4. Use in Dynamic Island

```bash
export OPENROUTER_API_KEY="sk-or-v1-..."
```

## 📱 UI Elements

### Collapsed State
- Compact pill-shaped island
- Shows "JARVIS AI" text
- Green pulsing indicator
- Click to expand

### Expanded State
- Text input field
- Send button
- Response area
- Model indicator
- Smooth animations

## 🎯 Available Models

### Fast & Cheap
- `gpt-3.5-turbo` - Quick responses, good for chat
- `mistral-7b` - Open-source, fast

### Balanced
- `claude-3-sonnet` - Good quality/speed balance
- `gpt-4-turbo` - Powerful and fast

### Most Capable
- `gpt-4` - Best responses, slower
- `claude-3-opus` - Most capable Claude

### Other Options
- `llama-2-70b` - Open-source powerful
- `palm-2-chat` - Google's model

## 📝 Python Usage

```python
from openrouter_island import DynamicIslandAI

# Initialize
island = DynamicIslandAI(api_key="sk-or-v1-...")

# Change model
island.set_model("gpt-4")

# Get response
response = island.get_response("What is AI?")
print(response)

# Get as JSON
result = island.display_island("Tell me a joke")
print(result)  # Returns: {timestamp, message, response, model, status}
```

## 🎨 Customize

### Change Model in Web Version
Edit the JavaScript:
```javascript
body: JSON.stringify({
    model: 'gpt-4',  // Change this
    messages: [...],
    temperature: 0.7,
    max_tokens: 150
})
```

### Styling
Edit CSS variables:
```css
/* Colors */
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);

/* Animation speed */
transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);

/* Island size */
padding: 12px 24px;
border-radius: 50px;
```

## 💡 Examples

### Chat with gpt-4
```bash
python openrouter_island.py --model gpt-4 -i
```

### Send quick question
```bash
python openrouter_island.py -m "Explain quantum computing" --model claude-3-sonnet
```

### Check available models
```python
island = DynamicIslandAI()
print(island.list_models())
```

## 🔧 Advanced Configuration

### Custom Temperature (Creativity)
Lower = more focused, Higher = more creative

```javascript
body: JSON.stringify({
    model: 'gpt-4',
    messages: [...],
    temperature: 0.3,  // More focused
    max_tokens: 200
})
```

### Max Tokens
Control response length:
- 100 = Short answers
- 200 = Medium answers
- 500+ = Long answers

## 🌐 Browser Support

- Chrome/Chromium ✅
- Firefox ✅
- Safari ✅
- Edge ✅

## ⚙️ System Requirements

**Web Version:**
- Modern browser
- Internet connection
- OpenRouter API key

**Python Version:**
- Python 3.7+
- `requests` library
- OpenRouter API key

## 📦 Installation

```bash
# Install Python dependencies
pip install requests

# Set API key
export OPENROUTER_API_KEY="your-key-here"

# Run
python openrouter_island.py -i
```

## 🚨 Troubleshooting

### "API key not configured"
```bash
export OPENROUTER_API_KEY="sk-or-v1-..."
```

### "Connection timeout"
- Check internet connection
- Verify API key is valid
- Try a different model

### "Rate limit exceeded"
- Wait a moment and try again
- OpenRouter has free tier limits

### Model not found
```python
island.list_models()  # Check available models
island.set_model("gpt-3.5-turbo")
```

## 📚 Learn More

- [OpenRouter Docs](https://openrouter.ai/docs)
- [Available Models](https://openrouter.ai/models)
- [Pricing](https://openrouter.ai/pricing)
- [API Reference](https://openrouter.ai/api/v1)

## 🎯 Use Cases

- 💬 Quick AI chat without opening ChatGPT
- 📝 Get writing help while coding
- 🔍 Research questions instantly
- 🎓 Learning companion
- 🐛 Code debugging assistant
- 📊 Data analysis help

## 🔐 Security

- API keys are encrypted in transit (HTTPS)
- Keys not stored locally (in web version)
- Never share your API key
- Use environment variables for keys

## 📄 License

MIT - Free to use and modify

---

**Made with ❤️ for the autovideo project**

Questions? Check the repo or OpenRouter docs!
