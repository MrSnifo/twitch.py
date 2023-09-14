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
from __future__ import annotations

from .utils import MISSING, Value, Images, convert_rfc3339
from .user import BaseUser

from typing import TYPE_CHECKING, overload
if TYPE_CHECKING:
    from typing import AsyncGenerator, Optional, Literal, Union, List
    from .types import chat as ChatTypes
    from .state import ConnectionState
    from datetime import datetime

__all__ = ('Message', 'MessageEmote',
           'Emote',
           'Cheermote', 'CheermoteTier', 'CheermoteImagesType',
           'Badge', 'BadgeVersion',
           'ChatSettings',
           'ChannelAutoMod', 'BlockedTerm', 'AutoModSettings',
           'ChannelShieldMode', 'ShieldModeSettings',
           'ChannelChat')


# --------------------------------------
#              + Message +
# --------------------------------------
class MessageEmote:
    """
    Represents an emote in a chat message.

    Attributes
    ----------
    id: str
        The unique ID of the emote.
    end: int
        The ending position of the emote in the message text.
    begin: int
        The starting position of the emote in the message text.

    Methods
    -------
    __eq__(other: object) -> bool
        Checks if two MessageEmote instances are equal based on their IDs.
    __ne__(other: object) -> bool
        Checks if two MessageEmote instances are not equal.
    """
    __slots__ = ('id', 'end', 'begin')

    if TYPE_CHECKING:
        id: str
        end: str
        begin: str

    def __init__(self, data: ChatTypes.MessageEmote) -> None:
        self._form_data(data=data)

    def __repr__(self) -> str:
        return f'<MessageEmote id={self.id} begin={self.begin} end={self.end}>'

    def __eq__(self, other: object) -> bool:
        if isinstance(other, (MessageEmote, Emote)):
            return self.id == other.id
        return False

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def _form_data(self, data: ChatTypes.MessageEmote) -> None:
        self.id: str = data['id']
        self.end: int = data['end']
        self.begin: int = data['begin']


class Message:
    """
    Represents a chat message with emotes.

    Attributes
    ----------
    text: str
        The text content of the chat message.
    emotes: List[MessageEmote]
        List of emotes present in the message.

    Methods
    -------
    __str__() -> str
        Returns the text content of the chat message.
    """
    __slots__ = ('text', 'emotes')

    if TYPE_CHECKING:
        text: str
        emotes: List[MessageEmote]

    def __init__(self, data: ChatTypes.Message) -> None:
        self._form_data(data=data)

    def __repr__(self) -> str:
        return f'<Message text={self.text} emotes={self.emotes}>'

    def __str__(self) -> str:
        return self.text

    def _form_data(self, data: ChatTypes.Message) -> None:
        self.text: str = data['text']
        self.emotes: List[MessageEmote] = [MessageEmote(data=emote) for emote in data['emotes']]


# ------------------------------------
#              + Emote +
# ------------------------------------
class Emote:
    """
    Represents an emote in a chat message.

    Attributes
    ----------
    id: str
        The unique ID of the emote.
    name: str
        The name of the emote.
    tier: Optional[str]
        The tier of the emote, if applicable.
    scale: List[str]
        A list of available scales for the emote.
    format: List[str]
        A list of available formats for the emote.
    images: Images
        An instance of the Images class representing emote images.
    theme_mode: List[str]
        A list of available theme modes for the emote.
    emote_type: str
        The type of emote (e.g., 'global').
    emote_set_id: Optional[str]
        The ID of the emote set, if applicable.

    Methods
    -------
    __eq__(other: object) -> bool
        Checks if two Emote instances are equal based on their IDs.
    __ne__(other: object) -> bool
        Checks if two Emote instances are not equal.
    """
    __slots__ = ('id', 'name', 'tier', 'scale', 'format', 'images', 'theme_mode', 'emote_type',
                 'emote_set_id', '_template_url')

    if TYPE_CHECKING:
        id: str
        name: str
        tier: Optional[str]
        scale: List[str]
        format: List[str]
        images: Images
        theme_mode: List[str]
        emote_type: str
        emote_set_id: Optional[str]

    def __init__(self, data: Union[ChatTypes.BaseEmote, ChatTypes.Emote], template_url: str) -> None:
        self._form_data(data=data, template_url=template_url)

    def __repr__(self) -> str:
        return f'<Emote id={self.id} name={self.name} emote_type={self.emote_type}>'

    def __str__(self) -> str:
        return self.name

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Emote):
            return self.id == other.id
        return False

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    @property
    def template_url(self) -> str:
        """
        Gets the template URL for fetching emote images.

        Returns
        -------
        str
            The URL template for fetching emote images.
        """
        return self._template_url

    def _form_data(self, data: Union[ChatTypes.BaseEmote, ChatTypes.Emote], template_url: str) -> None:
        self.id = data['id']
        self.name = data['name']
        # Tier is set to ``0`` only if `emote_type` is not subscriptions.
        self.tier = data.get('tier') or None
        self.scale = data['scale']
        self.format = data['format']
        self.images = Images(data=data['images'])
        self.theme_mode = data['theme_mode']
        self.emote_type = data.get('emote_type', 'global')
        self.emote_set_id = data.get('emote_set_id')
        self._template_url = template_url


