"""
Pytest configuration — sets up paths so tests can import tools directly.
The pythonpath = ["tools"] in pyproject.toml handles this for pytest >= 7,
but this conftest keeps things working for direct invocation too.
"""
import sys
from pathlib import Path

# Allow imports from tools/ and tools/lib/ in all tests
_TOOLS_DIR = Path(__file__).parent.parent / "tools"
if str(_TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(_TOOLS_DIR))
