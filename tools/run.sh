#!/bin/sh
exec ~/projects/LUT/.venv/bin/python "$(dirname "$0")/build.py" "$@"
