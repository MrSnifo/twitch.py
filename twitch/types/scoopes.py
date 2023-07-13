"""
The MIT License (MIT)

Copyright (c) 2023-present Snifo

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NON-INFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""
from typing import Literal, List

ScopesType = List[Literal[
    'analytics:read:extensions',
    'analytics:read:games',
    'bits:read',
    'channel:edit:commercial',
    'channel:manage:broadcast',
    'channel:manage:extensions',
    'channel:manage:guest_star',
    'channel:manage:moderators',
    'channel:manage:polls',
    'channel:manage:predictions',
    'channel:manage:raids',
    'channel:manage:redemptions',
    'channel:manage:schedule',
    'channel:manage:videos',
    'channel:manage:vips',
    'channel:moderate',
    'channel:read:charity',
    'channel:read:editors',
    'channel:read:goals',
    'channel:read:guest_star',
    'channel:read:hype_train',
    'channel:read:polls',
    'channel:read:predictions',
    'channel:read:redemptions',
    'channel:read:stream_key',
    'channel:read:subscriptions',
    'channel:read:vips',
    'chat:edit',
    'chat:read',
    'clips:edit',
    'moderation:read',
    'moderator:manage:announcements',
    'moderator:manage:automod',
    'moderator:manage:automod_settings',
    'moderator:manage:banned_users',
    'moderator:manage:blocked_terms',
    'moderator:manage:chat_messages',
    'moderator:manage:chat_settings',
    'moderator:manage:shield_mode',
    'moderator:manage:shoutouts',
    'moderator:read:automod_settings',
    'moderator:read:blocked_terms',
    'moderator:read:chat_settings',
    'moderator:read:chatters',
    'moderator:read:followers',
    'moderator:read:guest_star',
    'moderator:read:shield_mode',
    'moderator:read:shoutouts',
    'user:edit',
    'user:edit:broadcast',
    'user:edit:follows',
    'user:manage:blocked_users',
    'user:manage:chat_color',
    'user:manage:whispers',
    'user:read:blocked_users',
    'user:read:broadcast',
    'user:read:email',
    'user:read:follows',
    'user:read:subscriptions',
    'whispers:edit',
    'whispers:read']]
