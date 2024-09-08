---
icon: material/clock-start
hide:
  - toc
search:
  exclude: true
---

### What is the Difference Between Client and Bot?
Difference between a Client and a Bot:

- **Client**: The Client represents both the application and the Twitch user associated with it.
Essentially, the Client is a mix of the app and its user.

- **Bot**: The Bot extends the functionality of the Client. It allows you to register access tokens of different users.

The tasks that can only be performed by the Client can also be done with the Bot. Additionally,
creating custom events with the Bot **won’t incur extra costs** for registered users.


## Examples

=== "Client"

    !!! warning
        The provided code is missing the app client secret and user refresh token. Without these components,
        the access token won't be able to regenerate when it expires.

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

    ???+ tip
        After authentication, make sure to store the received `access_token` and `refresh_token`
        for future use. Storing these tokens eliminates the need for reauthorization.

    ```python
    from twitch.ext.oauth import DeviceAuthFlow, Scopes
    from twitch.errors import Forbidden
    from twitch.user import Broadcaster
    from twitch.types import eventsub
    from twitch.ext.bot import Bot
    
    client = Bot(client_id='YOUR_CLIENT_ID', client_secret='YOUR_CLIENT_SECRET')
    
    DeviceAuthFlow(
        client=client,
        scopes=[Scopes.USER_READ_EMAIL, Scopes.USER_READ_CHAT, Scopes.USER_WRITE_CHAT, Scopes.USER_MANAGE_WHISPERS]
    )
    
    
    @client.event
    async def on_code(code: str):
        """
        Handles the event when a device authorization code is generated.
        """
        print(f'Verification URI: https://www.twitch.tv/activate?device-code={code}')
    
    
    @client.event
    async def on_auth(access_token: str, refresh_token: str):
        """
        Handles the event after successful authentication, providing access and refresh tokens.
        """
        print(f'access_token={access_token}\nrefresh_token={refresh_token}')
    
    
    @client.event
    async def on_ready():
        """
        Handles the event when the bot is ready and connected to Twitch.
        """
        print('PogU')
    
    
    @client.event
    async def on_user_register(broadcaster: Broadcaster):
        """
        Handles the event when a new user registers as a broadcaster.
        """
        info = await broadcaster.get_info()
        print(info['display_name'], 'has registered!')
        # Additional custom events can be added here for post-registration actions.
    
    
    @client.event
    async def on_chat_message(data: eventsub.chat.MessageEvent):
        """
        Handles chat messages and responds to the !invite command by sending an authorization link.
        """
        if data['message']['text'].startswith('!invite'):
            # Start the device authorization flow
            auth = DeviceAuthFlow(client=client, scopes=[Scopes.USER_READ_EMAIL], dispatch=False)
    
            # Use 'async with' to automatically close the session when done
            async with auth:
                # Get the device code and other details for authorization
                user_code, device_code, expires_in, interval = await auth.get_device_code()
    
                # Fetch the user who sent the invite command
                user = client.get_user_by_id(data['chatter_user_id'])
    
                try:
                    # Send a whisper message with the authorization link
                    await client.user.whisper(
                        user,
                        message=f'Click this link to authorize: https://www.twitch.tv/activate?device-code={user_code} '
                                'Please complete the authorization within a few minutes. Kappa'
                    )
                except Forbidden:
                    # If whisper fails, send a message in the chat
                    await client.channel.chat.send_message(
                        'I couldn\'t send you a whisper. Please check your whisper settings. FailFish',
                        reply_message_id=data['message_id']
                    )
                    return
    
                # Wait for the user to authorize their device
                try:
                    # Set a custom expiration time of 2 minutes
                    expires_in = 120
                    access_token, refresh_token = await auth.poll_for_authorization(device_code, expires_in, interval)
    
                    # Register the user with the retrieved tokens
                    await client.register_user(access_token=access_token, refresh_token=refresh_token)
    
                    # Inform the user they have been successfully authorized
                    await client.user.whisper(user, message='You have been successfully authorized! PogChamp')
    
                except TimeoutError:
                    # If the authorization times out, notify the user
                    await client.user.whisper(user, message='Authorization timed out. Please try again.')
    
    # Start the bot
    client.run()
    ```

For more examples, check out the [examples repository](https://github.com/MrSniFo/twitch.py/tree/main/examples).
Remember, if you want to add more events, visit the [event reference](events/index.md) section.

