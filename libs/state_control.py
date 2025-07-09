import sublime as subl

from Helios.libs.model import *
from Helios.libs.editor_utils import *

###############
## Registers ##
###############

selectedRegister = None
registerData = {}

RESERVED_REGISTERS = {
    # https://docs.helix-editor.com/registers.html

    # Default Registers
    "\"": "Last yanked text",
    "/": "Last search",
    ":": "Last executed command",
    "@": "Last recorded macro",

    # Special Registers
    "_": "Empty (All values are discarded)",
    "#": "Selection Indicies",
    ".": "Selection Contents",
    "%": "Document Path",
    "+": "System Clipboard",
    "*": "Primary Clipboard",
}

def select_register(rId: str):
    if (len(rId) > 0):
        global selectedRegister
        selectedRegister = rId[0]

def clear_selected_register():
    global selectedRegister
    selectedRegister = None

def get_register_id(defaultId: str):
    global selectedRegister
    if (isinstance(selectedRegister, str)):
        return selectedRegister[0]
    else:
        return defaultId[0]

def get_register_content(defaultId: str):
    global registerData
    rId = get_register_id(defaultId)
    registerContent = []
    if (rId in registerData):
        registerContent = registerData[rId]
    return registerContent

def add_to_register(defaultId, contents):
    rId = get_register_id(defaultId)

    # global reservedRegisters
    global registerData
    registerData[rId] = contents


##################
## Plugin State ##
##################

SETTING_KEYS = {
    "enabled": "__helios_enabled",
    "mode": "__helios_mode",
    "statusMsg": "__helios_status_mode"
}

# TODO: Load from user config
MODE_SETTINGS = {
    Mode.NORMAL: ModeSettings(caretBlock=True),
    Mode.INSERT: ModeSettings(caretBlock=False),
    Mode.SELECT: ModeSettings(caretBlock=True),
    Mode.VIEW: ModeSettings(caretBlock=True),
}

def isEnabled(view: subl.View) -> bool:
    return isPluginEnabled() and isView(view)

def isPluginEnabled() -> bool:
    return bool(subl.active_window().settings().setdefault(SETTING_KEYS["enabled"], True))

def setPluginEnabled(newState: bool):
    subl.active_window().settings().set(SETTING_KEYS["enabled"], newState)

def togglePluginEnabled():
    newVal = not isPluginEnabled()
    setPluginEnabled(newVal)

def cleanView(view: subl.View):
    if (isEnabled(view)):
        if (subl.active_window().settings().get(SETTING_KEYS["mode"]) == None):
            setMode(Mode.NORMAL, view)
    else:
        subl.active_window().settings().erase(SETTING_KEYS["mode"])
        view.erase_status(SETTING_KEYS["statusMsg"])
        view.settings().erase("block_caret")

def setMode(newMode: Mode, view: subl.View):
    subl.active_window().settings().set(SETTING_KEYS["mode"], newMode.name)
    view.settings().set('block_caret', MODE_SETTINGS[newMode].caretBlock)
    view.set_status(SETTING_KEYS["statusMsg"], f"[{newMode.name}]")

def getMode() -> Mode:
    return Mode[str(subl.active_window().settings().get(SETTING_KEYS["mode"], Mode.NORMAL.name))]
