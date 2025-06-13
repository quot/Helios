import sublime_plugin as splug

from Helios.libs.state_control import *
from Helios.libs.editor_utils import *

##############
## Movement ##
##############
# https://docs.helix-editor.com/keymap.html#movement

# FIX: Moving left and right on single character doesn't move the caret
class MoveCharLeftCommand(splug.TextCommand):
    def run(self, edit):
        global state
        if (getMode() == Mode.NORMAL): clearSelected(self.view)
        self.view.run_command(cmd="move", args={"by": "characters", "forward": False, "word_begin": False, "empty_line": False, "punct_begin": False, "separators": False, "extend": (getMode() == Mode.SELECT)})

class MoveCharRightCommand(splug.TextCommand):
    def run(self, edit):
        global state
        if (getMode() == Mode.NORMAL): clearSelected(self.view)
        self.view.run_command(cmd="move", args={"by": "characters", "forward": True, "word_begin": False, "empty_line": False, "punct_begin": False, "separators": False, "extend": (getMode() == Mode.SELECT)})

class MoveVisualLineUpCommand(splug.TextCommand):
    def run(self, edit):
        global state
        if (getMode() == Mode.NORMAL): clearSelected(self.view)
        self.view.run_command(cmd="move", args={"by": "lines", "forward": False, "word_begin": False, "empty_line": False, "punct_begin": False, "separators": False, "extend": (getMode() == Mode.SELECT)})

class MoveVisualLineDownCommand(splug.TextCommand):
    def run(self, edit):
        global state
        if (getMode() == Mode.NORMAL): clearSelected(self.view)
        self.view.run_command(cmd="move", args={"by": "lines", "forward": True, "word_begin": False, "empty_line": False, "punct_begin": False, "separators": False, "extend": (getMode() == Mode.SELECT)})

class MoveNextWordStartCommand(splug.TextCommand):
    def run(self, edit):
        global state
        if (getMode() == Mode.NORMAL): clearSelected(self.view)
        self.view.run_command(cmd="move", args={"by": "words", "forward": True, "word_begin": True, "empty_line": False, "punct_begin": False, "separators": False, "extend": True})

class MovePrevWordStartCommand(splug.TextCommand):
    def run(self, edit):
        global state
        if (getMode() == Mode.NORMAL): clearSelected(self.view)
        self.view.run_command(cmd="move", args={"by": "words", "forward": False, "word_begin": True, "empty_line": False, "punct_begin": False, "separators": False, "extend": True})

class GotoLineStartCommand(splug.TextCommand):
    def run(self, edit):
        global state
        self.view.run_command(cmd="move_to", args={"to": "bol", "extend": (getMode() == Mode.SELECT)})

class GotoLineEndCommand(splug.TextCommand):
    def run(self, edit):
        global state
        self.view.run_command(cmd="move_to", args={"to": "eol", "extend": (getMode() == Mode.SELECT)})
