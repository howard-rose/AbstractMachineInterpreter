import pytest

from parser import *


@pytest.fixture(params=['sample1', 'sample2', 'sample3', 'sample4', 'sample5', 'sample6'])
def expected_machine(request):
    expected_memory = {}
    expected_tapes = {}
    expected_states = {}

    match request.param:
        case 'sample1':
            expected_states = {
                'q0': State(
                    command='SCAN',
                    transitions={'0': ['q0'], '1': ['q1', 'accept']}
                ),
                'q1': State(
                    command='SCAN',
                    transitions={'0': ['q0'], '1': ['q2']}
                ),
                'q2': State(
                    command='SCAN',
                    transitions={'0': ['q0'], '1': ['q1', 'accept']}
                )
            }
        case 'sample2':
            expected_states = {
                'A': State(
                    command='SCAN RIGHT',
                    transitions={'0': ['A'], '1': ['B'], '#': ['accept']}
                ),
                'B': State(
                    command='SCAN LEFT',
                    transitions={'0': ['C'], '1': ['reject']}
                ),
                'C': State(
                    command='SCAN RIGHT',
                    transitions={'1': ['A']}
                )
            }
        case 'sample3':
            expected_memory = {'S1': Stack()}
            expected_states = {
                'A': State(
                    command='WRITE',
                    transitions={'#': ['B']},
                    receiver='S1'
                ),
                'B': State(
                    command='SCAN',
                    transitions={'0': ['C'], '1': ['D']},
                ),
                'C': State(
                    command='WRITE',
                    transitions={'#': ['B']},
                    receiver='S1'
                ),
                'D': State(
                    command='READ',
                    transitions={'#': ['E']},
                    receiver='S1'
                ),
                'E': State(
                    command='SCAN',
                    transitions={'1': ['D'], '#': ['F']},
                ),
                'F': State(
                    command='READ',
                    transitions={'#': ['accept']},
                    receiver='S1'
                )
            }
        case 'sample4':
            expected_memory = {'S1': Stack()}
            expected_states = {
                'A': State(
                    command='WRITE',
                    transitions={'#': ['B']},
                    receiver='S1'
                ),
                'B': State(
                    command='SCAN RIGHT',
                    transitions={'a': ['C'], 'b': ['D']},
                ),
                'C': State(
                    command='WRITE',
                    transitions={'X': ['B']},
                    receiver='S1'
                ),
                'D': State(
                    command='READ',
                    transitions={'X': ['E']},
                    receiver='S1'
                ),
                'E': State(
                    command='SCAN RIGHT',
                    transitions={'b': ['D'], 'c': ['F'], '#': ['F']}
                ),
                'F': State(
                    command='READ',
                    transitions={'#': ['G']},
                    receiver='S1'
                ),
                'G': State(
                    command='WRITE',
                    transitions={'#': ['H']},
                    receiver='S1'
                ),
                'H': State(
                    command='SCAN LEFT',
                    transitions={'b': ['H'], 'a': ['I']}
                ),
                'I': State(
                    command='SCAN RIGHT',
                    transitions={'a': ['I'], 'b': ['J']}
                ),
                'J': State(
                    command='WRITE',
                    transitions={'X': ['K']},
                    receiver='S1'
                ),
                'K': State(
                    command='SCAN RIGHT',
                    transitions={'b': ['J'], 'c': ['L']}
                ),
                'L': State(
                    command='READ',
                    transitions={'X': ['M']},
                    receiver='S1'
                ),
                'M': State(
                    command='SCAN RIGHT',
                    transitions={'c': ['L'], '#': ['N']}
                ),
                'N': State(
                    command='READ',
                    transitions={'#': ['accept']},
                    receiver='S1'
                )
            }
        case 'sample5':
            expected_memory = {'S1': Stack(), 'S2': Stack()}
            expected_states = {
                'A': State(
                    command='WRITE',
                    transitions={'#': ['B']},
                    receiver='S1'
                ),
                'B': State(
                    command='SCAN',
                    transitions={'a': ['C'], 'b': ['E']}
                ),
                'C': State(
                    command='WRITE',
                    transitions={'X': ['B']},
                    receiver='S1'
                ),
                'D': State(
                    command='WRITE',
                    transitions={'X': ['F']},
                    receiver='S2'
                ),
                'E': State(
                    command='READ',
                    transitions={'X': ['D']},
                    receiver='S1'
                ),
                'F': State(
                    command='SCAN',
                    transitions={'b': ['E'], 'c': ['G']}
                ),
                'G': State(
                    command='READ',
                    transitions={'X': ['H']},
                    receiver='S2'
                ),
                'H': State(
                    command='SCAN',
                    transitions={'c': ['G'], '#': ['I']}
                ),
                'I': State(
                    command='READ',
                    transitions={'#': ['J']},
                    receiver='S1'
                ),
                'J': State(
                    command='READ',
                    transitions={'#': ['accept']},
                    receiver='S2'
                )
            }
        case 'sample6':
            expected_tapes = {'T1': Tape()}
            expected_states = {
                'A': State(
                    command='RIGHT',
                    transitions={'0': ['B'], 'Y': ['D'], '1': ['reject']},
                    receiver='T1',
                    overwrites={'0': ['X'], 'Y': ['Y'], '1': ['1']}
                ),
                'B': State(
                    command='RIGHT',
                    transitions={'0': ['B'], 'Y': ['B'], '1': ['C']},
                    receiver='T1',
                    overwrites={'0': ['0'], 'Y': ['Y'], '1': ['Y']}
                ),
                'C': State(
                    command='LEFT',
                    transitions={'0': ['C'], 'Y': ['C'], 'X': ['A']},
                    receiver='T1',
                    overwrites={'0': ['0'], 'Y': ['Y'], 'X': ['X']}
                ),
                'D': State(
                    command='RIGHT',
                    transitions={'Y': ['D'], '#': ['accept'], '1': ['reject']},
                    receiver='T1',
                    overwrites={'Y': ['Y'], '#': ['#'], '1': ['1']},
                ),
            }

    return request.param, expected_memory, expected_tapes, expected_states


def test_parse(expected_machine):
    machine, expected_memory, expected_tapes, expected_states = expected_machine

    with open(f'../sample_machines/{machine}.txt', 'r') as f:
        parsed_machine = parse(f)

    assert parsed_machine.timelines[0].memory == expected_memory
    assert parsed_machine.timelines[0].tapes == expected_tapes
    assert parsed_machine.states == expected_states
