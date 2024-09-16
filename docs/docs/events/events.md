---
icon: material/clock-time-eleven-outline
---

# Event Handlers

## Client Events
___

- `on_connect`
    - **Description**: Triggered when the client successfully connects to the eventsub websocket.
    - **Usage**:
    ```python
    @client.event
    async def on_connect() -> None:
        ...
    ```
  
---

- `on_ready`
    - **Description**: Triggered when the client is fully ready and connected.
    - **Usage**:
    ```python
    @client.event
    async def on_ready() -> None:
        ...
    ```
  
---

- `on_disconnect`
    - **Description**: Triggered when the client disconnects from the eventsub websocket server.
    - **Usage**:
    ```python
    @client.event
    async def on_disconnect() -> None:
        ...
    ```

---

- `setup_hook`
    - **Description**: Method to be implemented within the client class for setup actions that should occur before the client starts running.
    - **Usage**:
    ```python
    class Twitch(Client):
        async def setup_hook(self) -> None:
            # Your setup logic here
            ...
    ```
  
---

- `on_socket_raw_receive`
    - **Description**: Triggered when th client receives a raw message from the WebSocket.
    - **Event requirements**: You must enable `socket_debug` in client options.
    - **Usage**:
    ```python
    @client.event
    async def on_socket_raw_receive(data: Any) -> None:
        ...
    ```
  
---

- `on_error`
    - **Description**: Handles errors that occur during event dispatch. This method logs any exceptions that
crop up while processing an event.
    - **Usage**:
    ```python
    @client.event
    @staticmethod
    async def on_error(event_name: str, error: Exception, *args: Any, **kwargs: Any) -> None:
        ...
    ```
  

## Chat Events
___

- `on_chat_clear`
    - **Description**: Triggered when the chat is cleared.
    - **Scope**: `user:read:chat`
    - **Data Type**: [`ChatClearEvent`][twitch.types.eventsub.chat.ChatClearEvent]
    - **Usage**:
    ```python
    @client.event
    async def on_chat_clear(data: eventsub.chat.ChatClearEvent):
        ...
    ```
  
---

- `on_chat_clear_user_messages`
    - **Description**: Triggered when a user's messages are cleared.
    - **Scope**: `user:read:chat`
    - **Data Type**: [`ClearUserMessagesEvent`][twitch.types.eventsub.chat.ClearUserMessagesEvent]
    - **Usage**:
    ```python
    @client.event
    async def on_chat_clear_user_messages(data: eventsub.chat.ClearUserMessagesEvent):
        ...
    ```

- `on_chat_message`
    - **Description**: Triggered when a chat message is received.
    - **Scope**: `user:read:chat`
    - **Data Type**: [`MessageEvent`][twitch.types.eventsub.chat.MessageEvent]
    - **Usage**:
    ```python
    @client.event
    async def on_chat_message(data: eventsub.chat.MessageEvent):
        ...
    ```
  
---

- `on_chat_message_delete`
    - **Description**: Triggered when a chat message is deleted.
    - **Scopes**: `user:read:chat`
    - **Data Type**:  [`MessageDeleteEvent`][twitch.types.eventsub.chat.MessageDeleteEvent]
    - **Usage**:
    ```python
    @client.event
    async def on_chat_message_delete(data: eventsub.chat.MessageDeleteEvent):
        ...
    ```
  
---

- `on_chat_notification`
    - **Description**: Triggered when a chat notification is received.
    - **Scope**: `user:read:chat`
    - **Data Type**: [`NotificationEvent`][twitch.types.eventsub.chat.NotificationEvent]
    - **Usage**:
    ```python
    @client.event
    async def on_chat_notification(data: eventsub.chat.NotificationEvent):
        ...
    ```
  
---

- `on_chat_settings_update`
    - **Description**: Triggered when chat settings are updated.
    - **Scope**: `user:read:chat`
    - **Data Type**: [`SettingsUpdateEvent`][twitch.types.eventsub.chat.SettingsUpdateEvent]
    - **Usage**:
    ```python
    @client.event
    async def on_chat_settings_update(data: eventsub.chat.SettingsUpdateEvent):
        ...
    ```

