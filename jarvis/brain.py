from jarvis import actions
import re

def process_command(command):
    command = command.strip()
    command_lower = command.lower()

    # Match "open [app]"
    open_match = re.match(r"^open\s+(.+)", command_lower)
    if open_match:
        app_name = open_match.group(1).strip()
        return actions.open_app(app_name)

    # Match "close [app]" or "stop [app]"
    close_match = re.match(r"^(close|stop)\s+(.+)", command_lower)
    if close_match:
        app_name = close_match.group(2).strip()
        return actions.close_app(app_name)

    # Match "search google for [query]" or "google [query]"
    google_match = re.match(r"^(search google for|google)\s+(.+)", command_lower)
    if google_match:
        query = google_match.group(2).strip()
        return actions.google_search(query)

    # Match "ai search [query]" or "ask ai [query]"
    ai_match = re.match(r"^(ai search|ask ai)\s+(.+)", command_lower)
    if ai_match:
        query = ai_match.group(2).strip()
        return actions.ai_search(query)

    if command_lower in ["hello", "hi", "hey"]:
        return "Hello, I am JARVIS. How can I assist you today?"

    return ("I am not sure how to help with that command.\n"
            "Try: 'open [app]', 'close [app]', 'google [query]', or 'ai search [query]'.")
