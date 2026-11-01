import trashIcon from '../assets/trash.svg'
import linkIcon from  '../assets/link.svg'

export default function ChannelList(props) {
  return (
    <div>
      <input className="search-box" type="search" placeholder="Search for channel..." onChange={(event) => props.setSearchValue(event.target.value)}></input>
      <ul>
        {props.filteredChannels.length === 0 && props.searchValue != ""
          ? <p>No matching channels found. Try a different search.</p>
          : props.filteredChannels.map((channel) => (
          <li key={channel.channel_id}>
            {channel.name}
            <div className="channel-actions">
              <a className="channel-link" rel="noopener" target="_blank" href={`https://www.youtube.com/channel/${channel.channel_id}`}>{<img src={linkIcon}/>}</a>
              <button className="delete-button" onClick={() => props.handleDeleteClick(channel.name, channel.channel_id)}>{<img src={trashIcon}/>}</button>
            </div>
          </li>
        ))}
      </ul>
    </div>
  )
}
