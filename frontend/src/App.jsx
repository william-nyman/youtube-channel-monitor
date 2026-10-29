import { useEffect, useState } from 'react'
import './App.css'

function App() {
  const [channels, setChannels] = useState([])

  async function loadChannels() {
    try {
      const response = await fetch('/channels')

      if (!response.ok) {
        throw new Error('Could not load channels from database')
      }

      const fetchedChannels = await response.json()
      setChannels(fetchedChannels)
    } catch (error) {
      console.error(error.message)
    }
  }

  function handleSearchChange(searchValue) {
    if (searchValue === "") {loadChannels()}
    const filterBySearch = channels.filter((channel) => {
      if (channel.name.toLowerCase().includes(searchValue.toLowerCase())) {
        return channel
      }
    })
    setChannels(filterBySearch)
  }

  async function handleDeleteClick(name, channel_id) {
    if (confirm(`Are you sure you want to delete ${name}`)) {
      const response = await fetch(`/channels/${channel_id}`, {
        method: "delete"
      })
      if (response.ok) {
        alert("Deletion was successfull")
        loadChannels()
      } else {
        alert("Deletion failed")
      }
    }
  }


  useEffect(() => {
    // eslint-disable-next-line react-hooks/set-state-in-effect
    loadChannels()
  }, [])

  return (
    <main>
      <h1>Monitored:</h1>
      <input type="search" placeholder="search for channel..." onChange={(event) => handleSearchChange(event.target.value)}></input>
      <ul>
        {channels.map((channel) => (
          <li key={channel.channel_id}>
            {channel.name}
            <button onClick={() => handleDeleteClick(channel.name, channel.channel_id)}>Delete</button>
          </li>
        ))}
      </ul>

    </main>
  )
}

export default App
