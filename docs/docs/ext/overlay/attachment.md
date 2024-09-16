---
icon: material/attachment
hide:  
  - toc  
---

# Attachment Management in Overlay

Attachments like images and audio files are managed locally and loaded into memory
for ease of use. This approach simplifies the process of integrating local assets into your alerts.

## Managing Attachments
___

### Adding Attachments

Use the `add_attachment` method to load a file into memory. This makes it available for use in alerts.

```python
self.overlay.add_attachment('myimage', 'static/image.png')
self.overlay.add_attachment('mymusic', 'static/music.mp3')
```

- `'myimage'` and `'mymusic'` are names for the attachments.
- `'static/image.png'` and `'static/music.mp3'` are file paths.

### Removing Attachments

To remove a file from memory, use the `remove_attachment` method.

```python
self.overlay.remove_attachment('myimage')
```

### Clearing All Attachments

Use `clear_attachments` to remove all attachments from memory.

```python
self.overlay.clear_attachments()
```

## Example Usage

```python
async def setup_hook(self) -> None:
    # Add attachments
    self.overlay.add_attachment('myimage', 'static/image.png')
    self.overlay.add_attachment('mymusic', 'static/music.mp3')
    
    # Start the server
    await self.overlay.start_app()

    
async def on_follow(self, data: eventsub.channels.FollowEvent):
    await self.overlay.alert(f'PogU', image='myimage', audio='mymusic')
```
