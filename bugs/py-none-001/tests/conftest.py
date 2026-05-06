import sys
from pathlib import Path

sys.modules.pop("buggy", None)
sys.path.insert(0, str(Path(__file__).parent.parent))
