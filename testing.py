import sublime_plugin as splug

from Helios.libs import subl_ext
from Helios.libs.state_control import *
from Helios.libs import handlers


class YankCommand(splug.TextCommand):
    def run(self, edit):
        selectedContents = []
        for region in self.view.sel():
            selectedContents.append(self.view.substr(region))
        add_to_register("\"", selectedContents)
