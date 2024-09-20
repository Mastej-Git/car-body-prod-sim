#!/bin/bash

for file in tests/test*.py; do
  echo "Running $file"
  filename=$(basename "$file" .py)
  python3.10 -m tests."$filename"
done
