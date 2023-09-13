from twitch import Client, Follow

client = Client(
    client_id='CLIENT ID HERE',
    client_secret='CLIENT SECRET HERE'
)

@client.event
async def on_ready():
    """
    This called when the Twitch client is ready to receive events.
    """
    print(f"Ready as {client.user.display_name}")


@client.event
async def on_refresh_token(access_token: str):
    """
    This called when a new access token has been generated.
    """
    # Store this access_token for future use.
    print("Received a new access token:", access_token)


@client.event
async def on_follow(user: Follow):
    """
    This called when a user follows the channel.
    """
    print("%s just followed you!" % user.display_name)

# For authorization, you can choose one of the following methods:

# Method 1: Using access_token and refresh_token
# Replace with your actual access token and refresh token
client.run(access_token="YOUR_ACCESS_TOKEN", refresh_token="YOUR_REFRESH_TOKEN")

# Method 2: You can simply use this method for mainly authentication (scopes are optional)
# client.run(scopes=['moderator:read:followers'])
