from twitch.types import eventsub
from twitch import Client

client = Client(client_id='YOUR_CLIENT_ID')

total_followers = 0


@client.event
async def on_ready():
    """
    Handles the client ready event.

    Updates the total followers count when the client is ready.
    """
    global total_followers
    # Retrieve the total number of followers for the channel.
    total_followers = await client.channel.get_total_followers()
    print('PogU')


@client.event
async def on_follow(data: eventsub.channels.FollowEvent):
    """
    Handles the follow event.
    """
    global total_followers
    # Increment the follower count
    total_followers += 1

    # Send a message to the channel chat announcing the new follower.
    await client.channel.chat.send_message(f'{data["user_name"]} has followed the channel!, '
                                           f'Its {total_followers} juicers now! DinoDance')


client.run('YOUR_USER_ACCESS_TOKEN')
