import sublime_plugin as splug

from Helios.libs.state_control import *

###############
## View Mode ##
###############
# https://docs.helix-editor.com/keymap.html#view-mode

class HxAlignViewCenterCommand(splug.TextCommand):
    def run(self, edit):
        if (len(self.view.sel()) > 0):
            self.view.show_at_center(self.view.sel()[0])
        setMode(Mode.NORMAL, self.view)
