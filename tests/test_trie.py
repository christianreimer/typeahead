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