## Bits Events
___

- `on_cheer`
    - **Description**: Triggered when a cheer event occurs.
    - **Scope**: `bits:read`
    - **Data Type**: [`CheerEvent`][twitch.types.eventsub.bits.CheerEvent]
    - **Usage**:
    ```python
    @client.event
    async def on_cheer(data: eventsub.bits.CheerEvent):
     ...
    ```

## Moderation Events
___

- `on_shield_mode_begin`
    - **Description**: Triggered when shield mode begins.
    - **Possible Scopes**:
         - `moderator:read:shield_mode`
         - `moderator:manage:shield_mode`
    - **Data Type**: [`ShieldModeBeginEvent`][twitch.types.eventsub.moderation.ShieldModeBeginEvent]
    - **Usage**:
    ```python
    @client.event
    async def on_shield_mode_begin(data: eventsub.moderation.ShieldModeBeginEvent):
        ...
    ```
  
---

- `on_shield_mode_end`
    - **Description**: Triggered when shield mode ends.
    - **Possible Scopes**:
         - `moderator:read:shield_mode`
         - `moderator:manage:shield_mode`
    - **Data Type**: [`ShieldModeEndEvent`][twitch.types.eventsub.moderation.ShieldModeEndEvent]
    - **Usage**:
    ```python
    @client.event
    async def on_shield_mode_end(data: eventsub.moderation.ShieldModeEndEvent):
        ...
    ```
  
---

- `on_suspicious_user_message`
    - **Description**: Triggered when a suspicious user message is detected.
    - **Scope**: `moderator:read:suspicious_users`
    - **Data Type**: [`ShieldModeBeginEvent`][twitch.types.eventsub.moderation.ShieldModeBeginEvent]
    - **Usage**:
    ```python
    @client.event
    async def on_suspicious_user_message(data: eventsub.moderation.SuspiciousUserMessageEvent):
        ...
    ```
  
---

- `on_suspicious_user_update`
    - **Description**: Triggered when a suspicious user's status is updated.
    - **Scope**: `moderator:read:suspicious_users`
    - **Data Type**: [`SuspiciousUserUpdateEvent`][twitch.types.eventsub.moderation.SuspiciousUserUpdateEvent]
    - **Usage**:
    ```python
    @client.event
    async def on_suspicious_user_update(data: eventsub.moderation.SuspiciousUserUpdateEvent):
        ...
    ```
  
---

- `on_warning_acknowledge`
    - **Description**: Triggered when a warning is acknowledged.
    - **Possible Scopes**: 
         - `moderator:read:warnings`
         - `moderator:manage:warnings`
    - **Data Type**: [`WarningAcknowledgeEvent`][twitch.types.eventsub.moderation.WarningAcknowledgeEvent]
    - **Usage**:
    ```python
    @client.event
    async def on_warning_acknowledge(data: eventsub.moderation.WarningAcknowledgeEvent):
        ...
    ```
  
---

- `on_warning_send`
    - **Description**: Triggered when a warning is sent.
    - **Possible Scopes**: 
         - `moderator:read:warnings`
         - `moderator:manage:warnings`
    - **Data Type**: [`WarningSendEvent`][twitch.types.eventsub.moderation.WarningSendEvent]
    - **Usage**:
    ```python
    @client.event
    async def on_warning_send(data: eventsub.moderation.WarningSendEvent):
        ...
    ```
  
---

- `on_automod_message_hold`
    - **Description**: Triggered when a message is held by AutoMod.
    - **Scope**: `moderator:manage:automod`
    - **Data Type**: [`AutomodMessageHoldEvent`][twitch.types.eventsub.moderation.AutomodMessageHoldEvent]
    - **Usage**:
    ```python
    @client.event
    async def on_automod_message_hold(data: eventsub.moderation.AutomodMessageHoldEvent):
        ...
    ```
  
---

