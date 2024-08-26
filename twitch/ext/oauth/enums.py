"""
The MIT License (MIT)

Copyright (c) 2024-present Snifo

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the 'Software'),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT firstED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NON-INFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""

from enum import Enum

__all__ = ('Scopes',)


class Scopes(str, Enum):
    """
    An enumeration representing the available OAuth scopes.

    Each scope defines a specific permission that an application can request during
    the OAuth authentication process.

    Attributes
    ----------
    ANALYTICS_READ_EXTENSIONS : str
        Allows reading analytics data for extensions owned by the authenticated user.
    ANALYTICS_READ_GAMES : str
        Allows reading analytics data for games owned by the authenticated user.
    BITS_READ : str
        Allows reading information about Bits transactions involving the user.
    CHANNEL_BOT : str
        Grants access to manage and interact with a channel on behalf of the bot.
    CHANNEL_MANAGE_ADS : str
        Allows the application to start and manage ads for the authenticated user's channel.
    CHANNEL_READ_ADS : str
        Allows reading ad information for the authenticated user's channel.
    CHANNEL_MANAGE_BROADCAST : str
        Grants access to manage broadcasts, such as updating titles or categories.
    CHANNEL_READ_CHARITY : str
        Allows reading charity event details for the authenticated channel.
    CHANNEL_EDIT_COMMERCIAL : str
        Allows editing and running commercials on the channel.
    CHANNEL_READ_EDITORS : str
        Grants access to see the list of editors for a channel.
    CHANNEL_MANAGE_EXTENSIONS : str
        Allows management of extensions on the channel.
    CHANNEL_READ_GOALS : str
        Grants access to read goal information for the channel.
    CHANNEL_READ_GUEST_STAR : str
        Allows reading information about Guest Star events.
    CHANNEL_MANAGE_GUEST_STAR : str
        Allows managing Guest Star events for the channel.
    CHANNEL_READ_HYPE_TRAIN : str
        Grants access to read Hype Train events and statistics.
    CHANNEL_MANAGE_MODERATORS : str
        Allows management of moderators on the channel.
    CHANNEL_READ_POLLS : str
        Allows reading poll information for the channel.
    CHANNEL_MANAGE_POLLS : str
        Grants access to create and manage polls on the channel.
    CHANNEL_READ_PREDICTIONS : str
        Allows reading prediction data for the channel.
    CHANNEL_MANAGE_PREDICTIONS : str
        Allows managing predictions on the channel.
    CHANNEL_MANAGE_RAIDS : str
        Grants access to manage raids for the channel.
    CHANNEL_READ_REDEMPTIONS : str
        Allows reading channel point redemptions.
    CHANNEL_MANAGE_REDEMPTIONS : str
        Allows managing channel point redemptions.
    CHANNEL_MANAGE_SCHEDULE : str
        Grants access to manage the schedule of the channel.
    CHANNEL_READ_STREAM_KEY : str
        Allows reading the stream key of the channel.
    CHANNEL_READ_SUBSCRIPTIONS : str
        Allows reading subscription information for the channel.
    CHANNEL_MANAGE_VIDEOS : str
        Grants access to manage videos on the channel.
    CHANNEL_READ_VIPS : str
        Allows reading VIP information for the channel.
    CHANNEL_MANAGE_VIPS : str
        Allows managing VIPs on the channel.
    CLIPS_EDIT : str
        Grants access to edit clips for the channel.
    MODERATION_READ : str
        Allows reading moderation-related information for a channel.
    MODERATOR_MANAGE_ANNOUNCEMENTS : str
        Grants access to manage announcements on the channel.
    MODERATOR_MANAGE_AUTOMOD : str
        Allows managing AutoMod settings for the channel.
    MODERATOR_READ_AUTOMOD_SETTINGS : str
        Allows reading AutoMod settings for the channel.
    MODERATOR_MANAGE_AUTOMOD_SETTINGS : str
        Grants access to manage AutoMod settings for the channel.
    MODERATOR_MANAGE_BANNED_USERS : str
        Allows managing banned users for the channel.
    MODERATOR_READ_BLOCKED_TERMS : str
        Grants access to read blocked terms on the channel.
    MODERATOR_READ_CHAT_MESSAGES : str
        Allows reading chat messages on the channel.
    MODERATOR_MANAGE_BLOCKED_TERMS : str
        Grants access to manage blocked terms for the channel.
    MODERATOR_MANAGE_CHAT_MESSAGES : str
        Allows managing chat messages, including deleting them.
    MODERATOR_READ_CHAT_SETTINGS : str
        Allows reading chat settings for the channel.
    MODERATOR_MANAGE_CHAT_SETTINGS : str
        Grants access to manage chat settings for the channel.
    MODERATOR_READ_CHATTERS : str
        Allows reading the list of chatters in the channel.
    MODERATOR_READ_FOLLOWERS : str
        Grants access to read followers' information on the channel.
    MODERATOR_READ_GUEST_STAR : str
        Allows reading information about Guest Star events.
    MODERATOR_MANAGE_GUEST_STAR : str
        Grants access to manage Guest Star events on the channel.
    MODERATOR_READ_SHIELD_MODE : str
        Allows reading shield mode settings for the channel.
    MODERATOR_MANAGE_SHIELD_MODE : str
        Grants access to manage shield mode settings.
    MODERATOR_READ_SHOUTOUTS : str
        Allows reading shoutout information for the channel.
    MODERATOR_MANAGE_SHOUTOUTS : str
        Grants access to manage shoutouts for the channel.
    MODERATOR_READ_SUSPICIOUS_USERS : str
        Allows reading information about suspicious users in the channel.
    MODERATOR_READ_UNBAN_REQUESTS : str
        Grants access to read unban requests for the channel.
    MODERATOR_MANAGE_UNBAN_REQUESTS : str
        Grants access to manage unban requests for the channel.
    MODERATOR_READ_WARNINGS : str
        Allows reading warning information for the channel.
    MODERATOR_MANAGE_WARNINGS : str
        Grants access to manage warnings for the channel.
    USER_BOT : str
        Grants access to interact with the user's account on behalf of a bot.
    USER_EDIT : str
        Allows editing user details, such as display name or bio.
    USER_EDIT_BROADCAST : str
        Grants access to edit broadcast information for the user.
    USER_READ_BLOCKED_USERS : str
        Allows reading the list of blocked users.
    USER_MANAGE_BLOCKED_USERS : str
        Grants access to manage blocked users.
    USER_READ_BROADCAST : str
        Allows reading broadcast information for the user.
    USER_READ_CHAT : str
        Allows reading chat messages sent by the user.
    USER_MANAGE_CHAT_COLOR : str
        Grants access to manage the chat color for the user.
    USER_READ_EMAIL : str
        Allows reading the user's email address.
    USER_READ_EMOTES : str
        Allows reading the list of emotes for the user.
    USER_READ_FOLLOWS : str
        Grants access to read the list of users followed by the user.
    USER_READ_MODERATED_CHANNELS : str
        Allows reading information about channels moderated by the user.
    USER_READ_SUBSCRIPTIONS : str
        Allows reading subscription information for the user.
    USER_READ_WHISPERS : str
        Grants access to read whispers sent and received by the user.
    USER_MANAGE_WHISPERS : str
        Grants access to manage whispers for the user.
    USER_WRITE_CHAT : str
        Allows sending chat messages on behalf of the user.
    """

    # Analytics
    ANALYTICS_READ_EXTENSIONS = 'analytics:read:extensions'
    ANALYTICS_READ_GAMES = 'analytics:read:games'

    # Bits
    BITS_READ = 'bits:read'

    # Channel
    CHANNEL_BOT = 'channel:bot'
    CHANNEL_MANAGE_ADS = 'channel:manage:ads'
    CHANNEL_READ_ADS = 'channel:read:ads'
    CHANNEL_MANAGE_BROADCAST = 'channel:manage:broadcast'
    CHANNEL_READ_CHARITY = 'channel:read:charity'
    CHANNEL_EDIT_COMMERCIAL = 'channel:edit:commercial'
    CHANNEL_READ_EDITORS = 'channel:read:editors'
    CHANNEL_MANAGE_EXTENSIONS = 'channel:manage:extensions'
    CHANNEL_READ_GOALS = 'channel:read:goals'
    CHANNEL_READ_GUEST_STAR = 'channel:read:guest_star'
    CHANNEL_MANAGE_GUEST_STAR = 'channel:manage:guest_star'
    CHANNEL_READ_HYPE_TRAIN = 'channel:read:hype_train'
    CHANNEL_MANAGE_MODERATORS = 'channel:manage:moderators'
    CHANNEL_READ_POLLS = 'channel:read:polls'
    CHANNEL_MANAGE_POLLS = 'channel:manage:polls'
    CHANNEL_READ_PREDICTIONS = 'channel:read:predictions'
    CHANNEL_MANAGE_PREDICTIONS = 'channel:manage:predictions'
    CHANNEL_MANAGE_RAIDS = 'channel:manage:raids'
    CHANNEL_READ_REDEMPTIONS = 'channel:read:redemptions'
    CHANNEL_MANAGE_REDEMPTIONS = 'channel:manage:redemptions'
    CHANNEL_MANAGE_SCHEDULE = 'channel:manage:schedule'
    CHANNEL_READ_STREAM_KEY = 'channel:read:stream_key'
    CHANNEL_READ_SUBSCRIPTIONS = 'channel:read:subscriptions'
    CHANNEL_MANAGE_VIDEOS = 'channel:manage:videos'
    CHANNEL_READ_VIPS = 'channel:read:vips'
    CHANNEL_MANAGE_VIPS = 'channel:manage:vips'
    CLIPS_EDIT = 'clips:edit'

    # Moderation
    MODERATION_READ = 'moderation:read'
    MODERATOR_MANAGE_ANNOUNCEMENTS = 'moderator:manage:announcements'
    MODERATOR_MANAGE_AUTOMOD = 'moderator:manage:automod'
    MODERATOR_READ_AUTOMOD_SETTINGS = 'moderator:read:automod_settings'
    MODERATOR_MANAGE_AUTOMOD_SETTINGS = 'moderator:manage:automod_settings'
    MODERATOR_MANAGE_BANNED_USERS = 'moderator:manage:banned_users'
    MODERATOR_READ_BLOCKED_TERMS = 'moderator:read:blocked_terms'
    MODERATOR_READ_CHAT_MESSAGES = 'moderator:read:chat_messages'
    MODERATOR_MANAGE_BLOCKED_TERMS = 'moderator:manage:blocked_terms'
    MODERATOR_MANAGE_CHAT_MESSAGES = 'moderator:manage:chat_messages'
    MODERATOR_READ_CHAT_SETTINGS = 'moderator:read:chat_settings'
    MODERATOR_MANAGE_CHAT_SETTINGS = 'moderator:manage:chat_settings'
    MODERATOR_READ_CHATTERS = 'moderator:read:chatters'
    MODERATOR_READ_FOLLOWERS = 'moderator:read:followers'
    MODERATOR_READ_GUEST_STAR = 'moderator:read:guest_star'
    MODERATOR_MANAGE_GUEST_STAR = 'moderator:manage:guest_star'
    MODERATOR_READ_SHIELD_MODE = 'moderator:read:shield_mode'
    MODERATOR_MANAGE_SHIELD_MODE = 'moderator:manage:shield_mode'
    MODERATOR_READ_SHOUTOUTS = 'moderator:read:shoutouts'
    MODERATOR_MANAGE_SHOUTOUTS = 'moderator:manage:shoutouts'
    MODERATOR_READ_SUSPICIOUS_USERS = 'moderator:read:suspicious_users'
    MODERATOR_READ_UNBAN_REQUESTS = 'moderator:read:unban_requests'
    MODERATOR_MANAGE_UNBAN_REQUESTS = 'moderator:manage:unban_requests'
    MODERATOR_READ_WARNINGS = 'moderator:read:warnings'
    MODERATOR_MANAGE_WARNINGS = 'moderator:manage:warnings'

    # User
    USER_BOT = 'user:bot'
    USER_EDIT = 'user:edit'
    USER_EDIT_BROADCAST = 'user:edit:broadcast'
    USER_READ_BLOCKED_USERS = 'user:read:blocked_users'
    USER_MANAGE_BLOCKED_USERS = 'user:manage:blocked_users'
    USER_READ_BROADCAST = 'user:read:broadcast'
    USER_READ_CHAT = 'user:read:chat'
    USER_MANAGE_CHAT_COLOR = 'user:manage:chat_color'
    USER_READ_EMAIL = 'user:read:email'
    USER_READ_EMOTES = 'user:read:emotes'
    USER_READ_FOLLOWS = 'user:read:follows'
    USER_READ_MODERATED_CHANNELS = 'user:read:moderated_channels'
    USER_READ_SUBSCRIPTIONS = 'user:read:subscriptions'
    USER_READ_WHISPERS = 'user:read:whispers'
    USER_MANAGE_WHISPERS = 'user:manage:whispers'
    USER_WRITE_CHAT = 'user:write:chat'
