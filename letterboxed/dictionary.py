from functools import lru_cache

from typing import List

class Dictionary:

    def __init__(
            self,
            dictionary: List[str]):
        self._index: int = 0
        self._words = [w.lower() for w in dictionary if self.word_obeys_rules(w)]

    def __iter__(self) -> 'Dictionary':
        return self

    def __next__(self) -> str:
        if self._index < len(self._words):
            self._index += 1
            return self._words[self._index-1]
        else:
            raise StopIteration

    def __len__(self) -> int:
        return len(self._words)

    def __getitem__(self, item) -> str:
        return self._words[item]

    def __str__(self):
        return " ".join(self._words)

    def __contains__(self, word):
        return word in self._words

    @lru_cache(maxsize=26)
    def valid_next_words(self, char: str) -> List[str]:
        """Return all valid next words for the given last-character.

        Args:
            char (str): The last character of the current word.

        Returns:
            List[str]: List of valid next words.
        """
        return [x for x in self._words if x[0] == char]

    @classmethod
    def word_has_double_letters(cls, word: str):
        for idx in range(0, len(word)):
            try:
                if word[idx] == word[idx+1]:
                    return True
            except IndexError:
                pass
        return False

    @classmethod
    def word_obeys_rules(cls, word: str):
        # No words with apostrophes
        if '\'' in word:
            return False

        # Doubled-up letters are no bueno
        if Dictionary.word_has_double_letters(word):
            return False

        # Word is empty
        if not word:
            return False

        # Stupid roman numerals in the dictionary?
        if 'xx' in word or 'lx' in word:
            return False

        if 'é' in word:
            return False

        return True
