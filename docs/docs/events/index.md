---
icon: material/information-slab-circle
hide:
  - toc
---

# Introduction
___

Welcome to the wild world of Twitch EventSub! Imagine it as your backstage pass to all the Twitch drama and excitement,
where you can get live updates faster than you can say "PogChamp!" Just a heads-up,
keeping up with all the action might come with a cost, but it’s totally worth it for staying in the loop!

### Default Client Events
___

The following events are included by default to keep the client updated in real time. While these events 
do not require separate function definitions, you can add custom handlers if needed:

- **`channel_update`**: Triggered when a channel is updated.
- **`user_update`**: Triggered when a user’s profile is updated.
- **`stream_online`**: Triggered when a stream goes online.
- **`stream_offline`**: Triggered when a stream goes offline.

You may add custom handlers for these events to perform specific actions in response.

### Return Full Event Data 
___

When you need **full event data**, You can enable it by setting the `return_full_data` flag to `True`.
This will ensure that all event data such as metadata and payload gets returned,
and make sure to wrap it into [`MPData`][twitch.types.eventsub.MPData].

Here’s how you can use it:

```python
from twitch.types import eventsub
from twitch import Client

# Initialize the client with full data enabled
client = Client(..., ..., return_full_data=True)

@client.event
async def on_chat_message(data: eventsub.MPData[eventsub.chat.MessageEvent]):
    print(data)

client.run(...)
```

### Subscription Limits
___

EventSub uses a cost-based system to manage subscription limits. Here's how it works:

- You can have up to **3 subscriptions** with identical type and condition values.
- **No cost** is incurred for subscriptions requiring user authorization (e.g., `channel.subscribe`).
- **Costs apply** to subscriptions specifying a user but not requiring user authorization 
(e.g., `stream.online`, `channel.update`).


To monitor and manage your subscription expenses, use the 
[max_subscription_cost][twitch.client.Client.max_subscription_cost] and
[total_subscription_cost][twitch.client.Client.total_subscription_cost]
properties. These will help you stay within your budget and keep track of your subscription limits.
