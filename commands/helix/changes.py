import sublime_plugin as splug

from Helios.libs import subl_ext
from Helios.libs.state_control import *
from Helios.handlers.register_select import RegisterInputHandler

#############
## Changes ##
#############
# https://docs.helix-editor.com/keymap.html#changes

class HxDeleteSelectionCommand(splug.TextCommand):
    def run(self, edit):
        selectedContents = []
        for region in self.view.sel():
            selectedContents.append(self.view.substr(region))
            self.view.erase(edit, region)
        add_to_register("\"", selectedContents)

class HxChangeSelectionCommand(splug.TextCommand):
    def run(self, edit):
        for region in self.view.sel():
            self.view.erase(edit, region)
        setMode(Mode.INSERT, self.view)

class HxInsertAtLineEndCommand(splug.TextCommand):
    def run(self, edit):
        self.view.run_command(cmd="move_to", args={"to": "eol"})
        setMode(Mode.INSERT, self.view)

class HxOpenBelowCommand(splug.TextCommand):
    def run(self, edit):
        self.view.run_command(cmd="move_to", args={"to": "eol"})
        self.view.run_command(cmd="insert", args={"characters": "\n"})
        setMode(Mode.INSERT, self.view)

class HxOpenAboveCommand(splug.TextCommand):
    def run(self, edit):
        self.view.run_command(cmd="move_to", args={"to": "bol"})
        self.view.run_command(cmd="insert", args={"characters": "\n"})
        self.view.run_command(cmd="move", args={"by": "lines", "forward": False})
        setMode(Mode.INSERT, self.view)

class HxSelectRegisterCommand(subl_ext.ExtendedTextCommand):
    def run(self, edit, register):
        select_register(register)

    def input(self, args):
        return RegisterInputHandler(self)

class HxPasteAfterCommand(splug.TextCommand):
    def run(self, edit):
        registerContent = get_register_content("\"")
        if (len(registerContent) > 0):
            viewSel = self.view.sel()
            for i in range(0, len(viewSel)):
                if (str(registerContent[i % len(registerContent)]).endswith("\n")):
                    if (self.view.substr(viewSel[i].end()-1) == "\n"):
                        self.view.insert(edit, self.view.full_line(viewSel[i].end()-1).end(), registerContent[i % len(registerContent)])
                    else:
                        self.view.insert(edit, self.view.full_line(viewSel[i].end()).end(), registerContent[i % len(registerContent)])
                elif viewSel[i].size() > 0:
                    self.view.insert(edit, viewSel[i].end(), registerContent[i % len(registerContent)])
                else:
                    self.view.insert(edit, viewSel[i].end()+1, registerContent[i % len(registerContent)])

class HxPasteBeforeCommand(splug.TextCommand):
    def run(self, edit):
        global registerData
        rId = get_register_id("\"")
        registerContent = []
        if (rId in registerData):
            registerContent = registerData[rId]

        if (len(registerContent) > 0):
            viewSel = self.view.sel()
            for i in range(0, len(viewSel)):
                if (str(registerContent[i % len(registerContent)]).endswith("\n")):
                    self.view.insert(edit, self.view.full_line(viewSel[i].begin()).begin(), registerContent[i])
                else:
                    self.view.insert(edit, viewSel[i].begin(), registerContent[i])

class HxYankCommand(splug.TextCommand):
    def run(self, edit):
        selectedContents = []
        for region in self.view.sel():
            selectedContents.append(self.view.substr(region))
        add_to_register("\"", selectedContents)

