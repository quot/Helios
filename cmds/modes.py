import sublime_plugin as splug
from Helios.libs.state_control import *

class InsertModeCommand(splug.TextCommand):
    def run(self, edit):
        setMode(Mode.INSERT, view = self.view)

class NormalModeCommand(splug.TextCommand):
    def run(self, edit):
        setMode(Mode.NORMAL, view = self.view)

class SelectModeCommand(splug.TextCommand):
    def run(self, edit):
        setMode(Mode.SELECT, view = self.view)

class ViewModeCommand(splug.TextCommand):
    def run(self, edit):
        setMode(Mode.VIEW, view = self.view)

class SpaceModeCommand(splug.TextCommand):
    def run(self, edit):
        pass
