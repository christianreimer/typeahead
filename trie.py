"""
Trie datastructure which supports different values (weights) for
their tokens.
"""


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
        self.root = TrieNode('*', '*')
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
