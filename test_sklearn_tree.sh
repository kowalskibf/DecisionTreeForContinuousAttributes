#!/bin/bash

# Authors:
# Bartosz Kowalski 318382
# Dominika Wyszyńska 318409

PYTHON_SCRIPT="test_sklearn_tree.py"
declare -A FILES_DICT=(
    ["iris.csv"]=","
    ["wine.csv"]=";"
    ["glass3.csv"]=";"
    ["student_success.csv"]=";"
)

ID=0

for FILE_NAME in "${!FILES_DICT[@]}"; do
    SEPARATOR="${FILES_DICT[$FILE_NAME]}"
    for ((i=1; i<=25; i++)); do
        ((ID++))
        echo "Processing file: $FILE_NAME, run $i" 
        python3 "$PYTHON_SCRIPT" "$FILE_NAME" "$SEPARATOR" "$ID"
    done
done
