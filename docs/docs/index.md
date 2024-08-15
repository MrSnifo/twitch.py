# Twitchify

[![PyPI Version](https://img.shields.io/pypi/v/twitchify)](https://pypi.org/project/twitchify)
[![Python versions](https://img.shields.io/pypi/pyversions/twitchify)](https://pypi.org/project/twitchify)

Twitchify is your streamlined solution for interacting with the Twitch API.
It provides a straightforward way to handle real-time events and access Twitch's
Helix API-all from a single client. With Twitchify, you can easily manage and
interact with multiple channels using just one user access token.

## Quick Start

### Installation

Get Twitchify up and running with:

```shell
# Windows
py -3 -m pip install -U twitchify

# Linux/macOS
python3 -m pip install -U twitchify
```

### Basic Example

Start coding with ease:

```python
from twitch.types import eventsub
from twitch import Client

client = Client(client_id='YOUR_CLIENT_ID')

@client.event
async def on_ready():
    print('Client is ready.')

@client.event
async def on_follow(data: eventsub.channels.FollowEvent):
    await client.channel.chat.send_message(f'{data["user_name"]} just followed!')

client.run('YOUR_USER_ACCESS_TOKEN')
```

## OAuth Authentication

Setting up OAuth is a breeze-just add a single line and let Twitchify handle the rest.
It’s almost like magic!

```python
from twitch.ext.oauth import DeviceAuthFlow, Scopes
from twitch import Client

client = Client(client_id='YOUR_CLIENT_ID')

DeviceAuthFlow(
    client=client,
    scopes=[Scopes.USER_READ_EMAIL]
)

@client.event
async def on_auth(access_token: str, refresh_token: str):
    print(f'Token: {access_token}')

client.run()
```

## Learn More

Explore the [Documentation](https://twitchify.readthedocs.io/en/latest/) for more details and advanced features.

## Need Help?

Join the [Twitch API Discord](https://discord.gg/8NXaEyV) and mention @Snifo for support.

Pogu ^^