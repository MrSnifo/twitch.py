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
    """Handles the event when a device authorization code is generated."""
    print(f'Verification URI: https://www.twitch.tv/activate?device-code={code}')


@client.event
async def on_auth(access_token: str, refresh_token: str):
    """Handles the event after successful authentication, providing access and refresh tokens."""
    print(f'access_token={access_token}\nrefresh_token={refresh_token}')


@client.event
async def on_ready():
    """Handles the event when the bot is ready and connected to Twitch."""
    print('PogU')


@client.event
async def on_user_register(broadcaster: Broadcaster):
    """Handles the event when a new user registers as a broadcaster."""
    info = await broadcaster.get_info()
    print(info['display_name'], 'has registered!')


@client.event
async def on_chat_message(data: eventsub.chat.MessageEvent):
    """Handles chat messages and responds to the !invite command by sending an authorization link."""
    if data['message']['text'].startswith('!invite'):
        # Start the device authorization flow
        auth = DeviceAuthFlow(client=client, scopes=[Scopes.USER_READ_EMAIL], dispatch=False)

        # Use 'async with' to automatically close the session when done
        async with auth:
            # Get the device code and other details for authorization
            user_code, device_code, expires_in, interval = await auth.get_device_code()

            user = client.get_user_by_id(data['chatter_user_id'])
            try:
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
