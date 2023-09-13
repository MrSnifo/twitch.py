---
hide:
  - toc
search:
  exclude: true
---
  
???+ quote addressing Data Handling and Cache Challenges
    When managing data updates, deletions, or patches followed by retrieval across endpoints,
    it's crucial to consider interactions with diverse cache servers. Some of these servers may lack
    asynchronous functionality, leading to intermittent data inconsistencies. Solely relying on local
    caching doesn't adequately mitigate these issues, especially in scenarios involving client restarts
    or updates from sources like twitch.tv.

    Despite implementing a caching solution, it's vital to acknowledge its limitations. Notably,
    this solution might not cover all endpoints, and a more pressing concern arises when clients restart,
    resulting in the loss of cached data.

## Basic

!!! warning
    The provided code is missing the app client secret and user refresh token. Without these components,
    the access token won't be able to regenerate when it expires.

```python
from twitch import Client
from twitch.users import Follower

client = Client(client_id="YOUR_CLIENT_ID")


@client.event
async def on_ready():
    """
    This called when the Twitch client is ready to receive events.
    """
    print("Ready as %s" % client.user.display_name)


@client.event
async def on_follow(user: Follower):
    """
    This called when a user follows the channel.
    """
    print("%s just followed you!" % user.display_name)


# Run the client using your user access token.
client.run(access_token="YOUR_ACCESS_TOKEN")
```

## With Built-in Authentication

Twitchify simplifies the setup by allowing you to authenticate (1) without the need for third-party
apps to collect the tokens. However, you should complete the required steps in the [setup](setup.md).
{ .annotate }

1. Using authorization code grant flow (1)
    { .annotate }

    1. This flow is meant for apps that use a server, can securely store a client secret, and can make server-to-server requests to the Twitch API. To get a user access token using the authorization code grant flow, your app must Get the user to authorize your app and then Use the authorization code to get a token. [readmore](https://dev.twitch.tv/docs/authentication/getting-tokens-oauth/#authorization-code-grant-flow)

???+ tip
    After authentication, make sure to store the received tokens `access_token` and `refresh_token`
    for future use. Storing these tokens eliminates the need for reauthorization.

```python
from twitch import Client, Follower

client = Client(client_id="YOUR_CLIENT_ID", client_secret="YOUR_CLIENT_SECRET")

@client.event
async def on_ready():
    """
    This called when the Twitch client is ready to receive events.
    """
    print("Ready as %s" % client.user.display_name)
    
@client.event
async def on_follow(user: Follower):
    """
    This called when a user follows the channel.
    """
    print("%s just followed you!" % user.display_name)
    
@client.event
async def on_auth(access_token: str, refresh_token: str):
    """
    This called when the client is successfully authenticated.
    """
    print("Received access token:", access_token)
    print("Received refresh token:", refresh_token)
    
# User should visit the provided URL to authenticate.
client.run()
```

Remember, if you want to add more events,
go to the [references](http://127.0.0.1:8000/reference/event-reference/) section and make sure to register
the events using [client.event()](http://127.0.0.1:8000/reference/client/#twitch.client.Client.event).