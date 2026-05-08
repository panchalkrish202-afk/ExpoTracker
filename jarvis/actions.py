import subprocess
import webbrowser
import os
import platform
import shlex

def open_app(app_name):
    """Opens an application based on the OS securely."""
    system = platform.system()
    try:
        if system == "Windows":
            # Use subprocess with a list to avoid shell injection
            subprocess.Popen(["cmd", "/c", "start", "", app_name])
        elif system == "Darwin":  # macOS
            subprocess.run(["open", "-a", app_name], check=True)
        else:  # Linux
            subprocess.Popen([app_name], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return f"Opening {app_name}..."
    except Exception as e:
        return f"Failed to open {app_name}: {str(e)}"

def close_app(app_name):
    """Closes an application based on the OS securely."""
    system = platform.system()
    try:
        if system == "Windows":
            subprocess.run(["taskkill", "/f", "/im", f"{app_name}.exe"], check=True)
        elif system == "Darwin":  # macOS
            subprocess.run(["pkill", "-i", app_name], check=True)
        else:  # Linux
            subprocess.run(["pkill", app_name], check=True)
        return f"Closing {app_name}..."
    except Exception as e:
        return f"Failed to close {app_name}: {str(e)}"

def google_search(query):
    """Performs a Google search."""
    # webbrowser.open handles URL encoding to some extent, but query is just a parameter here.
    url = f"https://www.google.com/search?q={query}"
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
