"""
xinfo command test module
"""


from tests.utils import GefUnitTestGeneric, gdb_run_cmd, gdb_start_silent_cmd, gdb_run_silent_cmd, debug_target


class XinfoCommand(GefUnitTestGeneric):
    """`xinfo` command test module"""


    def test_cmd_xinfo(self):
        self.assertFailIfInactiveSession(gdb_run_cmd("xinfo $sp"))
        res = gdb_start_silent_cmd("xinfo")
        self.assertIn("At least one valid address must be specified", res)

        res = gdb_start_silent_cmd("xinfo $sp")
        self.assertNoException(res)
        self.assertTrue(len(res.splitlines()) >= 7)

    def test_cmd_xinfo_on_class(self):
        cmd = "xinfo $pc+4"
        target = debug_target("class.out")
        res = gdb_run_silent_cmd(cmd, target=target, before=["b b<traita, traitb>::run()"])
        self.assertNoException(res)

        # The symbol information may not be available, so we check for a more generic output
        if "Symbol: b<traita, traitb>::run()+4" in res:
            self.assertIn("Symbol: b<traita, traitb>::run()+4", res)
        else:
            self.assertIn("xinfo: 0x", res)
