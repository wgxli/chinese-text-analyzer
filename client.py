#! /bin/python3
# client.py - Analyzes the given Chinese text and displays results graphically.
# Usage: python3 client.py 中文文体

import json
import sys
import subprocess

import requests


# Address of the daemon
host, port = ('localhost', 1337)

def query(text):
    """Queries the daemon for a text analysis."""
    response = requests.get(f'http://{host}:{port}/{text}').text
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
    data = []
    for entry in results:
        data.append(entry['character'])
        data.append(' '.join(map(parse_pinyin, entry['pinyin'])))
        data.append(' · '.join(limit_length(entry['meaning'])))

    # You may have to alter the height computation below depending on your GTK setup
    subprocess.run([
        'zenity',
        '--list',
        '--title', 'Chinese Analysis',
        '--width', '650',
        '--height', str(120 + 29 * len(results)),
        '--text', 'Breakdown of the selected text:',
        '--column', 'Word',
        '--column', 'Pinyin',
        '--column', 'Meaning',
        *data
    ])

# We want exactly one argument, the Chinese text to analyze
if len(sys.argv) != 2:
    raise ValueError('Exactly one command-line argument should be provided!')

results = query(sys.argv[1])
display_results(results)
