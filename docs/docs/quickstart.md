---
icon: material/clock-start
hide:
  - toc
search:
  exclude: true
---

## Basic Usage

!!! warning
    The provided code is missing the app client secret and user refresh token. Without these components,
    the access token won't be able to regenerate when it expires.

```python
from twitch.types import eventsub
from twitch import Client

client = Client(client_id='YOUR_CLIENT_ID')

@client.event
async def on_ready():
    """
    Handles the client ready event.
    """
    print('PogU')
    
@client.event
async def on_follow(data: eventsub.channels.FollowEvent):
    """
    Handles the follow event.

    Parameters
    ----------
    data: eventsub.channels.FollowEvent
        The event data containing information about the new follower.
    """
    # Send a message to the channel chat announcing the new follower.
    await client.channel.chat.send_message(f'{data["user_name"]} has followed the channel!')

# Start the client and begin processing events.
# This method should be called to start the event loop and handle incoming events.
client.run('YOUR_USER_ACCESS_TOKEN')
```

## OAuth Authentication

Twitchify simplifies the setup by allowing you to authenticate processes.
For more information, see the [OAuth documentation](ext/oauth/index.md).

???+ tip
    After authentication, make sure to store the received `access_token` and `refresh_token`
    for future use. Storing these tokens eliminates the need for reauthorization.

## Examples

=== "Client"

    Here's a basic example with the use `DeviceAuthFlow` to authenticate and start the Twitch client.

    ```python
    from twitch.ext.oauth import DeviceAuthFlow, Scopes
    from twitch.types import eventsub
    from twitch import Client
    
    client = Client(client_id='YOUR_CLIENT_ID')
    
    # Setup Device Authentication Flow with necessary scopes.
    # This is required for obtaining user-specific access tokens.
    DeviceAuthFlow(
        client=client,
        scopes=[Scopes.USER_READ_FOLLOWS]
    )
    
    @client.event
    async def on_code(code: str):
        """
        Handles the device authorization code event.
    
        Parameters
        ----------
        code: str
            The device authorization code sent to the user.
        """
        print(f'Verification URI: https://www.twitch.tv/activate?device-code={code}')
    
    @client.event
    async def on_auth(access_token: str, refresh_token: str):
        """
        Handles the authentication event.
    
        Parameters
        ----------
        access_token: str
            The access token obtained after successful authentication.
        refresh_token: str
            The refresh token used to renew the access token when it expires.
        """
        print(f'access_token={access_token}\nrefresh_token={refresh_token}')
    
    @client.event
    async def on_ready():
        """
        Handles the client ready event.
        """
        print('PogU')
        
    @client.event
    async def on_follow(data: eventsub.channels.FollowEvent):
        """
        Handles the follow event.
    
        Parameters
        ----------
        data: eventsub.channels.FollowEvent
            The event data containing information about the new follower.
        """
        # Send a message to the channel chat announcing the new follower.
        await client.channel.chat.send_message(f'{data["user_name"]} has followed the channel!')
    
    # Start the client and begin processing events.
    # This method should be called to start the event loop and handle incoming events.
    client.run()
    
    ```

=== "Bot"

    This advanced example provides greater control over the `DeviceAuthFlow` process,
    including custom handling for device code retrieval and token management.

    ```python
    
    ```

For more examples, check out the [examples repository](https://github.com/MrSniFo/Twitchify/tree/main/examples).
Remember, if you want to add more events, visit the [event reference](events/index.md) section.