# Twitchify 

[![PyPI Version](https://img.shields.io/pypi/v/twitchify)](https://pypi.org/project/twitchify)
[![Python versions](https://img.shields.io/pypi/pyversions/twitchify)](https://pypi.org/project/twitchify)

Twitchify simplifies Twitch integration by combining WebSocket EventSub, Helix API, and IRC Chat for real-time event notifications and comprehensive Twitch functionality.

## Features
- **Real-time Event Notifications:** Stay up-to-date with Twitch events through WebSocket EventSub, ensuring your application responds instantly.
- **Helix API Support:** Access the full power of the Twitch Helix API with a single user access token.
- **Bot Support:** Easily listen to channel messages.
- **Type Hinting:** Twitchify includes built-in support for type hinting, promoting code clarity and maintainability.

### Why Choose Twitchify?
Twitchify puts the user first, making it ideal for personal use and hassle-free Twitch event setup. Unlike other libraries that require multiple tokens, Twitchify simplifies the process with just one user access token.
Developers can create Twitch applications effortlessly, thanks to Twitchify's seamless integration of WebSocket EventSub and Helix API. Real-time event notifications and built-in authentication make handling Twitch events a breeze.

### What is the difference between a Client and a Bot?
The client supports EventSub and Helix API, while the bot inherently supports IRC chat, allowing it to listen to any channel's chatroom.

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
from twitch import Follow, Message
from twitch.bot import Bot

bot = Bot(client_id='YOUR_CLIENT_ID', client_secret='YOUR_CLIENT_SECRET')

@bot.event
async def on_follow(user: Follow):
    """
    This called when a user follows the channel.
    """
    await bot.send(f'{user.display_name} just followed you!')

@bot.event
async def on_message(message: Message):
    """
    This called when the bot receives a message from a channel chat room.
    """
    if message.author != bot.user:
        if message.content.startswith('!ping'):
            await bot.replay(message, 'Pong!')
    print(f'{message.author}: {message}')
    
@bot.event
async def on_auth(access_token: str, refresh_token: str):
    """
    This called when the client is successfully authenticated.
    """
    # Store those for future use.
    print('Received access token:', access_token)
    print('Received refresh token:', refresh_token)

# Generate the authorization URL for the Twitch client.
# The user should visit the provided URL to authorize the app.
bot.run(scopes=['moderator:read:followers', 'chat:edit'])
```

Please refer to the [Documentation](https://twitchify.readthedocs.io/en/latest/) fore more details.
