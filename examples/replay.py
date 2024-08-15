from twitch.types import eventsub
from twitch import Client
import random

client = Client(client_id='YOUR_CLIENT_ID', client_secret='YOUR_CLIENT_SECRET')


@client.event
async def on_ready():
    """
    Handles the client ready event.
    """
    print('PogU')


@client.event
async def on_chat_message(data: eventsub.chat.MessageEvent):
    """
    Handles chat messages and responds to giveaway commands.
    """

    # replaying to ur self?
    if client.user.id == data['chatter_user_id']:
        return

    message_text = data['message']['text']

    # Handle the "!pog" command.
    if message_text.startswith('!pog'):
        await client.channel.chat.send_message('PogChamp', data['message_id'])
        return

    # Handle the "!random" command to send a random meme from a list.
    elif message_text.startswith('!random'):
        memes = [
            'Pepe is here!',
            'Much wow! Doge says hello!',
            'A cat meme to brighten your day!',
            'SpongeBob is laughing!',
            'Drake gives his approval!',
            'Crying Jordan makes a comeback!'
        ]
        meme_message = random.choice(memes)
        await client.channel.chat.send_message(meme_message, data['message_id'])
        return

client.run('YOUR_USER_ACCESS_TOKEN', 'YOUR_USER_REFRESH_TOKEN')
