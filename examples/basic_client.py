from twitch.ext.oauth import DeviceAuthFlow, Scopes
from twitch.types import eventsub
from twitch import Client

client = Client(client_id='YOUR_CLIENT_ID')

# Setup Device Authentication Flow with necessary scopes.
# This is required for obtaining user-specific access tokens.
DeviceAuthFlow(
    client=client,
    scopes=[Scopes.USER_READ_EMAIL, Scopes.USER_READ_CHAT, Scopes.USER_WRITE_CHAT]
)


@client.event
async def on_code(code: str):
    """Handles the device authorization code event."""
    print(f'Verification URI: https://www.twitch.tv/activate?device-code={code}')


@client.event
async def on_auth(access_token: str, refresh_token: str):
    """Handles the authentication event."""
    print(f'access_token={access_token}\nrefresh_token={refresh_token}')


@client.event
async def on_ready():
    """Handles the client ready event."""
    print('PogU')


@client.event
async def on_chat_message(data: eventsub.chat.MessageEvent):
    """Handles chat messages and responds to giveaway commands."""
    if data['message']['text'].startswith('!ping'):
        await client.channel.chat.send_message('Pong', data['message_id'])

# Start the client and begin processing events.
# This method should be called to start the event loop and handle incoming events.
client.run()