- `on_automod_message_update`
    - **Description**: Triggered when an AutoMod-held message is updated.
    - **Scope**: `moderator:manage:automod`
    - **Data Type**: [`AutomodMessageUpdateEvent`][twitch.types.eventsub.moderation.AutomodMessageUpdateEvent]
    - **Usage**:
    ```python
    @client.event
    async def on_automod_message_update(data: eventsub.moderation.AutomodMessageUpdateEvent):
        ...
    ```
  
---

- `on_automod_settings_update`
    - **Description**: Triggered when AutoMod settings are updated.
    - **Scopes**: `moderator:read:automod_settings`
    - **Data Type**: [`AutomodSettingsUpdateEvent`][twitch.types.eventsub.moderation.AutomodSettingsUpdateEvent]
    - **Usage**:
    ```python
    @client.event
    async def on_automod_settings_update(data: eventsub.moderation.AutomodSettingsUpdateEvent):
        ...
    ```
  
---

- `on_automod_terms_update`
    - **Description**: Triggered when AutoMod terms are updated.
    - **Scope**: `moderator:manage:automod`
    - **Data Type**: [`AutomodTermsUpdateEvent`][twitch.types.eventsub.moderation.AutomodTermsUpdateEvent]
    - **Usage**:
    ```python
    @client.event
    async def on_automod_terms_update(data: eventsub.moderation.AutomodTermsUpdateEvent):
        ...
    ```
  
---

- `on_ban`
    - **Description**: Triggered when a user is banned.
    - **Scope**: `channel:moderate`
    - **Data Type**: [`BanEvent`][twitch.types.eventsub.moderation.BanEvent]
    - **Usage**:
    ```python
    @client.event
    async def on_ban(data: eventsub.moderation.BanEvent):
     ...
    ```
  
---

- `on_unban`
    - **Description**: Triggered when a user is unbanned.
    - **Scope**: `channel:moderate`
    - **Data Type**: [`UnbanEvent`][twitch.types.eventsub.moderation.UnbanEvent]
    - **Usage**:
    ```python
    @client.event
    async def on_unban(data: eventsub.moderation.UnbanEvent):
        ...
    ```
  
---

- `on_unban_request_create`
    - **Description**: Triggered when an unban request is created.
    - **Possible Scopes**: 
         - `moderator:read:unban_requests` 
         - `moderator:manage:unban_requests`
    - **Data Type**: [`UnbanRequestCreateEvent`][twitch.types.eventsub.moderation.UnbanRequestCreateEvent]
    - **Usage**:
    ```python
    @client.event
    async def on_unban_request_create(data: eventsub.moderation.UnbanRequestCreateEvent):
        ...
    ```
  
---

- `on_unban_request_resolve`
    - **Description**: Triggered when an unban request is resolved.
    - **Possible Scopes**: 
         - `moderator:read:unban_requests` 
         - `moderator:manage:unban_requests`
    - **Data Type**: [`UnbanRequestResolveEvent`][twitch.types.eventsub.moderation.UnbanRequestResolveEvent]
    - **Usage**:
    ```python
    @client.event
    async def on_unban_request_resolve(data: eventsub.moderation.UnbanRequestResolveEvent):
        ...
    ```
  
---

- `on_channel_moderate`
    - **Description**: Triggered when a moderation action occurs.
    - **Possible Scopes**:
         - `moderator:read:blocked_terms` OR `moderator:manage:blocked_terms`
         - `moderator:read:chat_settings` OR `moderator:manage:chat_settings`
         - `moderator:read:unban_requests` OR `moderator:manage:unban_requests`
         - `moderator:read:banned_users` OR `moderator:manage:banned_users`
         - `moderator:read:chat_messages` OR `moderator:manage:chat_messages`
         - `moderator:read:warnings` OR `moderator:manage:warnings`
         - `moderator:read:moderators`
         - `moderator:read:vips`
    - **Data Type**: [`ModerateEvent`][twitch.types.eventsub.moderation.ModerateEvent]
    - **Usage**:
    ```python
    @client.event
    async def on_channel_moderate(data: eventsub.moderation.ModerateEvent):
        ...
    ```
  
