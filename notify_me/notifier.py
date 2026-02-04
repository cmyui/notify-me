"""macOS notification delivery via osascript."""

import subprocess


def send_notification(title: str, message: str, sound: str = "default") -> bool:
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
