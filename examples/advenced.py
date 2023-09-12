from twitch import Client, Cheerer


class User(Client):
    def __init__(self):
        super().__init__(client_id='CLIENT ID HERE',
                         client_secret='CLIENT SECRET HERE')

    async def on_connect(self):
        """
        This called when the Twitch client is ready to receive events.
        """
        print(f'Connected as {self.user.name} ID: {self.user.id}')

    async def on_ready(self):
        """
        This called when the Twitch client is ready to receive events.
        """
        print(f'Ready as {self.user.display_name}')

    async def on_auth_url(self, url: str, uri: str):
        """
        This called when the authentication URL is generated.
        """
        print('Auth url:', url)
        print('Redirect url:', uri)

    async def on_auth(self, access_token: str, refresh_token: str):
        """
        This called when the client is successfully authenticated.
        """
        # Store those for future use.
        print('Received access token:', access_token)
        print('Received refresh token:', refresh_token)

    async def on_cheer(self, cheerer: Cheerer):
        """
        This called when a user sends a cheer to the channel.
        """
        print(f'{cheerer.display_name} just cheered {cheerer.bits} bits!')

    async def on_refresh_token(self, access_token: str):
        """
        This called when a new access token has been generated.
        """
        # Store this access_token for future use.
        print('Received a new access token:', access_token)


client = User()
client.run()
