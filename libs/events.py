import sublime as subl
import sublime_plugin as splug

from Helios.libs.log import *
from Helios.libs.state_control import *
from Helios.libs.editor_utils import *

#####################
## Event Listeners ##
#####################

def plugin_loaded():
    subl.active_window().settings().erase("__helios_enabled")
    # pass

# def plugin_unloaded():
#     pass

class HeliosEventListener(splug.EventListener):
    def on_query_context(self, view: subl.View, contextKey: str, operator: subl.QueryOperator, operand: str, match_all: bool) -> bool:
        if (isEnabled(view) and contextKey == "helios_mode"):
            if (operator == subl.QueryOperator.EQUAL):
                return (str(operand).upper() == str(getMode().name))
            elif (operator == subl.QueryOperator.NOT_EQUAL):
                return (str(operand).upper() != str(getMode().name))
            else:
                return False
        else:
            return False

    def on_activated(self, view):
        activeInView = isEnabled(view) and isView(view)
        if activeInView:
            setMode(Mode.NORMAL, view=view)
        else:
            cleanView(view)
        # log.debug(f"on_activated triggered! Enabled for view: {activeInView}")

    # def on_text_command(self, view, command: str, args: dict):
    #     return None

    def on_post_text_command(self, view, command_name, args):
        if (not command_name in ["select_register"]):
            clear_selected_register()


    # def on_load(self, view):
    #     log.debug("on_load triggered")

    # def on_post_save(self, view):
    #     log.debug("on_post_save triggered")

    # def on_close(self, view):
    #     log.debug("on_close triggered")

    # def on_deactivated(self, view):
    #     log.debug("on_deactivated triggered")

    # def on_exit(self):
    #     log.debug("on_exit triggered")