# --------------------------------------
#             + Cheermote +
# --------------------------------------
class CheermoteImagesType:
    """
    Represents images for cheermote tiers in both dark and light themes.

    Attributes
    ----------
    dark: ChatTypes.ImagesType
        Images for the dark theme.
    light: ChatTypes.ImagesType
        Images for the light theme.
    """
    __slots__ = ('dark', 'light')

    if TYPE_CHECKING:
        dark: ChatTypes.ImagesType
        light: ChatTypes.ImagesType

    def __init__(self, data: ChatTypes.TierImages) -> None:
        self._form_data(data=data)

    def __repr__(self) -> str:
        return '<CheermoteImagesType>'

    def _form_data(self, data: ChatTypes.TierImages) -> None:
        self.dark = data['dark']
        self.light = data['light']


class CheermoteTier:
    """
    Represents a tier of a cheermote.

    Attributes
    ----------
    id: str
        The unique ID of the cheermote tier.
    color: str
        The color associated with the tier.
    images: CheermoteImagesType
        An instance of CheermoteImagesType representing tier images.
    min_bits: int
        The minimum number of bits required to unlock this tier.
    can_cheer: bool
        Indicates whether users can cheer for this tier.
    show_in_bits_card: bool
        Indicates whether this tier is shown in the bits card.

    Methods
    -------
    __eq__(other: object) -> bool
        Checks if two CheermoteTier instances are equal based on their IDs.
    __ne__(other: object) -> bool
        Checks if two CheermoteTier instances are not equal.
    """
    __slots__ = ('id', 'color', 'images', 'min_bits', 'can_cheer', 'show_in_bits_card')

    if TYPE_CHECKING:
        id: str
        color: str
        images: CheermoteImagesType
        min_bits: int
        can_cheer: bool
        show_in_bits_card: bool

    def __init__(self, data: ChatTypes.Tier) -> None:
        self._form_data(data=data)

    def __repr__(self) -> str:
        return (
            f'<CheermoteTier id={self.id} min_bits={self.min_bits} color={self.color}'
            f' can_cheer={self.can_cheer}>'
        )

    def __eq__(self, other: object) -> bool:
        if isinstance(other, CheermoteTier):
            return self.id == other.id
        return False

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def _form_data(self, data: ChatTypes.Tier) -> None:
        self.id: str = data['id']
        self.color: str = data['color']
        self.images: CheermoteImagesType = CheermoteImagesType(data=data['images'])
        self.min_bits: int = data['min_bits']
        self.can_cheer: bool = data['can_cheer']
        self.show_in_bits_card: bool = data['show_in_bits_card']


class Cheermote:
    """
    Represents a cheermote.

    Attributes
    ----------
    type: str
        The type of cheermote.
    prefix: str
        The prefix associated with the cheermote.
    tiers: List[CheermoteTier]
        A list of CheermoteTier instances representing the tiers of the cheermote.
    order: int
        The order of the cheermote.
    last_updated: datetime
        The datetime when the cheermote was last updated.

    Methods
    -------
    __str__() -> str
        Returns a string representation of the Cheermote prefix.
    """
    __slots__ = ('type', 'prefix', 'tiers', 'order', 'last_updated')

    if TYPE_CHECKING:
        type: str
        order: int
        tiers: List[CheermoteTier]
        prefix: str
        last_updated: datetime

    def __init__(self, data: ChatTypes.Cheermote) -> None:
        self._form_data(data=data)

    def __repr__(self) -> str:
        return f'<Cheermote prefix={self.prefix} type={self.type} order={self.order}>'

    def __str__(self) -> str:
        return self.prefix

    def _form_data(self, data: ChatTypes.Cheermote):
        self.type = data['type']
        self.order = data['order']
        self.tiers = [CheermoteTier(data=tier) for tier in data['tiers']]
        self.prefix = data['prefix']
        self.last_updated = convert_rfc3339(data['last_updated'])


# ------------------------------------
#              + Badge +
# ------------------------------------
class BadgeVersion:
    """
    Represents a version of a badge.

    Attributes
    ----------
    id: str
        The unique ID of the badge version.
    title: str
        The title of the badge version.
    images: Images
        An instance of Images representing badge images.
    click_url: Optional[str]
        The optional URL that the badge version can link to.
    description: str
        The description of the badge version.
    click_action: Optional[str]
        The optional click action associated with the badge version.

    Methods
    -------
    __str__() -> str
        Returns the title of the BadgeVersion.
    __eq__(other: object) -> bool
        Checks if two BadgeVersion instances are equal based on their IDs.
    __ne__(other: object) -> bool
        Checks if two BadgeVersion instances are not equal.
    """
    __slots__ = ('id', 'title', 'images', 'click_url', 'description', 'click_action')

    if TYPE_CHECKING:
        id: str
        title: str
        images: Images
        click_url: Optional[str]
        description: str
        click_action: Optional[str]

    def __init__(self, data: ChatTypes.BadgeVersion) -> None:
        self._form_data(data=data)

    def __repr__(self) -> str:
        return f'<BadgeVersion id={self.id} title={self.title} description={self.description}>'

    def __str__(self) -> str:
        return self.title

    def __eq__(self, other: object) -> bool:
        if isinstance(other, BadgeVersion):
            return self.id == other.id
        return False

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def _form_data(self, data: ChatTypes.BadgeVersion) -> None:
        self.id: str = data['id']
        self.title: str = data['title']
        _images = {'url_1x': data['image_url_1x'],
                   'url_2x': data['image_url_2x'],
                   'url_4x': data['image_url_4x']}
        self.images = Images(data=_images)
        self.click_url: Optional[str] = data['click_url']
        self.description: str = data['description']
        self.click_action: str = data['click_action']


