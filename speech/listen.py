import os

import speech_recognition as sr

WAKE_WORD = "hello"


def available_microphones() -> list[str]:
    return sr.Microphone.list_microphone_names()


def _preferred_microphone_index() -> int | None:
    preferred_name = os.getenv("TENKA_MICROPHONE_NAME", "").strip().lower()
    if not preferred_name:
        return None

    for index, name in enumerate(available_microphones()):
        if preferred_name in name.lower():
            return index
    return None


def _microphone() -> sr.Microphone:
    return sr.Microphone(device_index=_preferred_microphone_index())


def selected_microphone_name() -> str:
    index = _preferred_microphone_index()
    microphones = available_microphones()
    if index is None:
        return "System default"
    if 0 <= index < len(microphones):
        return microphones[index]
    return "System default"


def _listen(prompt: str) -> sr.AudioData | None:
    recognizer = sr.Recognizer()
    recognizer.pause_threshold = 0.8

    with _microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1.0)
        print(prompt)
        try:
            return recognizer.listen(source, timeout=5, phrase_time_limit=8)
        except sr.WaitTimeoutError:
            return None


def _recognize(audio: sr.AudioData | None) -> str:
    if audio is None:
        return ""

    recognizer = sr.Recognizer()
    try:
        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        return ""
    except sr.RequestError as error:
        print("Speech service unavailable.")
        return ""


def listen_for_wake_word():
    audio = _listen("[Wake] Say hello")
    text = _recognize(audio).lower()
    return WAKE_WORD in text


def listen_command():
    audio = _listen("[Listen] Command")
    return _recognize(audio)
