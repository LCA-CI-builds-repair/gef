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


def test\_cmd\_xinfo\_on\_class(self):
# Make sure that the `class.out` file is generated correctly
# ...

# Use `gdb.parse_and_eval` to evaluate the expression `'info symbol $pc+4'` directly in GDB
cmd = "xinfo"
target = debug\_target("class")
gdb.execute("file class.out")
gdb.execute("b B<TraitA, TraitB>::Run()")
gdb.execute("run")
gdb.execute("xinfo $pc+4")
res = gdb.selected\_inferior.stdout\_wait()

# Extract the necessary information from the `res` string
\_\_, _, address, name, _ = gdb.string\_of\_got\_sal\_symbol\_from\_xinfo(res)
self.assertEqual(name, "B<TraitA, TraitB>::Run()+4")
