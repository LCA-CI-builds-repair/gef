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
        target = debug_target("class")
        res = gdb_run_silent_cmd(cmd, target=target, before=["b B<TraitA, TraitB>::Run()"])
        self.assertNoException(res)
        self.assertIn("Symbol: B<TraitA, TraitB>::Run()+4", res)
        self.assertNotIn("Error while writing index for `/tmp/class.out\': mkstemp: No such file or directory.", res)
        self.assertNotIn("GEF for linux ready, type `gef\' to start, `gef config\' to configure", res)
        self.assertNotIn("89 commands loaded and 5 functions added for GDB 12.1 in 0.00ms using Python engine 3.10", res)
        self.assertNotIn("Breakpoint 1 at 0x1328: file class.cpp, line 21.", res)
        self.assertNotIn("Starting program: /tmp/class.out", res)
        self.assertNotIn("Using host libthread_db library", res)
        self.assertNotIn("Breakpoint 1, B<TraitA, TraitB>::Run (this=0x55555556b2b0) at class.cpp:21", res)
