from typing import TypeAlias, Tuple, List, Set

box_side : TypeAlias = Tuple[str, str, str]
box : TypeAlias = Tuple[box_side, box_side, box_side, box_side]

class Side:

    def __init__(
            self,
            letters: box_side):

        self._letters: List[str] = [letter.lower() for letter in letters]

    def __contains__(self, value):
        """X in Y?"""
        return value in self.letters

    @property
    def letters(self):
        """Return all letters on this side."""
        return self._letters


class Letterbox:

    def __init__(
            self,
            sides: box,
            dictionary: List[str]):

        self.sides: Tuple[Side, Side, Side, Side] = (
            Side(sides[0]),
            Side(sides[1]),
            Side(sides[2]),
            Side(sides[3]))
        self.valid_words: List[str] = [w for w in dictionary if self.__word_obeys_rules(w)]

    @property
    def __box_letters(self) -> List[str]:
        letters: List[str] = []
        for x in range(0,4):
            letters.extend(list(self.sides[x].letters))
        return letters

    def __side_with_letter(self, letter: str) -> Side:
        return [side for side in self.sides if letter in side].pop()

    def __is_valid_letter_pair(self, pair: str) -> bool:
        if len(pair) < 2:
            return True

        side_1 = self.__side_with_letter(pair[0])
        side_2 = self.__side_with_letter(pair[1])
        return side_1 != side_2

    def __all_letters_used(self, words: List[str]) -> bool:
        letters_used: Set[str] = set()
        for word in words:
            for letter in word:
                letters_used.add(letter)

        return sorted(self.__box_letters) == sorted(list(letters_used))

    def __word_obeys_rules(self, word: str):
        # Word must be at least 3 characters
        if len(word) < 3:
            return False

        # Letters in word must be in the letterbox
        for letter in word:
            if letter not in self.__box_letters:
                return False

        # Consecutive characters must not be from same side
        for index in range(0, len(word)):
            if not self.__is_valid_letter_pair(word[index:index+2]):
                return False

        return True

    def __valid_next_words(self, word: str) -> List[str]:
        return [x for x in self.valid_words if x[0] == word[len(word)-1]]

    def solve(self) -> List[List[str]]:
        """Solve the letterboxed puzzle.

        Return the all one or two word solutions found in the given dictionary.

        Returns:
            List[List[str]]: List of two-word lists that solve the puzzle.
        """
        answers: List[List[str]] = []
        for word in self.valid_words:
            # Check for one-word answer
            if self.__all_letters_used([word]):
                answers.append([word])
                continue

            # Check for two-word answer
            for next_word in self.__valid_next_words(word):
                if word == next_word:
                    continue
                if self.__all_letters_used([word, next_word]):
                    answers.append([word, next_word])
                    break

        return sorted(answers, key=lambda x: len(x))
