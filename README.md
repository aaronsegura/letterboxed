# Letterboxed Solver

Python module to solve the [daily word puzzle](https://www.nytimes.com/puzzles/letter-boxed) from the New York Times.

### Installation

    python -mpip install letterboxed

### Usage

You will need a local dictionary file in order to use this module if you want to specify custom puzzles with '-l'.

    $ letterboxed -h
    usage: letterboxed [-h] (-n | -l top-rgt-lft-btm) [-d <file>]

    NYT Letterboxed Two-Solver

    options:
    -h, --help          show this help message and exit
    -n                  Pull today's puzzle from the NYTimes website.
    -l top-rgt-lft-btm  Specify the letters you want on the box.
    -d <file>           Dictionary File

    # Puzzle for December 8, 2023
    $ letterboxed -d /usr/share/dict/american-english -l CTO-UFM-QZB-INA -d /usr/share/dict/american-english-huge
    quiz -> zombification

    $ letterboxed -n

    Today's puzzle is CTO-UFM-QZB-INA

    quiz -> zombification
    quoz -> zombification

Example python module usage:

    from letterboxed import Letterbox

    with open("/usr/share/dict/american-english-small", "r") as fp:
        dict = fp.read().split("\n")

    lbox = Letterbox((('a', 'e', 'g'), ('h','i','l'), ('c', 'm', 'v'), ('p', 'o', 't')), dict)

    for pair in lbox.solve():
        print(" -> ".join(pair))


