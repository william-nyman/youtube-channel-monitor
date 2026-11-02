import { useEffect, useState } from 'react'
import './App.css'
import ChannelList from './components/ChannelList'
import AddForm from './components/AddForm'


function App() {
  const [channels, setChannels] = useState([])
  const[searchValue, setSearchValue] = useState("")
  const[sortBy, setSortBy] = useState("newestFirst")


  const filteredChannels = channels.filter((channel) => {
    return channel.name.toLowerCase().includes(searchValue.toLowerCase())
  })

  const sorted = sortChannels(filteredChannels, sortBy);


  useEffect(() => {
    loadChannels()

  }, [])


  function sortChannels(filteredChannels, sortBy) {
    const sorted = [...filteredChannels];

    if (sortBy === "newestFirst") {
      sorted.reverse();
    } else if (sortBy === "nameAscending") {
      sorted.sort((a, b) => a.name.localeCompare(b.name));
    } else if (sortBy === "nameDescending") {
      sorted.sort((a, b) => b.name.localeCompare(a.name));
    }

    return sorted;
  }


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

      <ChannelList
        sortBy={sortBy}
        setSortBy={setSortBy}
        sorted={sorted}
        setSearchValue={setSearchValue}
        filteredChannels={filteredChannels}
        searchValue={searchValue}
        handleDeleteClick={handleDeleteClick}
      />

      <h3>Add new channel:</h3>

      <AddForm
        handleSubmitClick={handleSubmitClick}
      />

    </main>
  )
}

export default App