class Badge:
    """
    Represents a badge set.

    Attributes
    ----------
    set_id: str
        The unique ID of the badge set.
    versions: List[BadgeVersion]
        A list of BadgeVersion instances representing the versions of the badge set.

    Methods
    -------
    __eq__(other: object) -> bool
        Checks if two Badge instances are equal based on their set IDs.
    __ne__(other: object) -> bool
        Checks if two Badge instances are not equal.
    """
    __slots__ = ('set_id', 'versions')

    if TYPE_CHECKING:
        set_id: str
        versions: List[BadgeVersion]

    def __init__(self, data: ChatTypes.Badge) -> None:
        self._form_data(data=data)

    def __repr__(self) -> str:
        return f'<Badge set_id={self.set_id}>'

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Badge):
            return self.set_id == other.set_id
        return False

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def _form_data(self, data: ChatTypes.Badge) -> None:
        self.set_id = data['set_id']
        self.versions = [BadgeVersion(data=version) for version in data['versions']]


# -------------------------------------
#           + ChatSettings +
# -------------------------------------
class ChatSettings:
    """
    Represents settings for a chat.

    Attributes
    ----------
    slow_mode: Value
        The slow mode settings.
    follower_mode: Value
        The follower mode settings.
    is_emote_mode_enabled: bool
        Indicates whether emote mode is enabled.
    non_moderator_chat_delay: Optional[Value]
        Optional non-moderator chat delay settings.
    is_subscriber_mode_enabled: bool
        Indicates whether subscriber mode is enabled.
    is_unique_chat_mode_enabled: bool
        Indicates whether unique chat mode is enabled.
    """
    # ... (Constructor and other methods)
    __slots__ = ('slow_mode', 'follower_mode', 'is_emote_mode_enabled', 'non_moderator_chat_delay',
                 'is_subscriber_mode_enabled', 'is_unique_chat_mode_enabled')

    if TYPE_CHECKING:
        slow_mode: Value
        follower_mode: Value
        is_emote_mode_enabled: bool
        non_moderator_chat_delay: Optional[Value]
        is_subscriber_mode_enabled: bool
        is_unique_chat_mode_enabled: bool

    def __init__(self, data: ChatTypes.ChatSettings) -> None:
        self._form_data(data=data)

    def __repr__(self) -> str:
        return '<ChatSettings>'

    def _form_data(self, data: ChatTypes.ChatSettings) -> None:
        self.is_emote_mode_enabled = data['emote_mode']
        self.is_subscriber_mode_enabled = data['subscriber_mode']
        self.is_unique_chat_mode_enabled = data['unique_chat_mode']
        _follower_mode = data['follower_mode']
        _follower_mode_duration = data['follower_mode_duration'] or 0
        _slow_mode = data['slow_mode']
        _slow_mode_wait_time = data['slow_mode_wait_time']
        self.follower_mode = Value(data={'is_enabled': _follower_mode, 'value': _follower_mode_duration})
        self.slow_mode = Value(data={'is_enabled': _slow_mode, 'value': _slow_mode_wait_time})
        # Require a user access token that includes the ``moderator:read:chat_settings`` scope.
        _non_moderator_chat_delay = data.get('non_moderator_chat_delay')
        _non_moderator_chat_delay_duration = data.get('non_moderator_chat_delay_duration')
        self.non_moderator_chat_delay = None
        if _non_moderator_chat_delay:
            self.non_moderator_chat_delay = Value(data={'is_enabled': _non_moderator_chat_delay,
                                                        'value': _non_moderator_chat_delay_duration})

    def to_json(self) -> ChatTypes.ChatSettingsToJson:
        # This is useful when you want to modify settings of the object and update it.
        return ({
            'emote_mode': self.is_emote_mode_enabled,
            'follower_mode': self.follower_mode.is_enabled,
            'follower_mode_duration': self.follower_mode.value,
            'non_moderator_chat_delay': self.non_moderator_chat_delay.is_enabled,
            'non_moderator_chat_delay_duration': self.non_moderator_chat_delay.value,
            'slow_mode': self.slow_mode.is_enabled,
            'slow_mode_wait_time': self.slow_mode.value,
            'subscriber_mode': self.is_subscriber_mode_enabled,
            'unique_chat_mode': self.is_unique_chat_mode_enabled
        })


