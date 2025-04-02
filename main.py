from fastapi import FastAPI
from parser import parse

app = FastAPI()


@app.get("/")
async def root():
    with open('sample_machines/sample5.txt', 'r') as machine_input:
        machine = parse(machine_input)
        while not machine.verdict:
            machine.step()
        return machine
    # return {"message": "Hello World"}
