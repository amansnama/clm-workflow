import pytest
import os
import tempfile
import subprocess
from pathlib import Path
import shutil

# Path to clm-workflow/clm_scripts directed back from the test dir
CLMSCRIPTSDIR = Path(__file__).parent.parent

HOSTNAME = subprocess.run(["hostname"], capture_output=True, text=True).stdout.strip()


@pytest.fixture(scope="module")
def setup_env():
    if "derecho" in HOSTNAME:
        ctsmdir = r"/glade/u/home/amans/ctsm5.2.mksurfdat"  # For test in derecho
    else:
        # In other machines, create temp ctsmdir
        ctsmdir = tempfile.mkdtemp() # Could specify path to ctsm
        # Create mock create_newcase
        # (ctsmdir / "create_newcase").write_text("#!/bin/bash\necho 'Mock newcase executed!'\nexit 0\n")
    casedir = tempfile.mkdtemp()
    os.makedirs(Path(ctsmdir) / "cime" / "scripts", exist_ok=True)

    return {
        "ctsmdir": ctsmdir,
        "casedir": casedir,
        "casename": "TestCase",
        "res": "f19_g16",
        # available compsets depend on ctsm version
        "compset": "I2000Clm51Bgc",
        "project": "UMSU0016",
    }


def test_check_scripts_exist():
    """Test to check if scripts exist."""
    assert os.path.isfile(CLMSCRIPTSDIR / "CreateCase.sh")


def test_missing_arguments(setup_env):
    """Test that the script fails with missing arguments."""
    # print("Aman", os.getcwd(), CLMSCRIPTSDIR)
    result = subprocess.run(
        [
            CLMSCRIPTSDIR / "CreateCase.sh",
            setup_env["casename"],
            setup_env["ctsmdir"],
            setup_env["casedir"],
            setup_env["res"],
        ],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 1  # Exit code 1
    assert "Usage:" in result.stdout


def test_successful_execution_with_project(setup_env):
    """Test the script execution with all required arguments and project."""
    result = subprocess.run(
        [
            CLMSCRIPTSDIR / "CreateCase.sh",
            setup_env["casename"],
            setup_env["ctsmdir"],
            setup_env["casedir"],
            setup_env["res"],
            setup_env["compset"],
            setup_env["project"],
        ],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0


def test_default_project(setup_env):
    """Test the script with the default project when none is specified."""
    result = subprocess.run(
        [
            CLMSCRIPTSDIR / "CreateCase.sh",
            setup_env["casename"],
            setup_env["ctsmdir"],
            setup_env["casedir"],
            setup_env["res"],
            setup_env["compset"],
        ],
        capture_output=True,
        text=True,
    )
    assert (
        "PROJECT not provided. Running create_newcase without --project."
        in result.stdout
    )
    if "derecho" in HOSTNAME:
        # In derecho, PROJECT is always needed.
        # ./create_case fails with returncode 1
        assert result.returncode == 1
    else:
        # In other machine not requiring PROJECT.
        assert result.returncode == 0


@pytest.fixture(scope="module", autouse=True)
def cleanup(setup_env):
    """Cleanup temporary directories after tests."""
    yield  # Run tests
    # Cleanup
    # shutil.rmtree(setup_env["ctsmdir"])
    shutil.rmtree(setup_env["casedir"])