---

- `on_moderator_add`
    - **Description**: Triggered when a moderator is added.
    - **Scope**: `moderation:read`
    - **Data Type**: [`ModeratorAddEvent`][twitch.types.eventsub.moderation.ModeratorAddEvent]
    - **Usage**:
    ```python
    @client.event
    async def on_moderator_add(data: eventsub.moderation.ModeratorAddEvent):
        ...
    ```
  
---

- `on_moderator_remove`
    - **Description**: Triggered when a moderator is removed.
    - **Scope**: `moderation:read`
    - **Data Type**: [`ModeratorRemoveEvent`][twitch.types.eventsub.moderation.ModeratorRemoveEvent]
    - **Usage**:
    ```python
    @client.event
    async def on_moderator_remove(data: eventsub.moderation.ModeratorRemoveEvent):
        ...
    ```

## Channel Events
___

- `on_channel_update`
    - **Description**: Triggered when the channel is updated.
    - **Data Type**: [`ChannelUpdateEvent`][twitch.types.eventsub.channels.ChannelUpdateEvent]
    - **Usage**:
    ```python
    @client.event
    async def on_channel_update(data: eventsub.channels.ChannelUpdateEvent):
        ...
    ```

## Follow Events
___

- `on_follow`
    - **Description**: Triggered when a user follows the channel.
    - **Scope**: `moderator:read:followers`
    - **Data Type**: [`FollowEvent`][twitch.types.eventsub.channels.FollowEvent]
    - **Usage**:
    ```python
    @client.event
    async def on_follow(data: eventsub.channels.FollowEvent):
        ...
    ```

## Subscription Events
___

- `on_subscribe`
    - **Description**: Triggers when a user transitions from not subscribed to subscribed.
                       May also trigger on manual re-subs after a lapse but not for auto-renews.
    - **Scope**: `channel:read:subscriptions`
    - **Data Type**: [`SubscribeEvent`][twitch.types.eventsub.channels.SubscribeEvent]
    - **Usage**:
    ```python
    @client.event
    async def on_subscribe(data: eventsub.channels.SubscribeEvent):
        ...
    ```
  
---

- `on_subscription_end`
    - **Description**: Triggered when a user's subscription ends.
    - **Scope**: `channel:read:subscriptions`
    - **Data Type**: [`SubscriptionEndEvent`][twitch.types.eventsub.channels.SubscriptionEndEvent]
    - **Usage**:
    ```python
    @client.event
    async def on_subscription_end(data: eventsub.channels.SubscriptionEndEvent):
        ...
    ```
  
---

- `on_subscription_gift`
    - **Description**: Triggered when a subscription is gifted.
    - **Scope**: `channel:read:subscriptions`
    - **Data Type**: [`SubscriptionGiftEvent`][twitch.types.eventsub.channels.SubscriptionGiftEvent]
    - **Usage**:
    ```python
    @client.event
    async def on_subscription_gift(data: eventsub.channels.SubscriptionGiftEvent):
        ...
    ```
  
---

- `on_subscription_message`
    - **Description**: Triggered when a subscription message is received.
    - **Scope**: `channel:read:subscriptions`
    - **Data Type**: [`SubscriptionMessageEvent`][twitch.types.eventsub.channels.SubscriptionMessageEvent]
    - **Usage**:
    ```python
    @client.event
    async def on_subscription_message(data: eventsub.channels.SubscriptionMessageEvent):
        ...
    ```
  
---

- `on_vip_add`
    - **Description**: Triggered when a VIP is added.
    - **Possible Scopes**: 
         - `channel:read:vips` 
         - `channel:manage:vips`
    - **Data Type**: [`VIPAddEvent`][twitch.types.eventsub.channels.VIPAddEvent]
    - **Usage**:
    ```python
    @client.event
    async def on_vip_add(data: eventsub.channels.VIPAddEvent):
        ...
    ```
  
---

