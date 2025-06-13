import enum
from typing import List

class Mode(enum.Enum):
    NORMAL = enum.auto()
    INSERT = enum.auto()
    SELECT = enum.auto()
    VIEW = enum.auto()
    # SPACE = enum.auto()
    # GOTO = enum.auto()
    # MATCH = enum.auto()
    # COMMAND = enum.auto()
    # WINDOW = enum.auto()

minorModes: List[Mode] = [
    Mode.VIEW,
    # Mode.SPACE,
    # Mode.GOTO,
    # Mode.MATCH,
    # Mode.COMMAND,
    # Mode.WINDOW,
]

class ModeSettings:
    def __init__(self, caretBlock = True):
        self.caretBlock = caretBlock
