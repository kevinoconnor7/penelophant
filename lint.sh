#!/bin/bash

dir=$(dirname $0)

# pylint
output=$(pylint --rcfile=$dir/.pylintrc --disable=I0011 penelophant 2> /dev/null)
if [ -n "$output" ]; then
    echo "--pylint--"
    echo -e "$output"
fi

exit 0
