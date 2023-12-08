import re
import json

from requests import get

from letterboxed import Letterbox
from argparse import ArgumentParser

from typing import Tuple, Dict, List, Optional

def main():
    """The command line executable.

    See README for usage information.
    """
    values: Dict[str, Tuple[str, str, str]] = {}
    sides: List[str] = ['top', 'left', 'right', 'bottom']
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
        groups: List[str] = config.letters.split('-')
        for side in sides:
            try:
                group: str = groups.pop()
            except IndexError:
                print("Invalid format for letters.  Must have four segments separated by '-'.")
                exit(1)

            try:
                assert len(group) == 3
            except AssertionError:
                print("Groups of letters must be in threes.")
                exit(1)

            values[side] = tuple(list((x for x in group)))  # type: ignore

        if config.dictionary_file:
            with open(config.dictionary_file, "r") as fp:
                dict = fp.read().split("\n")
        else:
            raise RuntimeError("Must provide local dictionary if passing custom box letters.")

    if config.nyt:
        resp = get("https://www.nytimes.com/puzzles/letter-boxed")
        nyt_groups: Optional[re.Match[str]] = re.search(
            r'\"sides\":\[\"([A-Z]{3})\",\"([A-Z]{3})\",\"([A-Z]{3})\",\"([A-Z]{3})\"\]',
            resp.text)
        for z in zip(sides, nyt_groups.groups()):
            values[z[0]] = tuple(list((x for x in z[1])))  # type: ignore

        nyt_dictionary = re.search(r'\"dictionary\":\[([\"A-Z,]+)', resp.text)
        dict_str = f'[{nyt_dictionary.group(1)}]'
        dict = json.loads(dict_str)

        todays_puzzle: List[str] = []
        for k,v in values.items():
            todays_puzzle.append("".join(v))

        print(f'\nToday\'s puzzle is {"-".join(todays_puzzle)}\n')


    letterbox = Letterbox(
        (
            values['top'],
            values['left'],
            values['right'],
            values['bottom']),
        dict)

    answers = letterbox.solve()
    for pair in answers:
        print(" -> ".join(pair))
    print()

if __name__ == '__main__':
        main()
