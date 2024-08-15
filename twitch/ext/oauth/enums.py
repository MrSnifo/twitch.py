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


class Scopes(Enum):
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
