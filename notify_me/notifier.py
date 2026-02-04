"""macOS notification delivery via osascript."""

import subprocess
from enum import StrEnum


class NotificationSound(StrEnum):
    DEFAULT = "default"
    BASSO = "Basso"
    BLOW = "Blow"
    BOTTLE = "Bottle"
    FROG = "Frog"
    FUNK = "Funk"
    GLASS = "Glass"
    HERO = "Hero"
    MORSE = "Morse"
    PING = "Ping"
    POP = "Pop"
    PURR = "Purr"
    SOSUMI = "Sosumi"
    SUBMARINE = "Submarine"
    TINK = "Tink"


def send_notification(
    title: str,
    message: str,
    sound: NotificationSound = NotificationSound.DEFAULT,
) -> bool:
    """Send a macOS notification using osascript.

    Returns True if the notification was sent successfully.
    """
    script = f'''
    display notification "{message}" with title "{title}" sound name "{sound}"
    '''
    try:
        subprocess.run(
            ["osascript", "-e", script],
            check=True,
            capture_output=True,
        )
        return True
    except subprocess.CalledProcessError:
        return False
