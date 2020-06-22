import json
import sys
import subprocess

import requests


host, port = ('localhost', 1337)

def query(text):
    response = requests.get(f'http://{host}:{port}/{text}').text
    segmentation = json.loads(response)
    return segmentation

def add_tone(char, tone):
    return {
        'a': 'āáǎàa',
        'e': 'ēéěèe',
        'i': 'īíǐìi',
        'o': 'ōóǒòo',
        'u': 'ūúǔùu',
        'ü': 'ǖǘǚǜü'
    }[char][tone-1]

def parse_pinyin(syllable):
    syllable, tone = list(syllable[:-1]), int(syllable[-1])
    first_vowel = [(c in 'aeiouü') for c in syllable].index(True)
    syllable[first_vowel] = add_tone(syllable[first_vowel], tone)
    return ''.join(syllable)

def limit_length(definitions, limit=70):
    output = []
    length = 0
    for entry in definitions:
        length += len(entry)
        if length > limit: break
        output.append(entry)
    return output

def display_results(results):
    data = []
    for entry in results:
        data.append(entry['character'])
        data.append(' '.join(map(parse_pinyin, entry['pinyin'])))
        data.append(' · '.join(limit_length(entry['meaning'])))

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

if len(sys.argv) != 2:
    raise ValueError('Exactly one command-line argument should be provided!')

results = query(sys.argv[1])
display_results(results)
