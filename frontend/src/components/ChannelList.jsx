import { useState } from "react";

import gearIcon from "../assets/gear.svg";
import trashIcon from "../assets/trash.svg";
import linkIcon from "../assets/link.svg";
import sortIcon from "../assets/sort.svg";

export default function ChannelList(props) {
  const [openSettingsChannelId, setOpenSettingsChannelId] = useState(null);

  return (
    <div>
      <div className="channel-filters">
        <input
          className="search-box"
          type="search"
          placeholder="Search for channel..."
          onChange={(event) => {
            props.setSearchValue(event.target.value);
            props.setVisibleCount(10);
          }}
        ></input>
        <div className="sort-wrapper">
          <select
            className="sorting-selector"
            value={props.sortBy}
            onChange={(e) => props.setSortBy(e.target.value)}
          >
            <option value="newestFirst">Newest first</option>
            <option value="oldestFirst">Oldest first</option>
            <option value="nameAscending">Name (A-Z)</option>
            <option value="nameDescending">Name (Z-A)</option>
          </select>
          <span className="sort-icon" aria-hidden="true">
            {<img src={sortIcon} alt="" />}
          </span>
        </div>
      </div>
      <ul>
        {props.filteredChannels.length === 0 && props.searchValue != "" ? (
          <p>No matching channels found. Try a different search.</p>
        ) : (
          props.sorted.slice(0, props.visibleCount).map((channel) => (
            <li key={channel.channel_id}>
              {channel.name}
              <div className="channel-actions">
                <div className="channel-settings-wrapper">
                  <button
                    className={
                      openSettingsChannelId === channel.channel_id
                        ? "channel-settings-button is-open"
                        : "channel-settings-button"
                    }
                    onClick={() =>
                      setOpenSettingsChannelId((currentId) =>
                        currentId === channel.channel_id
                          ? null
                          : channel.channel_id,
                      )
                    }
                  >
                    {<img src={gearIcon} />}
                  </button>
                  {openSettingsChannelId === channel.channel_id ? (
                    <div className="settings-popover">
                      <div className="shorts-setting">
                        Monitor Shorts
                        <input
                          type="checkbox"
                          checked={Boolean(channel.monitor_shorts)}
                          onChange={(event) =>
                            props.updateShortsSetting(
                              channel.channel_id,
                              event.target.checked,
                            )
                          }
                        />
                      </div>
                    </div>
                  ) : null}
                </div>
                <a
                  className="channel-link"
                  rel="noopener"
                  target="_blank"
                  href={`https://www.youtube.com/channel/${channel.channel_id}`}
                >
                  {<img src={linkIcon} />}
                </a>
                <button
                  className="delete-button"
                  onClick={() =>
                    props.handleDeleteClick(channel.name, channel.channel_id)
                  }
                >
                  {<img src={trashIcon} />}
                </button>
              </div>
            </li>
          ))
        )}
      </ul>
      <div className="show-buttons-wrapper">
        {props.visibleCount > 10 && (
          <button
            className="show-less-button"
            onClick={() => props.setVisibleCount(props.visibleCount - 10)}
          >
            Show less
          </button>
        )}

        {props.sorted.length > props.visibleCount && (
          <button
            className="show-more-button"
            onClick={() => props.setVisibleCount(props.visibleCount + 10)}
          >
            Show more
          </button>
        )}
      </div>
    </div>
  );
}
