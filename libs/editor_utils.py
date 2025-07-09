from types import FunctionType
import sublime as subl

from Helios.libs.state_control import *

#############
## Helpers ##
#############

def clear_if_normal(view: subl.View):
    if (getMode() == Mode.NORMAL): clearSelected(view)

def clearSelected(view: subl.View):
    caretPoints: list[subl.Point] = []
    for range in view.sel(): caretPoints.append(range.b)
    view.sel().clear()
    view.sel().add_all(caretPoints)

# From Neovintageous
def isView(view: subl.View) -> bool:
    if not isinstance(view, subl.View): return False
    settings = view.settings()
    if settings.get('is_widget', False): return False
    # Useful for plugins to disable NeoVintageous for specific views.
    if settings.get('__vi_external_disable', False): return False
    return True
