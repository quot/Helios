import sublime_plugin as splug

from Helios.libs.state_control import *
from Helios.libs.editor_utils import *

##############
## Movement ##
##############
# https://docs.helix-editor.com/keymap.html#movement

def move_char(region: subl.Region, extend: bool, direction: str, **args) -> subl.Region:
    log.debug(f"move_char - args: {args}")
    return region

# FIX: Moving left and right on single character doesn't move the caret
class HxMoveCharLeftCommand(splug.TextCommand):
    def run(self, edit):
        global state
        if (getMode() == Mode.NORMAL): clearSelected(self.view)
        self.view.run_command(cmd="move", args={"by": "characters", "forward": False, "word_begin": False, "empty_line": False, "punct_begin": False, "separators": False, "extend": (getMode() == Mode.SELECT)})

class HxMoveCharRightCommand(splug.TextCommand):
    def run(self, edit):
        global state
        if (getMode() == Mode.NORMAL): clearSelected(self.view)
        self.view.run_command(cmd="move", args={"by": "characters", "forward": True, "word_begin": False, "empty_line": False, "punct_begin": False, "separators": False, "extend": (getMode() == Mode.SELECT)})

class HxMoveVisualLineUpCommand(splug.TextCommand):
    def run(self, edit):
        global state
        if (getMode() == Mode.NORMAL): clearSelected(self.view)
        self.view.run_command(cmd="move", args={"by": "lines", "forward": False, "word_begin": False, "empty_line": False, "punct_begin": False, "separators": False, "extend": (getMode() == Mode.SELECT)})

class HxMoveVisualLineDownCommand(splug.TextCommand):
    def run(self, edit):
        global state
        if (getMode() == Mode.NORMAL): clearSelected(self.view)
        self.view.run_command(cmd="move", args={"by": "lines", "forward": True, "word_begin": False, "empty_line": False, "punct_begin": False, "separators": False, "extend": (getMode() == Mode.SELECT)})

class HxMoveNextWordStartCommand(splug.TextCommand):
    def run(self, edit):
        global state
        if (getMode() == Mode.NORMAL): clearSelected(self.view)
        self.view.run_command(cmd="move", args={"by": "words", "forward": True, "word_begin": True, "empty_line": False, "punct_begin": False, "separators": False, "extend": True})

class HxMovePrevWordStartCommand(splug.TextCommand):
    def run(self, edit):
        global state
        if (getMode() == Mode.NORMAL): clearSelected(self.view)
        self.view.run_command(cmd="move", args={"by": "words", "forward": False, "word_begin": True, "empty_line": False, "punct_begin": False, "separators": False, "extend": True})

class HxGotoLineStartCommand(splug.TextCommand):
    def run(self, edit):
        global state
        self.view.run_command(cmd="move_to", args={"to": "bol", "extend": (getMode() == Mode.SELECT)})

class HxGotoLineEndCommand(splug.TextCommand):
    def run(self, edit):
        global state
        self.view.run_command(cmd="move_to", args={"to": "eol", "extend": (getMode() == Mode.SELECT)})
