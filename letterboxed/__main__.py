import re
import json

from requests import get

from letterboxed import Letterbox
from argparse import ArgumentParser

from typing import Tuple, Dict, List, Optional

_URL = 'https://www.nytimes.com/puzzles/letter-boxed'

def main():
    """The command line executable.

    See README for usage information.
    """
    letters: List[str] = []
    dict: List[str] = []

    parser = ArgumentParser(description='NYT Letterboxed Solver')

    source_select = parser.add_mutually_exclusive_group(required=True)

    source_select.add_argument(
        '-n',
        help='Pull today\'s puzzle from the NYTimes website.',
        dest='nyt',
        action='store_true')

    source_select.add_argument(
        '-l',
        dest='letters',
        type=str,
        help='Specify the letters you want on the box.',
        metavar='top-rgt-lft-btm')

    parser.add_argument(
        '-d',
        dest='dictionary_file',
        metavar='<file>',
        help="Dictionary File",
        required=False)

    config = parser.parse_args()

    if config.letters:
        letters: List[str] = config.letters.split('-')
        if len(letters) != 4:
            raise RuntimeError(
                "Invalid format for letters.  Must be four groups separated by '-'.")

        side_lengths = set([len(_) for _ in letters])
        if len(side_lengths) != 1:
            raise RuntimeError("Sides must all have same number of letters.")

        if config.dictionary_file:
            with open(config.dictionary_file, "r") as fp:
                dict = fp.read().split("\n")
        else:
            raise RuntimeError("Must provide local dictionary if passing custom box letters.")

    if config.nyt:
        resp = get(_URL)
        nyt_groups: Optional[re.Match[str]] = re.search(
            r'\"sides\":\[\"([A-Z]{3})\",\"([A-Z]{3})\",\"([A-Z]{3})\",\"([A-Z]{3})\"\]',
            resp.text)

        if not nyt_groups:
            raise RuntimeError(f'Unable to find puzzle at {_URL}')

        letters = list(nyt_groups.groups())

        nyt_dictionary = re.search(r'\"dictionary\":\[([\"A-Z,]+)', resp.text)
        dict_str = f'[{nyt_dictionary.group(1)}]'
        dict = json.loads(dict_str)

        print(f'\nToday\'s puzzle is {"-".join(letters)}\n')

    letterbox = Letterbox((letters[0], letters[1], letters[2], letters[3]), dict)

    answers = letterbox.solve()
    for pair in answers:
        print(" -> ".join(pair))
    print()

if __name__ == '__main__':
        main()