# ------------------------------------
#             + AutoMod +
# ------------------------------------
class AutoModSettings:
    """
    Represents AutoMod settings for a chat.

    Attributes
    ----------
    misogyny: int
        The misogyny filter level.
    bullying: int
        The bullying filter level.
    swearing: int
        The swearing filter level.
    disability: int
        The disability filter level.
    aggression: int
        The aggression filter level.
    overall_level: Optional[int]
        The overall moderation level (optional).
    sex_based_terms: int
        The filter level for sex-based terms.
    sexuality_sex_or_gender: int
        The filter level for sexuality, sex, or gender-related terms.
    race_ethnicity_or_religion: int
        The filter level for race, ethnicity, or religion-related terms.
    """
    __slots__ = ('misogyny', 'bullying', 'swearing', 'disability', 'aggression', 'overall_level',
                 'sex_based_terms', 'sexuality_sex_or_gender', 'race_ethnicity_or_religion')
    if TYPE_CHECKING:
        misogyny: int
        bullying: int
        swearing: int
        disability: int
        aggression: int
        overall_level: Optional[int]
        sex_based_terms: int
        sexuality_sex_or_gender: int
        race_ethnicity_or_religion: int

    def __init__(self, data: ChatTypes.AutoModSettings) -> None:
        self._form_data(data=data)

    def __repr__(self) -> str:
        return '<AutoModSettings>'

    def _form_data(self, data: ChatTypes.AutoModSettings) -> None:
        self.bullying = data['bullying']
        self.misogyny = data['misogyny']
        self.swearing = data['swearing']
        self.aggression = data['aggression']
        self.disability = data['disability']
        self.overall_level = data['overall_level']
        self.sex_based_terms = data['sex_based_terms']
        self.sexuality_sex_or_gender = data['sexuality_sex_or_gender']
        self.race_ethnicity_or_religion = data['race_ethnicity_or_religion']

    def to_json(self) -> ChatTypes.AutoModSettingsToJson:
        # This is useful when you want to modify settings of the object and update it.
        # overall_level does not Include
        return ({
            'bullying': self.bullying,
            'misogyny': self.misogyny,
            'swearing': self.swearing,
            'aggression': self.aggression,
            'disability': self.disability,
            'sex_based_terms': self.sex_based_terms,
            'sexuality_sex_or_gender': self.sexuality_sex_or_gender,
            'race_ethnicity_or_religion': self.race_ethnicity_or_religion})


class BlockedTerm:
    """
    Represents a blocked term in chat.

    Attributes
    ----------
    id: str
        The unique ID of the blocked term.
    text: str
        The text of the blocked term.
    created_at: datetime
        The date and time when the blocked term was created.
    expires_at: Optional[datetime]
        The date and time when the blocked term expires (optional).
    updated_at: datetime
        The date and time when the blocked term was last updated.

    Methods
    -------
    __str__() -> str
        Returns the text of the blocked term as a string.
    __eq__(other: object) -> bool
        Checks if two BlockedTerm instances are equal based on their IDs.
    __ne__(other: object) -> bool
        Checks if two BlockedTerm instances are not equal.
    """
    __slots__ = ('id', 'text', 'created_at', 'expires_at', 'updated_at')

    if TYPE_CHECKING:
        id: str
        text: str
        created_at: datetime
        expires_at: Optional[datetime]
        updated_at: datetime

    def __init__(self, data: ChatTypes.BlockedTerm) -> None:
        self._form_data(data=data)

    def __repr__(self) -> str:
        return f'<BlockedTerm id={self.id} text={self.text} created_at={self.created_at}>'

    def __str__(self) -> str:
        return self.text

    def __eq__(self, other: object) -> bool:
        if isinstance(other, BlockedTerm):
            return self.id == other.id
        return False

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def _form_data(self, data: ChatTypes.BlockedTerm) -> None:
        self.id = data['id']
        self.text = data['text']
        self.created_at = convert_rfc3339(data['created_at'])
        self.expires_at = convert_rfc3339(data['expires_at'])
        self.updated_at = convert_rfc3339(data['updated_at'])


