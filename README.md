# Twitchify

[![PyPI Version](https://img.shields.io/pypi/v/twitchify)](https://pypi.org/project/twitchify)
[![Python versions](https://img.shields.io/pypi/pyversions/twitchify)](https://pypi.org/project/twitchify)

Twitchify is a Python library designed for seamless Twitch API interactions. It integrates real-time event handling with Twitch’s Helix API, offering a streamlined and efficient approach to managing Twitch functionality.

## Quick Start

### Installation

Install Twitchify using the following commands:

```shell
# Windows
py -3 -m pip install -U twitchify

# Linux/macOS
python3 -m pip install -U twitchify
```

### Basic Example

Here’s a quick example to get you started:

```python
from twitch.types import eventsub
from twitch import Client

client = Client(client_id='YOUR_CLIENT_ID')

@client.event
async def on_ready():
    print('PogU.')

@client.event
async def on_follow(data: eventsub.channels.FollowEvent):
    await client.channel.chat.send_message(f'{data["user_name"]} just followed!')

client.run('YOUR_USER_ACCESS_TOKEN')
```

## OAuth Authentication

Authenticate easily using Device Flow:

```python
from twitch.ext.oauth import DeviceAuthFlow, Scopes
from twitch import Client

client = Client(client_id='YOUR_CLIENT_ID')

DeviceAuthFlow(
    client=client,
    scopes=[Scopes.USER_READ_FOLLOWS]
)

@client.event
async def on_code(code: str):
    print(f'Verification URI: https://www.twitch.tv/activate?device-code={code}')

@client.event
async def on_auth(access_token: str, refresh_token: str):
    print(f'Token: {access_token}')

client.run()
```

## Learn More

For detailed documentation, visit our [Documentation](https://twitchify.readthedocs.io/en/latest/).

## Need Help?

For support, join the [Twitch API Discord](https://discord.gg/8NXaEyV) and mention @Snifo.
