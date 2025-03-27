from machine import *
from tape import *
from memory_object import *
from io import StringIO
import re


def parse_data(lines):
    memory = {}
    tapes = {}

    for line in lines:
        match line.rstrip().split():
            case 'STACK', name:
                memory[name] = Stack()
            case 'QUEUE', name:
                memory[name] = Queue()
            case 'TAPE', name:
                tapes[name] = Tape()

    return memory, tapes


def parse_logic(lines):
    logic_regex = re.compile(r'^(?P<state>\w+)] (?P<command>\w+(?: RIGHT| LEFT)?)(?:\((?P<arg>\w+)\))? (?P<transitions>.*)$')

    for line in lines:
        m = logic_regex.match(line)
        if m:
            #print(m.group('state'), m.group('command'), m.group('transitions'))
            print(m.groupdict())


def parse_command(command):
    pass


def parse(stream):
    lines = list(stream)

    logic_index = lines.index('.LOGIC\n')
    data_section, logic_section = lines[:logic_index], lines[logic_index:]

    print(parse_data(data_section))
    parse_logic(logic_section)


if __name__ == '__main__':
    with open('sample_machines/sample3.txt', 'r') as machine_input:
        parse(machine_input)
