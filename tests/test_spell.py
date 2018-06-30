import pytest
import alt_spell


@pytest.fixture
def speller():
    return alt_spell.AltSpell('tests/vocab.text')


def test_single(speller):
    alternatives = speller.alternatives('a')
    assert alternatives


def test_max_alternatives(speller):
    alternatives = speller.alternatives('a', max_alternatives=2)
    assert len(alternatives) == 2


def test_double_edit(speller):
    alternatives = speller.alternatives('aaa')
    assert alternatives


def test_add_word(speller):
    alternatives = speller.alternatives('abcdefg')
    assert not alternatives
    speller.add('abcdefg')
    alternatives = speller.alternatives('abcdefg')
    assert alternatives


def test_remove_word(speller):
    alternatives = speller.alternatives('aaa')
    assert alternatives
    speller.remove('a')
    alternatives = speller.alternatives('aaa')
    assert not alternatives


def test_remove_nonexsiting_word(speller):
    with pytest.raises(ValueError):
        speller.remove('word that does not exit')
