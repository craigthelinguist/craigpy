#!/bin/sh
rm *.py
rm *.pyc
rm -rf __pycache__
cp craigpy/src/*.py .
echo done
