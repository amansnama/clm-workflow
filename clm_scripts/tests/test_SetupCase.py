import pytest
import os
import tempfile
import subprocess
from pathlib import Path
import shutil

# Path to clm-workflow/clm_scripts directed back from the test dir
CLMSCRIPTSDIR = Path(__file__).parent.parent

HOSTNAME = subprocess.run(["hostname"], capture_output=True, text=True).stdout.strip()

# Path to Testcase dir
TESTCASEDIR = Path("/glade/derecho/scratch/amans/Test")


@pytest.fixture
def setup_caseroot(tmp_path):
    caseroot = tmp_path / "caseroot"
    caseroot.mkdir()

    # Create mock case.setup and case.build scripts
    (caseroot / "case.setup").write_text(
        "#!/bin/bash\necho 'Mock setup executed!'\nexit 0\n"
    )
    (caseroot / "case.build").write_text(
        "#!/bin/bash\necho 'Mock build executed!'\nexit 0\n"
    )

    # Make the mock scripts executable
    os.chmod(caseroot / "case.setup", 0o755)
    os.chmod(caseroot / "case.build", 0o755)

    return caseroot


def run_script(args, env=None):
    """
    Helper function to run the script and return the result.
    """
    result = subprocess.run(
        [
            CLMSCRIPTSDIR / "Setup_Build_Case.sh",
        ]
        + args,
        capture_output=True,
        text=True,
        env=env,
    )
    return result


def test_no_arguments():
    """
    Test that the script fails with no arguments.
    """
    result = run_script([])
    assert result.returncode == 1
    assert "Usage:" in result.stderr or result.stdout


def test_invalid_flag(setup_caseroot):
    """
    Test that the script fails with an invalid flag.
    """
    result = run_script([str(setup_caseroot), "--wrong"])
    assert result.returncode == 2
    assert "Unexpected flag" in result.stderr or result.stdout


def test_setup_only(setup_caseroot):
    """
    Test the script with --setup flag only.
    """
    result = run_script([str(setup_caseroot), "--setup"])
    assert result.returncode == 0
    assert "Mock setup executed!" in result.stdout
    assert "Case setup successfull!" in result.stdout


def test_build_only(setup_caseroot):
    """
    Test the script with --build flag only.
    """
    if 'derecho' in HOSTNAME:
        result = run_script(
            [TESTCASEDIR, "--build"],
            env={"PRJ": "TestProject"},
        )
        assert "Building in derecho" in result.stdout
    else:
        result = run_script(
            [str(setup_caseroot), "--build"],
            env={"PRJ": "TestProject"},
        )
        assert "Mock build executed!" in result.stdout
        assert result.returncode == 0
        assert "Case build successfull!" in result.stdout


def test_setup_and_build(setup_caseroot):
    """
    Test the script with both --setup and --build flags.
    """
    if 'derecho' in HOSTNAME:
        result = run_script(
            [TESTCASEDIR, "--setup", "--build"],
            env={"PRJ": "TestProject"},
        )
        print(result.stdout)
        assert "Building in derecho" in result.stdout
    else:
        result = run_script(
            [str(setup_caseroot), "--setup", "--build"],
            env={"PRJ": "TestProject"},
        )
        assert "Mock setup executed!" in result.stdout
        assert "Mock build executed!" in result.stdout  
        assert result.returncode == 0
        assert "Case build successfull!" in result.stdout

    assert "Case setup successfull!" in result.stdout