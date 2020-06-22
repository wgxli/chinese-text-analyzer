#! /bin/python3
# client.py - Analyzes the given Chinese text and displays results graphically.
# Usage: python3 client.py 中文文体

import json
import sys
import subprocess

import requests

from config import host, port, anki_integration


# You may need to adjust the settings below
# to get a good window size for your GTK setup
base_height = 120 # Height of the popup window without any entries
row_height = 30 # Height of each entry row


def display_error(title, text):
    """Displays the given error message in a GTK window. Requires `zenity`."""
    subprocess.run([
        'zenity', '--error',
        '--width', '300',
        '--title', title, 
        '--text', text
    ])


def query(text):
    """Queries the daemon for a text analysis."""
    try:
        response = requests.get(f'http://{host}:{port}/{text}').text
    except requests.exceptions.ConnectionError:
        display_error('Daemon not Reachable', 'Please ensure that daemon.py is running.')
        sys.exit()
    segmentation = json.loads(response)
    return segmentation


def add_tone(vowel, tone):
    """
    Adds the given (numerical) tone to a vowel.
    >>> add_tone('a', 3)
    'ǎ'
    """
    return {
        'a': 'āáǎàa',
        'e': 'ēéěèe',
        'i': 'īíǐìi',
        'o': 'ōóǒòo',
        'u': 'ūúǔùu',
        'ü': 'ǖǘǚǜü'
    }[vowel][tone-1]


def parse_pinyin(syllable):
    """
    Converts numerical pinyin to accented pinyin.
    >>> parse_pinyin('yan2')
    'yán'
    """
    syllable, tone = list(syllable[:-1]), int(syllable[-1])
    first_vowel = [(c in 'aeiouü') for c in syllable].index(True)
    syllable[first_vowel] = add_tone(syllable[first_vowel], tone)
    return ''.join(syllable)


def limit_length(definitions, limit=70):
    """
    Returns an initial sublist (prefix) of `definitions` as long as possible
    without exceeding `limit` characters total.
    """
    output = []
    length = 0
    for entry in definitions:
        length += len(entry)
        if length > limit: break
        output.append(entry)
    return output


def display_results(results):
    """
    Displays the given parse results in a graphical window.
    Assumes that `zenity` is installed.
    """
    try:
        # Process raw segmentation from the daemon
        data = [(
            entry['character'],
            ' '.join(map(parse_pinyin, entry['pinyin'])),
            ' · '.join(limit_length(entry['meaning']))
        ) for entry in results]
    except ValueError:
        display_error('Parsing Failed', 'Please make sure that your input contains only simplified Chinese characters.')
        sys.exit()

    # Flatten data for zenity
    window_data = []
    for entry in data:
        if anki_integration: window_data.append('')
        window_data.extend(entry)
        

    # Open zenity window and get selections (if Anki integration active)
    window_output = subprocess.run([
        'zenity',
        '--list',
        '--title', 'Chinese Analysis',
        '--width', '650',
        '--height', str(base_height + row_height * len(results)),
        *([
            '--checklist',
            '--text', 'Select any words to add them to Anki.',
            '--column', 'Anki'
        ] if anki_integration else
        [
            '--text', 'Breakdown of the selected text:',
        ]),
        '--column', 'Word',
        '--column', 'Pinyin',
        '--column', 'Meaning',
        *window_data
    ], capture_output=True).stdout.decode()

    # Add selected word to Anki csv
    selected_words = [x for x in window_output.strip().split('|') if x]
    if anki_integration and selected_words:
        print('Adding', ', '.join(selected_words), 'to Anki')
        with open('anki.csv', 'a') as f:
            for word in selected_words:
                entry = next(x for x in data if x[0] == word)
                print(*entry, sep=',', file=f)


# We want exactly one argument, the Chinese text to analyze
if len(sys.argv) != 2:
    raise ValueError('Exactly one command-line argument should be provided!')

results = query(sys.argv[1])
display_results(results)
