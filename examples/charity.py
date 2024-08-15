from twitch.types import eventsub
from twitch import Client

client = Client(client_id='YOUR_CLIENT_ID')


@client.event
async def on_ready():
    """
    Triggered when the client is successfully connected and ready to interact with Twitch.
    """
    print('PogU')


@client.event
async def on_charity_campaign_start(data: eventsub.activity.CharityCampaignStartEvent):
    """
    Triggered when a charity campaign starts.
    """
    await client.channel.chat.send_message('A new Charity Campaign has just started! Let\'s make a difference!')


@client.event
async def on_charity_campaign_progress(data: eventsub.activity.CharityCampaignProgressEvent):
    """
    Triggered when there is an update on the progress of an ongoing charity campaign.
    """
    await client.channel.chat.send_message(
        f'We’ve raised ${data["current_amount"]} so far in our Charity Campaign! Keep it up!')


@client.event
async def on_charity_campaign_stop(data: eventsub.activity.CharityCampaignStopEvent):
    """
    Triggered when a charity campaign ends.
    """
    await client.channel.chat.send_message(f'The Charity Campaign has ended! We raised a '
                                           f'total of ${data["current_amount"]}!'
                                           f' Thank you all for your support! 🎉')


@client.event
async def on_charity_campaign_donate(data: eventsub.activity.CharityDonationEvent):
    """
    Triggered when a donation is made to an ongoing charity campaign.
    """
    await client.channel.chat.send_message(f'{data["user_login"]} has generously donated'
                                           f' to the charity! Thank you! 👏🎉')


client.run('YOUR_USER_ACCESS_TOKEN')
