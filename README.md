# Twitchify

[![PyPI Version](https://img.shields.io/pypi/v/twitchify)](https://pypi.org/project/twitchify)
[![Python Versions](https://img.shields.io/pypi/pyversions/twitchify)](https://pypi.org/project/twitchify)

**Twitchify** is a streamlined Python library that bridges real-time Twitch event handling via WebSocket EventSub and API interaction through the Helix API. It simplifies Twitch app development by combining powerful features with ease of use.

## Quick Start

For detailed instructions and documentation, visit the [Twitchify Documentation](https://twitchify.readthedocs.io/en/latest/).

Need help or want to join the community? Join the [Twitchify Discord server](https://discord.gg/UFTkgnse7d).

### Installation

Install Twitchify using pip:

```bash
# On Windows
py -3 -m pip install -U twitchify

# On Linux/macOS
python3 -m pip install -U twitchify
```

### Basic Example

Here’s a simple example to get started with Twitchify:

```python
from twitch import Client
from twitch.types import eventsub

client = Client(client_id='YOUR_CLIENT_ID')

@client.event
async def on_ready():
    print('Client is ready!')

@client.event
async def on_follow(data: eventsub.channels.FollowEvent):
    await client.channel.chat.send_message(f'{data["user_name"]} just followed the channel!')

client.run('YOUR_USER_ACCESS_TOKEN')
```

### OAuth Authentication

Easily authenticate with Twitch using the Device Flow authentication method:

```python
from twitch import Client
from twitch.ext.oauth import DeviceAuthFlow, Scopes

client = Client(client_id='YOUR_CLIENT_ID')

DeviceAuthFlow(
    client=client,
    scopes=[Scopes.USER_READ_FOLLOWS]
)

@client.event
async def on_code(code: str):
    print(f'Go to https://www.twitch.tv/activate and enter this code: {code}')

@client.event
async def on_auth(access_token: str, refresh_token: str):
    print(f'Access Token: {access_token}')

client.run()
```