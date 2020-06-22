#! /bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd $DIR
echo "test" > debug.txt
xclip -out -selection primary | xclip -in -selection clipboard
SELECTED=$(xsel --clipboard | tr "\n" " ")
python3 client.py $SELECTED
