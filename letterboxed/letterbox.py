import random

from functools import lru_cache

from typing import TypeAlias, Tuple, List, Set, Dict, Optional

from .dictionary import Dictionary

box : TypeAlias = Tuple[str, str, str, str]

class Side:

    def __init__(
            self,
            letters: str):

        self._letters: str = letters.lower()

    def __len__(self):  # noqa: D105
        return len(self._letters)

    def __contains__(self, letters: str):
        """X in Y?"""
        for x in letters:
            if x in self._letters:
                return True
        return False

    def __str__(self):  # noqa: D105
        return self._letters

    def add(self, letter):
        """Add letter to this side."""
        self._letters += letter

    @classmethod
    def blank(cls):
        """Create a new blank side."""
        return cls("")

    @property
    def letters(self):
        """Return all letters on this side."""
        return self._letters


class Letterbox:

    def __init__(
            self,
            sides: Tuple[str, str, str, str],
            dictionary: Optional[List[str]] = None):

        self.sides: Tuple[Side, Side, Side, Side] = (
            Side(sides[0]),
            Side(sides[1]),
            Side(sides[2]),
            Side(sides[3]))

        if dictionary:
            self.words: Dictionary = Dictionary([
                w.lower() for w in dictionary if self.__word_obeys_rules(w.lower())])

    @classmethod
    def __invalid_pairs(cls, letters: str) -> Dict[str, List[str]]:
        """Return dictionary of letter that can't be on the same side.

        Args:
            letters (str): The solution to the puzzle.

        Returns:
            Dict[str, List[str]]: Dictionary where keys are a letter and the values
            are letters that cannot be on the same side.
        """
        idx = 0
        invalid_pairs: Dict[str, List[str]] = {x: [] for x in letters}
        while idx < len(letters):
            lettertrio = letters[idx:idx+3]

            if len(lettertrio) == 1:
                break

            invalid_pairs[lettertrio[1]].append(lettertrio[0])

            if len(lettertrio) == 3:
                invalid_pairs[lettertrio[1]].append(lettertrio[2])

            idx += 1

        return invalid_pairs

    @classmethod
    def __generate_box(cls, wordpair: List[str], size: int = 3) -> box:
        """Create a new random letterbox.

        Args:
            wordpair (List[str]): A two-word solution.
            size (int, optional): Size of each side. Defaults to 3.

        Returns:
            box: _description_
        """
        sides: Tuple[Side, Side, Side, Side] = (
            Side.blank(), Side.blank(), Side.blank(), Side.blank())
        all_letters = wordpair[0] + wordpair[1][1:]
        sides[random.randint(0,3)].add(all_letters[0])
        used_letters = [all_letters[0]]
        invalid_pairs = Letterbox.__invalid_pairs(all_letters)
        idx: int = 0

        while idx < len(all_letters):
            idx += 1
            letterpair = all_letters[idx-1:idx+1]

            if len(letterpair) == 1:
                break

            if letterpair[1] in used_letters:
                continue

            random_side = random.randint(0,3)
            tries = 0
            try:
                while "".join(invalid_pairs[letterpair[1]]) in sides[random_side] \
                        or len(sides[random_side]) == size:
                    tries += 1
                    if tries == 12:
                        raise IndexError
                    random_side = random.randint(0,3)
            except IndexError:
                # If we just can't do it after 12 tries, start over and try again.
                idx = 0
                sides = (Side.blank(), Side.blank(), Side.blank(), Side.blank())
                sides[random.randint(0,3)].add(all_letters[0])
                used_letters = [all_letters[0]]
                continue

            sides[random_side].add(letterpair[1])
            used_letters.append(letterpair[1])

        return (sides[0].letters, sides[1].letters, sides[2].letters, sides[3].letters)

    @classmethod
    def create_from_wordpair(cls, wordpair: List[str], size: int = 3) -> 'Letterbox':
        """Contructor for creating a letterbox from a known word pair.

        Args:
            wordpair (List[str]): The pair of words.
            size (int, optional): Size of the box sides. Defaults to 3.

        Raises:
            RuntimeError: When the words don't make sense.

        Returns:
            Letterbox: The letterbox!
        """
        unique_letters = list(set("".join(wordpair)))
        if len(unique_letters) == size * 4:
            box = Letterbox.__generate_box(wordpair)
            return Letterbox(box)
        else:
            raise RuntimeError("Invalid wordpair passed.")

    @classmethod
    def create_random(cls, dictionary: List[str], size: int = 3) -> 'Letterbox':
        """Constructor for new random letterbox.

        Args:
            dictionary (List[str]): Dictionary to use.
            size (int, optional): Size of each side.. Defaults to 3.

        Returns:
            Letterbox: A new letterbox puzzle!
        """
        words = Dictionary(dictionary)

        wordpair = []
        unique_letters: List[str] = []
        starting_word: str = ""
        ending_word: str = ""

        while not wordpair:
            starting_word = random.choice(words)
            for ending_word in words.valid_next_words(starting_word[len(starting_word)-1]):
                unique_letters = list(set(starting_word + ending_word))
                if len(unique_letters) == size * 4:
                    wordpair = [starting_word, ending_word]
                    break

        box = Letterbox.__generate_box(wordpair, size)
        return cls(box, dictionary)

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

    def puzzle(self) -> str:
        """Return the letters on each side for this box.

        Returns:
            str: _description_
        """
        return "-".join([str(x) for x in self.sides])

    def guess(self, words: List[str]) -> bool:
        """Evaluate a guess as right or wrong."""
        for word in words:
            if word.lower() not in self.words:
                raise RuntimeError(f'"{word}" is not a valid word for this puzzle.')

        idx: int = 0
        while idx < len(words):
            try:
                if words[idx][len(words[idx])-1] != words[idx+1][0]:
                    raise RuntimeError("Words do not form a chain.")
            except IndexError:
                pass
            idx += 1

        return self.__all_letters_used(words)

    def solve(self, dictionary: Optional[List[str]] = None) -> List[List[str]]:
        """Solve the letterboxed puzzle.

        Return the all one or two word solutions found in the given dictionary.

        Returns:
            List[List[str]]: List of two-word lists that solve the puzzle.
        """
        if dictionary:
            self.words: Dictionary = Dictionary([
                w.lower() for w in dictionary if self.__word_obeys_rules(w.lower())])

        if not self.words:
            raise RuntimeError(
                "Must pass a dictionary for solving when one was not passed for creation.")

        answers: List[List[str]] = []
        for word in self.words:
            # Check for one-word answer
            if self.__all_letters_used([word]):
                answers.append([word])
                continue

            # Check for two-word answer
            for next_word in self.words.valid_next_words(word[len(word)-1]):
                if self.__all_letters_used([word, next_word]):
                    answers.append([word, next_word])

        return sorted(answers, key=lambda x: len(x))
