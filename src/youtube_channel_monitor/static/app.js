async function getChannels() {
  const response = await fetch("/channels");
  const channels = await response.json();
  return channels;
}


async function deleteChannel(channelId) {
  const response = await fetch(`/channels/${channelId}`, {
    method: "delete"
  });

  if (response.ok) {
    return true;
  } else {
    return false;
  }
}



function renderChannels(channels, searchText = "") {
  const channelList = document.getElementById("channels-list");
  channelList.innerHTML = "";

  for (const channel of channels) {
    if (searchText === "" || channel.name.toLowerCase().includes(searchText)) {
      const channelItem = document.createElement("li");
      channelItem.textContent = channel.name;

      const deleteChannelItem = document.createElement("button");
      deleteChannelItem.textContent = "delete";

      channelList.appendChild(channelItem);
      channelItem.appendChild(deleteChannelItem);

      deleteChannelItem.addEventListener("click", async function () {
        if (confirm(`Are you sure you want to delete ${channel.name}`)) {
          if (await deleteChannel(channel.channel_id)) {
            alert("Deletion was successful");
            channelItem.remove();
          } else {
            alert("Deletion failed");
          }
        }
      });
    }
  }
}


async function addChannel() {
  const addChannelForm = document.getElementById("add-channel-form");

  addChannelForm.addEventListener("submit", async function (event) {
    event.preventDefault();

    const submitButton = document.getElementById("submit-add-channel");
    submitButton.disabled = true;

    const channelHandle = document.getElementById("handle").value;

    try {
      const response = await fetch("/channels", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ "handle": channelHandle })
      });

      if (response.ok) {
        alert("Channel added");
        const updatedChannels = await getChannels();
        renderChannels(updatedChannels);
        document.getElementById("handle").value = "";
      }
    } finally {
      submitButton.disabled = false;
    }
  });
}


document.addEventListener("DOMContentLoaded", async function () {
  let channels = await getChannels();
  renderChannels(channels);


  const searchInput = document.getElementById("channel-search");
  searchInput.addEventListener("input", async function () {
    let channels = await getChannels();
    const searchText = searchInput.value.toLowerCase();
    renderChannels(channels, searchText);
  });
  
  addChannel();
});
