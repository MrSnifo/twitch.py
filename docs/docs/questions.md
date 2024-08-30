---
icon: octicons/question-16
search:
  exclude: true
---

### Why Twitchify?
Why not? Twitchify is all about making Twitch interactions smooth and fun, 
without drowning you in Pythonese. It’s designed for those who want things easy and efficient.

### Is Twitchify compatible with the latest Twitch API?
Twitchify stays up-to-date with the Twitch API. If Twitch adds new features,
we’re right there making sure Twitchify doesn’t miss out on the fun.

### How can I contribute to Twitchify?
We love company! You can contribute by reporting bugs, suggesting cool new features, or even sending us a pull request,
or even [more](https://github.com/MrSniFo/Twitchify/blob/main/.github/CONTRIBUTING.md).

### How do I report a bug or issue?
Found a bug? Don’t worry, we’re not bugged out. Just head over to our GitHub issues page and let us know.

### Can I use Twitchify for commercial purposes?
Absolutely! Use it for personal projects, big business, or even that wild startup idea you’ve got.
Just remember, it’s MIT-licensed, so play nice!

### How can I get support for Twitchify?
For assistance, feel free to mention @Snifo in the #general-python channel
on the [Twitch API Discord](https://discord.gg/8NXaEyV).

### Are there any known limitations or issues with Twitchify?
Twitchify is pretty solid, I'm always working on improvements.

### Does Twitchify comply with Twitch’s rules?
Absolutely! Twitchify follows Twitch's rules. And every access token is validated every 55 minutes.

### What is the Difference Between Client and Bot?
Difference between a Client and a Bot:

- **Client**: The Client represents both the application and the Twitch user associated with it.
Essentially, the Client is a mix of the app and its user.

- **Bot**: The Bot extends the functionality of the Client. It allows you to register access tokens of different users.


### Can You Scale Twitchify?
Currently, scaling Twitchify directly isn't possible, but it's possible with
[Conduits](https://dev.twitch.tv/docs/eventsub/handling-conduit-events/) for advanced scalability. 
Conduits offer scalability options but can be complex unless Twitch improves them as suggested 
[here](https://twitch.uservoice.com/forums/310213-developers/suggestions/48773702-metadata-and-ordering-features-for-conduits). 

Conduits help bypass WebSocket limitations, allowing for more subscriptions and new event types. However,
the current Conduit setup does not integrate with Twitchify.

### What are the system requirements for using Twitchify?
Twitchify’s requirements are pretty chill: Python 3.8 or later.
