from twitch import Client, Prediction

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
async def on_auth_url(url: str, uri: str):
    """
    This function is called when the authentication URL is generated.
    """
    # Note: The URL is already logged by the client, but you can collect the URL
    # and perhaps send it to a webhook URL
    # so that users can authenticate without needing to check the console logs.
    print(f'Authenticate using this URL: {url}')

@client.event
async def on_auth(access_token: str, refresh_token: str):
    """
    This function is called when the client is successfully authenticated.
    """
    # Note: You can send a message to the user indicating that authentication was successful.
    # Tip: You should store the refresh_token and access_token so you don't need
    # to repeat this process every time.
    print('Successfully authenticated')

# Without adding specific scopes, all of them will be added by default.
# Alternatively, you can refer to the documentation for the scopes that are relevant to your needs.
client.run(scopes=['channel:read:predictions'])
