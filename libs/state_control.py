import sublime as subl

from Helios.libs.model import *
from Helios.libs.log import *
from Helios.libs.editor_utils import *

######################
## State Management ##
######################

settingKeys = {
    "enabled": "__helios_enabled",
    "mode": "__helios_mode",
    "statusMsg": "__helios_status_mode"
}

# TODO: Load from user config
modeSettings = {
    Mode.NORMAL: ModeSettings(caretBlock=True),
    Mode.INSERT: ModeSettings(caretBlock=False),
    Mode.SELECT: ModeSettings(caretBlock=True),
    Mode.VIEW: ModeSettings(caretBlock=True),
}

def isEnabled(view: subl.View) -> bool:
    return isPluginEnabled() and isView(view)

def isPluginEnabled() -> bool:
    # curState = subl.active_window().settings().has(settingKeys["enabled"])
    # curVal = subl.active_window().settings().get(settingKeys["enabled"])
    # logger.debug(f"isEnabled: isDefined:{curState} value:{curVal}")
    return bool(subl.active_window().settings().setdefault(settingKeys["enabled"], True))

def setPluginEnabled(newState: bool):
    logger.debug(f"window: {subl.active_window().id()}")
    subl.active_window().settings().set(settingKeys["enabled"], newState)

def togglePluginEnabled():
    logger.debug(f"window: {subl.active_window().id()}")
    newVal = not isPluginEnabled()
    logger.debug(f"current::: {isPluginEnabled()} newStatus::: {newVal}")
    setPluginEnabled(newVal)

def cleanView(view: subl.View):
    if (isEnabled(view)):
        if (subl.active_window().settings().get(settingKeys["mode"]) == None):
            setMode(Mode.NORMAL, view)
    else:
        subl.active_window().settings().erase(settingKeys["mode"])
        view.erase_status(settingKeys["statusMsg"])
        view.settings().erase("block_caret")

def setMode(newMode: Mode, view: subl.View):
    subl.active_window().settings().set(settingKeys["mode"], newMode.name)
    view.settings().set('block_caret', modeSettings[newMode].caretBlock)
    view.set_status(settingKeys["statusMsg"], f"[{newMode.name}]")

def getMode() -> Mode:
    return Mode[str(subl.active_window().settings().get(settingKeys["mode"], Mode.NORMAL.name))]
