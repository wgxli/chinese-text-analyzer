# Chinese Text Analyzer (中文文本分析器)
A basic utility that displays an analysis (word segmentation, pinyin, meaning) of any selected Chinese text.

Optional feature: Quickly add detected words to Anki. See the `Anki integration` section below for details.

![Screenshot of the program](screenshot.png)

Note: This is a toy project. I've only tested it on my computer (Ubuntu 20.04). Send any bugs to `bug.report@samuelj.li`.

## Requirements
This project requires `zenity` and `xclip` to interface with GTK,
as well as the following packages on Python 3.6 or higher:
- requests
- g2pc

## Usage
- Start `daemon.py`. You might have to edit `config.py` if the default port is taken.
- Run `python3 client.py "your Chinese text here"`. This will open the analysis results in a popup window.
- Running `shortcut.sh` will analyze whatever text is currently selected.

## Anki integration
You can enable or disable Anki integration in `config.py`.

If enabled, the output window will add any selected words to a file called `anki.csv`.
This file can be added to Anki via `File → Import`. 
You should delete the file immediately after importing to avoid duplicates later.

## Tips
This is my current setup:
- Have the daemon (`daemon.py`) run on startup.
- Bind `shortcut.sh` to a keyboard shortcut.

This makes looking up words extremely quick. (Just select the text, and press a few keys.)
