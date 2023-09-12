# Twitchify 

[![PyPI Version](https://img.shields.io/pypi/v/twitchify)](https://pypi.org/project/twitchify)
[![Python versions](https://img.shields.io/pypi/pyversions/twitchify)](https://pypi.org/project/twitchify)

Twitchify is a Python library that unites Twitch's WebSocket EventSub and Helix API, seamlessly providing real-time event notifications and facilitating Helix API utilization.



## Features

- Real-time Twitch event notifications through WebSocket EventSub.
- Helix API support with user access token for broader Twitch functionality.
- Built-in support for type hinting, ensuring code clarity and maintainability.

## Why Twitchify?

Twitchify is user-centric, perfect for self-use and hassle-free Twitch event setup.
Unlike other libraries with multiple tokens,
Twitchify prioritizes simplicity by using a single user access token.

Developers can create Twitch apps effortlessly, as Twitchify seamlessly integrates WebSocket EventSub
and Helix API. With real-time event notifications and built-in authentication, event handling is a breeze.

## Installation
You can install Twitchify using pip:

```shell
# Windows
py -3 -m pip install -U twitchify

# Linux/macOS
python3 -m pip install -U twitchify
```

## Quick Example
```python
from twitch import Client, Follow

client = Client(client_id="YOUR_CLIENT_ID")

@client.event
async def on_ready():
    """
    This called when the Twitch client is ready to receive events.
    """
    print("Ready as %s" % client.user.display_name)


@client.event
async def on_follow(user: Follow):
    """
    This called when a user follows the channel.
    """
    print("%s just followed you!" % user.display_name)

# Run the client with your user access token.
client.run(access_token="YOUR_ACCESS_TOKEN")
```

### With built-in Authentication

```python
from twitch import Client, Follow

client = Client(client_id="YOUR_CLIENT_ID", client_secret="YOUR_CLIENT_SECRET")

@client.event
async def on_ready():
    """
    This called when the Twitch client is ready to receive events.
    """
    print("Ready as %s" % client.user.display_name)
    
@client.event
async def on_follow(user: Follow):
    """
    This called when a user follows the channel.
    """
    print("%s just followed you!" % user.display_name)

@client.event
async def on_auth(access_token: str, refresh_token: str):
    """
    This called when the client is successfully authenticated.
    """
    # Store those for future use.
    print('Received access token:', access_token)
    print('Received refresh token:', refresh_token)
    
# Generate the authorization URL for the Twitch client.
# The user should visit the provided URL to authorize the app.
client.run(scopes=['moderator:read:followers'])
```

Please refer to the [Documentation](https://twitchify.readthedocs.io/en/latest/) fore more details.
