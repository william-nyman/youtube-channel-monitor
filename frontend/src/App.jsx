import { useEffect, useState } from 'react'
import './App.css'

function App() {
  const [channels, setChannels] = useState([])
  async function loadChannels() {
    try {
      const response = await fetch('/channels/')

      if (!response.ok) {
        throw new Error('Could not load channels from database')
      }

      const fetchedChannels = await response.json()
      setChannels(fetchedChannels)
    } catch (error) {
      console.error(error.message)
    }
  }

  useEffect(() => {
    // eslint-disable-next-line react-hooks/set-state-in-effect
    loadChannels()
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
