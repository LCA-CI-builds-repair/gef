import os
import pathlib
import random
import re
import subprocess
import tempfile
import time
from typing import Tuple
import unittest

import rpyc

from .utils import debug_target

COVERAGE_DIR = os.getenv("COVERAGE_DIR", "")
GEF_PATH = pathlib.Path(os.getenv("GEF_PATH", "gef.py")).absolute()
RPYC_GEF_PATH = GEF_PATH.parent / "scripts/remote_debug.py"
RPYC_HOST = "localhost"
RPYC_PORT = 18812
RPYC_SPAWN_TIME = 1.0
GDB_INIT_TIME = 0.5  # Additional time to wait for GDB initialization
RPYC_MAX_REMOTE_CONNECTION_ATTEMPTS = 5


class RemoteGefUnitTestGeneric(unittest.TestCase):
    """
    The base class for GEF test cases. This will create the `rpyc` environment to programmatically interact with
    GDB and GEF in the test.
    """

    def setUp(self) -> None:
        attempt = RPYC_MAX_REMOTE_CONNECTION_ATTEMPTS
        while True:
            try:
                #
                # Port collisions can happen, allow a few retries
                #
                self._coverage_file = None
                self.__setup()
                break
            except ConnectionRefusedError:
                attempt -= 1
                if attempt == 0:
                    raise
                time.sleep(0.2)
                continue

        self._gdb = self._conn.root.gdb
        self._gef = self._conn.root.gef
        return super().setUp()

    def __setup(self):
        if not hasattr(self, "_target"):
            setattr(self, "_target", debug_target("default"))
        else:
            assert isinstance(self._target, pathlib.Path)  # type: ignore pylint: disable=E1101
            assert self._target.exists()  # type: ignore pylint: disable=E1101

        #
        # Select a random tcp port for rpyc
        #
        self._port = random.randint(1025, 65535)
        self._commands = ""

        if COVERAGE_DIR:
            self._coverage_file = pathlib.Path(COVERAGE_DIR) / os.getenv(
                "PYTEST_XDIST_WORKER", "gw0"
            )
            self._commands += f"""
pi import coverage
pi cov = coverage.Coverage(data_file="{self._coverage_file}", auto_data=True, branch=True)
pi cov.start()
"""

        self._commands += f"""
source {GEF_PATH}
gef config gef.debug True
gef config gef.propagate_debug_exception True
gef config gef.disable_color True
source {RPYC_GEF_PATH}
pi start_rpyc_service({self._port})
start
"""

        self._verify_commands = """
pi import time
pi time.sleep(0.1)
info proc mappings
pi import os
pi assert os.path.exists("/proc/self/maps"), "Process maps not accessible"
"""

        self._initfile = tempfile.NamedTemporaryFile(mode="w", delete=False)
        self._initfile.write(self._commands)
        self._initfile.flush()
        self._command = [
            "gdb",
            "-q",
            "-nx",
            "-ex",
            f"source {self._initfile.name}",
            "--",
            str(self._target.absolute()),  # type: ignore pylint: disable=E1101
        ]
        self._process = subprocess.Popen(self._command)
        assert self._process.pid > 0
        time.sleep(RPYC_SPAWN_TIME)
        self._conn = rpyc.connect(
            RPYC_HOST,
            self._port,
        )
        
        # Allow time for GDB to fully initialize and verify process state
        time.sleep(GDB_INIT_TIME)
        try:
            self._gdb.execute(self._verify_commands)
        except Exception as e:
            raise RuntimeError("Failed to verify GDB initialization") from e

    def tearDown(self) -> None:
        if COVERAGE_DIR:
            self._gdb.execute("pi cov.stop()")
            self._gdb.execute("pi cov.save()")
        self._conn.close()
        self._process.terminate()
        return super().tearDown()

    @property
    def gdb_version(self) -> Tuple[int, int]:
        res = [int(d) for d in re.search(r"(\d+)\D(\d+)", self._gdb.VERSION).groups()] 
        assert len(res) >= 2
        return res