class ChannelAutoMod:
    """
    Represents a channel's AutoMod settings.
    """
    __slots__ = ('_b_id', '_m_id', '__state')

    def __init__(self, state: ConnectionState, broadcaster_id: str, moderator_id: str):
        self._b_id: str = broadcaster_id
        self._m_id: str = moderator_id
        self.__state: ConnectionState = state

    async def get_automod_settings(self) -> AutoModSettings:
        """
        Get the AutoMod settings for the channel.

        | Scopes                            | Description           |
        | --------------------------------- | ----------------------|
        | `moderator:read:automod_settings` | Get AutoMod Settings. |

        Raises
        ------
        Unauthorized
            * The user access token must include the moderator:read:automod_settings scope.
        Forbidden
            * The user in moderator_id is not one of the broadcaster's moderators.

        Returns
        -------
        AutoModSettings
            The AutoMod settings for the channel.
        """
        data = await self.__state.http.get_automod_settings(broadcaster_id=self._b_id,
                                                            moderator_id=self._m_id)
        return AutoModSettings(data=data)

    @overload
    async def update_automod_settings(self, automod: AutoModSettings) -> AutoModSettings:
        ...

    @overload
    async def update_automod_settings(self, overall_level: int) -> AutoModSettings:
        ...

    @overload
    async def update_automod_settings(self,
                                      aggression: int = MISSING,
                                      bullying: int = MISSING,
                                      disability: int = MISSING,
                                      misogyny: int = MISSING,
                                      race_ethnicity_or_religion: int = MISSING,
                                      sex_based_terms: int = MISSING,
                                      sexuality_sex_or_gender: int = MISSING,
                                      swearing: int = MISSING) -> AutoModSettings:
        ...

    async def update_automod_settings(self,
                                      automod: AutoModSettings = MISSING,
                                      overall_level: int = MISSING,
                                      aggression: int = MISSING,
                                      bullying: int = MISSING,
                                      disability: int = MISSING,
                                      misogyny: int = MISSING,
                                      race_ethnicity_or_religion: int = MISSING,
                                      sex_based_terms: int = MISSING,
                                      sexuality_sex_or_gender: int = MISSING,
                                      swearing: int = MISSING) -> AutoModSettings:
        """
        Update the AutoMod settings for the channel.

        ???+ Warning
            You must choose either `automod` (AutoModSettings object) or `overall_level`
            or `rest of Parameters` as they are mutually exclusive.

        ??? Note
            You can set either an overall AutoMod level (overall_level) or individual filter levels,
            but not both.
            - If you set an overall_level, it applies default filter levels to the individual settings.

            The filter levels range from 0 (no filtering) to 4 (most aggressive filtering).
            Higher levels indicate more aggressive filtering.

        Parameters
        ----------
        automod: AutoModSettings
            An instance of AutoModSettings containing updated settings.
        overall_level: int
            The overall AutoMod level for the channel.
        aggression: int
            The aggression filter level.
        bullying: int
            The bullying filter level.
        disability: int
            The disability filter level.
        misogyny: int
            The misogyny filter level.
        race_ethnicity_or_religion: int
            The race/ethnicity/religion filter level.
        sex_based_terms: int
            The sex-based terms filter level.
        sexuality_sex_or_gender: int
            The sexuality/sex/gender filter level.
        swearing: int
            The swearing filter level.

        Raises
        ------
        BadRequest
            * The value of one or more AutoMod settings is not valid.
        Unauthorized
            * The user access token must include the moderator:manage:automod_settings scope.
        Forbidden
            * The user in moderator_id is not one of the broadcaster's moderators.

        Returns
        -------
        AutoModSettings
            The updated AutoMod settings for the channel.
        """
        settings = {'broadcaster_id': self._b_id, 'moderator_id': self._m_id}
        if isinstance(automod, AutoModSettings):
            for key, value in automod.to_json().items():
                settings[key] = value
        else:
            settings['overall_level'] = overall_level
            settings['aggression'] = aggression
            settings['bullying'] = bullying
            settings['disability'] = disability
            settings['misogyny'] = misogyny
            settings['race_ethnicity_or_religion'] = race_ethnicity_or_religion
            settings['sex_based_terms'] = sex_based_terms
            settings['sexuality_sex_or_gender'] = sexuality_sex_or_gender
            settings['swearing'] = swearing
        data = await self.__state.http.update_automod_settings(**settings)
        return AutoModSettings(data=data)

    async def fetch_blocked_terms(self, limit: int = 4) -> AsyncGenerator[List[BlockedTerm]]:
        """
        Fetch the list of blocked terms for the channel.

        ???+ Warning
            This method uses [pagination](https://dev.twitch.tv/docs/api/guide/#pagination).
            Set the limit to -1 to retrieve all data, but exercise caution due to potential performance
            and rate limit impacts.

        | Scopes                                                             | Description        |
        | ------------------------------------------------------------------ | -------------------|
        | `moderator:read:blocked_terms` or `moderator:manage:blocked_terms` | Get Blocked Terms. |

        Raises
        ------
        Unauthorized
            * The user access token must include the moderator:read:blocked_terms or
             moderator:manage:blocked_terms scope.
        Forbidden
            * The user in moderator_id is not one of the broadcaster's moderators.

        Parameters
        ----------
        limit: int
            The maximum number of blocked terms to fetch (default is 4).

        Yields
        ------
        List[BlockedTerm]
            A list of blocked terms for the channel.
        """
        async for terms in self.__state.http.fetch_blocked_terms(limit=limit,
                                                                 broadcaster_id=self._b_id,
                                                                 moderator_id=self._m_id):
            yield [BlockedTerm(data=term) for term in terms]

    async def add_blocked_term(self, text: str) -> BlockedTerm:
        """
        Add a blocked term to the channel's AutoMod settings.

        | Scopes                           | Description        |
        | -------------------------------- | -------------------|
        | `moderator:manage:blocked_terms` | Add Blocked Term.  |

        Parameters
        ----------
        text: str
            The word or phrase to block from being used in the broadcaster’s chat room.

            The term must contain a minimum of 2 characters and may contain up to a
            maximum of 500 characters.

        Raises
        ------
        ValueError
            * The term must contain 2 to 500 characters.
        Unauthorized
            * The user access token must include the moderator:manage:blocked_terms scope.
        Forbidden
            * The user in moderator_id is not one of the broadcaster's moderators.

        Returns
        -------
        BlockedTerm
            The blocked term that was added.
        """
        data = await self.__state.http.add_blocked_term(broadcaster_id=self._b_id, moderator_id=self._m_id,
                                                        text=text)
        return BlockedTerm(data=data)

    async def remove_blocked_term(self, term: BlockedTerm) -> None:
        """
        Remove a blocked term from the channel's AutoMod settings.

        | Scopes                          | Description          |
        | ------------------------------- | ---------------------|
        | `moderator:manage:blocked_term` | Remove Blocked Term. |


        Parameters
        ----------
        term: BlockedTerm
            The blocked term to remove.

        Raises
        ------
        Unauthorized
            * The user access token must include the moderator:manage:blocked_terms scope.
        Forbidden
            * The user in moderator_id is not one of the broadcaster's moderators.
        """
        await self.__state.http.remove_blocked_term(broadcaster_id=self._b_id, moderator_id=self._m_id,
                                                    term_id=term.id)


