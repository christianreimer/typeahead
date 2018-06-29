import trie
import pytest


def test_empty_trie():
    t = trie.Trie()
    assert t.query('hello', 1) == trie.EMPTY_RESULT

def test_empty_trie_len():
    t = trie.Trie()
    assert len(t) == 0

def test_single_trie():
    word = 'Hello'
    t = trie.Trie([word])
    r = t.query(word[:1], 5)
    assert r[0] == True
    assert r[1] == 1
    assert r[2][0][1] == word

def test_single_trie_false():
    word = 'Hello'
    t = trie.Trie([word])
    r = t.query(word[2:], 5)
    assert r == trie.EMPTY_RESULT

def test_single_trie_len():
    word = 'Hello'
    t = trie.Trie([word])
    assert len(t) == 1

def test_double_similar_token():
    word1 = 'Hello'
    word2 = 'HellO'
    t = trie.Trie([word1, word2])
    r = t.query(word1[:1], 5)
    assert r[0] == True
    assert r[1] == 2
    assert r[2][0][1] in (word1, word2)

def test_double_identical_token():
    word = 'Hello'
    t = trie.Trie([word])
    with pytest.raises(ValueError):
        t.add(word)

def test_update():
    word = 'Hello'
    t = trie.Trie([word])
    r = t.query(word[:1], 5)
    assert r[0] == True
    assert r[1] == 1
    assert r[2][0][1] == word
    assert r[2][0][0] == 1

    t.update('Hello', 2)
    r = t.query(word[:1], 5)
    assert r[0] == True
    assert r[1] == 1
    assert r[2][0][1] == word
    assert r[2][0][0] == 3


def test_update_no_exit():
    word = 'Hello'
    t = trie.Trie([word])
    with pytest.raises(ValueError):
        t.update('DoesNotExist', 2)


def test_lookup_table_empty():
    t = trie.Trie()
    assert t.lookup_table() == {}


def test_lookup_table_1_level_length():
    t = trie.Trie(['a', 'aa', 'aaa', 'b', 'bb', 'c'])
    table = t.lookup_table(1)
    assert table['a'][0] == 3
    assert len(table['a'][1]) == 3
    assert table['b'][0] == 2
    assert len(table['b'][1]) == 2
    assert table['c'][0] == 1
    assert len(table['c'][1]) == 1


def test_lookup_table_1_level_content():
    t = trie.Trie(['a', 'aa', 'aaa', 'b', 'bb', 'c'])
    table = t.lookup_table(1)
    for t in ((1, 'a'), (1, 'aa'), (1, 'aaa')):
        assert t in table['a'][1]
    for t in ((1, 'b'), (1, 'bb')):
        assert t in table['b'][1]
    assert (1, 'c') in table['c'][1]


def test_lookup_table_2_level_excludes():
    t = trie.Trie(['a', 'aa', 'aaa', 'b', 'bb', 'c'])
    table = t.lookup_table(2)
    assert table['aa'][0] == 2
    assert len(table['aa'][1]) == 2
    assert table['bb'][0] == 1
    assert len(table['bb'][1]) == 1
    assert 'cc' not in table


def test_lookup_table_2_level_priority():
    t = trie.Trie(['a', 'aa', 'aaa', 'b', 'bb', 'c'])
    t.update('bb', 3)
    t.update('aaa', 2)
    t.update('aa', 1)
    table = t.lookup_table()
    assert table['b'][1][0] == (4, 'bb')
    assert table['a'][1][0] == (3, 'aaa')
    assert table['a'][1][1] == (2, 'aa')
