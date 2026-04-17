import os

from brain.logic import handle_command
from speech.listen import listen_command, listen_for_wake_word, selected_microphone_name
from speech.speak import speak


def run_assistant() -> None:
    preferred_mic = os.getenv("TENKA_MICROPHONE_NAME")
    if preferred_mic:
        print(f"[Mic] {selected_microphone_name()} (filter: {preferred_mic})")
    else:
        print(f"[Mic] {selected_microphone_name()}")

    speak("Tenka is online.")

    while True:
        if not listen_for_wake_word():
            continue

        speak("Yes?")
        command = listen_command()
        if not command:
            speak("I did not catch that.")
            continue

        result = handle_command(command)
        speak(result.text)

        if result.should_exit:
            break


if __name__ == "__main__":
    run_assistant()
