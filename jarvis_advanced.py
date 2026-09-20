#!/usr/bin/env python3
"""
JARVIS Advanced - Extended system control capabilities
Includes file operations, process management, and system monitoring
"""

import os
import sys
import json
import subprocess
import psutil
import platform
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, List

from jarvis_assistant import JarvisAssistant


class JarvisAdvanced(JarvisAssistant):
    """Extended JARVIS with advanced system control"""

    def __init__(self, language: str = "en"):
        super().__init__(language)
        self.system_info = self.get_system_info()
        print(f"💻 System: {self.system_info['os']}")

    def get_system_info(self) -> Dict:
        """Get system information"""
        return {
            "os": platform.system(),
            "platform": platform.platform(),
            "processor": platform.processor(),
            "cpu_count": psutil.cpu_count(),
            "total_memory": psutil.virtual_memory().total,
        }

    def get_system_status(self) -> str:
        """Get current system status"""
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')

        return f"""
System Status:
- CPU: {cpu_percent}%
- Memory: {memory.percent}% ({memory.used // (1024**3)}GB / {memory.total // (1024**3)}GB)
- Disk: {disk.percent}% ({disk.used // (1024**3)}GB / {disk.total // (1024**3)}GB)
- Running Processes: {len(psutil.pids())}
"""

    def get_running_processes(self, limit: int = 5) -> str:
        """Get top running processes"""
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'memory_percent']):
            try:
                processes.append(proc)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

        top_processes = sorted(processes,
                              key=lambda p: p.info['memory_percent'] or 0,
                              reverse=True)[:limit]

        result = "Top Processes:\n"
        for proc in top_processes:
            result += f"- {proc.info['name']}: {proc.info['memory_percent']:.2f}%\n"

        return result

    def list_files(self, directory: str = ".") -> str:
        """List files in directory"""
        try:
            path = Path(directory).expanduser()
            if not path.exists():
                return f"Directory not found: {directory}"

            files = list(path.iterdir())[:10]  # Limit to 10 files
            result = f"Files in {directory}:\n"
            for f in files:
                result += f"- {f.name}\n"

            return result
        except Exception as e:
            return f"Error listing files: {e}"

    def get_file_info(self, filepath: str) -> str:
        """Get file information"""
        try:
            path = Path(filepath).expanduser()
            if not path.exists():
                return f"File not found: {filepath}"

            stat = path.stat()
            size_mb = stat.st_size / (1024 * 1024)

            return f"""
File: {path.name}
- Size: {size_mb:.2f}MB
- Modified: {datetime.fromtimestamp(stat.st_mtime)}
- Type: {'Directory' if path.is_dir() else 'File'}
"""
        except Exception as e:
            return f"Error getting file info: {e}"

    def list_processes(self, search: Optional[str] = None) -> str:
        """List running processes"""
        processes = []
        try:
            for proc in psutil.process_iter(['pid', 'name']):
                if search and search.lower() in proc.info['name'].lower():
                    processes.append(proc.info['name'])

            if not processes:
                return f"No processes found matching '{search}'"

            result = "Running Processes:\n"
            for proc in processes[:10]:
                result += f"- {proc}\n"

            return result
        except Exception as e:
            return f"Error listing processes: {e}"

    def kill_process(self, process_name: str) -> str:
        """Safely kill a process"""
        try:
            killed = False
            for proc in psutil.process_iter(['pid', 'name']):
                if process_name.lower() in proc.info['name'].lower():
                    proc.kill()
                    killed = True

            if killed:
                return f"Successfully terminated {process_name}"
            else:
                return f"Process '{process_name}' not found"
        except Exception as e:
            return f"Error killing process: {e}"

    def set_brightness(self, level: int) -> str:
        """Set screen brightness (Linux only)"""
        try:
            if level < 0 or level > 100:
                return "Brightness must be between 0 and 100"

            # For Linux with xrandr
            if platform.system() == "Linux":
                brightness = level / 100
                os.system(f"xrandr --output $(xrandr | grep ' connected' | head -1 | cut -d' ' -f1) --brightness {brightness}")
                return f"Brightness set to {level}%"
            else:
                return "Brightness control not available on this system"
        except Exception as e:
            return f"Error setting brightness: {e}"

    def take_screenshot(self, filename: str = "screenshot.png") -> str:
        """Take a screenshot"""
        try:
            import subprocess

            if platform.system() == "Linux":
                subprocess.run(["import", "-window", "root", filename], check=True)
            elif platform.system() == "Darwin":  # macOS
                subprocess.run(["screencapture", filename], check=True)
            elif platform.system() == "Windows":
                from PIL import ImageGrab
                ImageGrab.grab().save(filename)

            return f"Screenshot saved as {filename}"
        except Exception as e:
            return f"Error taking screenshot: {e}"

    def process_command(self, user_input: str) -> str:
        """Process advanced commands"""
        lower_input = user_input.lower()

        # System status
        if "system status" in lower_input or "system info" in lower_input:
            return self.get_system_status()

        if "running processes" in lower_input or "top processes" in lower_input:
            return self.get_running_processes()

        if "list files" in lower_input or "show files" in lower_input:
            return self.list_files()

        if "file info" in lower_input:
            # Extract filename
            parts = user_input.split("file info")
            if len(parts) > 1:
                filename = parts[1].strip()
                return self.get_file_info(filename)

        if "list processes" in lower_input:
            search_term = user_input.replace("list processes", "").strip() or None
            return self.list_processes(search_term)

        if "kill process" in lower_input:
            parts = user_input.split("kill process")
            if len(parts) > 1:
                process_name = parts[1].strip()
                return self.kill_process(process_name)

        if "brightness" in lower_input:
            try:
                level = int(''.join(filter(str.isdigit, user_input)))
                return self.set_brightness(level)
            except:
                return "Please specify brightness level (0-100)"

        if "screenshot" in lower_input or "take screenshot" in lower_input:
            return self.take_screenshot()

        # Fall back to parent class
        return super().process_command(user_input)


def main():
    import argparse

    parser = argparse.ArgumentParser(description="JARVIS Advanced - AI Assistant with System Control")
    parser.add_argument("--language", default="en", help="Language code")
    parser.add_argument("--text-mode", action="store_true", help="Run in text mode")
    parser.add_argument("--api-key", help="Set ANTHROPIC_API_KEY")

    args = parser.parse_args()

    if args.api_key:
        os.environ["ANTHROPIC_API_KEY"] = args.api_key

    try:
        jarvis = JarvisAdvanced(language=args.language)

        if args.text_mode:
            jarvis.run_text_mode()
        else:
            jarvis.run()

    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
