"""Determines which notifications to send based on current time."""

import json
from datetime import datetime
from pathlib import Path

from notify_me.config import Reminder

STATE_DIR = Path.home() / ".local" / "share" / "notify-me"
STATE_FILE = STATE_DIR / "state.json"


def load_state() -> dict[str, str]:
    """Load the last-sent timestamps for each reminder."""
    if not STATE_FILE.exists():
        return {}
    return json.loads(STATE_FILE.read_text())


def save_state(state: dict[str, str]) -> None:
    """Save the last-sent timestamps."""
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, indent=2))


def get_due_reminders(reminders: list[Reminder], now: datetime) -> list[Reminder]:
    """Return reminders that should be sent now."""
    state = load_state()
    current_hour = now.hour
    today_str = now.strftime("%Y-%m-%d")

    due = []
    for reminder in reminders:
        if current_hour not in reminder.hours:
            continue

        # Check if already sent this hour today
        state_key = f"{reminder.name}:{today_str}:{current_hour}"
        if state_key in state:
            continue

        due.append(reminder)

    return due


def mark_sent(reminder: Reminder, now: datetime) -> None:
    """Mark a reminder as sent for the current hour."""
    state = load_state()
    today_str = now.strftime("%Y-%m-%d")
    state_key = f"{reminder.name}:{today_str}:{now.hour}"
    state[state_key] = now.isoformat()

    # Clean up old entries (keep only today's)
    state = {k: v for k, v in state.items() if today_str in k}
    save_state(state)
