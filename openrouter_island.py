#!/usr/bin/env python3
"""
Dynamic Island - OpenRouter AI Integration
Creates a floating Dynamic Island popup with AI responses
"""

import requests
import json
import os
from typing import Optional
from datetime import datetime


class DynamicIslandAI:
    """Dynamic Island with OpenRouter API integration"""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("OPENROUTER_API_KEY")
        self.base_url = "https://openrouter.ai/api/v1"

        if not self.api_key:
            print("⚠️  OPENROUTER_API_KEY not set")
            print("Get it from: https://openrouter.ai")
        else:
            print("✅ OpenRouter API configured")

        self.conversation_history = []
        self.model = "gpt-3.5-turbo"  # Default model

    def set_model(self, model: str):
        """Change AI model

        Available models:
        - gpt-3.5-turbo (fast, cheap)
        - gpt-4 (powerful, slower)
        - claude-3-sonnet (balanced)
        - claude-3-opus (most capable)
        """
        self.model = model
        print(f"📝 Model set to: {model}")

    def get_response(self, user_message: str) -> str:
        """Get AI response from OpenRouter"""
        if not self.api_key:
            return "⚠️ API key not configured. Set OPENROUTER_API_KEY environment variable."

        try:
            # Add to conversation history
            self.conversation_history.append({
                "role": "user",
                "content": user_message
            })

            # Make API request
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "HTTP-Referer": "http://localhost:8000",
                "X-Title": "Dynamic Island AI",
                "Content-Type": "application/json"
            }

            payload = {
                "model": self.model,
                "messages": self.conversation_history,
                "temperature": 0.7,
                "max_tokens": 200
            }

            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload,
                timeout=10
            )

            if response.status_code != 200:
                return f"❌ Error: {response.json().get('error', {}).get('message', 'Unknown error')}"

            data = response.json()
            assistant_message = data['choices'][0]['message']['content']

            # Add to history
            self.conversation_history.append({
                "role": "assistant",
                "content": assistant_message
            })

            return assistant_message

        except Exception as e:
            return f"❌ Connection error: {str(e)}"

    def create_html_popup(self, output_file: str = "dynamic_island.html"):
        """Generate HTML file with Dynamic Island"""
        with open(output_file, 'r') as f:
            content = f.read()

        print(f"✅ Dynamic Island HTML ready: {output_file}")
        print("📱 Open in browser to use")

    def display_island(self, message: str) -> dict:
        """Return island data as JSON"""
        response = self.get_response(message)

        return {
            "timestamp": datetime.now().isoformat(),
            "message": message,
            "response": response,
            "model": self.model,
            "status": "success" if not response.startswith("❌") else "error"
        }

    def list_models(self) -> list:
        """List available models"""
        models = [
            "gpt-3.5-turbo",
            "gpt-4",
            "gpt-4-turbo",
            "claude-3-haiku",
            "claude-3-sonnet",
            "claude-3-opus",
            "mistral-7b",
            "llama-2-70b"
        ]
        return models

    def interactive_mode(self):
        """Run interactive Dynamic Island"""
        print("\n🎤 Dynamic Island - Interactive Mode")
        print("=" * 40)
        print("Commands:")
        print("  /models  - List available models")
        print("  /model <name> - Change model")
        print("  /clear   - Clear history")
        print("  /exit    - Quit")
        print("=" * 40)

        while True:
            try:
                user_input = input("\n💬 You: ").strip()

                if not user_input:
                    continue

                if user_input == "/exit":
                    print("👋 Goodbye!")
                    break

                if user_input == "/models":
                    print("Available models:")
                    for model in self.list_models():
                        print(f"  • {model}")
                    continue

                if user_input.startswith("/model "):
                    self.set_model(user_input.replace("/model ", "").strip())
                    continue

                if user_input == "/clear":
                    self.conversation_history = []
                    print("✅ Conversation cleared")
                    continue

                # Get response
                response = self.get_response(user_input)
                print(f"\n🤖 JARVIS: {response}")

            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Dynamic Island - OpenRouter AI")
    parser.add_argument("--api-key", help="OpenRouter API key")
    parser.add_argument("--model", default="gpt-3.5-turbo", help="AI model to use")
    parser.add_argument("--interactive", "-i", action="store_true", help="Interactive mode")
    parser.add_argument("--message", "-m", help="Send a message")
    parser.add_argument("--html", action="store_true", help="Generate HTML popup")

    args = parser.parse_args()

    # Initialize
    island = DynamicIslandAI(api_key=args.api_key)
    island.set_model(args.model)

    if args.html:
        island.create_html_popup()

    if args.message:
        result = island.display_island(args.message)
        print(json.dumps(result, indent=2))

    if args.interactive or (not args.message and not args.html):
        island.interactive_mode()


if __name__ == "__main__":
    main()
