# Twitchify

[![PyPI Version](https://img.shields.io/pypi/v/twitchify)](https://pypi.org/project/twitchify) [![Python Versions](https://img.shields.io/pypi/pyversions/twitchify)](https://pypi.org/project/twitchify)

**Twitchify** is a Python library designed for seamless Twitch event handling via WebSocket EventSub and API integration through the Helix API. It simplifies building Twitch apps by combining both real-time event notifications and API functionality into a single, user-friendly package.

## Installation

Install Twitchify using pip:

```bash
# On Windows
py -3 -m pip install -U twitchify

# On Linux/macOS
python3 -m pip install -U twitchify
```

## Quick Start

Here’s a simple example to get you started with Twitchify:

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

## OAuth Authentication

Authenticate easily with Twitch using the Device Flow authentication method:

```python
from twitch import Client
from twitch.types import eventsub
from twitch.ext.oauth import DeviceAuthFlow, Scopes

client = Client(client_id='YOUR_CLIENT_ID')

DeviceAuthFlow(
    client=client,
    scopes=[Scopes.CHANNEL_READ_SUBSCRIPTIONS]
)

@client.event
async def on_code(code: str):
    print(f'Go to https://www.twitch.tv/activate and enter this code: {code}')

@client.event
async def on_auth(access_token: str, refresh_token: str):
    print(f'Access Token: {access_token}')
    
@client.event
async def on_subscribe(data: eventsub.channels.SubscribeEvent):
    await client.channel.chat.send_message(f'{data["user_name"]} just Subscribed!')

client.run()
```

## Documentation and Support

For more detailed instructions,
visit the [Twitchify Documentation](https://twitchify.readthedocs.io/en/latest/).

Need help or want to join the community? Join the [Discord server](https://discord.gg/UFTkgnse7d).
