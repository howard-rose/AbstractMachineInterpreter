from typing import Annotated
from io import StringIO

from fastapi import Body, FastAPI
from parser import parse

app = FastAPI()

machine = None


@app.get("/")
async def root():
    # global machine
    # with open('sample_machines/sample6.txt', 'r') as machine_input:
    #     machine = parse(machine_input)
    #     while not machine.verdict:
    #         machine.step()
    #     return machine
    return {"message": "Hello World"}


@app.get("/machine")
async def get_machine():
    return machine


@app.post("/machine")
async def load_machine(machine_str: Annotated[str, Body()]):
    global machine
    machine = parse(StringIO(machine_str))
    return 'Machine loaded!'


@app.post("/step")
async def step():
    if machine:
        machine.step()
        return 'Performed step!'
    return 'Machine not loaded.'


@app.post("/input")
async def load_input(input: Annotated[str, Body()]):
    if machine:
        machine.reset(input)
    return f'Got {input}!'