- `on_vip_remove`
    - **Description**: Triggered when a VIP is removed.
    - **Possible Scopes**: 
         - `channel:read:vips` 
         - `channel:manage:vips`
    - **Data Type**: [`VIPRemoveEvent`][twitch.types.eventsub.channels.VIPRemoveEvent]
    - **Usage**:
    ```python
    @client.event
    async def on_vip_remove(data: eventsub.channels.VIPRemoveEvent):
        ...
    ```

## Points Reward Events
___

- `on_points_automatic_reward_redemption_add`
    - **Description**: Triggered when a viewer has redeemed an automatic channel points reward.
    - **Possible Scopes**: 
         - `channel:read:redemptions` 
         - `channel:manage:redemptions`
    - **Data Type**: [`AutomaticRewardRedemptionAddEvent`][twitch.types.eventsub.interaction.AutomaticRewardRedemptionAddEvent]
    - **Usage**:
    ```python
    @client.event
    async def on_points_automatic_reward_redemption_add(data: eventsub.interaction.AutomaticRewardRedemptionAddEvent):
        ...
    ```
  
---

- `on_points_reward_add`
    - **Description**: Triggered when a custom channel points reward has been created.
    - **Possible Scopes**: 
         - `channel:read:redemptions` 
         - `channel:manage:redemptions`
    - **Data Type**: [`RewardAddEvent`][twitch.types.eventsub.interaction.PointRewardEvent]
    - **Usage**:
    ```python
    @client.event
    async def on_points_reward_add(data: eventsub.interaction.PointRewardEvent):
        ...
    ```
  
---

- `on_points_reward_update`
    - **Description**: Triggered when a custom channel points reward has been updated.
    - **Possible Scopes**: 
         - `channel:read:redemptions`
         - `channel:manage:redemptions`
    - **Custom event options**:
         - `reward_id`
    - **Data Type**: [`RewardUpdateEvent`][twitch.types.eventsub.interaction.PointRewardEvent]
    - **Usage**:
    ```python
    @client.event
    async def on_points_reward_update(data: eventsub.interaction.PointRewardEvent):
        ...
    ```
  
---

- `on_points_reward_remove`
    - **Description**: Triggered when a custom channel points reward has been removed.
    - **Possible Scopes**: 
         - `channel:read:redemptions`
         - `channel:manage:redemptions`
    - **Custom event options**:
         - `reward_id`
    - **Data Type**: [`PointRewardEvent`][twitch.types.eventsub.interaction.PointRewardEvent]
    - **Usage**:
    ```python
    @client.event
    async def on_points_reward_remove(data: eventsub.interaction.PointRewardEvent):
        ...
    ```
  
---

- `on_points_reward_redemption_add`
    - **Description**: Triggered when a viewer has redeemed a custom channel points reward.
    - **Possible Scopes**: 
         - `channel:read:redemptions` 
         - `channel:manage:redemptions`
    - **Custom event options**:
         - `reward_id`
    - **Data Type**: [`RewardRedemptionEvent`][twitch.types.eventsub.interaction.RewardRedemptionEvent]
    - **Usage**:
    ```python
    @client.event
    async def on_points_reward_redemption_add(data: eventsub.interaction.RewardRedemptionEvent):
        ...
    ```
  
---

- `on_points_reward_redemption_update`
    - **Description**: Triggered when a redemption of a channel points custom reward has been updated.
    - **Possible Scopes**: 
         - `channel:read:redemptions` 
         - `channel:manage:redemptions`
    - **Custom event options**:
         - `reward_id`
    - **Data Type**: [`RewardRedemptionEvent`][twitch.types.eventsub.interaction.RewardRedemptionEvent]
    - **Usage**:
    ```python
    @client.event
    async def on_points_reward_redemption_update(data: eventsub.interaction.RewardRedemptionEvent):
        ...
    ```

## Poll Events
___

