from twitch.ext.oauth import DeviceAuthFlow, Scopes
from twitch.types import eventsub
from twitch import Client
import asyncio


class Twitch(Client):
    def __init__(self, client_id: str, **options):
        super().__init__(client_id, **options)
        self.auth_flow = DeviceAuthFlow(
            self,
            scopes=[Scopes.USER_READ_EMAIL, Scopes.MODERATOR_READ_FOLLOWERS],
            wrap_run=False
        )

    async def on_ready(self):
        """
        Notify when the bot is ready.
        """
        print('Client is ready!')

    async def on_follow(self, data: eventsub.channels.FollowEvent):
        """
        Handle new follower events.
        """
        await self.channel.chat.send_message(f'{data["user_name"]} has followed the channel!')

    async def custom_auth_flow(self):
        """
        Custom method to manage device authentication flow.
        """
        async with self.auth_flow:
            # Retrieve device code and display the verification URL
            user_code, device_code, expires_in, interval = await self.auth_flow.get_device_code()
            print(f'Verification URI: https://www.twitch.tv/activate?device-code={user_code}')

            # Poll for the authorization and handle token retrieval
            try:
                access_token, refresh_token = await self.auth_flow.poll_for_authorization(device_code,
                                                                                          expires_in,
                                                                                          interval)
                print(f'Access Token: {access_token}\nRefresh Token: {refresh_token}')
            except Exception as e:
                print(f'Failed to authorize: {e}')
                return

        # Start the client with the obtained tokens
        async with self:
            await self.start(access_token, refresh_token)

    async def run_bot(self):
        """
        Run the bot with full control over device authentication and event handling.
        """
        await self.custom_auth_flow()


# Initialize and run the bot
bot = Twitch(client_id='YOUR_CLIENT_ID')
asyncio.run(bot.run_bot())
