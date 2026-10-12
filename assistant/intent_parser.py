import re


def parse_intent(command):
    if not command:
        return None

    command = " ".join(command.lower().split())

    # Search in application
    match = re.match(
        r"search in (.+?) for (.+)",
        command
    )

    if match:
        return {
            "action": "search",
            "app": match.group(1).strip(),
            "value": match.group(2).strip()
        }

    # Scroll down in application
    match = re.match(
        r"scroll down in (.+)",
        command
    )

    if match:
        return {
            "action": "scroll_down",
            "app": match.group(1).strip()
        }

    # Scroll up in application
    match = re.match(
        r"scroll up in (.+)",
        command
    )

    if match:
        return {
            "action": "scroll_up",
            "app": match.group(1).strip()
        }

    # Open application
    match = re.match(
        r"(?:open|launch|start) (.+)",
        command
    )

    if match:
        return {
            "action": "open",
            "app": match.group(1).strip()
        }

    # Type text in application
    match = re.match(
        r"type (.+?) in (.+)",
        command
    )

    if match:
        return {
            "action": "type",
            "app": match.group(2).strip(),
            "value": match.group(1).strip()
        }

    return None