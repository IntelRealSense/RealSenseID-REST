# flake8: noqa: F401

import pathlib
import sys

from rsid_rest._version import __version__, __version_info__

sys.path.append(str(pathlib.Path(__file__).resolve().parents[1] / "app"))
