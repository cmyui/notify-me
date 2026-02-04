"""Reminder configuration and schedule definitions."""

import tomllib
from dataclasses import dataclass
from pathlib import Path

from notify_me.notifier import NotificationSound

CONFIG_DIR = Path.home() / ".config" / "notify-me"
CONFIG_FILE = CONFIG_DIR / "config.toml"

DEFAULT_CONFIG = """\
# notify-me configuration
# Available sounds: default, Basso, Blow, Bottle, Frog, Funk, Glass,
#                   Hero, Morse, Ping, Pop, Purr, Sosumi, Submarine, Tink

[[reminders]]
name = "water"
title = "💧 Hydration Reminder"
message = "Time to drink some water!"
sound = "default"
# Hours of the day to send (24-hour format)
hours = [9, 10, 11, 12, 13, 14, 15, 16, 17, 18]

[[reminders]]
name = "break"
title = "🧘 Break Reminder"
message = "Take a short break and stretch!"
sound = "Funk"
hours = [11, 15]
"""


@dataclass
class Reminder:
    name: str
    title: str
    message: str
    hours: list[int]
    sound: NotificationSound = NotificationSound.DEFAULT


def load_config() -> list[Reminder]:
    """Load reminders from config file, creating default if needed."""
    if not CONFIG_FILE.exists():
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        CONFIG_FILE.write_text(DEFAULT_CONFIG)

    with open(CONFIG_FILE, "rb") as f:
        data = tomllib.load(f)

    return [
        Reminder(
            name=r["name"],
            title=r["title"],
            message=r["message"],
            hours=r["hours"],
            sound=NotificationSound(r.get("sound", "default")),
        )
        for r in data.get("reminders", [])
    ]
