import { Button, VStack, Textarea, Input, Text } from '@chakra-ui/react'
import {useState, useEffect, useContext} from "react";
import { useForm } from "react-hook-form"
import {MachineContext} from "@/App.tsx";

export const MachineInput = () => {
  const { machine, fetchMachine } = useContext(MachineContext)
  const [steps, setSteps] = useState(0);

  const { register, handleSubmit } = useForm()
  const onSubmit = async (data) => {
    console.log(data)
    const machine_response = await fetch("http://localhost:8000/machine", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data.MachineDefinition)
    })
    const input_response = await fetch("http://localhost:8000/input", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data.Input)
    })
    console.log(machine_response)
    console.log(input_response)
    fetchMachine()
  }
  const onStepClick = async () => {
    const step_response = await fetch("http://localhost:8000/step", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
    })
    console.log(step_response)
    fetchMachine()
    setSteps((steps) => steps + 1)
  }

  return (
      <form onSubmit={handleSubmit(onSubmit)}>
        <VStack>
          <Text>Machine definition</Text>
          <Textarea {...register('MachineDefinition')} placeholder="Machine definition" />
          <Text>Initial input</Text>
          <Input {...register('Input')} placeholder="Initial input" />
          <Button type="submit">Load</Button>
          <Button onClick={onStepClick}>Step</Button>
          <Text>{steps}</Text>

        </VStack>
      </form>
  )
}