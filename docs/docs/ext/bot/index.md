---
icon: material/information-slab-circle  
hide:  
  - toc  
---

# Introduction

## Overview

`Bot` is a Python class that extends [Client][twitch.client.Client] to manage Twitch interactions more effectively.

## Features

- **User Registration**: Register broadcasters with their access tokens and manage their tokens for API requests.
- **Broadcaster Management**: Retrieve and manage registered broadcasters within the bot's connection.
- **Flexible Authentication**: Authenticate users using their access or refresh tokens.
  
## Basic Usage

### Initialization

Create an instance of `Bot` with your client ID and client secret to start interacting with the Twitch API.

```python
from twitch.ext.bot import Bot

bot = Bot(client_id='YOUR_CLIENT_ID', client_secret='YOUR_CLIENT_SECRET')
```

### Registering a User

You can register a user using their access token or refresh token. Once registered, the bot can perform actions on their behalf.

```python
@bot.event
async def on_ready():
    # Register a broadcaster with an access token
    broadcaster = await bot.register_user(access_token='USER_ACCESS_TOKEN')
    print(f'{broadcaster.display_name} is now registered!')
```

### Checking User Registration

Verify whether a user is registered within the bot before subscribing to events.

```python
@bot.event
async def on_ready():
    user = await bot.get_user('snifo')
    
    if not bot.is_registered(user):
        print(f'{user.display_name} is not registered')
```

