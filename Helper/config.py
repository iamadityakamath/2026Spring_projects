from pathlib import Path

# Resolved at import time — points to the Data/ folder regardless of who runs it
BASE = str(Path(__file__).resolve().parent.parent / "Data")
