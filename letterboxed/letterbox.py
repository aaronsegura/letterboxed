from typing import TypeAlias, Tuple, List, Optional, Set

box_side : TypeAlias = Tuple[str, str, str]
box : TypeAlias = Tuple[box_side, box_side, box_side, box_side]

class Letterbox:

    def __init__(
            self,
            sides: box,
            dictionary: List[str]):

        self.sides: box = sides
        self.dictionary = dictionary
        self.valid_words: List[str] = [w for w in self.dictionary if self.__word_obeys_rules(w)]

    def __side(self, side: int) -> box_side:
        return self.sides[side]

    @property
    def __all_letters(self) -> List[str]:
        letters: List[str] = []
        for x in range(0,4):
            letters.extend(self.__side(x))
        return letters

    def __side_with_letter(self, letter: str) -> Optional[int]:
        for x in range(0,3):
            if letter in self.__side(x):
                return x
        return None

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

        return sorted(self.__all_letters) == sorted(list(letters_used))

    def __word_obeys_rules(self, word: str):
        # Word must be at least 3 characters
        if len(word) < 3:
            return False

        # Letters in word must be in the letterbox
        for letter in word:
            if letter not in self.__all_letters:
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

        Return the all two-word solutions found in the given dictionary.

        Returns:
            List[str]: List of two words to solve the puzzle.
        """
        answers: List[List[str]] = []
        for word in self.valid_words:
            for next_word in self.__valid_next_words(word):
                if word == next_word:
                    continue
                if self.__all_letters_used([word, next_word]):
                    answers.append([word, next_word])
                    break

        return answers
