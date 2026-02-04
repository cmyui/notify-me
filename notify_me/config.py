"""Reminder configuration and schedule definitions."""

import tomllib
from dataclasses import dataclass
from pathlib import Path

CONFIG_DIR = Path.home() / ".config" / "notify-me"
CONFIG_FILE = CONFIG_DIR / "config.toml"

DEFAULT_CONFIG = """\
# notify-me configuration

[[reminders]]
name = "water"
title = "💧 Hydration Reminder"
message = "Time to drink some water!"
# Hours of the day to send (24-hour format)
hours = [9, 10, 11, 12, 13, 14, 15, 16, 17, 18]

[[reminders]]
name = "break"
title = "🧘 Break Reminder"
message = "Take a short break and stretch!"
hours = [11, 15]
"""


@dataclass
class Reminder:
    name: str
    title: str
    message: str
    hours: list[int]


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
        )
        for r in data.get("reminders", [])
    ]
