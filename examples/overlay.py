from twitch.ext.overlay import Overlay
from twitch.types import eventsub
from twitch import Client


class Twitch(Client):
    def __init__(self, client_id: str, client_secret: str, **options):
        super().__init__(client_id, client_secret, **options)
        self.overlay = Overlay(self)

    async def setup_hook(self) -> None:
        """Called when the client is setting up"""
        await self.overlay.start_app()

    async def on_ready(self):
        """Called when the client is ready."""
        print('Bot is ready!')

    async def on_overlay_ready(self):
        """Called when the overlay is ready."""
        # Link it to your OBS.
        print('Overlay URL: ', self.overlay.url('follow'))

    async def on_follow(self, data: eventsub.channels.FollowEvent):
        """Handles follow events."""
        await self.overlay.alert(
            f'<<{data["user_name"]}>> just followed!',
            font_size=64,
            default='follow'
        )


client = Twitch('YOUR_CLIENT_ID', 'YOUR_CLIENT_SECRET')
client.run('YOUR_ACCESS_TOKEN')
