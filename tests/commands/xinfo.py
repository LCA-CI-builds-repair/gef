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
    self.assertin("Symbol: B<TraitA, TraitB>::Run()+4", res)
    self.assertin("reading symbols from /tmp/class.out...\nerror while writing index for `/tmp/class.out\": mkstemp: no such file or directory.\ngef for linux ready, type `gef\' to start, `gef config\' to configure\n89 commands loaded and 5 functions added for gdb 12.1 in 0.00ms using python engine 3.10\nbreakpoint 1 at 0x1328: file class.cpp, line 21.\nstarting program: /tmp/class.out \n[thread debugging using libthread_db enabled]\nusing host libthread_db library "/lib/x86_64-linux-gnu/libthread_db.so.1".\n\nbreakpoint 1, B<TraitA, TraitB>::Run (this=0x55555556b2b0) at class.cpp:21\n21\t    virtual void run() { printf(\"i am b\\n"); }\n────────────────────────────────────────────────────────────────────────────────────────────────────\n────────────────────────────────────── xinfo: 0x55555555532c ──────────────────────────────────────\npage: 0x0000555555555000  →  0x0000555555556000 (size=0x1000)\npermissions: r-x\npathname: /tmp/class.out\noffset (from page): 0x32c\ninode: 37098\nsegment: .text (0x00005555555550a0-0x000055555555533a)\noffset (from segment): 0x28c\nsymbol: B<TraitA, TraitB>::Run()+20'
        self.assertTrue(len(res.splitlines()) >= 7)

    def test_cmd_xinfo_on_class(self):
        cmd = "xinfo $pc+4"
        target = debug_target("class")
        res = gdb_run_silent_cmd(cmd, target=target, before=["b B<TraitA, TraitB>::Run()"])
        self.assertNoException(res)
        self.assertIn("Symbol: B<TraitA, TraitB>::Run()+4", res)
