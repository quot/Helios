import sublime as subl
import sublime_plugin as splug

from Helios.libs.state_control import *

class HeliosToggleCommand(splug.TextCommand):
    def run(self, edit: subl.Edit):
        togglePluginEnabled()
        cleanView(self.view)

class HeliosDisableCommand(splug.TextCommand):
    def run(self, edit: subl.Edit):
        setPluginEnabled(False)
        cleanView(self.view)

class HeliosEnableCommand(splug.TextCommand):
    def run(self, edit: subl.Edit):
        setPluginEnabled(True)
        cleanView(self.view)

class HeliosInputCommand(splug.TextCommand):
    # Capture unmapped input
    def run(self, edit):
        global minorModes
        # Minor modes should cancel if unbound input is pressed.
        if (getMode() in minorModes):
            setMode(Mode.NORMAL, self.view)
        else: pass
