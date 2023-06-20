from twitch import Client
from twitch.channel import Cheer


class Twitch(Client):
    def __init__(self):
        super().__init__(client_id="CLIENT ID HERE",
                         client_secret="CLIENT SECRET HERE")

    async def on_connect(self):
        """
        Event handler triggered when the client is connecting.
        """
        print("Connecting...")

    async def on_ready(self):
        """
        Event handler triggered when the client is ready to start processing events.
        """
        print("Ready as %s" % self.user.display_name)

    async def on_refresh_token(self, access_token: str):
        """
        Event handler triggered when the client receives a new access token.

        Note: The refresh_token and client_secret are required for the on_refresh_token event to trigger.
        """
        # Store this access_token for future use.
        print("Received a new access token:", access_token)

    async def on_cheer(self, cheer: Cheer):
        """
        Event handler triggered when a user sends a cheer to the channel.
        """
        print("%s just cheered %s bits!" % cheer.user.display_name, cheer.bits)

    def run_client(self):
        """
        You can import the access token here and use it
        """
        self.run(
            access_token="USER ACCESS TOKEN HERE",
            refresh_token="USER REFRESH TOKEN HERE")


client = Twitch()
client.run_client()
