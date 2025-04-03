import { useContext, useEffect } from 'react'
import { Text } from '@chakra-ui/react'
import {MachineContext} from "@/App.tsx";

export const Timelines = () => {
  const { machine, fetchMachine } = useContext(MachineContext)
  useEffect(() => {
    fetchMachine()
  }, [])

  return (
    <Text>
      {JSON.stringify(machine)}
    </Text>
  )
}