- `on_poll_begin`
    - **Description**: Triggered when a poll begins.
    - **Possible Scopes**: 
         - `channel:read:polls` 
         - `channel:manage:polls`
    - **Data Type**: [`PollBeginEvent`][twitch.types.eventsub.interaction.PollBeginEvent]
    - **Usage**:
    ```python
    @client.event
    async def on_poll_begin(data: eventsub.interaction.PollBeginEvent):
        ...
    ```
  
---

- `on_poll_progress`
    - **Description**: Triggered when a poll progresses.
    - **Possible Scopes**: 
         - `channel:read:polls` 
         - `channel:manage:polls`
    - **Data Type**: [`PollProgressEvent`][twitch.types.eventsub.interaction.PollProgressEvent]
    - **Usage**:
    ```python
    @client.event
    async def on_poll_progress(data: eventsub.interaction.PollProgressEvent):
        ...
    ```

---

- `on_poll_end`
    - **Description**: Triggered when a poll ends.
    - **Possible Scopes**: 
         - `channel:read:polls` 
         - `channel:manage:polls`
    - **Data Type**: [`PollEndEvent`][twitch.types.eventsub.interaction.PollEndEvent]
    - **Usage**:
    ```python
    @client.event
    async def on_poll_end(data: eventsub.interaction.PollEndEvent):
        ...
    ```

## Prediction Events
___

- `on_prediction_begin`
    - **Description**: Triggered when a prediction begins.
    - **Possible Scopes**: 
         - `channel:read:predictions` 
         - `channel:manage:predictions`
    - **Data Type**: [`PredictionBeginEvent`][twitch.types.eventsub.interaction.PredictionBeginEvent]
    - **Usage**:
    ```python
    @client.event
    async def on_prediction_begin(data: eventsub.interaction.PredictionBeginEvent):
        ...
    ```
  
---

- `on_prediction_progress`
    - **Description**: Triggered when a prediction progresses.
    - **Possible Scopes**: 
         - `channel:read:predictions` 
         - `channel:manage:predictions`
    - **Data Type**: [`PredictionProgressEvent`][twitch.types.eventsub.interaction.PredictionProgressEvent]
    - **Usage**:
    ```python
    @client.event
    async def on_prediction_progress(data: eventsub.interaction.PredictionProgressEvent):
        ...
    ```
  
---

- `on_prediction_lock`
    - **Description**: Triggered when a prediction is locked.
    - **Possible Scopes**: 
         - `channel:read:predictions` 
         - `channel:manage:predictions`
    - **Data Type**: [`PredictionLockEvent`][twitch.types.eventsub.interaction.PredictionLockEvent]
    - **Usage**:
    ```python
    @client.event
    async def on_prediction_lock(data: eventsub.interaction.PredictionLockEvent):
        ...
    ```
  
---

- `on_prediction_end`
    - **Description**: Triggered when a prediction ends.
    - **Possible Scopes**: 
         - `channel:read:predictions` 
         - `channel:manage:predictions`
    - **Data Type**: [`PredictionEndEvent`][twitch.types.eventsub.interaction.PredictionEndEvent]
    - **Usage**:
    ```python
    @client.event
    async def on_prediction_end(data: eventsub.interaction.PredictionEndEvent):
        ...
    ```

## Hype Train Events
___

- `on_hype_train_begin`
    - **Description**: Triggered when a Hype Train begins.
    - **Scope**: `channel:read:hype_train`
    - **Data Type**: [`HypeTrainEvent`][twitch.types.eventsub.interaction.HypeTrainEvent]
    - **Usage**:
    ```python
    @client.event
    async def on_hype_train_begin(data: eventsub.interaction.HypeTrainEvent):
        ...
    ```
  
---

- `on_hype_train_progress`
    - **Description**: Triggered when a Hype Train progresses.
    - **Scope**: `channel:read:hype_train`
    - **Data Type**: [`HypeTrainEvent`][twitch.types.eventsub.interaction.HypeTrainEvent]
    - **Usage**:
    ```python
    @client.event
    async def on_hype_train_progress(data: eventsub.interaction.HypeTrainEvent):
        ...
    ```
  
---

