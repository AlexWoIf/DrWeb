#!/bin/bash

DIRECTORY=tests/func_tests

for testcase in "$DIRECTORY"/*.txt; do
    filename=$(basename "${testcase%.txt}")
    echo Start testcase "$filename"
    res_file="$DIRECTORY/$filename.res"
    cat "$testcase" | python src/database.py > "$DIRECTORY/test.out"
    diff_output=$(diff "$DIRECTORY/test.out" "$res_file")

    if [ -z "$diff_output" ]; then
        echo Test SUCCESS
    else
        echo Test FAIL
    fi
    
    rm "$DIRECTORY/test.out"
done