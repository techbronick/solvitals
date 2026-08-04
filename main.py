#!/usr/bin/env python3
"""Run SolVitals: python3 main.py [--watch] [--output-dir DIR]"""

import sys

from solvitals.cli import main

if __name__ == "__main__":
    sys.exit(main())
