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
