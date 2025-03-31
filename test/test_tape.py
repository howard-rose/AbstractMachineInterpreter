import pytest
import copy

from tape import *


@pytest.fixture
def tape():
    return Tape()


@pytest.fixture
def tape2D():
    return Tape2D()


def test_set_tape(tape):
    test_str = 'abcdefghijklmnop'

    tape.set_tape(test_str)

    assert str(tape) == '#' + test_str + '#'


def test_tape_copy(tape):
    test_str = 'abcdefghijklmnop'
    tape.set_tape(test_str)

    tape2 = copy.copy(tape)
    tape2.set_tape('wxyz')
    tape2.head = 100

    assert tape.tape is not tape2.tape


def test_tape_scan(tape):
    test_str = 'abcdefghijklmnop'
    tape.set_tape(test_str)

    tape.right()
    tape.right()
    symbol = tape.scan()

    assert symbol == 'b'


def test_tape_write(tape):
    test_str = 'abcdefghijklmnop'
    tape.set_tape(test_str)

    tape.right()
    tape.right()
    tape.write('Z')
    symbol = tape.scan()

    assert symbol == 'Z'


def test_tape_2D(tape2D):
    tape2D.set_tape('abcdefghijklmnop')
    tape2D.down()
    tape2D.down()
    tape2D.write('Z')
    tape2D.up()
    tape2D.up()
    tape2D.up()

    expected_str = (
        '##################\n'
        '#abcdefghijklmnop#\n'
        '##################\n'
        'Z#################'
    )

    assert str(tape2D) == expected_str
