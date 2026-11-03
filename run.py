#!/usr/bin/env python3
"""Spec Ghost entry point — Kiroween 2026, fresh build, stdlib only.

Usage:
  python3 run.py                 # serve the web UI on http://127.0.0.1:8768/
  python3 run.py scan            # scan the bundled demo house (sample/)
  python3 run.py scan .          # scan this repo itself
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.specghost import scan


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "scan":
        target = sys.argv[2] if len(sys.argv) > 2 else "sample"
        base = os.path.dirname(os.path.abspath(__file__))
        path = base if target == "." else os.path.join(base, target)
        print(json.dumps(scan(path), indent=2))
        return
    from app.server import main as serve
    serve()


if __name__ == "__main__":
    main()
