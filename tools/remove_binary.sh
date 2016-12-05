#!/bin/bash

# Remove binary files
find . -iname '*.py[cod]' -delete

# Remove __pycache__ Py3k
rm --recursive --force --verbose pybooru/__pycache__
