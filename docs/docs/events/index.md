---
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

### Custom Events
___

You have the ability to add and remove custom event subscriptions using the client. Here’s how you can manage them:

- **[Adding Custom Events][twitch.client.Client.add_custom_event]**: Register a callback function for a 
custom event and user. This allows you to define how the client should handle specific custom events.

- **[Removing Custom Events][twitch.client.Client.remove_custom_event]**: Unsubscribe a user from a custom event.
This stops the client from triggering the callback function for that event.

Note: Client Events are not included (e.g., on_ready… etc.).

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
