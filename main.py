#!/usr/bin/env python3
"""Run SolPulse: python3 main.py [--watch] [--output-dir DIR]"""

import sys

from solpulse.cli import main

if __name__ == "__main__":
    sys.exit(main())
