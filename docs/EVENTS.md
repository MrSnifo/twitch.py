# Events Documentation

## Table of Contents
- [on_connect()](#on_connect)
- [on_ready()](#on_ready)
- [on_refresh_token(access_token: str)](#on_refresh_tokenaccess_token-str)
- [on_channel_update(channel: Channel)](#on_channel_updatechannel-channel)
- [on_follow(user: Follower)](#on_followuser-follower)
- [on_subscribe(subscribe: Subscription)](#on_subscribesubscribe-subscription)
- [on_subscription_end(subscription: Subscription)](#on_subscription_endsubscribe-subscription)
- [on_subscription_gift(subscription: SubscriptionGift)](#on_subscription_giftsubscription-subscriptiongift)
- [on_subscription_message(subscription: SubscriptionMessage)](#on_subscription_messagesubscription-subscriptionmessage)
- [on_cheer(cheer: Cheer)](#on_cheercheer-cheer)
- [on_raid(raid: Raid)](#on_raidraid-raid)
- [on_ban(ban: Ban)](#on_banban-ban)
- [on_unban(unban: UnBan)](#on_unbanunban-unban)
- [on_moderator_add(user: User)](#on_moderator_adduser-user)
- [on_moderator_remove(user: User)](#on_moderator_removeuser-user)
- [on_points_reward_add(reward: Reward)](#on_points_reward_addreward-reward)
- [on_points_reward_update(reward: Reward)](#on_points_reward_updatereward-reward)
- [on_points_reward_remove(reward: Reward)](#on_points_reward_removereward-reward)
- [on_points_reward_redemption(redemption: Redemption)](#on_points_reward_redemptionredemption-redemption)
- [on_points_reward_redemption_update(redemption: Redemption)](#on_points_reward_redemption_updateredemption-redemption)
- [on_poll_begin(poll: Poll)](#on_poll_beginpoll-poll)
- [on_poll_progress(poll: Poll)](#on_poll_progresspoll-poll)
- [on_poll_end(poll: Poll)](#on_poll_endpoll-poll)
- [on_prediction_begin(prediction: Prediction)](#on_prediction_beginprediction-prediction)
- [on_prediction_progress(prediction: Prediction)](#on_prediction_progressprediction-prediction)
- [on_prediction_lock(prediction: Prediction)](#on_prediction_lockprediction-prediction)
- [on_charity_campaign_donate(donation: Donation)](#on_charity_campaign_donatedonation-donation)
- [on_charity_campaign_start(charity: Charity)](#on_charity_campaign_startcharity-charity)
- [on_charity_campaign_progress(charity: Charity)](#on_charity_campaign_progresscharity-charity)
- [on_charity_campaign_stop(charity: Charity)](#on_charity_campaign_stopcharity-charity)
- [on_goal_begin(goal: Goal)](#on_goal_begingoal-goal)
- [on_goal_progress(goal: Goal)](#on_goal_progressgoal-goal)
- [on_goal_end(goal: Goal)](#on_goal_endgoal-goal)
- [on_hype_train_begin(train: HyperTrain)](#on_hype_train_begintrain-hypertrain)
- [on_hype_train_progress(train: HyperTrain)](#on_hype_train_progresstrain-hypertrain)
- [on_hype_train_end(train: HyperTrain)](#on_hype_train_endtrain-hypertrain)
- [on_shield_mode_begin(mode: ShieldMode)](#on_shield_mode_beginmode-shieldmode)
- [on_shield_mode_end(mode: ShieldMode)](#on_shield_mode_endmode-shieldmode)
- [on_shoutout_create(shoutout: Shoutout)](#on_shoutout_createshoutout-shoutout)
- [on_shoutout_receive(shoutout: Shoutout)](#on_shoutout_receiveshoutout-shoutout)
- [on_stream_online(stream: Online)](#on_stream_onlinestream-online)
- [on_stream_offline(stream: Offline)](#on_stream_offlinestream-offline)
- [on_user_update(user: Update)](#on_user_updateuser-update)

---

### on_connect()

This event is triggered when the client successfully connected to the eventsub websocket.

---

### on_ready()

This event is triggered when the client is ready to start processing events.

---

### on_refresh_token(access_token: str)

This event is triggered when the client receives a new access token.

- `access_token` (str): The new access token.

---

### on_channel_update(channel: Channel)

This event is triggered when a channel is updated.

- `channel` (twitch.channel.Channel): The updated channel.

---

### on_follow(user: Follower)

This event is triggered when a user follows the channel.

- `user` (twitch.user.Follower): The user who followed the channel.

---

### on_subscribe(subscribe: Subscription)

This event is triggered when a user subscribes to the channel.

- `subscribe` (twitch.channel.Subscription): The subscription information.

---

### on_subscription_end(subscribe: Subscription)

This event is triggered when a user's subscription to the channel ends.

- `subscribe` (twitch.channel.Subscription): The subscription information.

---

### on_subscription_gift(subscription: SubscriptionGift)

This event is triggered when a user gifts a subscription to the channel.

- `subscription` (twitch.channel.SubscriptionGift): The subscription gift information.

---

### on_subscription_message(subscription: SubscriptionMessage)

This event is triggered when a user resubscribes to the channel.

- `subscription` (twitch.channel.SubscriptionMessage): The resubscription information.

---

### on_cheer(cheer: Cheer)

This event is triggered when a user sends a cheer to the channel.

- `cheer` (twitch.channel.Cheer): The cheer information.

---

### on_raid(raid: Raid)

This event is triggered when the channel receives a raid from another channel.

- `raid` (twitch.channel.Raid): The raid information.

---

### on_ban(ban: Ban)

This event is triggered when a user is banned from the channel.

- `ban` (twitch.moderation.Ban): The banned user information.

---

### on_unban(unban: UnBan)

This event is triggered when a user is unbanned from the channel.

- `unban` (twitch.moderation.UnBan): The unbanned user information.

---

### on_moderator_add(user: User)

This event is triggered when a user is added as a moderator for the channel.

- `user` (twitch.user.User): The user who was added as a moderator.

---

### on_moderator_remove(user: User)

This event is triggered when a user is removed as a moderator from the channel.

- `user` (twitch.user.User): The user who was removed as a moderator.

---

### on_points_reward_add(reward: Reward)

This event is triggered when a new channel points reward is added.

- `reward` (twitch.reward.Reward): The new reward information.

---

### on_points_reward_update(reward: Reward)

This event is triggered when an existing channel points reward is updated.

- `reward` (twitch.reward.Reward): The updated reward information.

---

### on_points_reward_remove(reward: Reward)

This event is triggered when a channel points reward is removed.

- `reward` (twitch.reward.Reward): The removed reward information.

---

### on_points_reward_redemption(redemption: Redemption)

This event is triggered when a viewer redeems a channel points reward.

- `redemption` (twitch.reward.Redemption): The redemption information.

---

### on_points_reward_redemption_update(redemption: Redemption)

This event is triggered when the status of a channel points reward redemption is updated.

- `redemption` (twitch.reward.Redemption): The updated redemption information.

---

### on_poll_begin(poll: Poll)

This event is triggered when a poll begins in the channel.

- `poll` (twitch.survey.Poll): The poll information.

---

### on_poll_progress(poll: Poll)

This event is triggered when there is progress or updates in an ongoing poll.

- `poll` (twitch.survey.Poll): The poll information.

---

### on_poll_end(poll: Poll)

This event is triggered when a poll ends in the channel.

- `poll` (twitch.survey.Poll): The poll information.

---

### on_prediction_begin(prediction: Prediction)

This event is triggered when a prediction begins in the channel.

- `prediction` (twitch.survey.Prediction): The prediction information.

---

### on_prediction_progress(prediction: Prediction)

This event is triggered when there is progress or updates in an ongoing prediction.

- `prediction` (twitch.survey.Prediction): The prediction information.

---

### on_prediction_lock(prediction: Prediction)

This event is triggered when a prediction is locked and can no longer be modified.

- `prediction` (twitch.survey.Prediction): The prediction information.

---

### on_charity_campaign_donate(donation: Donation)

This event is triggered when a viewer donates to a charity campaign.

- `donation` (twitch.goals.Donation): The donation information.

---

### on_charity_campaign_start(charity: Charity)

This event is triggered when a charity campaign starts in the channel.

- `charity` (twitch.goals.Charity): The charity campaign information.

---

### on_charity_campaign_progress(charity: Charity)

This event is triggered when there is progress or updates in an ongoing charity campaign.

- `charity` (twitch.goals.Charity): The charity campaign information.

---

### on_charity_campaign_stop(charity: Charity)

This event is triggered when a charity campaign ends in the channel.

- `charity` (twitch.goals.Charity): The charity campaign information.

---

### on_goal_begin(goal: Goal)

This event is triggered when a goal begins in the channel.

- `goal` (twitch.goals.Goal): The goal information.

---

### on_goal_progress(goal: Goal)

This event is triggered when there is progress or updates in an ongoing goal.

- `goal` (twitch.goals.Goal): The goal information.

---

### on_goal_end(goal: Goal)

This event is triggered when a goal ends in the channel.

- `goal` (twitch.goals.Goal): The goal information.

---

### on_hype_train_begin(train: HyperTrain)

This event is triggered when a Hype Train begins in the channel.

- `train` (twitch.goals.HyperTrain): The Hype Train information.

---

### on_hype_train_progress(train: HyperTrain)

This event is triggered when there is progress or updates in an ongoing Hype Train.

- `train` (twitch.goals.HyperTrain): The Hype Train information.

---

### on_hype_train_end(train: HyperTrain)

This event is triggered when a Hype Train ends in the channel.

- `train` (twitch.goals.HyperTrain): The Hype Train information.

---

### on_shield_mode_begin(mode: ShieldMode)

This event is triggered when the channel enters Shield Mode.

- `mode` (twitch.moderation.ShieldMode): The Shield Mode information.

---

### on_shield_mode_end(mode: ShieldMode)

This event is triggered when the channel exits Shield Mode.

- `mode` (twitch.moderation.ShieldMode): The Shield Mode information.

---

### on_shoutout_create(shoutout: Shoutout)

This event is triggered when a shoutout is created for another channel.

- `shoutout` (twitch.stream.Shoutout): The shoutout information.

---

### on_shoutout_receive(shoutout: Shoutout)

This event is triggered when the channel receives a shoutout from another channel.

- `shoutout` (twitch.stream.Shoutout): The shoutout information.

---

### on_stream_online(stream: Online)

This event is triggered when the channel goes live and starts streaming.

- `stream` (twitch.stream.Online): The stream information.

---

### on_stream_offline(stream: Offline)

This event is triggered when the channel stops streaming and goes offline.

- `stream` (twitch.stream.Offline): The stream information.

---

### on_user_update(user: Update)

This event is triggered when a user's information is updated.

- `user` (twitch.user.Update): The updated user information.
