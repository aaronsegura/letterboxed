# Letterboxed Solver

Python module to solve the [daily word puzzle](https://www.nytimes.com/puzzles/letter-boxed) from the New York Times.

### Installation

    python -mpip install letterboxed

### Usage

You will need a local dictionary file in order to use this module.  On Linux they are usually available under `/usr/share/dict`.

    $ letterboxed -h
    usage: letterboxed [-h] -d <file> top left right bottom

    NYT Letterboxed Two-Solver

    positional arguments:
    top         Comma-separated letters from top side.
    left        Comma-separated letters from left side.
    right       Comma-separated letters from right side.
    bottom      Comma-separated letters from bottom side.

    options:
    -h, --help  show this help message and exit
    -d <file>   Dictionary File

    # Puzzle for December 7, 2023
    $ letterboxed -d /usr/share/dict/american-english a,e,g p,o,t h,i,l c,m,v
    glove -> empathetic

Example python module usage:

    from letterboxed import Letterbox

    with open("/usr/share/dict/american-english-small", "r") as fp:
        dict = fp.read().split("\n")

    lbox = Letterbox((('a', 'e', 'g'), ('h','i','l'), ('c', 'm', 'v'), ('p', 'o', 't')), dict)

    for pair in lbox.solve():
        print(" -> ".join(pair))


