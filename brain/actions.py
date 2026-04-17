from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
import os
import platform
import socket
import subprocess
import webbrowser


APP_ALIASES = {
    "notepad": ["notepad.exe"],
    "calculator": ["calc.exe"],
    "calc": ["calc.exe"],
    "paint": ["mspaint.exe"],
    "command prompt": ["cmd.exe"],
    "cmd": ["cmd.exe"],
    "powershell": ["powershell.exe"],
    "explorer": ["explorer.exe"],
}

WEBSITE_ALIASES = {
    "google": "https://www.google.com",
    "youtube": "https://www.youtube.com",
    "gmail": "https://mail.google.com",
    "github": "https://github.com",
    "spotify": "https://open.spotify.com",
}

FOLDER_ALIASES = {
    "desktop": Path.home() / "Desktop",
    "documents": Path.home() / "Documents",
    "downloads": Path.home() / "Downloads",
    "pictures": Path.home() / "Pictures",
}


@dataclass(frozen=True)
class ActionResult:
    message: str
    performed: bool = True


def tell_time() -> ActionResult:
    current_time = datetime.now().strftime("%I:%M %p").lstrip("0")
    return ActionResult(f"It is {current_time}.")


def tell_date() -> ActionResult:
    current_date = datetime.now().strftime("%A, %d %B %Y")
    return ActionResult(f"Today is {current_date}.")


def system_summary() -> ActionResult:
    host = socket.gethostname()
    system = platform.system()
    version = platform.release()
    return ActionResult(f"This PC is {host}. It is running {system} {version}.")


def open_website(target: str) -> ActionResult:
    url = WEBSITE_ALIASES.get(target.lower(), target)
    if not url.startswith(("http://", "https://")):
        url = f"https://{url}"
    webbrowser.open(url)
    return ActionResult(f"Opening {target}.")


def search_web(query: str) -> ActionResult:
    encoded_query = query.replace(" ", "+")
    webbrowser.open(f"https://www.google.com/search?q={encoded_query}")
    return ActionResult(f"Searching the web for {query}.")


def open_folder(target: str) -> ActionResult:
    folder = FOLDER_ALIASES.get(target.lower())
    if folder is None:
        return ActionResult(f"I do not know which folder {target} refers to.", False)
    os.startfile(folder)
    return ActionResult(f"Opening your {target} folder.")


def open_application(target: str) -> ActionResult:
    command = APP_ALIASES.get(target.lower())
    if command is None:
        return ActionResult(f"I do not have an app shortcut for {target} yet.", False)
    subprocess.Popen(command)
    return ActionResult(f"Opening {target}.")
