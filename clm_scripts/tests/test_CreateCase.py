import pytest
import os
import tempfile
import subprocess
from pathlib import Path

@pytest.fixture(scope='module')
def setup_env():
    ctsmdir = tempfile.mkdtemp()
    casedir = tempfile.mkdtemp()
    os.makedirs(Path(ctsmdir)/'cime'/'scripts', exist_ok=True)

    return {
        "ctsmdir": ctsmdir,
        "casedir": casedir,
        "casename": "TestCase",
        "res": "f19_f19_mg16",
        "compset": "I2000Clm50Bgc",
        "project": "test_project"
    }

def test_missing_arguments(setup_env):
    """Test that the script fails with missing arguments."""
    result = subprocess.run(
        ["../CreateCase.sh", setup_env["casename"], setup_env["ctsmdir"], setup_env["casedir"], setup_env["res"]],
        capture_output=True, text=True
    )
    assert result.returncode == 1 # Exit code 1
    assert "Usage:" in result.stdout

def test_successful_execution_with_project(setup_env):
    """Test the script execution with all required arguments and project."""
    result = subprocess.run(
        ["../CreateCase.sh", setup_env["casename"], setup_env["ctsmdir"], setup_env["casedir"], setup_env["res"], setup_env["compset"], setup_env["project"]],
        capture_output=True, text=True
    )
    assert result.returncode == 0

def test_default_project(setup_env):
    """Test the script with the default project when none is specified."""
    result = subprocess.run(
        ["../CreateCase.sh", setup_env["casename"], setup_env["ctsmdir"], setup_env["casedir"], setup_env["res"], setup_env["compset"]],
        capture_output=True, text=True
    )
    assert "PROJECT not provided. Running create_newcase without --project." in result.stdout

@pytest.fixture(scope="module", autouse=True)
def cleanup(setup_env):
    """Cleanup temporary directories after tests."""
    yield  # Run tests
    # Cleanup
    os.rmdir(setup_env["ctsmdir"])
    os.rmdir(setup_env["casedir"])