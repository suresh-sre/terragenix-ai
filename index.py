#!/usr/bin/env python3
"""Deployment entrypoint for platforms that expect a root-level Flask app."""

from pathlib import Path
import sys


BACKEND_DIR = Path(__file__).resolve().parent / "backend"
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from backend.index import app

