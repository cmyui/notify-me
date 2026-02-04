"""Command-line interface for notify-me."""

import argparse
import subprocess
import sys
from datetime import datetime
from pathlib import Path

from notify_me.config import CONFIG_FILE, load_config
from notify_me.notifier import send_notification
from notify_me.scheduler import get_due_reminders, mark_sent

LAUNCHD_PLIST = Path.home() / "Library/LaunchAgents/com.notify-me.plist"
PLIST_TEMPLATE = """\
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.notify-me</string>
    <key>ProgramArguments</key>
    <array>
        <string>{python_path}</string>
        <string>-m</string>
        <string>notify_me.cli</string>
        <string>check</string>
    </array>
    <key>StartInterval</key>
    <integer>900</integer>
    <key>RunAtLoad</key>
    <true/>
    <key>StandardOutPath</key>
    <string>{log_dir}/notify-me.log</string>
    <key>StandardErrorPath</key>
    <string>{log_dir}/notify-me.error.log</string>
</dict>
</plist>
"""


def cmd_check() -> None:
    """Check and send any due notifications."""
    reminders = load_config()
    now = datetime.now()
    due = get_due_reminders(reminders, now)

    for reminder in due:
        if send_notification(reminder.title, reminder.message, reminder.sound):
            mark_sent(reminder, now)
            print(f"Sent: {reminder.name}")


def cmd_list() -> None:
    """List all configured reminders."""
    reminders = load_config()
    print(f"Config: {CONFIG_FILE}\n")
    for r in reminders:
        hours_str = ", ".join(f"{h}:00" for h in r.hours)
        print(f"[{r.name}]")
        print(f"  Title: {r.title}")
        print(f"  Message: {r.message}")
        print(f"  Sound: {r.sound}")
        print(f"  Hours: {hours_str}")
        print()


def cmd_test(message: str) -> None:
    """Send a test notification."""
    if send_notification("notify-me Test", message):
        print("Notification sent!")
    else:
        print("Failed to send notification", file=sys.stderr)
        sys.exit(1)


def cmd_install() -> None:
    """Install the launchd service."""
    python_path = sys.executable
    log_dir = Path.home() / ".local" / "share" / "notify-me"
    log_dir.mkdir(parents=True, exist_ok=True)

    plist_content = PLIST_TEMPLATE.format(
        python_path=python_path,
        log_dir=log_dir,
    )

    LAUNCHD_PLIST.parent.mkdir(parents=True, exist_ok=True)
    LAUNCHD_PLIST.write_text(plist_content)

    subprocess.run(["launchctl", "load", str(LAUNCHD_PLIST)], check=True)
    print(f"Installed and loaded: {LAUNCHD_PLIST}")


def cmd_uninstall() -> None:
    """Uninstall the launchd service."""
    if LAUNCHD_PLIST.exists():
        subprocess.run(["launchctl", "unload", str(LAUNCHD_PLIST)], check=False)
        LAUNCHD_PLIST.unlink()
        print("Uninstalled notify-me service")
    else:
        print("Service not installed")


def main() -> None:
    parser = argparse.ArgumentParser(description="Daily notification system")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("check", help="Check and send due notifications")
    subparsers.add_parser("list", help="List configured reminders")

    test_parser = subparsers.add_parser("test", help="Send a test notification")
    test_parser.add_argument("message", help="Test message to send")

    subparsers.add_parser("install", help="Install launchd service")
    subparsers.add_parser("uninstall", help="Uninstall launchd service")

    args = parser.parse_args()

    match args.command:
        case "check":
            cmd_check()
        case "list":
            cmd_list()
        case "test":
            cmd_test(args.message)
        case "install":
            cmd_install()
        case "uninstall":
            cmd_uninstall()


if __name__ == "__main__":
    main()
