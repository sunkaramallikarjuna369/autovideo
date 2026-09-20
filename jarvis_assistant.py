#!/usr/bin/env python3
"""
JARVIS - Powerful AI Voice Assistant
Controls your entire system through voice commands
Supports multiple languages
"""

import os
import sys
import json
import subprocess
import threading
import time
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any

try:
    from anthropic import Anthropic
except ImportError:
    print("Installing Anthropic...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "anthropic"])
    from anthropic import Anthropic

try:
    import speech_recognition as sr
except ImportError:
    sr = None

try:
    import pyttsx3
except ImportError:
    pyttsx3 = None


class JarvisAssistant:
    def __init__(self, language: str = "en"):
        self.language = language
        self.api_key = os.getenv("ANTHROPIC_API_KEY")

        if not self.api_key:
            print("⚠️  ANTHROPIC_API_KEY not set. Using demo mode (no AI responses)")
            self.client = None
        else:
            self.client = Anthropic(api_key=self.api_key)

        self.recognizer = sr.Recognizer() if sr else None
        self.engine = pyttsx3.init() if pyttsx3 else None
        if self.engine:
            self.engine.setProperty('rate', 150)

        self.conversation_history = []
        self.running = True
        self.commands_executed = []

        print(f"🎤 JARVIS initialized with language: {language}")
        print(f"📝 API Key: {'✓ Configured' if self.api_key else '✗ Not configured'}")
        if not sr or not pyttsx3:
            print("⚠️  Voice mode not available. Use --text-mode")

    def speak(self, text: str):
        """Convert text to speech"""
        print(f"🔊 JARVIS: {text}")
        if not self.engine:
            return
        try:
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            print(f"Error in speech: {e}")

    def listen(self) -> Optional[str]:
        """Listen to microphone input"""
        if not sr or not self.recognizer:
            return None
        try:
            with sr.Microphone() as source:
                print("🎤 Listening...")
                audio = self.recognizer.listen(source, timeout=5)

            text = self.recognizer.recognize_google(audio, language=self.language)
            print(f"👤 You: {text}")
            return text
        except sr.UnknownValueError:
            self.speak("Sorry, I didn't understand that.")
            return None
        except sr.RequestError as e:
            self.speak(f"Error with speech recognition: {e}")
            return None
        except Exception as e:
            print(f"Error: {e}")
            return None

    def process_command(self, user_input: str) -> str:
        """Process user command and generate response"""

        # Local command execution
        if any(cmd in user_input.lower() for cmd in ["open", "run", "execute"]):
            return self.execute_system_command(user_input)

        if "time" in user_input.lower():
            return f"Current time is {datetime.now().strftime('%H:%M:%S')}"

        if "date" in user_input.lower():
            return f"Today is {datetime.now().strftime('%A, %B %d, %Y')}"

        if "stop" in user_input.lower() or "exit" in user_input.lower():
            self.running = False
            return "Shutting down. Goodbye!"

        if "hello" in user_input.lower() or "hi" in user_input.lower():
            return "Hello! I'm JARVIS. How can I help you today?"

        # AI-powered response
        if self.client:
            return self.get_ai_response(user_input)
        else:
            return "I understood: " + user_input

    def get_ai_response(self, user_input: str) -> str:
        """Get response from Claude AI"""
        try:
            self.conversation_history.append({
                "role": "user",
                "content": user_input
            })

            response = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=500,
                system="You are JARVIS, a powerful AI assistant. Be concise, helpful, and direct. Keep responses under 100 words.",
                messages=self.conversation_history
            )

            assistant_message = response.content[0].text
            self.conversation_history.append({
                "role": "assistant",
                "content": assistant_message
            })

            return assistant_message
        except Exception as e:
            return f"Error getting AI response: {e}"

    def execute_system_command(self, command: str) -> str:
        """Safely execute system commands"""
        try:
            # Extract command from user input
            if "open" in command.lower():
                app = command.lower().replace("open", "").strip()
                if app in ["calculator", "calc"]:
                    subprocess.Popen("gnome-calculator" if os.name != 'nt' else "calc.exe")
                    return f"Opening {app}"
                elif app in ["terminal", "console"]:
                    subprocess.Popen("gnome-terminal" if os.name != 'nt' else "cmd.exe")
                    return f"Opening {app}"
                else:
                    return f"Can open: calculator, terminal"

            return "Command not recognized"
        except Exception as e:
            return f"Error executing command: {e}"

    def run(self):
        """Main loop"""
        self.speak("Hello! I'm JARVIS, your AI assistant. How can I help?")

        while self.running:
            try:
                user_input = self.listen()
                if not user_input:
                    continue

                response = self.process_command(user_input)
                self.speak(response)

                self.commands_executed.append({
                    "timestamp": datetime.now().isoformat(),
                    "input": user_input,
                    "response": response
                })

            except KeyboardInterrupt:
                self.speak("Shutting down.")
                break
            except Exception as e:
                print(f"Error: {e}")
                self.speak("An error occurred.")

        self.save_history()

    def save_history(self):
        """Save conversation history"""
        history_file = "jarvis_history.json"
        with open(history_file, "w") as f:
            json.dump(self.commands_executed, f, indent=2)
        print(f"📝 History saved to {history_file}")

    def run_text_mode(self):
        """Run in text mode (no voice)"""
        self.speak("JARVIS started in text mode")

        while self.running:
            try:
                user_input = input("You: ").strip()
                if not user_input:
                    continue

                response = self.process_command(user_input)
                print(f"JARVIS: {response}")

                self.commands_executed.append({
                    "timestamp": datetime.now().isoformat(),
                    "input": user_input,
                    "response": response
                })

            except KeyboardInterrupt:
                print("\nShutting down...")
                self.running = False
            except Exception as e:
                print(f"Error: {e}")

        self.save_history()


def main():
    import argparse

    parser = argparse.ArgumentParser(description="JARVIS - AI Voice Assistant")
    parser.add_argument("--language", default="en", help="Language code (en, es, fr, de, etc)")
    parser.add_argument("--text-mode", action="store_true", help="Run in text mode (no voice)")
    parser.add_argument("--api-key", help="Set ANTHROPIC_API_KEY")

    args = parser.parse_args()

    if args.api_key:
        os.environ["ANTHROPIC_API_KEY"] = args.api_key

    try:
        jarvis = JarvisAssistant(language=args.language)

        if args.text_mode:
            jarvis.run_text_mode()
        else:
            jarvis.run()

    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
