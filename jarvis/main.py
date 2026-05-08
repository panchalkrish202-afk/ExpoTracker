try:
    from jarvis import brain
except ImportError:
    import brain
import sys

def main():
    print("JARVIS: Initializing... System Online.")
    print("JARVIS: Hello. How can I help you today? (Type 'exit' to quit)")

    while True:
        try:
            user_input = input("You: ")
            if user_input.lower() in ['exit', 'quit', 'bye']:
                print("JARVIS: Goodbye. Shutting down systems.")
                break

            if not user_input.strip():
                continue

            response = brain.process_command(user_input)
            print(f"JARVIS: {response}")

        except KeyboardInterrupt:
            print("\nJARVIS: Forced shutdown detected. Goodbye.")
            break
        except Exception as e:
            print(f"JARVIS: An error occurred: {e}")

if __name__ == "__main__":
    main()
