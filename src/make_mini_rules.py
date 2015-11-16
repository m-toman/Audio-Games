#!/usr/bin/env python

# FTW Telecommunications Research Center Vienna (www.ftw.at)
# Dietmar Schabus (schabus@ftw.at)
# July 2014

# library imports
import argparse
import os
import os.path
import re
import sys

selfpath = os.path.realpath(os.path.dirname(__file__))
svnroot = os.path.realpath(selfpath + '/../../..')
defaultlex = os.path.realpath(svnroot +
    '/data/lexicon/at/sampa-austrian-at.checked.iso.out.hts')

# import lexicon class from pyblah incubator
sys.path.append(svnroot + '/src')
from pyblah.incub import lexicon

# ------------------------------------------------------------------------------
def make_mini_lex(lexfile, infile, outfile):
    wordlistfile = 'data/tts/lexicon/tmp_wordlist'
    resultlex = 'data/tts/lexicon/tmp_lex'
    make_word_list(infile, wordlistfile)

    lexicon.write_canonical_lexicon_for_text(wordlistfile, lexfile, resultlex,
        textencoding='utf-8', outlexencoding='utf-8')

    with open(outfile, 'w') as f:
        with open(resultlex) as rl:
            line = rl.read()
            line = replace_phones(line)
            f.write(line)
        with open('data/tts/lexicon/rules.bottompart') as bp:
            f.write(bp.read())
    
    os.remove(wordlistfile)
    os.remove(resultlex)

# ------------------------------------------------------------------------------
def make_word_list(infile, wordlistfile):
    blacklist = (
        '{}',
        'left', 'right', 'forward', 'back',
        'small', 'medium', 'large', 'huge'
    )
    wlist = []
    with open(infile) as f:
        for line in f:
            strs = re.findall(r"'[^']+'", line)
            for s in strs:
                s = s.strip("'")
                words = re.split(r'[ -]', s)
                for w in words:
                    w = w.rstrip(',.!?')
                    if w in blacklist:
                        continue
                    if w not in wlist:
                        wlist.append(w)
    
    wlist.sort()
    with open(wordlistfile, 'w') as f:
        for word in wlist:
            f.write(word + '\n')

# ------------------------------------------------------------------------------
def replace_phones(line):

    replacements = {
        'Ahn'  : 'O',
        'I6'   : 'I P6',
        'Ohn'  : 'O',
        'P3hn' : 'P9',
        'P3h'  : 'P9',
        'P96'  : 'P9 P6',
        'P9hn' : 'P9',
        'Y6'   : 'Y P6',
        'Z'    : 'S',
    }
    
    for k,v in replacements.items():
        line = line.replace(k, v)
    
    return line

# ------------------------------------------------------------------------------
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--lexicon', type=str, default=defaultlex)
    parser.add_argument('infile', type=str)
    parser.add_argument('outfile', type=str)
    args = parser.parse_args()
    
    make_mini_lex(args.lexicon, args.infile, args.outfile)
