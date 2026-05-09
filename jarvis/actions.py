import subprocess
import webbrowser
import os
import platform
import re
import urllib.parse

def sanitize_app_name(name):
    """Sanitizes application name to prevent argument injection."""
    # Allow only alphanumeric, spaces, dots, and underscores.
    # Importantly, prevent names starting with hyphens.
    if not name or name.startswith('-'):
        return None
    # Use regex to keep only safe characters
    sanitized = re.sub(r'[^a-zA-Z0-9._\s-]', '', name)
    return sanitized.strip()

def open_app(app_name):
    """Opens an application based on the OS securely."""
    sanitized_name = sanitize_app_name(app_name)
    if not sanitized_name:
        return f"Invalid application name: {app_name}"

    system = platform.system()
    try:
        if system == "Windows":
            # Using list with Popen is safer
            subprocess.Popen(["cmd", "/c", "start", "", sanitized_name])
        elif system == "Darwin":  # macOS
            subprocess.run(["open", "-a", sanitized_name], check=True)
        else:  # Linux
            subprocess.Popen([sanitized_name], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return f"Opening {sanitized_name}..."
    except Exception as e:
        return f"Failed to open {sanitized_name}: {str(e)}"

def close_app(app_name):
    """Closes an application based on the OS securely."""
    sanitized_name = sanitize_app_name(app_name)
    if not sanitized_name:
        return f"Invalid application name: {app_name}"

    system = platform.system()
    try:
        if system == "Windows":
            subprocess.run(["taskkill", "/f", "/im", f"{sanitized_name}.exe"], check=True)
        elif system == "Darwin":  # macOS
            subprocess.run(["pkill", "-i", sanitized_name], check=True)
        else:  # Linux
            # Use -- to ensure sanitized_name is treated as a positional argument, not a flag
            subprocess.run(["pkill", "--", sanitized_name], check=True)
        return f"Closing {sanitized_name}..."
    except Exception as e:
        return f"Failed to close {sanitized_name}: {str(e)}"

def google_search(query):
    """Performs a Google search with proper URL encoding."""
    encoded_query = urllib.parse.quote(query)
    url = f"https://www.google.com/search?q={encoded_query}"
    webbrowser.open(url)
    return f"Searching Google for: {query}"

def ai_search(query):
    """Mocks an AI search with a clear explanation."""
    return (f"AI Search result for '{query}':\n"
            "JARVIS: To provide real-time AI insights, I require an integration with an LLM API (like OpenAI or Anthropic). "
            "Currently, I am operating in 'Local-Only' mode. Please configure an API key in your environment to enable this feature.")

def list_processes():
    """Lists running processes (simplified)."""
    try:
        if platform.system() == "Windows":
            return subprocess.check_output(["tasklist"]).decode()
        else:
            return subprocess.check_output(["ps", "aux"]).decode()
    except Exception as e:
        return f"Failed to list processes: {str(e)}"
