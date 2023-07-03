``## Client
Represents the Twitch client
### Attributes
- `user`: retrieves the [Broadcaster](#Broadcaster)
- `async get_channel()`: Retrieves the [Channel](#Channel) associated with the broadcaster
- `async get_stream()`: Retrieve the [Stream](#Stream) of the broadcaster **if currently live**.
- `async start()`:  Starts the client by establishing a connection and initiating the event loop.
- `run()`: Runs the Client without establishing an event loop.


---
### Broadcaster
Represents a Twitch broadcaster

##### Attributes
- `id: str`: The ID of the broadcaster.
- `name: str`: The username of the broadcaster.
- `display_name: str`: The display name of the broadcaster.
- `email: Optional[str]`: The email address of the broadcaster (optional).
- `images: Images`: An instance of the [Images](#Images) representing the images associated with the broadcaster.
- `tier: Tier`: The broadcaster tier.
- `type: Types`: The user type.
- `joined_at: datetime`: The timestamp when the broadcaster joined.
- `description`: The description of the broadcaster (optional).

####  `async` `get_channel(self) -> Channel`

Retrieve the channel associated with the broadcaster.
- Returns: An instance of the [Channel](#channel) class representing the channel.

####  `async` `get_stream(self) -> Optional[Stream]`

Retrieve the stream of the broadcaster if currently live.
- Returns: An instance of the [Stream](#Stream) class representing the stream if live, otherwise `None`.

##### Caching Timeout
Both the `get_channel` and `get_stream` methods are decorated with a caching mechanism. The cache timeout for `get_channel` is **14 seconds**, while the cache timeout for `get_stream` is **8 seconds**. This means that once the channel or stream data is fetched, it will be cached for the specified timeout period before making another request to the Twitch API. This helps to reduce the number of API calls and improve performance.

---

### Images
Images associated with a Twitch user.

##### Attributes
- `profile: str`: The URL of the user's profile image.
- `offline: str`: The URL of the user's offline image.
  
---

### Channel
Represents a Twitch channel.

### Attributes
- `title: Optional[str]`: The title of the channel.
- `description: Optional[str]`: The description of the channel.
- `delay: int`: The delay of the channel in seconds.
- `tags: List[str]`: The tags associated with the channel.
- `category: Optional[Category]`: The [Category](#category) of the channel, if available.

---

#### Category
Represents a category for a channel.

### Attributes
- `id: str`: Category ID.
- `name: str`: Category name.

---

### Stream
Represents a twitch stream.

### Attributes
- `id: str`: The stream ID.
- `language: str`: The language that the stream uses.
- `viewers: int`: The number of users watching the stream.
- `thumbnail_url: str`: A URL to an image of a frame from the last 5 minutes of the stream
- `is_mature: bool` whether the stream is meant for mature audiences
- `started_at: datetime` = The date and time of when the broadcast began.
