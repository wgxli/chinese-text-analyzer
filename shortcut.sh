#! /bin/bash

# cd to base directory
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd $DIR

# Run client script on current text selection
SELECTED=$(xclip -out -selection primary | tr "\n" " ")
python3 client.py $SELECTED
