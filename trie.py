"""
Trie datastructure which supports different values (weights) for
their tokens.
"""

import string
import itertools


EMPTY_RESULT = (False, 0, [''])


class TrieNode(object):
    __slots__ = ['character', 'children', 'token_finished', 'count', 'tokens']

    def __init__(self, character,  token):
        self.character = character
        self.children = []
        self.token_finished = False
        self.count = 1
        self.tokens = [token]


class Trie(object):
    def __init__(self, vocabulary=None):
        self.root = TrieNode('', '')
        self.tokens = {}
        if vocabulary:
            for word in vocabulary:
                self.add(word)
    
    def __len__(self):
        return len(self.tokens)
    
    def add(self, word, value=1):
        """
        Add new token to the trie.
        """
        if word in self.tokens:
            raise ValueError(f'Token for {word} already exists')
        
        self.tokens[word] = value

        node = self.root
        for char in word:
            for child in node.children:
                if child.character == char:
                    child.count += 1
                    child.tokens.append(word)
                    node = child
                    break
            else:
                # Hit end of for loop, so char was not found in children
                new_node = TrieNode(char, word)
                node.children.append(new_node)
                node = new_node

        node.token_finished = True

    def update(self, word, delta_value=1):
        """
        Update the score for the specified token.
        """
        if not word in self.tokens:
            raise ValueError(f'Token for {word} does not exist')
            
        self.tokens[word] += delta_value
    
    def remove(self, query_string):
        """
        Remove the token(s) corresponsing to this query string.
        """
        pass  # pragma: nocover

    def prune_trie(self, query_string):
        """
        Remove all tokens that have query_string as a prefix.
        """
        pass   # pragma: nocover

    def query(self, query_string, max_results=None):
        """
        Return the most likely tokens for query_string. Cap the result at
        max_results.

        Example:
            >>> t = Trie(['green', 'growth', 'grail', 'gummy', 'glad'])
            >>> t.query('gr')
            (True, 3, [(1, 'growth'), (1, 'green'), (1, 'grail')])
            >>> t.add('grand', value=3)
            >>> t.query('gr', max_results=2)
            (True, 4, [(3, 'grand'), (1, 'growth')])
        """
        if not self.root.children:
            return EMPTY_RESULT

        node = self.root
        for char in query_string:
            for child in node.children:
                if child.character == char:
                    node = child
                    break
            else:
                # Hit end of for loop, so char not found
                return EMPTY_RESULT

        # The resulting tokens need to be sorted based on their value which is
        # tracked in the sepearate tokens dict
        tokens = [(self.tokens[t], t) for t in node.tokens]
        tokens = sorted(tokens, reverse=True)
        return True, node.count, tokens[:max_results]

    def lookup_table(self, depth=2, max_results=10):
        """
        Generate a lookup table of the possible tokens for all query strings
        with the indicated depth.

        The table will map from query string to a tuple with the number of
        tokens the query string is root to, as well as a sorted list of tokens
        and their value.

        Example:
            >>> t = Trie()
            >>> t.add('a')
            >>> t.add('aa', value=4)
            >>> t.add('aaa', value=2)
            >>> table = t.lookup_table()
            >>> table['a']
            (3, [(4, 'aa'), (2, 'aaa'), (1, 'a')])
            >>>
        """
        query_strings = []
        for i in range(depth):
            query_strings += ["".join(t) for t in 
                itertools.combinations_with_replacement(string.ascii_lowercase, i+1)]
        
        table = {}
        for qs in query_strings:
            found, pos_tokens, tokens = self.query(qs, max_results)
            if found:
                table[qs] = (pos_tokens, tokens)
        return table
