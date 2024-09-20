#!/bin/bash

find . -type f -name "*.py" | while read -r file; do
    echo "Running pylint on $file"
    pylint "$file"
done