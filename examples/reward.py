from twitch.types import eventsub
from twitch import Client

client = Client(client_id='YOUR_CLIENT_ID')


@client.event
async def on_ready():
    """
    Handles the client ready event.
    """
    print('PogU')  # Client is live and ready to farm PogChamps.


@client.event
async def on_points_reward_redemption_add(data: eventsub.interaction.RewardRedemptionEvent):
    """
    Handles points reward redemption events.

    Automatically gives a VIP or bans the user based on the reward.
    """
    if data['status'] == 'fulfilled':
        await client.channel.chat.send_message(f'{data["user_name"]} has redeemed {data["reward"]["title"]}!')
        user = client.get_user_by_id(data['user_id'])

        # MAXWIN reward, 10 million points?! Someone's been grinding hard.
        if data['reward']['title'] == 'A MAXWIN points reward with 10m points ?':
            await client.channel.add_vip(user)

        # Poof! Someone wants to disappear like a magician.
        if data['reward']['title'] == 'vanish':

            await client.channel.ban(user, duration=10)

client.run('YOUR_USER_ACCESS_TOKEN')
