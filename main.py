#!/usr/bin/env python3
"""Legacy entrypoint for backward compatibility. Directs to herdr_compose CLI."""

import sys
from herdr_compose.cli import main

if __name__ == "__main__":
    main(sys.argv[1:])
