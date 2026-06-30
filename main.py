import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent / "src"))

from scanner import run_scan


if __name__ == "__main__":
    run_scan()