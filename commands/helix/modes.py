import sublime
import sublime_plugin

import re

from Helios.libs import subl_ext
from Helios.libs.state_control import *
from Helios.handlers.goto_menu import GotoInputHandler

####################
## Mode Switching ##
####################

# Mappings from various sections.
# https://docs.helix-editor.com/keymap.html

class HxInsertModeCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        setMode(Mode.INSERT, view = self.view)

class HxNormalModeCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        setMode(Mode.NORMAL, view = self.view)

class HxSelectModeCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        setMode(Mode.SELECT, view = self.view)

class HxViewModeCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        setMode(Mode.VIEW, view = self.view)

class HxSpaceModeCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        pass

class HxGotoCommand(subl_ext.ExtendedTextCommand):
    def visible_to_palette(self):
        return False

    def run(self, edit, goto_value, goto_item=None):
        view = sublime.active_window().active_view()
        if (view == None):
            return
        elif (goto_item == "g"):
            line_num = re.sub("[^0-9]", "", goto_value)
            if (line_num == ""):
                view.run_command(cmd="move_to", args={"to": "bof"})
            else:
                view.run_command(cmd="goto_line", args={"line": line_num})
        elif (goto_item == "e"):
            # TODO: Needs custom command to match exact Helix behavior
            #   -- Hx moves to line before final blank line
            view.run_command(cmd="move_to", args={"to": "eof"})

    def input(self, args: dict):
        return GotoInputHandler(self)
