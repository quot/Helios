import logging
import enum
from typing import List

import sublime as subl
import sublime_plugin as splug

# Plenty of this is based on/ripped from Neovintageous.

#############
## Logging ##
#############

logger = logging.getLogger(__package__)
logger.propagate = False
logger.setLevel(logging.INFO)

# Avoid duplicate loggers e.g., if the plugin is reloaded.
if not logger.hasHandlers():
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(logging.Formatter('HELIX.%(levelname)-7s [%(filename)20s:%(lineno)-4d] %(message)s'))
    logger.addHandler(stream_handler)

############
## Models ##
############

class Settings:
    def __init__(self, caretBlock = True):
        self.caretBlock = caretBlock

class Mode(enum.Enum):
    NORMAL = enum.auto()
    INSERT = enum.auto()
    SELECT = enum.auto()
    MINOR_VIEW = enum.auto()
    # SPACE = enum.auto()
    # GOTO = enum.auto()
    # MATCH = enum.auto()
    # COMMAND = enum.auto()
    # WINDOW = enum.auto()

minorModes: List[Mode] = [Mode.MINOR_VIEW]

#############
## Globals ##
#############

sublSettings = subl.load_settings

settings = {
    Mode.NORMAL: Settings(caretBlock=True),
    Mode.INSERT: Settings(caretBlock=False),
    Mode.SELECT: Settings(caretBlock=True),
    Mode.MINOR_VIEW: Settings(caretBlock=True),
}

state = {
    # "pluginEnabled": False,
    "pluginEnabled": True,
    "mode": Mode.NORMAL,
}

######################
## State Management ##
######################

def set_mode(newMode: Mode, view: subl.View):
    global state, sublSettings
    state["mode"] = newMode
    view.settings().set('block_caret', settings[newMode].caretBlock)
    # subl.status_message(f"[{newMode.name}]")
    view.set_status(key = "helix_mode", value = f"[{newMode.name}]")

#############
## Helpers ##
#############

def clear_selected(view: subl.View):
    points: List[subl.Point] = []
    for range in view.sel(): points.append(range.b)
    view.sel().clear()
    for point in points: view.sel().add_all(points)

# From Neovintageous
def is_view(view) -> bool:
    if not isinstance(view, subl.View): return False
    settings = view.settings()
    if settings.get('is_widget', False): return False
    # Useful for plugins to disable NeoVintageous for specific views.
    if settings.get('__vi_external_disable', False): return False
    return True

##############
## Commands ##
##############

class HelixToggleCommand(splug.TextCommand):
    def run(self, edit):
        global state
        state["pluginEnabled"] = (not state["pluginEnabled"])

class HelixDisableCommand(splug.TextCommand):
    def run(self, edit):
        global state
        state["pluginEnabled"] = False

class HelixEnableCommand(splug.TextCommand):
    def run(self, edit):
        global state
        state["pluginEnabled"] = True

class HelixIgnoreCommand(splug.TextCommand):
    # Capture unmapped input
    def run(self, edit, **kwargs):
        # character = kwargs.get('character', None)
        global state
        global minorModes
        # Minor modes should cancel if unbound input is pressed.
        if (state["mode"] in minorModes):
            set_mode(Mode.NORMAL, self.view)
        else: pass

    # def run(self, edit, character):
    #     global state
    #     global minorModes
    #     # Minor modes should cancel if unbound input is pressed.
    #     if (state["mode"] in minorModes):
    #         set_mode(Mode.NORMAL, self.view)
    #     else: pass

    # def run(self, edit):
    #     global state
    #     # Minor modes should cancel if unbound input is pressed.
    #     if (state["mode"] in minorModes):
    #         set_mode(Mode.NORMAL, self.view)

####################
## Input Handlers ##
####################
# https://docs.sublimetext.io/guide/extensibility/plugins/input_handlers/

# class MyTextInputHandler(splug.TextInputHandler):
#     def name(self):
#         return "text"

#     def placeholder(self):
#         return "Text to insert"

############
## Events ##
############

def plugin_loaded():
    pass

def plugin_unloaded():
    pass

class HelixEventListener(splug.EventListener):
    def on_query_context(self, view: subl.View, contextKey: str, operator: subl.QueryOperator, operand: str, match_all: bool):
        logger.debug(f"on_query_context triggered! Query: key [{contextKey}], operator [{operator}], operand [{operand}]")
        global state
        if (state["pluginEnabled"] and contextKey  == "helix_mode"):
            if (operator == subl.QueryOperator.EQUAL):
                return (str(operand).upper() == str(state["mode"].name))
            elif (operator == subl.QueryOperator.NOT_EQUAL):
                return (str(operand).upper() != str(state["mode"].name))
            else:
                return False
        else:
            return False

    def on_activated(self, view):
        logger.debug("on_activated triggered")
        if (is_view(view)):
            logger.debug(f"is_view: True")
            set_mode(Mode.NORMAL, view=view)
        else:
            logger.debug(f"is_view: False -- Disabling helix!")
            global state
            state["pluginEnabled"] = False

    def on_text_command(self, view, command: str, args: dict):
        logger.debug("on_text_command triggered")

    def on_post_text_command(self, view, command, args):
        logger.debug("on_post_text_command triggered")

    def on_load(self, view):
        logger.debug("on_load triggered")

    def on_post_save(self, view):
        logger.debug("on_post_save triggered")

    def on_close(self, view):
        logger.debug("on_close triggered")

    def on_deactivated(self, view):
        logger.debug("on_deactivated triggered")

    def on_exit(self):
        logger.debug("on_exit triggered")

