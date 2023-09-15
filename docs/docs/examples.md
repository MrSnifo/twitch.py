---
search:
  exclude: true
---

### Authentication Code Snippet

```py
# Replace these placeholders with your actual client_id and client_secret.
# Note: The client_secret is required for authentication.
client_id = "YOUR_CLIENT_ID"
client_secret = "YOUR_CLIENT_SECRET"

client = Client(client_id=client_id, client_secret=client_secret)

@client.event
async def on_prediction_begin(prediction: Prediction):
    """
    This called when the prediction is updated or in progress.
    """
    print(f'{prediction.title} just started!.')


@client.event
async def on_auth_url(url, uri):
    """
    This function is called when the authentication URL is generated.
    """
    # Note: The URL is already logged by the client, but you can collect the URL and perhaps send it to a webhook URL
    # so that users can authenticate without needing to check the console logs.
    print(f'Authenticate using this URL: {url}')

@client.event
async def on_auth(access_token, refresh_token):
    """
    This function is called when the client is successfully authenticated.
    """
    # Note: You can send a message to the user indicating that authentication was successful.
    # Tip: You should store the refresh_token and access_token so you don't need to repeat this process every time.
    print('Successfully authenticated')

# Without adding specific scopes, all of them will be added by default.
# Alternatively, you can refer to the documentation for the scopes that are relevant to your needs.
client.run(scopes=['channel:read:predictions'])
```

### Auto VIP and Follow Announcements
```py
from twitch import Client, Gifter, UserRoleConflict, Follow

# Replace with your actual client_id and client_secret
client_id = "YOUR_CLIENT_ID"
client_secret = "YOUR_CLIENT_SECRET"

client = Client(client_id=client_id, client_secret=client_secret)


@client.event
async def on_ready():
     print("Ready as %s" % client.user.display_name)


@client.event
async def on_subscription_gift(gifter: Gifter):
    """
    Automatically grants VIP to a gifter.
    """
    # Checks if the gifter is not anonymous.
    if not gifter.is_anonymous:
        try:
            await client.channel.vips.add(gifter)
            print(f"Granted VIP to {gifter.display_name}.")
        except UserRoleConflict:
            print(f"{gifter.display_name} is a moderator or already a VIP.")
        except Exception as error:
            print(f"An error occurred while processing {gifter.display_name}: {error}")


@client.event
async def on_follow(user: Follow):
    """
    Automatically announces when someone follows the channel.
    """
    announcement = f"{user.display_name} just followed the channel!"
    await client.chat.send_announcement(announcement)
    print(announcement)
    
# For authorization, you can choose one of the following methods:

# Method 1: Using access_token and refresh_token
# Replace with your actual access token and refresh token
access_token = "YOUR_ACCESS_TOKEN"
refresh_token = "YOUR_REFRESH_TOKEN"
client.run(access_token=access_token, refresh_token=refresh_token)

# Method 2: You can simply use this method for mainly authentication (scopes are optional)
# client.run(scopes=['channel:read:subscriptions', 'moderator:read:followers'])
```

### HypeTrain Cheers and Subscriptions Tracking
```py
from twitch import Client, HypeTrain, Gifter, Subscriber, Cheerer


class User(Client):
    def __init__(self):
        super().__init__(client_id='YOUR_CLIENT_ID', client_secret='YOUR_CLIENT_SECRET')
        self.total_subs: int = 0
        self.total_cheers: int = 0

    async def on_cheer(self, cheerer: Cheerer):
        self.total_cheers += cheerer.bits

    async def on_subscribe(self, subscriber: Subscriber):
        self.total_subs += 1

    async def on_resubscribe(self, subscriber: Subscriber):
        self.total_subs += 1

    async def on_subscription_gift(self, gifter: Gifter):
        self.total_subs += gifter.total

    async def on_hype_train_begin(self, train: HypeTrain):
        # Cleaning the data
        self.total_subs = 0
        self.total_cheers = 0

    async def on_hype_train_end(self, train: HypeTrain):
        message = f"Thank you for your contribution! we just raises {self.total_cheers}" \
                  f" bits and {self.total_subs} subs!"
        await self.chat.send_announcement(message)
        # You could give vip to the top contributor!
        # user = await self.get_user(id=train.top_contributions[0].user_id)
        # await client.channel.vips.add(user)


client = User()

access_token = "YOUR_ACCESS_TOKEN"
refresh_token = "YOUR_REFRESH_TOKEN"

client.run(access_token=access_token, refresh_token=refresh_token)
```