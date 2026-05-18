#!/usr/bin/env python3
# Canonical implementation is patch_compatibility_checker.py
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from patch_compatibility_checker import main

if __name__ == "__main__":
    main()
