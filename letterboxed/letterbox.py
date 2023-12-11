from functools import lru_cache

from typing import TypeAlias, Tuple, List, Set

box : TypeAlias = Tuple[str, str, str, str]

class Side:

    def __init__(
            self,
            letters: str):

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
        self.valid_words: List[str] = [
            w.lower() for w in dictionary if self.__word_obeys_rules(w.lower())]

    @property
    @lru_cache(maxsize=None)
    def __box_letters(self) -> List[str]:
        """Return all letters in the box.

        Returns:
            List[str]: List of letters.
        """
        letters: List[str] = []
        for x in range(0,4):
            letters.extend(list(self.sides[x].letters))
        return letters

    @lru_cache(maxsize=None)
    def __side_with_letter(self, letter: str) -> Side:
        """Return side of box containing the given letter.

        Args:
            letter (str): The letter.

        Returns:
            Side: Side of the box.
        """
        return [side for side in self.sides if letter in side].pop()

    @lru_cache(maxsize=26*26)
    def __is_valid_letter_pair(self, pair: str) -> bool:
        """Return true if pair is valid.

        Valid pairs must not come from same side of box.

        Args:
            pair (str): Two letters

        Returns:
            bool: True if letters are not from same side of box.
        """
        if len(pair) < 2:
            return True

        side_1 = self.__side_with_letter(pair[0])
        side_2 = self.__side_with_letter(pair[1])
        return side_1 != side_2

    def __all_letters_used(self, words: List[str]) -> bool:
        """Determines if a word pair uses all the letters in the box.

        Args:
            words (List[str]): List of words.

        Returns:
            bool: True if all letters are used.
        """
        letters_used: Set[str] = set()
        for word in words:
            for letter in word:
                letters_used.add(letter)

        return sorted(self.__box_letters) == sorted(list(letters_used))

    def __word_obeys_rules(self, word: str):
        """Return True if word is valid for this box.

        Words must follow three rules:

        1. Must be at least 3 characters
        2. Letters must be in the letterbox
        3. Consecutive characters must not be from same side

        Args:
            word (str): The word.

        Returns:
            bool: True if valid.  False if invalid.
        """
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

    @lru_cache(maxsize=26)
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
