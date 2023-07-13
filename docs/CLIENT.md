# Twitchify Documentation

## Client
Represents the Twitch Client.

### Attributes
- `user`: Retrieves the [Broadcaster](#Broadcaster).
- `def auth() -> Auth`: [Authorizes](#Auth) your app without the need for third-party apps.
- `async def get_channel() -> Channel`: Retrieves the [Channel](#Channel) associated with the broadcaster.
- `async def get_stream() -> Optional[Stream]`: Retrieves the [Stream](#Stream) of the broadcaster if currently live.
- `async def start()`: Starts the client by establishing a connection and initiating the event loop.
- `def run()`: Runs the Client without establishing an event loop.
---

## Broadcaster
Represents a Twitch Broadcaster.

### Attributes
- `id: str`: The ID of the broadcaster.
- `name: str`: The username of the broadcaster.
- `display_name: str`: The display name of the broadcaster.
- `email: Optional[str]`: The email address of the broadcaster (optional).
- `images: Images`: An instance of the [Images](#Images) representing the images associated with the broadcaster.
- `tier: Tier`: The broadcaster tier.
- `type: Types`: The user type.
- `joined_at: datetime`: The timestamp when the broadcaster joined.
- `description: Optional[str]`: The description of the broadcaster (optional).

### Methods
- `async def get_channel() -> Channel`: Retrieve the channel associated with the broadcaster.
- `async def get_stream() -> Optional[Stream]`: Retrieve the stream of the broadcaster if currently live.

---

## Images
Images associated with a Twitch User.

### Attributes
- `profile: str`: The URL of the user's profile image.
- `offline: str`: The URL of the user's offline image.

---

## Channel
Represents a Twitch Channel.

### Attributes
- `title: Optional[str]`: The title of the channel.
- `description: Optional[str]`: The description of the channel.
- `delay: int`: The delay of the channel in seconds.
- `tags: List[str]`: The tags associated with the channel.
- `category: Optional[Category]`: The [Category](#Category) of the channel, if available.
- `classification: List[str]`: Classification currently applied to the channel.
- `is_branded_content: bool`: Indicates if the channel has branded content.

---

## Category
Represents a Category for a channel.

### Attributes
- `id: str`: The category ID.
- `name: str`: The category name.

---

## Stream
Represents a Twitch Stream.

### Attributes
- `id: str`: The stream ID.
- `language: str`: The language used in the stream.
- `viewers: int`: The number of users watching the stream.
- `thumbnail_url: str`: A URL to an image of a frame from the last 5 minutes of the stream.
- `is_mature: bool`: Indicates if the stream is for mature audiences.
- `started_at: datetime`: The date and time when the broadcast began.

---

## Auth
Represents Twitch Authorization.

### Attributes
- `access_token: Optional[str]`: User access token.
- `refresh_token: Optional[str]`: User refresh token.
- `scopes: List[str]`: Access Token Scopes.
- `url: str`: Authorization URL.
- `uri: str`: The URI of the server.