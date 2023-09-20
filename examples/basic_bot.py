from twitch import Follow, Message
from twitch.bot import Bot

# Replace with your actual client_id and client_secret
client_id = "YOUR_CLIENT_ID"
client_secret = "YOUR_CLIENT_SECRET"

bot = Bot(
    client_id=client_id,
    client_secret=client_secret
)


@bot.event
async def on_ready():
    """
    This called when the Twitch client is ready to receive events.
    """
    print(f"Ready as {bot.user.display_name}")


@bot.event
async def on_refresh_token(access_token: str):
    """
    This called when a new access token has been generated.
    """
    # Store this access_token for future use.
    print("Received a new access token:", access_token)


@bot.event
async def on_follow(user: Follow):
    """
    This called when a user follows the channel.
    """
    await bot.send(f"{user.display_name} just followed you!")


@bot.event
async def on_auth(access_token: str, refresh_token: str):
    """
    This called when the client is successfully authenticated.
    """
    # Store those for future use.
    print('Successfully authenticated!')


@bot.event
async def on_message(message: Message):
    """
    This called when the bot receives a message from a channel chat room.
    """
    if message.author == bot.user:
        if message.content.startswith('!ping'):
            await bot.replay(message, 'Pong!')
    print(f'{message.author}: {message}')


# You can simply use this method for mainly authentication.
bot.run(scopes=['moderator:read:followers', 'chat:edit'])
