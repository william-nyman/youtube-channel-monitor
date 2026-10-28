import { useEffect, useState } from 'react'
import {loadChannels} from './utils'
import './App.css'

function App() {
  const [channels, setChannels] = useState([])



  useEffect (() => {
    loadChannels()
    .then((fetchedChannels) => {
    setChannels(fetchedChannels)
    })
    .catch((error) => {
      console.error(error.message)
    })
  }, [])

  return (
    <main>
      <ul>
        {channels.map((channel) => (
          <li key={channel.channel_id}>{channel.name}</li>
        ))}
      </ul>
    </main>
  )
}

export default App
