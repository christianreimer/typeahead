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