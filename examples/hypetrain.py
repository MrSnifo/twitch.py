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
