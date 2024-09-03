---
icon: material/information-slab-circle
hide:
  - toc
---

# Introduction

## Overview

`DeviceAuthFlow` is a Python class designed for managing Twitch's device authentication flow. It simplifies obtaining access tokens and managing the authentication process.

## Features

- **Easy Device Authentication**: Simplifies obtaining and managing Twitch access tokens.
- **Automatic Integration**: Works seamlessly with the `Client` class.
- **Event Handling**: Dispatches events for authentication and token retrieval.

## Basic Usage

### Initialization

Create an instance of `DeviceAuthFlow` with your Twitch client and required scopes.
Ensure to manage the access token and refresh token properly to prevent errors.

```python
from twitch import Client
from twitch.ext.oauth import DeviceAuthFlow, Scopes

client = Client(client_id='...')

DeviceAuthFlow(client=client, scopes=[Scopes.USER_READ_EMAIL])
```

### Getting Device Code

Start the device authentication flow and get the device code.

```python
@client.event
async def on_code(code: str):
    print(f'Verification URI: https://www.twitch.tv/activate?device-code={code}')
```

### Receiving Tokens

Check if the user has authorized your application and retrieve the access and refresh tokens.

```python
@client.event
async def on_auth(access_token: str, refresh_token: str):
    """
    Handles the authentication event.
    """
    print(f'access_token={access_token}\nrefresh_token={refresh_token}')
```

### Revoking a Token

Revoke an access token or refresh token.

```python
await auth.revoke_token('your_token')
```

## Examples

=== "Basic"

    Here's a basic example demonstrating how to use `DeviceAuthFlow` to authenticate and start the Twitch client.
    from twitch.ext.oauth import DeviceAuthFlow, Scopes
    from twitch import Client

    ```python
    from twitch.ext.oauth import DeviceAuthFlow, Scopes
    from twitch import Client
    
    client = Client(client_id='YOUR_CLIENT_ID')
    
    DeviceAuthFlow(
        client=client,
        scopes=[Scopes.USER_READ_EMAIL]
    )
    
    @client.event
    async def on_code(code: str):
        """
        Handles the device authorization code event.
        """
        print(f'Verification URI: https://www.twitch.tv/activate?device-code={code}')
    
    @client.event
    async def on_auth(access_token: str, refresh_token: str):
        """
        Handles the authentication event.
        """
        print(f'access_token={access_token}\nrefresh_token={refresh_token}')
    
    @client.event
    async def on_ready():
        """
        Handles the client ready event.
        """
        print('PogU')
    
    # Start the client and begin processing events.
    client.run()
    ```

=== "Advanced"

    This advanced example provides greater control over the `DeviceAuthFlow` process,
    including custom handling for device code retrieval and token management.

    ```python
    from twitch.ext.oauth import DeviceAuthFlow, Scopes
    from twitch.types import eventsub
    from twitch import Client
    import asyncio
    
    
    class Twitch(Client):
        def __init__(self, client_id: str, **options):
            super().__init__(client_id, **options)
            self.auth_flow = DeviceAuthFlow(
                self,
                scopes=[Scopes.USER_READ_EMAIL, Scopes.MODERATOR_READ_FOLLOWERS],
                wrap_run=False
            )
    
        async def on_ready(self):
            """
            Notify when the bot is ready.
            """
            print('Client is ready!')
    
        async def on_follow(self, data: eventsub.channels.FollowEvent):
            """
            Handle new follower events.
            """
            await self.channel.chat.send_message(f'{data["user_name"]} has followed the channel!')
    
        async def custom_auth_flow(self):
            """
            Custom method to manage device authentication flow.
            """
            async with self.auth_flow:
                # Retrieve device code and display the verification URL
                user_code, device_code, expires_in, interval = await self.auth_flow.get_device_code()
                print(f'Verification URI: https://www.twitch.tv/activate?device-code={device_code}')
    
                # Poll for the authorization and handle token retrieval
                try:
                    access_token, refresh_token = await self.auth_flow.poll_for_authorization(device_code,
                                                                                              expires_in,
                                                                                              interval)
                    print(f'Access Token: {access_token}\nRefresh Token: {refresh_token}')
                except Exception as e:
                    print(f'Failed to authorize: {e}')
                    return
    
            # Start the client with the obtained tokens
            async with self:
                await self.start(access_token, refresh_token)
    
        async def run_bot(self):
            """
            Run the bot with full control over device authentication and event handling.
            """
            await self.custom_auth_flow()
    
    
    # Initialize and run the bot
    bot = Twitch(client_id='YOUR_CLIENT_ID')
    asyncio.run(bot.run_bot())
    ```