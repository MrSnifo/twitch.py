---
icon: material/timer-edit
---

# Custom Events
___

The client allows you to add and remove custom event subscriptions, providing flexibility in handling events for specific users. Here’s how to manage custom events:

- **[Adding Custom Events][twitch.client.Client.add_custom_event]**: Register a callback function for a specific custom event and user. This defines how the client should respond to that event.

- **[Removing Custom Events][twitch.client.Client.remove_custom_event]**: Unsubscribe a user from a custom event to stop triggering the callback function for that event.

Events with a scope starting with `moderator:` can be used, but only if you have moderator privileges in the channel.
Almost Without scopes events are accessible, but it’s important to monitor the **[total subscription cost][twitch.client.Client.total_subscription_cost]** to stay within your limit.

#### Example Usage

Here’s an example of how to subscribe to custom events for a user:

```python
@client.event
async def on_ready():
    """Handles the client ready event."""
    print("Client is ready!")

    user = await client.get_user("Snifo")

    await client.add_custom_event("on_follow", user, callback=on_follow_event)
    await client.add_custom_event("on_raid", user, callback=on_raid_event)

    print(f"{client.total_subscription_cost} / {client.max_subscription_cost} points remaining.")

async def on_follow_event(data):
    """Handles the follow event."""
    print("Follow event:", data)

async def on_raid_event(data):
    """Handles the raid event."""
    print("Raid event:", data)
```

Note: Built-in client events (e.g., `on_ready`) are not included in custom event subscriptions.