import sublime

from Helios.libs import subl_ext
from Helios.libs.state_control import *

registerSelectMenu = []
for k,v in RESERVED_REGISTERS.items():
    # Not all special registers will show in the selection menu.
    if k in ["_", "#", ".", "%", "+", "*"]:
        registerSelectMenu.append((f"{k}\t{v}", k))

class RegisterInputHandler(subl_ext.ExtendedListHandler):
    def list_items(self):
        return registerSelectMenu

    def accept_input(self, view: sublime.View) -> bool:
        if (len(view.substr(view.full_line(0))) > 0):
            return True
        else:
            return False

    # def confirm(self, text: str):
    #     logger.debug(f"Confirm value::: {text}")
