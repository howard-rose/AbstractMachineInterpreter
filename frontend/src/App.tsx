import {createContext, useState} from 'react'
import './App.css'
import {Provider} from "@/components/ui/provider"
import {MachineInput} from "@/components/MachineInput.tsx";
import {Timelines} from "@/components/Timelines.tsx";


export const MachineContext = createContext({
  machine: {}, fetchMachine: () => {}
})

function App() {
  const [machine, setMachine] = useState({})
  const fetchMachine = async () => {
    const response = await fetch("http://localhost:8000/machine")
    const machine = await response.json()
    setMachine(machine)
  }
  const [count, setCount] = useState(0)

  return (
    <Provider>
      <MachineContext.Provider value={{machine, fetchMachine}}>
        <MachineInput/>
        <Timelines/>
      </MachineContext.Provider>
      {/*<div>*/}
      {/*  <a href="https://vite.dev" target="_blank">*/}
      {/*    <img src={viteLogo} className="logo" alt="Vite logo" />*/}
      {/*  </a>*/}
      {/*  <a href="https://react.dev" target="_blank">*/}
      {/*    <img src={reactLogo} className="logo react" alt="React logo" />*/}
      {/*  </a>*/}
      {/*</div>*/}
      {/*<h1>Vite + React</h1>*/}
      {/*<div className="card">*/}
      {/*  <button onClick={() => setCount((count) => count + 1)}>*/}
      {/*    count is {count}*/}
      {/*  </button>*/}
      {/*  <p>*/}
      {/*    Edit <code>src/App.tsx</code> and save to test HMR*/}
      {/*  </p>*/}
      {/*</div>*/}
      {/*<p className="read-the-docs">*/}
      {/*  Click on the Vite and React logos to learn more*/}
      {/*</p>*/}

    </Provider>
  )
}

export default App
