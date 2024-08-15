from twitch.ext.oauth import DeviceAuthFlow, Scopes
from twitch.types import eventsub
from twitch import Client

client = Client(client_id='YOUR_CLIENT_ID')


@client.event
async def on_ready():
    """
    Triggered when the client is fully connected and ready to handle events.

    This function demonstrates adding custom event subscriptions and tracking subscription costs.
    """
    print('PogU')

    # Display the remaining subscription points before adding any custom events.
    print(f'{client.max_subscription_cost - client.total_subscription_cost} points left')

    # self client subscription. This typically has no cost.
    await client.add_custom_event('on_raid', client.user, on_live)

    # Points remain unchanged as subscribing to your own events usually doesn't incur a cost.
    print(f'{client.max_subscription_cost - client.total_subscription_cost} points left after raid subscription')

    # Adding another custom event subscription for a different user.
    user2 = await client.get_user('cricrow')
    await client.add_custom_event('on_stream_online', user2, on_live)

    # Display the remaining subscription points after adding the second event.
    print(f'{client.max_subscription_cost - client.total_subscription_cost} points left after cricrow subscription')

    # Adding a third custom event subscription for another user.
    user3 = await client.get_user('twitch')
    await client.add_custom_event('on_stream_offline', user3, on_live)

    # Display the remaining subscription points after adding the third event.
    print(f'{client.max_subscription_cost - client.total_subscription_cost} points left after twitch subscription')


async def on_live(data: eventsub.streams.StreamOnlineEvent):
    """
    Custom event handler for when a stream goes live.
    """
    print(f'{data["broadcaster_user_name"]} is live!')


async def someone_raided(data: eventsub.streams.RaidEvent):
    """
    Custom event handler for when the client is raided.
    """
    print(f'{data["from_broadcaster_user_name"]} has raided {data["to_broadcaster_user_name"]}')


client.run('YOUR_USER_ACCESS_TOKEN')