# -------------------------------------
#            + ShieldMode +
# -------------------------------------
class ShieldModeSettings:
    """
    Represents shield mode settings.

    Attributes
    ----------
    is_active: bool
        Indicates if shield mode is currently active.
    moderator: Optional[BaseUser]
        The moderator who activated shield mode (optional).
    last_activated_at: Optional[datetime]
        The date and time when shield mode was last activated (optional).

    Methods
    -------
    __bool__() -> bool
        Checks if shield mode is currently active.
    """
    __slots__ = ('is_active', 'moderator', 'last_activated_at')

    if TYPE_CHECKING:
        is_active: bool
        moderator: Optional[BaseUser]
        last_activated_at: Optional[datetime]

    def __init__(self, data: Union[ChatTypes.ShieldMode, Union[ChatTypes.ShieldModeBeginEvent,
                                                               ChatTypes.ShieldModeEndEvent]]) -> None:
        self._form_data(data=data)

    def __repr__(self) -> str:
        return f'<ShieldMode is_active={self.is_active} moderator={self.moderator!r}>'

    def __bool__(self) -> bool:
        return self.is_active

    def _form_data(self, data: Union[ChatTypes.ShieldMode, Union[ChatTypes.ShieldModeBeginEvent,
                                                                 ChatTypes.ShieldModeEndEvent]]) -> None:
        # Both of the attributes last_activated_at and moderator could be ``None``,
        # if the broadcaster has never used shieldmode.
        self.moderator = None
        if data.get('moderator_id') or data.get('moderator_user_id'):
            self.moderator = BaseUser(data, prefix=['moderator_', 'moderator_user_'])
        # Missing Between events.
        _last_activated_at: Optional[str] = data.get('last_activated_at')
        _started_at: Optional[str] = data.get('started_at')
        _ended_at: Optional[str] = data.get('ended_at')
        self.last_activated_at = convert_rfc3339(timestamp=_last_activated_at or _started_at or _ended_at)
        _is_active: Optional[bool] = data.get('is_active')
        self.is_active: bool = _is_active if bool(_is_active) else (bool(_started_at))


class ChannelShieldMode:
    """
    Represents a channel's shield mode settings.
    """
    __slots__ = ('_b_id', '_m_id', '__state')

    def __init__(self, state: ConnectionState, broadcaster_id: str, moderator_id: str):
        self._b_id: str = broadcaster_id
        self._m_id: str = moderator_id
        self.__state: ConnectionState = state

    async def get_status(self) -> ShieldModeSettings:
        """
        Get the current shield mode settings of the channel.

        | Scopes                                                         | Description             |
        | -------------------------------------------------------------- | ------------------------|
        | `moderator:read:shield_mode` or `moderator:manage:shield_mode` | Get Shield Mode Status. |

        Raises
        ------
        Unauthorized
            * The user access token must include the moderator:read:shield_mode or
             moderator:manage:shield_mode scope.
        Forbidden
            * The user in moderator_id is not one of the broadcaster's moderators.

        Returns
        -------
        ShieldModeSettings
            The current shield mode settings for the channel.
        """
        data = await self.__state.http.get_shield_mode_status(broadcaster_id=self._b_id,
                                                              moderator_id=self._m_id)
        return ShieldModeSettings(data=data)

    async def update_status(self, activate: bool) -> ShieldModeSettings:
        """
        Update the shield mode status for the channel.

        | Scopes                         | Description                |
        | -------------------------------| ---------------------------|
        | `moderator:manage:shield_mode` | Update Shield Mode Status. |

        Parameters
        ----------
        activate: bool
            Indicates whether to activate or deactivate shield mode.

        Raises
        ------
        Unauthorized
            * The user access token must include the moderator:manage:shield_mode scope.
        Forbidden
            * The user in moderator_id is not one of the broadcaster's moderators.

        Returns
        -------
        ShieldModeSettings
            The updated shield mode settings for the channel.
        """
        data = await self.__state.http.update_shield_mode_status(broadcaster_id=self._b_id,
                                                                 moderator_id=self._m_id,
                                                                 activate=activate)
        return ShieldModeSettings(data=data)


