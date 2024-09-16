---
icon: material/information-slab-circle
hide:
  - toc
---

# Introduction

## Overview
___

The `Overlay` class enables you to integrate dynamic overlays into your stream, allowing you to display customized alerts and messages in response to various Twitch events.

![overlay example](obs-alert.gif)

## Features

### Overlay Management
- **Dynamic Alerts**: Show and customize alerts for different Twitch events.
- **Customization**: Tailor alerts with text, images, and fonts to fit your stream’s branding.

### Custom Alerts
- **Text and Images**: Include custom text and images in your alerts, with options for highlighting and animations.
- **Animation Support**: Use animations from [Animate.css](https://animate.style/) to add visual effects to your alerts.

## Basic Usage

### Initialization

Set up the `Twitch` client and initialize the `Overlay` class.

```python
from twitch.ext.overlay import Overlay
from twitch import Client

class Twitch(Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.overlay = Overlay(self)
        
    async def setup_hook(self) -> None:
        await self.overlay.start_app()

client = Twitch('YOUR_CLIENT_ID', 'YOUR_CLIENT_SECRET')
client.run('YOUR_ACCESS_TOKEN')
```

### Send Alerts Anywhere

Define event handlers to send alerts.

```python
async def on_ready(self):
    print('Bot is ready!')

async def on_overlay_ready(self):
    # Get URL for the follow overlay
    print('Overlay URL: ', self.overlay.url('follow'))

async def on_follow(self, data: eventsub.channels.FollowEvent):
    # Send an alert to the 'follow' overlay
    await self.overlay.alert(f'<<{data["user_name"]}>> just followed!',
                             font_size=64,
                             default='follow')
```