---
icon: octicons/question-16
search:
  exclude: true
---

### Why twitch.py?
Why not? twitch.py is all about making Twitch interactions smooth and fun, 
without drowning you in Pythonese. It’s designed for those who want things easy and efficient.

### Is twitch.py compatible with the latest Twitch API?
twitch.py stays up-to-date with the Twitch API. If Twitch adds new features,
we’re right there making sure twitch.py doesn’t miss out on the fun.

### How can I contribute to twitch.py?
We love company! You can contribute by reporting bugs, suggesting cool new features, or even sending us a pull request,
or even [more](https://github.com/MrSniFo/twitch.py/blob/main/.github/CONTRIBUTING.md).

### How do I report a bug or issue?
Found a bug? Don’t worry, we’re not bugged out. Just head over to our GitHub issues page and let us know.

### Can I use twitch.py for commercial purposes?
Absolutely! Use it for personal projects, big business, or even that wild startup idea you’ve got.
Just remember, it’s MIT-licensed, so play nice!

### How can I get support for twitch.py?
For assistance, feel free to mention @Snifo in the #general-python channel
on the [Twitch API Discord](https://discord.gg/8NXaEyV).

### Are there any known limitations or issues with twitch.py?
twitch.py is pretty solid, I'm always working on improvements.

### Does twitch.py comply with Twitch’s rules?
Absolutely! twitch.py follows Twitch's rules. And every access token is validated every 55 minutes.

### What is the Difference Between Client and Bot?
Difference between a Client and a Bot:

- **Client**: The Client represents both the application and the Twitch user associated with it.
Essentially, the Client is a mix of the app and its user.

- **Bot**: The Bot extends the functionality of the Client. It allows you to register access tokens of different users.


### Can You Scale twitch.py?
Currently, scaling twitch.py directly isn't possible, but it's possible with
[Conduits](https://dev.twitch.tv/docs/eventsub/handling-conduit-events/) for advanced scalability. 
Conduits offer scalability options but can be complex unless Twitch improves them as suggested 
[here](https://twitch.uservoice.com/forums/310213-developers/suggestions/48773702-metadata-and-ordering-features-for-conduits).

Conduits help bypass WebSocket limitations, allowing for more subscriptions and new event types. However,
the current Conduit setup does not integrate with twitch.py.

#### Future of Scaling
In most cases, the bot extension will be able to provide scalable solutions by registering 
multiple users. The vanilla WebSocket, however, only supports authentication for a single user,
so scaling isn't necessary in this scenario. With Conduit, however, things change. Essentially,
you have a parent that subscribes to events from multiple users,
and the child connections can be either WebSockets or webhooks.

In this case, Twitch.py uses WebSockets, where each WebSocket operates on a single shard.
With Conduit, all events are distributed to the child connections,
making it possible to scale massively. This setup simplifies creating large bots,
and I’m working to streamline the usability of Twitch.py.

### What are the system requirements for using twitch.py?
twitch.py requirements are pretty chill: Python 3.8 or later.
