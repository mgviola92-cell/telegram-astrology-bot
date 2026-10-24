"""Static safety checks for the native Telegram bot.

These inspect the repository without importing aiogram, Telegram secrets,
a live database, or remote astronomical packages.
"""
import ast
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]

def source_ast(path):
    return ast.parse((ROOT/path).read_text(encoding="utf-8"),filename=path)

class StaticIntegrityTests(unittest.TestCase):
    def test_evidence_registry_covers_all_literal_buttons(self):
        registry=source_ast("evidence_ui.py")
        ids=set()
        for node in ast.walk(registry):
            if isinstance(node,ast.Assign):
                if any(isinstance(target,ast.Name) and target.id=="RULES" for target in node.targets):
                    ids=set(ast.literal_eval(node.value))
        self.assertTrue(ids,"Evidence registry was not found")
        for path in ("bot.py", "evidence_ui.py"):
            tree=source_ast(path)
            for node in ast.walk(tree):
                if (isinstance(node,ast.Call) and isinstance(node.func,ast.Name)
                    and node.func.id=="evidence_button" and node.args
                    and isinstance(node.args[0],ast.Constant)
                    and isinstance(node.args[0].value,str)):
                    with self.subTest(path=path,rule=node.args[0].value):
                        self.assertIn(node.args[0].value,ids)
    def test_no_hardcoded_telegram_token(self):
        tree=source_ast("bot.py")
        for node in ast.walk(tree):
            if isinstance(node,ast.Call) and isinstance(node.func,ast.Name) and node.func.id=="Bot":
                tokens = list(node.args) + [kw.value for kw in node.keywords if kw.arg=="token"]
                self.assertTrue(tokens,"Bot constructor must receive a token from configuration")
                self.assertTrue(all(not isinstance(value,ast.Constant) for value in tokens),
                                "Do not embed a Telegram token as a literal")
    def test_private_birth_commands_guard_chat(self):
        tree=source_ast("profile_commands.py")
        for node in ast.walk(tree):
            if isinstance(node,ast.AsyncFunctionDef) and node.name in (
                "save_birth","forget_birth","show_birth"):
                code=ast.get_source_segment((ROOT/"profile_commands.py").read_text(encoding="utf-8"),node)
                with self.subTest(handler=node.name):
                    self.assertIn('message.chat.type!="private"',code)
                    self.assertIn("message.from_user is None",code)
    def test_no_network_ephemeris_fetch_in_natal_engine(self):
        source=(ROOT/"western_chart.py").read_text(encoding="utf-8")
        self.assertIn("load_file(",source)
        self.assertNotIn("load('de421.bsp')",source)
        self.assertNotIn('load("de421.bsp")',source)
    def test_python_parse_all_first_party_modules(self):
        for path in sorted(ROOT.glob("*.py")):
            with self.subTest(module=path.name):
                ast.parse(path.read_text(encoding="utf-8"),filename=str(path))

if __name__=="__main__":
    unittest.main()
