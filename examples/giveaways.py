from twitch.types import eventsub
from twitch import Client
from random import choice


class GiveawaysBot(Client):
    def __init__(self, client_id: str, **options):
        super().__init__(client_id, **options)
        self._is_giveaway_on = False
        self._users = []

    @staticmethod
    async def on_ready():
        """
        Called when the bot is ready and connected to Twitch.
        """
        print('Bot is ready!')

    async def on_chat_message(self, data: eventsub.chat.MessageEvent):
        """
        Handles chat messages and responds to giveaway commands.
        """
        # Handle the "!join" command
        message_text = data['message']['text']

        # Handle the "!join" command
        if message_text.startswith('!join'):
            await self.join(data['chatter_user_name'], data['message_id'])
            return

        # Check if the message sender is a moderator or broadcaster
        if any(badge['set_id'] in {'moderator', 'broadcaster'} for badge in data['badges']):
            if message_text.startswith('!start'):
                await self.start_giveaway()
                return

            # Handle commands if a giveaway is ongoing
            if self._is_giveaway_on:
                if message_text.startswith('!end'):
                    await self.end_giveaway()
                    return

                if message_text.startswith('!total'):
                    await self.channel.chat.send_message('%s chatters have entered the giveaway!' % len(self._users))
                    return

                if message_text.startswith('!cancel'):
                    await self.channel.chat.send_message('Giveaway has been canceled.')
                    self.clear_giveaway()
                    return

            if (not self._is_giveaway_on) and data['message']['text'].startswith(('!end', '!total')):
                await self.channel.chat.send_message('There is no active giveaway.')

    def clear_giveaway(self):
        """
        Clears the giveaway state, resetting the user list and ending the giveaway.
        """
        self._users.clear()
        self._is_giveaway_on = False

    async def join(self, name: str, message_id: str):
        """
        Adds a user to the giveaway if they haven't already joined.
        """
        if name not in self._users:
            self._users.append(name)
        else:
            await self.channel.chat.send_message('You have already joined!', message_id)

    async def start_giveaway(self):
        """
        Starts the giveaway if one is not already in progress.
        """
        if self._is_giveaway_on:
            await self.channel.chat.send_message('The giveaway is already running! Type !end to stop it.')
        else:
            self._is_giveaway_on = True
            await self.channel.chat.send_message('The giveaway has started! Type !join to enter BopBop')

    async def end_giveaway(self):
        """
        Ends the giveaway and announces the winner, if there are participants.
        """
        if len(self._users) >= 1:
            winner = choice(self._users)
            await self.channel.chat.send_message('@%s has won the giveaway! Congratulations! Pog' % winner)
        else:
            await self.channel.chat.send_message('It seems like no one participated in the giveaway. D:')
        self.clear_giveaway()


bot = GiveawaysBot(client_id='YOUR_CLIENT_ID')
bot.run(access_token='YOUR_USER_ACCESS_TOKEN')
