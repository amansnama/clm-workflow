import pytest
import os
import tempfile
import subprocess
from pathlib import Path
import shutil

# Path to clm-workflow/clm_scripts directed back from the test dir
CLMSCRIPTSDIR = Path(__file__).parent.parent