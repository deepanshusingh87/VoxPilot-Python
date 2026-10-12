
from automation.universal_controller import controller


class ActionExecutor:

    def execute(self, action, app_name=None, value=None):

        action = action.lower().strip()

        if app_name:
            app_name = app_name.lower().strip()

        if action == "open":
            if not app_name:
                return False
            return controller.open_app(app_name)

        if action == "focus":
            return controller.focus_app(app_name)

        if action == "search":
            if not value:
                return False
            return controller.search(value, app_name)

        if action == "type":
            if not value:
                return False
            return controller.type_text(value, app_name)

        if action == "scroll down":
            return controller.scroll("down", app_name)

        if action == "scroll up":
            return controller.scroll("up", app_name)

        if action == "enter":
            return controller.press_key("enter", app_name)

        if action == "copy":
            if not controller.focus_app(app_name):
                return False
            return controller.shortcut("ctrl", "c")

        if action == "paste":
            if not controller.focus_app(app_name):
                return False
            return controller.shortcut("ctrl", "v")

        if action == "new tab":
            if not controller.focus_app(app_name):
                return False
            return controller.shortcut("ctrl", "t")

        print(f"Unsupported action: {action}")
        return False


executor = ActionExecutor()
