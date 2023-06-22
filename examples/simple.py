from twitch import Client
from twitch.user import Follower

# Create a Twitch client
client = Client(
    client_id='CLIENT ID HERE',
    client_secret='CLIENT SECRET HERE'
)


@client.event
async def on_connect():
    """
    Event handler triggered when the client successfully connected to the eventsub websocket.
    """
    print('Connected to the Websocket!')


@client.event
async def on_ready():
    """
    Event handler triggered when the client is ready to start processing events.
    """
    print(f"Ready as {client.user.display_name}")


@client.event
async def on_refresh_token(access_token: str):
    """
    Event handler triggered when the client receives a new access token.

    Note:
        The refresh_token and client_secret are required for the on_refresh_token event to trigger.
    """
    # Store this access_token for future use.
    print("Received a new access token:", access_token)


@client.event
async def on_follow(user: Follower):
    """
    Event handler triggered when a user follows the channel.
    """
    print(f'{user.display_name} just followed you!')


client.run(
    access_token='USER ACCESS TOKEN HERE',
    refresh_token='USER REFRESH TOKEN HERE')
