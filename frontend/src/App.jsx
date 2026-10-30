import { useEffect, useState } from 'react'
import './App.css'


function App() {
  const [channels, setChannels] = useState([])
  const[searchValue, setSearchValue] = useState("")


  const filteredChannels = channels.filter((channel) => {
    return channel.name.toLowerCase().includes(searchValue.toLowerCase())
  })


  useEffect(() => {
    loadChannels()

  }, [])


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


  async function handleSubmitClick(event) {
    event.preventDefault()

    const handle = event.currentTarget.elements.handle.value
    const form = event.currentTarget

    try {
      const response = await fetch("/channels", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ "handle": handle })
      })
      if (!response.ok) {
        throw new Error(`Could not add channel: ${response.status} ${await response.text()}`)
      }

      loadChannels()
    } catch(error) {
      console.error(error.message)
    } finally {
      form.reset()
    }
  }


  return (
    <main>
      <h1>Monitored:</h1>
      <input type="search" placeholder="search for channel..." onChange={(event) => setSearchValue(event.target.value)}></input>
      <ul>
        {filteredChannels.map((channel) => (
          <li key={channel.channel_id}>
            {channel.name}
            <button onClick={() => handleDeleteClick(channel.name, channel.channel_id)}>Delete</button>
          </li>
        ))}
      </ul>
      <form onSubmit={(event) => handleSubmitClick(event)}>
        <input type="text" placeholder="@handle.." name="handle"></input>
        <input type="submit" value="Add"></input>
      </form>

    </main>
  )
}

export default App