# -------------------------------------
#             + UserChat +
# -------------------------------------
class ChannelChat:
    """
    Represents the chat-related functionality for a channel.
    """
    __slots__ = ('_b_id', '_m_id', '_state')

    def __init__(self, state: ConnectionState, broadcaster_id: str, moderator_id: str):
        self._b_id: str = broadcaster_id
        self._m_id: str = moderator_id
        self._state: ConnectionState = state

    @property
    def shieldmode(self) -> ChannelShieldMode:
        """
        Represents the shield mode settings for the channel's chat.

        Returns
        -------
        ChannelShieldMode
            The shield mode settings for the chat.
        """
        return ChannelShieldMode(state=self._state, broadcaster_id=self._b_id, moderator_id=self._m_id)

    @property
    def automod(self) -> ChannelAutoMod:
        """
        Represents the AutoMod settings for the channel's chat.

        Returns
        -------
        ChannelAutoMod
            The AutoMod settings for the chat.
        """
        return ChannelAutoMod(state=self._state, broadcaster_id=self._b_id, moderator_id=self._m_id)

    async def get_settings(self) -> ChatSettings:
        """
        Get the chat settings for the channel.

        Returns
        -------
        ChatSettings
            The chat settings for the channel.
        """
        data = await self._state.http.get_chat_settings(broadcaster_id=self._b_id, moderator_id=self._m_id)
        return ChatSettings(data=data)

    @overload
    async def update_settings(self, chat_settings: ChatSettings):
        ...

    @overload
    async def update_settings(self,
                              emote_mode: bool = MISSING,
                              subscriber_mode: bool = MISSING,
                              unique_chat_mode: bool = MISSING,
                              follower_mode: bool = MISSING,
                              follower_mode_duration: int = MISSING,
                              non_moderator_chat_delay: bool = MISSING,
                              non_moderator_chat_delay_duration: Literal[2, 4, 6] = MISSING,
                              slow_mode: bool = MISSING,
                              slow_mode_wait_time: int = MISSING):
        ...

    async def update_settings(self,
                              chat_settings: ChatSettings = MISSING,
                              emote_mode: bool = MISSING,
                              subscriber_mode: bool = MISSING,
                              unique_chat_mode: bool = MISSING,
                              follower_mode: bool = MISSING,
                              follower_mode_duration: int = MISSING,
                              non_moderator_chat_delay: bool = MISSING,
                              non_moderator_chat_delay_duration: Literal[2, 4, 6] = MISSING,
                              slow_mode: bool = MISSING,
                              slow_mode_wait_time: int = MISSING):
        """
        Update the chat settings for the channel.

        ???+ Warning
            You must choose either `chat_settings` (ChatSettings object)
            `rest of Parameters` as they are mutually exclusive.

        | Scopes                           | Description           |
        | -------------------------------- | ----------------------|
        | `moderator:manage:chat_settings` | Update Chat Settings. |

        Parameters
        ----------
        chat_settings: ChatSettings
            An instance of ChatSettings containing updated settings.
        emote_mode: bool
            Set to True if only emotes are allowed in chat messages
        follower_mode: bool
            Set to True if the chat room should be restricted to followers only
        follower_mode_duration: int
            The length of time in minutes that users must follow the broadcaster before participating
            in chat.

             `Only set if follower_mode is True`.

            Possible values:

            * 0 through 129600 (3 months).
        non_moderator_chat_delay: bool
            Set to True if a delay should be applied before chat messages appear
        non_moderator_chat_delay_duration: Literal[2, 4, 6]
            The amount of time in seconds that messages are delayed before appearing in chat.

            `Set only if non_moderator_chat_delay is True`.
        slow_mode: bool
            Set to True if a wait period should be applied between messages
        slow_mode_wait_time: int
            The amount of time in seconds that users must wait between sending messages.

            `Set only if slow_mode is True`.

            Possible values:

            * 3 through 120.
        subscriber_mode: bool
            Set to True if the chat room should be restricted to subscribers only
        unique_chat_mode: bool
            Set to True if users must post only unique messages

        Raises
        ------
        Unauthorized
            * The user access token must include the moderator:manage:chat_settings scope.
        Forbidden
            * The user in the moderator_id query parameter must have moderator privileges
             in the broadcaster's channel.

        Returns
        -------
        ChatSettings
            The updated chat settings for the channel.
        """

        settings = {'broadcaster_id': self._b_id, 'moderator_id': self._m_id}
        if isinstance(chat_settings, ChatSettings):
            for key, value in chat_settings.to_json().items():
                settings[key] = value
        else:
            settings['emote_mode'] = emote_mode
            settings['follower_mode'] = follower_mode
            settings['follower_mode_duration'] = follower_mode_duration
            settings['non_moderator_chat_delay'] = non_moderator_chat_delay
            settings['non_moderator_chat_delay_duration'] = non_moderator_chat_delay_duration
            settings['slow_mode'] = slow_mode
            settings['slow_mode_wait_time'] = slow_mode_wait_time
            settings['subscriber_mode'] = subscriber_mode
            settings['unique_chat_mode'] = unique_chat_mode
        data = await self._state.http.update_chat_settings(**settings)
        return ChatSettings(data=data)

    async def fetch_chatters(self, limit: int = 4) -> AsyncGenerator[List[BaseUser]]:
        """
        Fetch a list of chatters in the channel.

        ???+ Warning
            This method uses [pagination](https://dev.twitch.tv/docs/api/guide/#pagination).
            Set the limit to -1 to retrieve all data, but exercise caution due to potential performance
            and rate limit impacts.

        ??? Note
            There might be a delay between when users join and leave a chat and when the count
            is updated accordingly.

        | Scopes                    | Description   |
        | ------------------------- | --------------|
        | `moderator:read:chatters` | Get Chatters. |

        Parameters
        ----------
        limit: int
            The maximum number of chatters to fetch.

        Raises
        ------
        Unauthorized
            * The user access token must include the moderator:read:chatters scope.
        Forbidden
            * The user in the moderator_id query parameter is not one of the broadcaster's moderators.

        Yields
        ------
        List[BaseUser]
            A list of BaseUser objects representing the chatters.
        """
        async for users in self._state.http.fetch_chatters(limit=limit,
                                                           broadcaster_id=self._b_id,
                                                           moderator_id=self._b_id):
            yield [BaseUser(user, prefix='user_') for user in users]

    async def get_total_chatters(self) -> int:
        """
        Get the total number of chatters in the channel.

        | Scopes                    | Description   |
        | ------------------------- | --------------|
        | `moderator:read:chatters` | Get Chatters. |

        Raises
        ------
        Unauthorized
            * The user access token must include the moderator:read:chatters scope.
        Forbidden
            * The user in the moderator_id query parameter is not one of the broadcaster's moderators.

        Returns
        -------
        int
            The total number of chatters in the channel.
        """
        data = await self._state.http.get_total_chatters(broadcaster_id=self._b_id, moderator_id=self._m_id)
        return data

    async def get_emotes(self) -> List[Emote]:
        """
        Get the emotes available in the channel.

        Returns
        -------
        List[Emote]
            A list of Emote objects representing the emotes.
        """
        data = await self._state.http.get_channel_emotes(broadcaster_id=self._b_id)
        return [Emote(data=emote, template_url=data[0]) for emote in data[1]]

    async def get_cheermotes(self) -> List[Cheermote]:
        """
        Retrieve a list of Cheermotes that users can use to cheer with Bits in any Bits-enabled channel's
        chat room.

        Returns
        -------
        List[Cheermote]
            A list of Cheermote instances representing the available cheermotes.
        """
        data = await self._state.http.get_cheermotes(broadcaster_id=self._b_id)
        return [Cheermote(data=cheermote) for cheermote in data]

    async def get_badges(self) -> List[Badge]:
        """
        Retrieve the broadcaster's list of custom chat badges.

        Returns
        -------
        List[Badge]
            A list of Badge instances representing the custom chat badges.
        """
        data = await self._state.http.get_channel_chat_badges(broadcaster_id=self._b_id)
        return [Badge(data=badge) for badge in data]

    async def send_announcement(self, message: str, *,
                                color: ChatTypes.AnnouncementColors = MISSING) -> None:
        """
        Sends an announcement to the broadcaster's chat room.

        | Scopes                           | Description             |
        | -------------------------------- | ------------------------|
        | `moderator:manage:announcements` | Send Chat Announcement. |

        Parameters
        ----------
        message: str
            The message to be sent as an announcement.
        color: str
            The color of the announcement message.
            Possible values are:
             * primary (default)
             * blue,
             * green,
             * orange
             * purple

        Raises
        ------
        Unauthorized
            * The user access token is missing the moderator:manage:announcements scope.
        """
        await self._state.http.send_chat_announcements(broadcaster_id=self._b_id,
                                                       moderator_id=self._m_id,
                                                       message=message, color=color)

    async def clear_chat(self):
        """
        Clears all chat messages from the broadcaster's chat room.

        | Scopes                           | Description           |
        | -------------------------------- | ----------------------|
        | `moderator:manage:chat_messages` | Delete Chat Messages. |

        Raises
        ------
        Unauthorized
            * The user access token is missing the moderator:manage:chat_messages scope.
        """
        await self._state.http.delete_chat_messages(broadcaster_id=self._b_id,
                                                    moderator_id=self._m_id)

    async def delete_message(self, message_id: str):
        """
        Removes a single chat message from the broadcaster’s chat room.

        | Scopes                           | Description           |
        | -------------------------------- | ----------------------|
        | `moderator:manage:chat_messages` | Delete Chat Messages. |

        Parameters
        ----------
        message_id: str
            The ID of the message to remove. The id tag in the PRIVMSG tag contains the message’s ID.
            Restrictions:
            * The message must have been created within the last 6 hours.
            * The message must not belong to the broadcaster.
            * The message must not belong to another moderator.

        Raises
        ------
        BadRequest
            * You may not delete another moderator's messages.
            * You may not delete the broadcaster's messages.
        Unauthorized
            * The user access token is missing the moderator:manage:chat_messages scope.
        Forbidden
            * The user in moderator_id is not one of the broadcaster's moderators.
        NotFound
            * The ID in message_id was not found.
            * The specified message was created more than 6 hours ago.
        """
        await self._state.http.delete_chat_messages(broadcaster_id=self._b_id, moderator_id=self._m_id,
                                                    message_id=message_id)

    async def get_chat_colors(self, users: List[Union[str, BaseUser]]):
        """
        Get the chat colors of more than one user at once.

        Parameters
        ----------
        users: List[Union[str, BaseUser]]
            A list of usernames or BaseUser objects for which to retrieve chat colors.

        Returns
        -------
        List[str]
            A list of chat colors corresponding to the specified users.
        """
        users = [user.id for user in (await self._state.get_users(users))]
        data = await self._state.http.get_users_chat_color(user_ids=users)
        return data
