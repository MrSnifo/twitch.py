# Events Documentation
All events must be **coroutine Function**.

## Table of Contents
- [on_connect()](#async-def-on_connect)
- [on_ready()](#async-def-on_ready)
- [on_refresh_token(access_token: str)](#async-def-on_refresh_tokenaccess_token-str)
- [on_channel_update(channel: ChannelUpdate)](#async-def-on_channel_updatechannel-channelupdate)
- [on_follow(user: Follower)](#async-def-on_followuser-follower)
- [on_subscribe(subscribe: Subscription)](#async-def-on_subscribesubscribe-subscription)
- [on_subscription_end(subscription: Subscription)](#async-def-on_subscription_endsubscribe-subscription)
- [on_subscription_gift(subscription: SubscriptionGift)](#async-def-on_subscription_giftsubscription-subscriptiongift)
- [on_subscription_message(subscription: SubscriptionMessage)](#async-def-on_subscription_messagesubscription-subscriptionmessage)
- [on_cheer(cheer: Cheer)](#async-def-on_cheercheer-cheer)
- [on_raid(raid: Raid)](#async-def-on_raidraid-raid)
- [on_ban(ban: Ban)](#async-def-on_banban-ban)
- [on_unban(unban: UnBan)](#async-def-on_unbanunban-unban)
- [on_moderator_add(user: User)](#async-def-on_moderator_adduser-user)
- [on_moderator_remove(user: User)](#async-def-on_moderator_removeuser-user)
- [on_points_reward_add(reward: Reward)](#async-def-on_points_reward_addreward-reward)
- [on_points_reward_update(reward: Reward)](#async-def-on_points_reward_updatereward-reward)
- [on_points_reward_remove(reward: Reward)](#async-def-on_points_reward_removereward-reward)
- [on_points_reward_redemption(redemption: Redemption)](#async-def-on_points_reward_redemptionredemption-redemption)
- [on_points_reward_redemption_update(redemption: Redemption)](#async-def-on_points_reward_redemption_updateredemption-redemption)
- [on_poll_begin(poll: Poll)](#async-def-on_poll_beginpoll-poll)
- [on_poll_progress(poll: Poll)](#async-def-on_poll_progresspoll-poll)
- [on_poll_end(poll: Poll)](#async-def-on_poll_endpoll-poll)
- [on_prediction_begin(prediction: Prediction)](#async-def-on_prediction_beginprediction-prediction)
- [on_prediction_progress(prediction: Prediction)](#async-def-on_prediction_progressprediction-prediction)
- [on_prediction_lock(prediction: Prediction)](#async-def-on_prediction_lockprediction-prediction)
- [on_charity_campaign_donate(donation: Donation)](#async-def-on_charity_campaign_donatedonation-donation)
- [on_charity_campaign_start(charity: Charity)](#async-def-on_charity_campaign_startcharity-charity)
- [on_charity_campaign_progress(charity: Charity)](#async-def-on_charity_campaign_progresscharity-charity)
- [on_charity_campaign_stop(charity: Charity)](#async-def-on_charity_campaign_stopcharity-charity)
- [on_goal_begin(goal: Goal)](#async-def-on_goal_begingoal-goal)
- [on_goal_progress(goal: Goal)](#async-def-on_goal_progressgoal-goal)
- [on_goal_end(goal: Goal)](#async-def-on_goal_endgoal-goal)
- [on_hype_train_begin(train: HyperTrain)](#async-def-on_hype_train_begintrain-hypertrain)
- [on_hype_train_progress(train: HyperTrain)](#async-def-on_hype_train_progresstrain-hypertrain)
- [on_hype_train_end(train: HyperTrain)](#async-def-on_hype_train_endtrain-hypertrain)
- [on_shield_mode_begin(mode: ShieldMode)](#async-def-on_shield_mode_beginmode-shieldmode)
- [on_shield_mode_end(mode: ShieldMode)](#async-def-on_shield_mode_endmode-shieldmode)
- [on_shoutout_create(shoutout: Shoutout)](#async-def-on_shoutout_createshoutout-shoutout)
- [on_shoutout_receive(shoutout: Shoutout)](#async-def-on_shoutout_receiveshoutout-shoutout)
- [on_stream_online(stream: Online)](#async-def-on_stream_onlinestream-online)
- [on_stream_offline(stream: Offline)](#async-def-on_stream_offlinestream-offline)
- [on_user_update(user: Update)](#async-def-on_user_updateuser-userupdate)
- [on_guest_star_session_begin(guest_star: GuestStar)](#async-def-on_guest_star_session_beginguest_star-gueststar)
- [on_guest_star_session_end(guest_star: GuestStar)](#async-def-on_guest_star_session_endguest_star-gueststar)
- [on_guest_star_guest_update(guest_star: GuestStarUpdate)](#async-def-on_guest_star_guest_updateguest_star-gueststarupdate)
- [on_guest_star_slot_update(guest_star: GuestStarSlotUpdate)](#async-def-on_guest_star_slot_updateguest_star-gueststarslotupdate)
- [on_guest_star_settings_update(guest_star: GuestStarSettingsUpdate)](#async-def-on_guest_star_settings_updateguest_star-gueststarsettingsupdate)

---

# Client
### `async def on_connect()`
This event is triggered when the client successfully connected to the eventsub websocket.
#
### `async def on_ready()`
This event is triggered when the client is ready to start processing events.
#
### `async def on_refresh_token(access_token: str)`
This event is triggered when the client receives a new access token.
- `access_token` (str)`: The new access token.

---

# Channel
### `async def on_channel_update(channel: ChannelUpdate)`
This event is triggered when a channel is updated.
- `channel` (twitch.channel.ChannelUpdate)`: The updated channel.
#
### `async def on_follow(user: Follower)`
This event is triggered when a user follows the channel.
- `user` (twitch.user.Follower)`: The user who followed the channel.
#
### `async def on_subscribe(subscribe: Subscription)`
This event is triggered when a user subscribes to the channel.
- `subscribe` (twitch.channel.Subscription)`: The subscription information.
#
### `async def on_subscription_end(subscribe: Subscription)`
This event is triggered when a user's subscription to the channel ends.
- `subscribe` (twitch.channel.Subscription)`: The subscription information.
#
### `async def on_subscription_gift(subscription: SubscriptionGift)`
This event is triggered when a user gifts a subscription to the channel.
- `subscription` (twitch.channel.SubscriptionGift)`: The subscription gift information.
#
### `async def on_subscription_message(subscription: SubscriptionMessage)`
This event is triggered when a user resubscribes to the channel.
- `subscription` (twitch.channel.SubscriptionMessage)`: The resubscription information.
#
### `async def on_cheer(cheer: Cheer)`
This event is triggered when a user sends a cheer to the channel.
- `cheer` (twitch.channel.Cheer)`: The cheer information.
#
### `async def on_raid(raid: Raid)`
This event is triggered when the channel receives a raid from another channel.
- `raid` (twitch.channel.Raid)`: The raid information.

---

# Moderation
### `async def on_ban(ban: Ban)`
This event is triggered when a user is banned from the channel.
- `ban` (twitch.moderation.Ban)`: The banned user information.
#
### `async def on_unban(unban: UnBan)`
This event is triggered when a user is unbanned from the channel.
- `unban` (twitch.moderation.UnBan)`: The unbanned user information.
#
### `async def on_moderator_add(user: User)`
This event is triggered when a user is added as a moderator for the channel.
- `user` (twitch.user.User)`: The user who was added as a moderator.
#
### `async def on_moderator_remove(user: User)`
This event is triggered when a user is removed as a moderator from the channel.
- `user` (twitch.user.User)`: The user who was removed as a moderator.

---

# Reward
### `async def on_points_reward_add(reward: Reward)`
This event is triggered when a new channel points reward is added.
- `reward` (twitch.reward.Reward)`: The new reward information.
#
### `async def on_points_reward_update(reward: Reward)`
This event is triggered when an existing channel points reward is updated.
- `reward` (twitch.reward.Reward)`: The updated reward information.
#
### `async def on_points_reward_remove(reward: Reward)`
This event is triggered when a channel points reward is removed.
- `reward` (twitch.reward.Reward)`: The removed reward information.
#
### `async def on_points_reward_redemption(redemption: Redemption)`
This event is triggered when a viewer redeems a channel points reward.
- `redemption` (twitch.reward.Redemption)`: The redemption information.
#
### `async def on_points_reward_redemption_update(redemption: Redemption)`
This event is triggered when the status of a channel points reward redemption is updated.
- `redemption` (twitch.reward.Redemption)`: The updated redemption information.

---

# Poll
### `async def on_poll_begin(poll: Poll)`
This event is triggered when a poll begins in the channel.
- `poll` (twitch.survey.Poll)`: The poll information.
#
### `async def on_poll_progress(poll: Poll)`
This event is triggered when there is progress or updates in an ongoing poll.
- `poll` (twitch.survey.Poll)`: The poll information.
#
### `async def on_poll_end(poll: Poll)`
This event is triggered when a poll ends in the channel.
- `poll` (twitch.survey.Poll)`: The poll information.

---

# Prediction
### `async def on_prediction_begin(prediction: Prediction)`
This event is triggered when a prediction begins in the channel.
- `prediction` (twitch.survey.Prediction)`: The prediction information.
#
### `async def on_prediction_progress(prediction: Prediction)`
This event is triggered when there is progress or updates in an ongoing prediction.
- `prediction` (twitch.survey.Prediction)`: The prediction information.
#
### `async def on_prediction_lock(prediction: Prediction)`
This event is triggered when a prediction is locked and can no longer be modified.
- `prediction` (twitch.survey.Prediction)`: The prediction information.

---

# Charity
### `async def on_charity_campaign_donate(donation: Donation)`
This event is triggered when a viewer donates to a charity campaign.
- `donation` (twitch.goals.Donation)`: The donation information.
#
### `async def on_charity_campaign_start(charity: Charity)`
This event is triggered when a charity campaign starts in the channel.
- `charity` (twitch.goals.Charity)`: The charity campaign information.
#
### `async def on_charity_campaign_progress(charity: Charity)`
This event is triggered when there is progress or updates in an ongoing charity campaign.
- `charity` (twitch.goals.Charity)`: The charity campaign information.
#
### `async def on_charity_campaign_stop(charity: Charity)`
This event is triggered when a charity campaign ends in the channel.
- `charity` (twitch.goals.Charity)`: The charity campaign information.

---

# Goal
### `async def on_goal_begin(goal: Goal)`
This event is triggered when a goal begins in the channel.
- `goal` (twitch.goals.Goal)`: The goal information.
#
### `async def on_goal_progress(goal: Goal)`
This event is triggered when there is progress or updates in an ongoing goal.
- `goal` (twitch.goals.Goal)`: The goal information.
#
### `async def on_goal_end(goal: Goal)`
This event is triggered when a goal ends in the channel.
- `goal` (twitch.goals.Goal)`: The goal information.

---

# HyperTrain
### `async def on_hype_train_begin(train: HyperTrain)`
This event is triggered when a Hype Train begins in the channel.
- `train` (twitch.goals.HyperTrain)`: The Hype Train information.
#
### `async def on_hype_train_progress(train: HyperTrain)`
This event is triggered when there is progress or updates in an ongoing Hype Train.
- `train` (twitch.goals.HyperTrain)`: The Hype Train information.
#
### `async def on_hype_train_end(train: HyperTrain)`
This event is triggered when a Hype Train ends in the channel.
- `train` (twitch.goals.HyperTrain)`: The Hype Train information.

---

# ShieldMode
### `async def on_shield_mode_begin(mode: ShieldMode)`
This event is triggered when the channel enters Shield Mode.
- `mode` (twitch.moderation.ShieldMode)`: The Shield Mode information.
#
### `async def on_shield_mode_end(mode: ShieldMode)`
This event is triggered when the channel exits Shield Mode.
- `mode` (twitch.moderation.ShieldMode)`: The Shield Mode information.

---

# Shoutout
### `async def on_shoutout_create(shoutout: Shoutout)`
This event is triggered when a shoutout is created for another channel.
- `shoutout` (twitch.stream.Shoutout)`: The shoutout information.
#
### `async def on_shoutout_receive(shoutout: Shoutout)`
This event is triggered when the channel receives a shoutout from another channel.
- `shoutout` (twitch.stream.Shoutout)`: The shoutout information.

---

# Stream
### `async def on_stream_online(stream: Online)`
This event is triggered when the channel goes live and starts streaming.
- `stream` (twitch.stream.Online)`: The stream information.
#
### `async def on_stream_offline(stream: Offline)`
This event is triggered when the channel stops streaming and goes offline.
- `stream` (twitch.stream.Offline)`: The stream information.

---

# User
### `async def on_user_update(user: UserUpdate)`
This event is triggered when a user's information is updated.
- `user` (twitch.user.UserUpdate)`: The updated user information.

---

# GuestStar
### `async def on_guest_star_session_begin(guest_star: GuestStar)`
This event is triggered when a guest star session begins in the channel.
- `guest_star` (twitch.guest.GuestStar)`: The guest star session information.
#
### `async def on_guest_star_session_end(guest_star: GuestStar)`
This event is triggered when a guest star session ends in the channel.
- `guest_star` (twitch.guest.GuestStar)`: The guest star session information.
#
### `async def on_guest_star_guest_update(guest_star: GuestStarUpdate)`
This event is triggered when there is an update in the guest star information.
- `guest_star` (twitch.guest.GuestStarUpdate)`: The updated guest star information.
#
### `async def on_guest_star_slot_update(guest_star: GuestStarSlotUpdate)`
This event is triggered when there is an update in the guest star slot information.
- `guest_star` (twitch.guest.GuestStarSlotUpdate)`: The updated guest star slot information.
#
### `async def on_guest_star_settings_update(guest_star: GuestStarSettingsUpdate)`
This event is triggered when there is an update in the guest star settings.
- `guest_star` (twitch.guest.GuestStarSettingsUpdate): The updated guest star settings.
