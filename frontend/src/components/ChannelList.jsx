import trashIcon from '../assets/trash.svg'
import linkIcon from  '../assets/link.svg'
import sortIcon from '../assets/sort.svg'

export default function ChannelList(props) {
  return (
    <div>
      <div className="channel-filters">
        <input className="search-box" type="search" placeholder="Search for channel..." onChange={(event) => props.setSearchValue(event.target.value)}></input>
        <div className="sort-wrapper">
          <select className="sorting-selector" value={props.sortBy} onChange={(e) => props.setSortBy(e.target.value)}>
            <option value="newestFirst">Newest first</option>
            <option value="oldestFirst">Oldest first</option>
            <option value="nameAscending">Name (A-Z)</option>
            <option value="nameDescending">Name (Z-A)</option>
          </select>
          <span className="sort-icon" aria-hidden="true">{<img src={sortIcon} alt="" />}</span>
        </div>
      </div>
      <ul>
        {props.filteredChannels.length === 0 && props.searchValue != ""
          ? <p>No matching channels found. Try a different search.</p>
          : props.sorted.map((channel) => (
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
