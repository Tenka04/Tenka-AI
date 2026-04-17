from __future__ import annotations

from dataclasses import dataclass
import re

from brain.actions import (
    ActionResult,
    open_application,
    open_folder,
    open_website,
    search_web,
    system_summary,
    tell_date,
    tell_time,
)


@dataclass(frozen=True)
class Reply:
    text: str
    should_exit: bool = False
    understood: bool = True


UNSAFE_PATTERNS = (
    "shutdown",
    "restart",
    "format",
    "delete everything",
    "factory reset",
)


def _clean(text: str) -> str:
    return " ".join(text.lower().strip().split())


def _match_open_target(pattern: str, text: str) -> str | None:
    match = re.search(pattern, text)
    if not match:
        return None
    return match.group(1).strip(" .?!")


def _reply_from_action(result: ActionResult) -> Reply:
    return Reply(result.message, understood=result.performed)


def reply(text: str) -> str:
    return handle_command(text).text


def handle_command(text: str) -> Reply:
    cleaned = _clean(text)
    if not cleaned:
        return Reply("I did not catch that. Please say it again.", understood=False)

    if any(phrase in cleaned for phrase in UNSAFE_PATTERNS):
        return Reply(
            "I will not run high-risk system commands automatically. "
            "We can wire those in later with explicit confirmation.",
            understood=False,
        )

    if cleaned in {"exit", "quit", "goodbye", "stop listening"}:
        return Reply("Going quiet. Call me again when you need me.", should_exit=True)

    if "time" in cleaned:
        return _reply_from_action(tell_time())

    if "date" in cleaned or "day" in cleaned:
        return _reply_from_action(tell_date())

    if "who are you" in cleaned or "your name" in cleaned:
        return Reply("I am Tenka, your desktop assistant.")

    if "help" in cleaned or "what can you do" in cleaned:
        return Reply(
            "I can open apps, websites, and folders, search the web, "
            "and answer basic PC questions like time, date, and system info."
        )

    if "system info" in cleaned or "pc info" in cleaned or "computer info" in cleaned:
        return _reply_from_action(system_summary())

    folder_target = _match_open_target(
        r"open (?:my )?(desktop|documents|downloads|pictures)", cleaned
    )
    if folder_target:
        return _reply_from_action(open_folder(folder_target))

    app_target = _match_open_target(
        r"open (notepad|calculator|calc|paint|command prompt|cmd|powershell|explorer)",
        cleaned,
    )
    if app_target:
        return _reply_from_action(open_application(app_target))

    website_target = _match_open_target(
        r"open (google|youtube|gmail|github|spotify|https?://\S+|\S+\.\S+)",
        cleaned,
    )
    if website_target:
        return _reply_from_action(open_website(website_target))

    search_match = re.search(r"(?:search for|search)\s+(.+)", cleaned)
    if search_match:
        return _reply_from_action(search_web(search_match.group(1).strip(" .?!")))

    return Reply(
        "I understood the words, but I do not know that skill yet. "
        "Right now I can open apps, folders, websites, and do simple PC info tasks.",
        understood=False,
    )
