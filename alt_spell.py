"""
Slightly modified probabilistic spell checker based on work by Peter Norwig.
See http://norvig.com/spell-correct.html for original essay. 
"""

import collections
import re
import string


class AltSpell(object):
    def __init__(self, word_file):
        with open(word_file, 'r') as f:
            data = f.read()
            self.corpus = collections.Counter(re.findall(r'\w+', data.lower()))
        self.sum_words = sum(self.corpus.values())
    
    def add(self, word):
        """
        Add new word to vocabulary.
        """
        self.corpus[word] += 1
        self.sum_words += 1
    
    def remove(self, word):
        """
        Remove word from vocabulary.
        """
        if not word in self.corpus:
            raise ValueError(f'{word} not found in corpus')
        self.sum_words -= self.corpus[word]
        del self.corpus[word]

    def prob(self, word):
        """
        Return probability of word given the corpus.
        """
        return self.corpus[word] / self.sum_words

    def alternatives(self, word, max_alternatives=3):
        """
        Generate possible alternatives for word.
        """
        alternatives = self.known([word])
        alternatives |= self.known(self.edits1(word))
        if len(alternatives) < max_alternatives:
            alternatives |= self.known(self.edits2(word))
        alternatives = list(alternatives)
        alternatives = sorted(alternatives, key=self.prob, reverse=True)
        return alternatives[:max_alternatives]

    def known(self, words):
        """
        The subset of `words` that appear in the corpus.
        """
        return set(w for w in words if w in self.corpus)

    def edits1(self, word):
        """
        All edits that are one edit away from `word`.
        """
        letters = string.ascii_lowercase
        splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
        deletes = [L + R[1:] for L, R in splits if R]
        transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1]
        replaces = [L + c + R[1:] for L, R in splits if R for c in letters]
        inserts = [L + c + R for L, R in splits for c in letters]
        return set(deletes + transposes + replaces + inserts)

    def edits2(self, word):
        """
        All edits that are two edits away from `word`.
        """
        return (e2 for e1 in self.edits1(word) for e2 in self.edits1(e1))