- `on_hype_train_end`
    - **Description**: Triggered when a Hype Train ends.
    - **Scope**: `channel:read:hype_train`
    - **Data Type**: [`HypeTrainEndEvent`][twitch.types.eventsub.interaction.HypeTrainEndEvent]
    - **Usage**:
    ```python
    @client.event
    async def on_hype_train_end(data: eventsub.interaction.HypeTrainEndEvent):
        ...
    ```

## Charity Events
___

- `on_charity_campaign_start`
    - **Description**: Triggered when a charity campaign starts.
    - **Scope**: `channel:read:charity`
    - **Data Type**: [`CharityCampaignStartEvent`][twitch.types.eventsub.activity.CharityCampaignStartEvent]
    - **Usage**:
    ```python
    @client.event
    async def on_charity_campaign_start(data: eventsub.activity.CharityCampaignStartEvent):
        ...
    ```
  
---

- `on_charity_campaign_progress`
    - **Description**: Triggered when a charity campaign progresses.
    - **Scope**: `channel:read:charity`
    - **Data Type**: [`CharityCampaignProgressEvent`][twitch.types.eventsub.activity.CharityCampaignProgressEvent]
    - **Usage**:
    ```python
    @client.event
    async def on_charity_campaign_progress(data: eventsub.activity.CharityCampaignProgressEvent):
        ...
    ```
  
---

- `on_charity_campaign_stop`
    - **Description**: Triggered when a charity campaign stops.
    - **Scope**: `channel:read:charity`
    - **Data Type**:  [`CharityCampaignStopEvent`][twitch.types.eventsub.activity.CharityCampaignStopEvent]
    - **Usage**:
    ```python
    @client.event
    async def on_charity_campaign_stop(data: eventsub.activity.CharityCampaignStopEvent):
        ...
    ```
  
---
  
- `on_charity_campaign_donate`
    - **Description**: Triggered when a donation is made to a charity campaign.
    - **Scope**: `channel:read:charity`
    - **Data Type**: [`CharityDonationEvent`][twitch.types.eventsub.activity.CharityDonationEvent]
    - **Usage**:
    ```python
    @client.event
    async def on_charity_campaign_donate(data: eventsub.activity.CharityDonationEvent):
        ...
    ```

## Goal Events
___

- `on_goal_begin`
    - **Description**: Triggered when a goal begins.
    - **Scope**: `channel:read:goals`
    - **Data Type**: [`GoalsEvent`][twitch.types.eventsub.activity.GoalsEvent]
    - **Usage**:
    ```python
    @client.event
    async def on_goal_begin(data: eventsub.activity.GoalsEvent):
        ...
    ```
  
---

- `on_goal_progress`
    - **Description**: Triggered when a goal progresses.
    - **Scope**: `channel:read:goals`
    - **Data Type**: [`GoalsEvent`][twitch.types.eventsub.activity.GoalsEvent]
    - **Usage**:
    ```python
    @client.event
    async def on_goal_progress(data: eventsub.activity.GoalsEvent):
        ...
    ```
  
---

- `on_goal_end`
    - **Description**: Triggered when a goal ends.
    - **Scope**: `channel:read:goals`
    - **Data Type**: [`GoalsEvent`][twitch.types.eventsub.activity.GoalsEvent]
    - **Usage**:
    ```python
    @client.event
    async def on_goal_end(data: eventsub.activity.GoalsEvent):
        ...
    ```
  
## Stream Events
___

- `on_ad_break_begin`
    - **Description**: Triggered when an ad break begins on the stream.
    - **Scope**: `channel:read:ads`
    - **Data Type**: [`AdBreakBeginEvent`][twitch.types.eventsub.streams.AdBreakBeginEvent]
    - **Usage**:
    ```python
    @client.event
    async def on_ad_break_begin(data: eventsub.streams.AdBreakBeginEvent):
        ...
    ```

---

- `on_raid`
    - **Description**: Triggered when a raid starts on the stream.
    - **Data Type**: [`RaidEvent`][twitch.types.eventsub.streams.RaidEvent]
    - **Usage**:
    ```python
    @client.event
    async def on_raid(data: eventsub.streams.RaidEvent):
        ...
    ```
  
