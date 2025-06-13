import sublime_plugin as splug
from Helios.libs.state_control import *
from Helios.libs.editor_utils import *

###########################
## Selection Manipultaion

class GotoNextParagraphCommand(splug.TextCommand):
    def run(self, edit):
        global state
        if (getMode() == Mode.NORMAL): clearSelected(self.view)
        newSelections: List[subl.Region] = []
        for curSel in self.view.sel():
            nextParPoint = self.view.find(pattern="^\n[^\n]", start_pt=(curSel.b+1)).end()-1
            if (nextParPoint < 0): nextParPoint = len(self.view)
            if (nextParPoint == curSel.end()):
                newSelections.append(subl.Region(a=nextParPoint, b=nextParPoint, xpos=curSel.xpos))
            else:
                newSelections.append(subl.Region(a=curSel.a, b=nextParPoint, xpos=curSel.xpos))
        self.view.sel().clear()
        self.view.sel().add_all(newSelections)
        self.view.show(self.view.sel()[0])

class GotoPrevParagraphCommand(splug.TextCommand):
    def run(self, edit):
        global state
        if (getMode() == Mode.NORMAL): clearSelected(self.view)
        newSelections: List[subl.Region] = []
        for curSel in self.view.sel():
            nextParPoint = self.view.find(pattern="^\n[^\n]", start_pt=(curSel.b-1), flags=subl.FindFlags.REVERSE).begin()+1
            if (nextParPoint < 0): nextParPoint = 0
            if (nextParPoint == curSel.begin()):
                newSelections.append(subl.Region(a=nextParPoint, b=nextParPoint, xpos=curSel.xpos))
            else:
                newSelections.append(subl.Region(a=curSel.a, b=nextParPoint, xpos=curSel.xpos))
        self.view.sel().clear()
        self.view.sel().add_all(newSelections)
        self.view.show(self.view.sel()[0])

class ExtendToLineBounds(splug.TextCommand):
    def run(self, edit):
        newRegions: List[subl.Region] = []
        for curReg in self.view.sel():
            endPoint = curReg.end()
            if curReg.a != curReg.b and self.view.substr(curReg.end()-1) == '\n':
                endPoint = curReg.end()-1
            if curReg.b >= curReg.a:
                newRegions.append(
                    subl.Region(
                        a=self.view.full_line(curReg.a).begin(),
                        b=self.view.full_line(endPoint).end()))
            else:
                newRegions.append(
                    subl.Region(
                        a=self.view.full_line(endPoint).end(),
                        b=self.view.full_line(curReg.b).begin()))
        self.view.sel().clear()
        self.view.sel().add_all(newRegions)

class ExtendLineBelowCommand(splug.TextCommand):
    def run(self, edit):
        newRegions: List[subl.Region] = []
        for curReg in self.view.sel():
            newReg = subl.Region(
                    a=self.view.full_line(curReg.begin()).a,
                    b=self.view.full_line(curReg.end()).b,
                )
            if (newReg.a, newReg.b) == (curReg.a, curReg.b):
                newReg.b = self.view.full_line((curReg.end()+1)).end()
            newRegions.append(newReg)
        self.view.sel().clear()
        self.view.sel().add_all(newRegions)
