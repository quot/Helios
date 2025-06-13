import sublime_plugin as splug

from Helios.libs.state_control import *

#############
## Changes ##
#############
# https://docs.helix-editor.com/keymap.html#changes

class DeleteSelectionCommand(splug.TextCommand):
    def run(self, edit):
        for region in self.view.sel():
            self.view.erase(edit, region)

class ChangeSelectionCommand(splug.TextCommand):
    def run(self, edit):
        for region in self.view.sel():
            self.view.erase(edit, region)
        setMode(Mode.INSERT, self.view)

class InsertAtLineEndCommand(splug.TextCommand):
    def run(self, edit):
        self.view.run_command(cmd="move_to", args={"to": "eol"})
        setMode(Mode.INSERT, self.view)

class OpenBelowCommand(splug.TextCommand):
    def run(self, edit):
        self.view.run_command(cmd="move_to", args={"to": "eol"})
        self.view.run_command(cmd="insert", args={"characters": "\n"})
        setMode(Mode.INSERT, self.view)

class OpenAboveCommand(splug.TextCommand):
    def run(self, edit):
        self.view.run_command(cmd="move_to", args={"to": "bol"})
        self.view.run_command(cmd="insert", args={"characters": "\n"})
        self.view.run_command(cmd="move", args={"by": "lines", "forward": False})
        setMode(Mode.INSERT, self.view)

class GotoFileStartCommand(splug.TextCommand):
    def run(self, edit):
        self.view.run_command(cmd="move_to", args={"to": "bof"})




# def try_eval(str):
#     try:
#         return eval(str, {}, {})
#     except Exception:
#         return None


# def eval_expr(orig, i, expr):
#     x = try_eval(orig) or 0

#     return eval(expr, {"s": orig, "x": x, "i": i, "math": math}, {})


# class ExprInputHandler(splug.TextInputHandler):
#     def __init__(self, view):
#         self.view = view

#     def placeholder(self):
#         return "Expression"

#     def initial_text(self):
#         if len(self.view.sel()) == 1:
#             return self.view.substr(self.view.sel()[0])
#         elif self.view.sel()[0].size() == 0:
#             return "i + 1"
#         elif try_eval(self.view.substr(self.view.sel()[0])) is not None:
#             return "x"
#         else:
#             return "s"

#     def preview(self, expr):
#         try:
#             v = self.view
#             s = v.sel()
#             count = len(s)
#             if count > 5:
#                 count = 5
#             results = [repr(eval_expr(v.substr(s[i]), i, expr)) for i in range(count)]
#             if count != len(s):
#                 results.append("...")
#             return ", ".join(results)
#         except Exception:
#             return ""

#     def validate(self, expr):
#         try:
#             v = self.view
#             s = v.sel()
#             for i in range(len(s)):
#                 eval_expr(v.substr(s[i]), i, expr)
#             return True
#         except Exception:
#             return False

# class PaletteRegisterCommand(subl_hacks.KeyBindTextCommand):
#     def run(self, edit, expr):
#         logger.debug("SUCCESS!")

#     def input(self, args):
#         return ExprInputHandler(self.view)
