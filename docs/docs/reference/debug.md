---
icon: fontawesome/solid/bug
hide:
  - toc
---

# Debugging
___

## Overview

Twitchify supports testing of EventSub events through a command-line interface ([CLI](https://dev.twitch.tv/docs/cli/))
mock WebSocket server. This feature allows you to simulate and test EventSub events without needing to deploy a
live Twitch application. The following guide shows you how to set up and use the CLI mock server with Twitchify.

## Setup
___

### Starting the Mock WebSocket Server

To start the mock WebSocket server, use the following command in your terminal:

```bash
twitch event websocket start-server
```

This command will start a WebSocket server on `127.0.0.1:8080` and provide endpoints for simulating EventSub events.
You should see output similar to:

```
2023/03/19 11:45:17 `Ctrl + C` to exit mock WebSocket servers.
2023/03/19 11:45:17 Started WebSocket server on 127.0.0.1:8080
2023/03/19 11:45:17 Simulate subscribing to events at: http://127.0.0.1:8080/eventsub/subscriptions
2023/03/19 11:45:17 Events can be forwarded to this server from another terminal with --transport=websocket
2023/03/19 11:45:17 Connect to the WebSocket server at: ws://127.0.0.1:8080/ws
```

### Connecting Twitchify to the Mock Server

Update your Twitchify client code to connect to the local WebSocket server. Here is an example configuration:

```python
from twitch.types import eventsub
from logging import DEBUG
from twitch import Client


# Initialize Twitch client with CLI support
client = Client(client_id='YOUR_CLIENT_ID', cli=True, cli_port=8080)

@client.event
async def on_ready():
    print('Ready with total cost events %s' % client.total_subscription_cost)
    
@client.event
async def on_ban(data: eventsub.moderation.BanEvent):
 print(data)

# Start the client and begin processing events.
client.run('YOUR_USER_ACCESS_TOKEN', log_level=DEBUG)
```

### Forwarding Mock Events

To forward mock events to your client, use the `twitch event trigger` command with the `--transport=websocket` flag.
For example, to trigger a channel ban event:

```bash
twitch event trigger channel.ban --transport=websocket
```

To target a specific client, use the `--session` flag with the session ID:

```bash
twitch event trigger channel.ban --transport=websocket --session=your_session_id
```

For more information on the CLI WebSocket event command and its options, visit the [official Twitch documentation](https://dev.twitch.tv/docs/cli/websocket-event-command/).