---

- `on_shoutout_create`
    - **Description**: Triggered when a shoutout is created.
    - **Possible Scopes**: 
         - `moderator:read:shoutouts` 
         - `moderator:manage:shoutouts`
    - **Data Type**: [`ShoutoutCreateEvent`][twitch.types.eventsub.streams.ShoutoutCreateEvent]
    - **Usage**:
    ```python
    @client.event
    async def on_shoutout_create(data: eventsub.streams.ShoutoutCreateEvent):
        ...
    ```
  
---

- `on_shoutout_received`
    - **Description**: Triggered when a shoutout is received.
    - **Possible Scopes**: 
         - `moderator:read:shoutouts` 
         - `moderator:manage:shoutouts`
    - **Data Type**: [`ShoutoutReceivedEvent`][twitch.types.eventsub.streams.ShoutoutReceivedEvent]
    - **Usage**:
    ```python
    @client.event
    async def on_shoutout_received(data: eventsub.streams.ShoutoutReceivedEvent):
        ...
    ```
  
---

- `on_stream_online`
    - **Description**: Triggered when a stream goes live.
    - **Data Type**: [`StreamOnlineEvent`][twitch.types.eventsub.streams.StreamOnlineEvent]
    - **Usage**:
    ```python
    @client.event
    async def on_stream_online(data: eventsub.streams.StreamOnlineEvent):
        ...
    ```
  
---

- `on_stream_offline`
    - **Description**: Triggered when a stream goes offline.
    - **Data Type**: [`StreamOfflineEvent`][twitch.types.eventsub.streams.StreamOfflineEvent]
    - **Usage**:
    ```python
    @client.event
    async def on_stream_offline(data: eventsub.streams.StreamOfflineEvent):
        ...
    ```

## User Events
___

- `on_user_update`
    - **Description**: Triggered when a user updates their profile, such as changing their display name or profile image.
    - **Optional Scope**: `user:read:email`
    - **Data Type**: [`UserUpdateEvent`][twitch.types.eventsub.users.UserUpdateEvent]
    - **Usage**:
    ```python
    @client.event
    async def on_user_update(data: eventsub.users.UserUpdateEvent):
        ...
    ```

---

- `on_whisper_received`
    - **Description**: Triggered when a user receives a whisper message.
    - **Possible Scopes**: 
         - `user:read:whispers` 
         - `user:manage:whispers`
    - **Data Type**: [`WhisperReceivedEvent`][twitch.types.eventsub.users.WhisperReceivedEvent]
    - **Usage**:
    ```python
    @client.event
    async def on_whisper_received(data: eventsub.users.WhisperReceivedEvent):
        ...
    ```

---

- `on_chat_user_message_hold`
    - **Description**: Triggered when a chat message from a user is held by AutoMod.
    - **Possible Scopes**: 
         - `user:read:whispers` 
         - `user:manage:whispers`
    - **Possible Scopes**: 
         - `user:read:chat` - Receive chatroom messages and informational notifications relating to a channel’s chatroom.
    - **Data Type**: [`MessageHoldEvent`][twitch.types.eventsub.users.MessageHoldEvent]
    - **Usage**:
    ```python
    @client.event
    async def on_chat_user_message_hold(data: eventsub.users.MessageHoldEvent):
        ...
    ```

---

- `on_chat_user_message_update`
    - **Description**: Triggered when a held chat message from a user is updated by AutoMod.
    - **Scope**: `user:read:chat`
    - **Possible Scopes**: 
         - `user:read:chat` - Receive chatroom messages and informational notifications relating to a channel’s chatroom.
    - **Data Type**: [`MessageUpdateEvent`][twitch.types.eventsub.users.MessageUpdateEvent]
    - **Usage**:
    ```python
    @client.event
    async def on_chat_user_message_update(data: eventsub.users.MessageUpdateEvent):
        ...
    ```
  