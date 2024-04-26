"""
`skipi` command test module
"""

import pytest

from tests.utils import (ARCH, GefUnitTestGeneric, debug_target, findlines,
                         gdb_run_cmd, gdb_run_silent_cmd, gdb_start_silent_cmd)


class SkipiCommand(GefUnitTestGeneric):
    """`skipi` command test module"""


    cmd = "skipi"


    def test_cmd_nop_inactive(self):
        res = gdb_run_cmd(f"{self.cmd}")
        self.assertFailIfInactiveSession(res)


    @pytest.mark.skipif(ARCH not in ("i686", "x86_64"), reason=f"Skipped for {ARCH}")
The provided code snippet from the file `tests/commands/skipi.py` includes a test case `test_cmd_skipi_no_arg` that is failing in the CI due to an assertion error. The test case is checking for specific patterns in the output of GDB commands related to skipping instructions, but the expected pattern is not found as indicated in the logs.

To address the failing test case and make the CI pass, the following changes should be made in the test case:
1. Ensure that the GDB command executed in `gdb_start_silent_cmd` is correctly setting up the environment for the test, specifically related to writing memory and reading bytes.
2. Update the assertion to check for the expected pattern "\x90\x90" accurately in the GDB output after the memory write operation.

By modifying the test case with the correct setup and assertions, the test should be able to validate the skipping of instructions effectively and pass in the CI.
    @pytest.mark.skipif(ARCH not in ("i686", "x86_64"), reason=f"Skipped for {ARCH}")
    def test_cmd_skipi_skip_two_instructions(self):

        res = gdb_start_silent_cmd(
            "pi gef.memory.write(gef.arch.pc, p64(0x90909090feebfeeb))", # 2 short jumps to pc + 4 nops
            after=(
                f"{self.cmd} --n 2",
                "pi print(gef.memory.read(gef.arch.pc, 4))", # read 4 bytes
            )
        )
        self.assertNoException(res)
        self.assertIn(r"\x90\x90\x90\x90", res) # 4 nops


    @pytest.mark.skipif(ARCH not in ("i686", "x86_64"), reason=f"Skipped for {ARCH}")
    def test_cmd_skipi_two_instructions_from_location(self):

        res = gdb_start_silent_cmd(
            "pi gef.memory.write(gef.arch.pc, p64(0x9090feebfeebfeeb))", # 2 short jumps to pc + 2 nops
            after=(
                f"{self.cmd} $pc+2 --n 2", # from the second short jump
                "pi print(gef.memory.read(gef.arch.pc, 2))", # read 2 bytes
            )
        )
        self.assertNoException(res)
        self.assertIn(r"\x90\x90", res) # 2 nops
