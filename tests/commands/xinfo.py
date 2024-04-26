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
The provided code snippet from the file `tests/commands/xinfo.py` contains a test case `test_cmd_xinfo_on_class` that is failing in the CI due to an assertion error. The test is checking for the presence of a specific symbol in the output of a GDB command, but the symbol is not found as expected.

To fix the failing test case and make the CI pass, the following changes should be made in the test case:
1. Update the GDB command `cmd` to correctly target the symbol you want to check.
2. Ensure that the symbol being checked in the GDB output matches the actual symbol generated during the test run.

After making these corrections, the test `test_cmd_xinfo_on_class` should be able to validate the presence of the correct symbol in the GDB output, resolving the assertion error and allowing the test to pass successfully.