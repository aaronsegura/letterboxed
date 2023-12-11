# Letterboxed Solver

Python module to solve the [daily word puzzle](https://www.nytimes.com/puzzles/letter-boxed) from the New York Times.

### Installation

    python -mpip install letterboxed

### Usage

You will need a local dictionary file in order to use this module if you want to specify custom puzzles with the `-l` argument.

    $ letterboxed -h
    usage: letterboxed [-h] (-n | -l top-rgt-lft-btm | -r) [-d <file>] [-g word1,word2]

    NYT Letterboxed Solver

    options:
    -h, --help          show this help message and exit
    -n                  Pull today's puzzle from the NYTimes website.
    -l top-rgt-lft-btm  Specify the letters you want on the box.
    -r                  Generate a random letterbox puzzle.
    -d <file>           Dictionary File
    -g word1,word2      Make a guess on the supplied letterbox.

    # Puzzle for December 8, 2023
    $ letterboxed -d /usr/share/dict/american-english -l CTO-UFM-QZB-INA -d /usr/share/dict/american-english-huge
    quiz -> zombification

    $ letterboxed -n

    Today's puzzle is CTO-UFM-QZB-INA

    quiz -> zombification
    quoz -> zombification

    $ letterboxed -l CTO-UFM-QZB-INA -g quiz,zombification -d /usr/share/dict/american-english-huge
    You got it!

    $ letterboxed -r -d /usr/share/dict/american-english
    Your letterbox puzzle is

            vdi-tsn-aeo-mrl

    Run `letterboxed -l vdi-tsn-aeo-mrl -g your,guess` to make a guess.

Example python module usage:

    from letterboxed import Letterbox

    with open("/usr/share/dict/american-english-small", "r") as fp:
        dict = fp.read().split("\n")

    lbox = Letterbox((('a', 'e', 'g'), ('h','i','l'), ('c', 'm', 'v'), ('p', 'o', 't')), dict)

    for pair in lbox.solve():
        print(" -> ".join(pair))


