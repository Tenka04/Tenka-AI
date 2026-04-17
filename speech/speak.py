import base64
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import time

os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")

from dotenv import load_dotenv

try:
    import pygame
except ModuleNotFoundError:
    pygame = None

load_dotenv()

PIPER_COMMAND = os.getenv("PIPER_COMMAND", "piper")
PIPER_MODEL = os.getenv("PIPER_MODEL", "")
PIPER_SPEAKER_ID = os.getenv("PIPER_SPEAKER_ID", "").strip()
_LAST_VOICE_MODE = None


def _set_voice_mode(mode: str) -> None:
    global _LAST_VOICE_MODE
    if mode != _LAST_VOICE_MODE:
        print(f"[Voice] {mode}")
        _LAST_VOICE_MODE = mode


def _resolve_piper_command() -> str | None:
    if not PIPER_COMMAND:
        return None

    command_path = Path(PIPER_COMMAND)
    if command_path.exists():
        return str(command_path)

    return shutil.which(PIPER_COMMAND)


def _resolve_piper_model() -> str | None:
    if not PIPER_MODEL:
        return None

    model_path = Path(PIPER_MODEL)
    if not model_path.exists():
        return None

    return str(model_path)


def _play_audio_file(path: str) -> bool:
    if pygame is None:
        return False

    if not pygame.mixer.get_init():
        pygame.mixer.init()

    try:
        pygame.mixer.music.load(path)
        pygame.mixer.music.play()
    except Exception:
        return False

    while pygame.mixer.music.get_busy():
        time.sleep(0.1)

    return True


def _speak_with_piper(text: str) -> bool:
    command = _resolve_piper_command()
    model = _resolve_piper_model()
    if command is None or model is None:
        return False

    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as handle:
        output_path = handle.name

    args = [command, "--model", model, "--output_file", output_path]
    if PIPER_SPEAKER_ID:
        args.extend(["--speaker", PIPER_SPEAKER_ID])

    try:
        subprocess.run(
            args,
            input=text,
            text=True,
            capture_output=True,
            check=True,
            timeout=120,
        )
    except Exception:
        return False

    return _play_audio_file(output_path)


def _speak_with_windows_voice(text: str) -> bool:
    safe_text = text.replace("'", "''")
    command = (
        "Add-Type -AssemblyName System.Speech; "
        "$voice = New-Object System.Speech.Synthesis.SpeechSynthesizer; "
        f"$voice.Speak('{safe_text}')"
    )
    encoded = base64.b64encode(command.encode("utf-16le")).decode("ascii")
    try:
        subprocess.run(
            ["powershell", "-NoProfile", "-EncodedCommand", encoded],
            check=True,
            capture_output=True,
            text=True,
        )
        return True
    except Exception:
        return False


def speak(text):
    print("Tenka:", text)

    if _speak_with_piper(text):
        _set_voice_mode("Piper")
        return

    if _speak_with_windows_voice(text):
        _set_voice_mode("Local voice")
    else:
        _set_voice_mode("Text only")
