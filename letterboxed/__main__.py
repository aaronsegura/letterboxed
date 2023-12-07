from letterboxed import Letterbox
from argparse import ArgumentParser

from typing import Tuple, Dict, List

def main():
    """The command line executable.

    Example:
        $ letterboxed -d /usr/share/dict/american-english a,e,g p,o,t h,i,l c,m,v

    The order of the sides given doesn't matter.
    """
    values: Dict[str, Tuple[str, str, str]] = {}
    sides: List[str] = ['top', 'left', 'right', 'bottom']
    dict: List[str] = []

    parser = ArgumentParser(description='NYT Letterboxed Two-Solver')
    parser.add_argument(
        '-d',
        dest='dictionary_file',
        metavar='<file>',
        help="Dictionary File", required=True)

    for side in sides:
        parser.add_argument(
            dest=side,
            type=str,
            help=f'Comma-separated letters from {side} side.')

    config = parser.parse_args()

    for side in sides:
        values[side] = vars(config)[side].split(",")

    with open(config.dictionary_file, "r") as fp:
        dict = fp.read().split("\n")

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

if __name__ == '__main__':
    main()
