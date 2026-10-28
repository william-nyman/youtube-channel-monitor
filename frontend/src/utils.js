
export async function loadChannels() {
  const response = await fetch('/channels')

  if (!response.ok) {
    throw new Error(`Could not load channels: ${response.status}`)
  }

  return response.json()
}
