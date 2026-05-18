#!/usr/bin/env python3
# Canonical implementation is provider_output_validator.py
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from provider_output_validator import main

if __name__ == "__main__":
    main()
