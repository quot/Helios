import sublime_plugin as splug

from Helios.libs.state_control import *

####################
## Mode Switching ##
####################

# Mappings from various sections.
# https://docs.helix-editor.com/keymap.html

class HxInsertModeCommand(splug.TextCommand):
    def run(self, edit):
        setMode(Mode.INSERT, view = self.view)

class HxNormalModeCommand(splug.TextCommand):
    def run(self, edit):
        setMode(Mode.NORMAL, view = self.view)

class HxSelectModeCommand(splug.TextCommand):
    def run(self, edit):
        setMode(Mode.SELECT, view = self.view)

class HxViewModeCommand(splug.TextCommand):
    def run(self, edit):
        setMode(Mode.VIEW, view = self.view)

class HxSpaceModeCommand(splug.TextCommand):
    def run(self, edit):
        pass
