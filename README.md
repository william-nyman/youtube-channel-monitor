# YouTube Channel Monitor

## Description

YouTube Channel Monitor is a self-hosted program that monitors YouTube channels and sends a notification through ntfy when a new video is published.

## Motivation

I built this because having YouTube installed on my phone made me spend more time on it. YouTube's recommendation algorithm and Shorts are designed to grab your attention, so I started watching through the browser instead, logged out. That way, I only opened YouTube when I had something specific to watch.

The problem was that I no longer received notifications from the channels I actually wanted to follow, so I built this small program to solve that.

## Features

- Monitor multiple YouTube channels for new uploads.
- Add, list, and remove channels through a simple web interface or command-line interface.
- Receive notifications through ntfy.

## Requirements

- Docker with Docker Compose.
- Git for cloning the project.
- Access to an ntfy server, such as ntfy.sh or a self-hosted instance.

## Installation

### Clone the project

Open a terminal in the directory where you want to store the project, then run:

```
git clone https://github.com/william-nyman/youtube-channel-monitor.git
cd youtube-channel-monitor
```

### Configure notifications

Create a file named `.env` in the project directory:

```dotenv
NTFY_SERVER=https://ntfy.sh
NTFY_TOPIC=your-topic-name
```

Replace the values with your ntfy server address and topic. Subscribe to the same server and topic in your ntfy client. Full documentation is available at https://docs.ntfy.sh/.

### Start the application

From the project directory, run:

```
docker compose up -d --build
```

This builds the Docker image and starts the application.

On the computer running Docker, open:

http://127.0.0.1:8070

### Configure the check interval

The check interval is configured in `config.toml`:

```toml
check_interval_minutes = 10
```

The default is ten minutes. After changing this file, rebuild and recreate the container:

```
docker compose up -d --build
```

## Usage

### Web interface

Open http://127.0.0.1:8070 to:

- View monitored channels.
- Add a channel using its `@handle`.
- Remove a channel using its delete button.

### Command-line interface

Run these commands from the project directory while the container is running.

Add a channel:

```
docker compose exec ytmonitor ytmonitor add @handle
```

List monitored channels and their IDs:

```
docker compose exec ytmonitor ytmonitor list
```

Remove a channel using its channel ID:

```
docker compose exec ytmonitor ytmonitor delete {channelID}
```
