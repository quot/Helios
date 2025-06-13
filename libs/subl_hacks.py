import sublime_plugin
import traceback

# Command that can only be triggered from a key bind.
# Adding the command to Default.sublime-commands will make the command
# avaiable for InputHandlers without showing in the command palette.
class KeyBindTextCommand(sublime_plugin.TextCommand):
    def is_visible(self) -> bool:
        # Replace with co_qualname when it becomes available
        # https://docs.python.org/3/library/inspect.html#types-and-members
        #
        # This seems to be the best way to tell if a keypress is the origin
        # of the command event. Requests from the command palette will originate
        # from the `is_visible_` method.
        # Ideally, this can be replaced with something that is sure the request
        # is from a key press.
        return (traceback.extract_stack()[0].name == "run_")