####################
## Helix Commands ##
####################
# Direct mapping of Helix commands to Sublime commands.

#################
## Mode Switch
class InsertModeCommand(splug.TextCommand):
    def run(self, edit):
        set_mode(Mode.INSERT, view = self.view)

class NormalModeCommand(splug.TextCommand):
    def run(self, edit):
        set_mode(Mode.NORMAL, view = self.view)

class SelectModeCommand(splug.TextCommand):
    def run(self, edit):
        set_mode(Mode.SELECT, view = self.view)

class ViewModeCommand(splug.TextCommand):
    def run(self, edit):
        set_mode(Mode.MINOR_VIEW, view = self.view)

class SpaceModeCommand(splug.TextCommand):
    def run(self, edit):
        pass

##############
## Movement

class MoveCharLeftCommand(splug.TextCommand):
    def run(self, edit):
        global state
        if (state["mode"] == Mode.NORMAL): clear_selected(self.view)
        self.view.run_command(cmd="move", args={"by": "characters", "forward": False, "word_begin": False, "empty_line": False, "punct_begin": False, "separators": False, "extend": (state["mode"] == Mode.SELECT)})

class MoveCharRightCommand(splug.TextCommand):
    def run(self, edit):
        global state
        if (state["mode"] == Mode.NORMAL): clear_selected(self.view)
        self.view.run_command(cmd="move", args={"by": "characters", "forward": True, "word_begin": False, "empty_line": False, "punct_begin": False, "separators": False, "extend": (state["mode"] == Mode.SELECT)})

class MoveVisualLineUpCommand(splug.TextCommand):
    def run(self, edit):
        global state
        if (state["mode"] == Mode.NORMAL): clear_selected(self.view)
        self.view.run_command(cmd="move", args={"by": "lines", "forward": False, "word_begin": False, "empty_line": False, "punct_begin": False, "separators": False, "extend": (state["mode"] == Mode.SELECT)})

class MoveVisualLineDownCommand(splug.TextCommand):
    def run(self, edit):
        global state
        if (state["mode"] == Mode.NORMAL): clear_selected(self.view)
        self.view.run_command(cmd="move", args={"by": "lines", "forward": True, "word_begin": False, "empty_line": False, "punct_begin": False, "separators": False, "extend": (state["mode"] == Mode.SELECT)})

class MoveNextWordStartCommand(splug.TextCommand):
    def run(self, edit):
        global state
        if (state["mode"] == Mode.NORMAL): clear_selected(self.view)
        self.view.run_command(cmd="move", args={"by": "words", "forward": True, "word_begin": True, "empty_line": False, "punct_begin": False, "separators": False, "extend": True})

class MovePrevWordStartCommand(splug.TextCommand):
    def run(self, edit):
        global state
        if (state["mode"] == Mode.NORMAL): clear_selected(self.view)
        self.view.run_command(cmd="move", args={"by": "words", "forward": False, "word_begin": True, "empty_line": False, "punct_begin": False, "separators": False, "extend": True})

class GotoLineStartCommand(splug.TextCommand):
    def run(self, edit):
        global state
        self.view.run_command(cmd="move_to", args={"to": "bol", "extend": (state["mode"] == Mode.SELECT)})

class GotoLineEndCommand(splug.TextCommand):
    def run(self, edit):
        global state
        self.view.run_command(cmd="move_to", args={"to": "eol", "extend": (state["mode"] == Mode.SELECT)})

############
## Changes

class DeleteSelectionCommand(splug.TextCommand):
    def run(self, edit):
        for region in self.view.sel():
            self.view.erase(edit, region)

class ChangeSelectionCommand(splug.TextCommand):
    def run(self, edit):
        for region in self.view.sel():
            self.view.erase(edit, region)
        set_mode(Mode.INSERT, self.view)

class InsertAtLineEndCommand(splug.TextCommand):
    def run(self, edit):
        self.view.run_command(cmd="move_to", args={"to": "eol"})
        set_mode(Mode.INSERT, self.view)

class OpenBelowCommand(splug.TextCommand):
    def run(self, edit):
        self.view.run_command(cmd="move_to", args={"to": "eol"})
        self.view.run_command(cmd="insert", args={"characters": "\n"})
        set_mode(Mode.INSERT, self.view)

class OpenAboveCommand(splug.TextCommand):
    def run(self, edit):
        self.view.run_command(cmd="move_to", args={"to": "bol"})
        self.view.run_command(cmd="insert", args={"characters": "\n"})
        self.view.run_command(cmd="move", args={"by": "lines", "forward": False})
        set_mode(Mode.INSERT, self.view)

class GotoFileStartCommand(splug.TextCommand):
    def run(self, edit):
        self.view.run_command(cmd="move_to", args={"to": "bof"})

##############
## View Mode

class AlignViewCenterCommand(splug.TextCommand):
    def run(self, edit):
        if (len(self.view.sel()) > 0):
            self.view.show_at_center(self.view.sel()[0])
        set_mode(Mode.NORMAL, self.view)
