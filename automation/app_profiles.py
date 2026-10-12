APP_PROFILES = {

    "whatsapp": {
        "window_title": "WhatsApp",
        "launch_name": "whatsapp",

        "search_shortcut": ("ctrl", "f"),
        "search_supported": True,

        "messaging_supported": True,

        # Left-side chat/contact list
        "scroll_position": (0.15, 0.55),

        # Number of mouse-wheel steps
        "scroll_steps": 10,

        # Bottom message composer
        "message_position": (0.68, 0.94),
    },

    "chrome": {
        "window_title": "Chrome",
        "launch_name": "chrome",

        "search_shortcut": ("ctrl", "l"),
        "search_supported": True,

        "messaging_supported": False,

        # Main webpage area
        "scroll_position": (0.50, 0.55),

        "scroll_steps": 10,
    },

    "notepad": {
        "window_title": "Notepad",
        "launch_name": "notepad",

        "search_shortcut": ("ctrl", "f"),
        "search_supported": True,

        "messaging_supported": False,

        # Main text area
        "scroll_position": (0.50, 0.50),

        "scroll_steps": 8,
    },

    "instagram": {
        "window_title": "Instagram",
        "launch_name": "instagram",

        "search_shortcut": None,
        "search_supported": False,

        "messaging_supported": False,

        # Main feed area
        "scroll_position": (0.50, 0.55),

        "scroll_steps": 10,
    },

    "spotify": {
        "window_title": "Spotify",
        "launch_name": "spotify",

        "search_shortcut": None,
        "search_supported": False,

        "messaging_supported": False,

        # Main content area
        "scroll_position": (0.50, 0.55),

        "scroll_steps": 10,
    },
}


def get_app_profile(app_name):
    if not app_name:
        return None

    return APP_PROFILES.get(
        app_name.lower().strip()
    )


def get_app_shortcut(app_name, action):
    profile = get_app_profile(app_name)

    if not profile:
        return None

    return profile.get(
        f"{action}_shortcut"
    )