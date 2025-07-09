import re

from Helios.libs.subl_ext import RegexListHandler
from Helios.libs.subl_ext.model import RegexListItem

class GotoInputHandler(RegexListHandler):
    def list_items(self):
        return [
            RegexListItem("g", "Goto line number <b>&lt;n&gt;</b> else file start", re.compile("[0-9]*"), "Goto line number <b>&lt;{text}&gt;</b>", re.compile("[0-9]*g")),
            RegexListItem("e", "Goto last line", re.compile("e"), "Goto last line", re.compile("e")),
        ]

