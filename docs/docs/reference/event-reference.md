---
icon: material/clock-time-eleven-outline
---

There are two methods for event registration: 

1. Using [Client.event()][twitch.client.Client.event].
2. Subclassing [Client][twitch.client.Client] and overriding specific events.

An example with event decorator:
```py
@client.event
async def on_follow(user):
    print(user.name, 'just followed me!')
```

## Authorization
___
```py
async def on_auth_url(url, uri):
```
This called when the authentication URL is generated.
##### Parameters:
:   * `url` ([str][str]) - The authentication URL.
* `uri` ([str][str]) - The Redirect URI.

---

```py
async def on_auth(access_token, refresh_token):
```
This called when the client is successfully authenticated.
##### Parameters:
:   * `access_token` ([str][str]) - User access token.
* `refresh_token` ([str][str]) - User refresh token.

---

```py
async def on_refresh_token(access_token, refresh_token):
```
*Require `client secret` and `refresh token`.*

This called when a new access token has been generated.


##### Parameters:
:   * `access_token` ([str][str]) - User access token.


## Gateway
___
```py
async def on_ready():
```
This called when the Twitch client is ready to receive events.

---

```py
async def on_connect():
```
This called when the client has successfully established a connection to the WebSocket.
However, it does not indicate that the client is fully prepared. For full readiness,
refer to the `on_ready()` callback.

---

```py
async def on_reconnect():
```
This called when the Twitch client switches to a new EventSub WebSocket.

For more information on reconnecting
[read this](https://dev.twitch.tv/docs/eventsub/handling-websocket-events/#reconnect-message).


## Debug
___
```py
async def on_error(event_name, /, *args, **kwargs):
```
The default error handler provided by the client can be overridden 
if you don't want to receive logger errors.
##### Parameters:
:   * `event_name` ([str][str]) - Event name.

---

```py
async def on_socket_raw_receive(msg):
```
This called when the Twitch client receives a raw message from the WebSocket.
Typically, before parsing events from the message.
##### Parameters:
:   * `msg` ([str][str]) - Websocket receive message.



## User
___
```py
async def on_user_update(user):
```
This called when a client information is updated.
##### Parameters:
:   * `user` ([ClientUser][twitch.broadcaster.ClientUser]) - The client user.
##### Scopes:
:   * `user:read:email` - The notification will include email field (default).



## Channel
___
```py
async def on_channel_update(channel):
```
This called when client channel is updated.
##### Parameters:
:   * `channel` ([ClientChannel][twitch.broadcaster.ClientChannel]) - The client channel.

---

```py
async def on_follow(user):
```
This called when a user follows the channel.
##### Parameters:
:   * `user` ([Follow][twitch.channel.Follow]) - The user who followed the channel.
##### Scopes:
:   * `moderator:read:followers`

---

```py
async def on_subscribe(subscriber):
```
This called when a user subscribes to the channel.
##### Parameters:
:   * `subscriber` ([Subscriber][twitch.alerts.Subscriber]) - The subscriber who has subscribed to the channel.
##### Scopes:
:   * `channel:read:subscriptions`

---

```py
async def on_resubscribe(subscriber):
```
This called when a user resubscribes to the channel.
##### Parameters:
:   * `subscriber` ([Subscriber][twitch.alerts.Subscriber]) - The user who has resubscribed to the channel.
##### Scopes:
:   * `channel:read:subscriptions`

---

```py
async def on_subscription_end(subscriber):
```
This called when a user's subscription ends.
##### Parameters:
:   * `subscriber` ([Subscriber][twitch.alerts.Subscriber]) - The user whose subscription has ended.
##### Scopes:
:   * `channel:read:subscriptions`

---

```py
async def on_subscription_gift(gifter):
```
This called when a user gifts a subscription.
##### Parameters:
:   * `gifter` ([Gifter][twitch.alerts.Gifter]) - The user who gifted the subscription.
##### Scopes:
:   * `channel:read:subscriptions`

---

```py
async def on_cheer(cheerer):
```
This called when a user sends a cheer to the channel.
##### Parameters:
:   * `cheerer` ([Cheerer][twitch.alerts.Cheerer]) - The user who cheered the channel.
##### Scopes:
:   * `bits:read`

---

```py
async def on_raid(raider):
```
This called when the channel receives a raid from another channel.
##### Parameters:
:   * `raider` ([Raider][twitch.alerts.Raider]) - The user who raided the channel.



## Moderation
___
```py
async def on_moderator_add(user):
```
This called when a user is added as a moderator for the channel.
##### Parameters:
:   * `user` ([BaseUser][twitch.user.BaseUser]) - The new moderator.
##### Scopes:
:   * `moderation:read`

---

```py
async def on_moderator_remove(user):
```
This called when a user is removed as a moderator from the channel.
##### Parameters:
:   * `user` ([BaseUser][twitch.user.BaseUser]) - The old moderator.
##### Scopes:
:   * `moderation:read`

---

```py
async def on_ban(banned):
```
This called when a user is banned from the channel.
##### Parameters:
:   * `banned` ([BannedUser][twitch.channel.BannedUser]) - The user who has been banned.
##### Scopes:
:   * `channel:moderate`


```py
async def on_unban(user, moderator):
```
This called when a user is unbanned from the channel.
##### Parameters:
:   * `user` ([BaseUser][twitch.user.BaseUser]) - The user who was unbanned.
* `moderator` ([moderator][twitch.user.BaseUser]) - The moderator who performed the unbanning action.
##### Scopes:
:   * `channel:moderate`


## ShieldMode
___
```py
async def on_shield_mode_begin(mode):
```
This called when the channel's Shield Mode is enabled.
##### Parameters:
:   * `mode` ([ShieldModeSettings][twitch.chat.ShieldModeSettings]) - The current state of Shield Mode.
##### Scopes:
:   * `moderator:read:shield_mode`
 
---

```py
async def on_shield_mode_end(mode):
```
This called when the channel's Shield Mode is disabled.
##### Parameters:
:   * `mode` ([ShieldModeSettings][twitch.chat.ShieldModeSettings]) - The current state of Shield Mode.
##### Scopes:
:   * `moderator:read:shield_mode`


## Reward
___
```py
async def on_points_reward_add(reward):
```
This called when a new channel points reward is added.
##### Parameters:
:   * `reward` ([Reward][twitch.reward.Reward]) - The channel reward.
##### Scopes:
:   * `channel:read:redemptions`
 

---

```py
async def on_points_reward_update(reward):
```
This called when an existing channel points reward is updated.
##### Parameters:
:   * `reward` ([Reward][twitch.reward.Reward]) - The channel reward.
##### Scopes:
:   * `channel:read:redemptions`

---

```py
async def on_points_reward_remove(reward):
```
This called when a channel points reward is removed.
##### Parameters:
:   * `reward` ([Reward][twitch.reward.Reward]) - The channel reward.
##### Scopes:
:   * `channel:read:redemptions`

---

```py
async def on_points_reward_redemption(redemption):
```
This called when a user redeems a channel points reward.
##### Parameters:
:   * `reward` ([Reward][twitch.reward.Redemption]) - The user's reward redemption.
##### Scopes:
:   * `channel:read:redemptions`

---

```py
async def on_points_reward_redemption_update(redemption):
```
This called when the status of a reward redemption is updated.
##### Parameters:
:   * `reward` ([Reward][twitch.reward.Redemption]) - The reward redemption status.
##### Scopes:
:   * `channel:read:redemptions`



## Poll
___
```py
async def on_poll_begin(poll):
```
This called when a poll begins in the channel.
##### Parameters:
:   * `poll` ([Poll][twitch.poll.Poll]) - The poll information.
##### Scopes:
:   * `channel:read:polls`

---

```py
async def on_poll_progress(poll):
```
This called when the poll is updated or in progress.
##### Parameters:
:   * `poll` ([Poll][twitch.poll.Poll]) - The poll information.
##### Scopes:
:   * `channel:read:polls`

---

```py
async def on_poll_end(poll):
```
This called when a poll ends in the channel.
##### Parameters:
:   * `poll` ([Poll][twitch.poll.Poll]) - The poll information.
##### Scopes:
:   * `channel:read:polls`



## Prediction
___
```py
async def on_prediction_begin(prediction):
```
This called when a prediction begins in the channel.
##### Parameters:
:   * `prediction` ([Prediction][twitch.prediction.Prediction]) - The prediction information.
##### Scopes:
:   * `channel:read:predictions`

---

```py
async def on_prediction_progress(prediction):
```
This called when the prediction is updated or in progress.
##### Parameters:
:   * `prediction` ([Prediction][twitch.prediction.Prediction]) - The prediction information.
##### Scopes:
:   * `channel:read:predictions`

---

```py
async def on_prediction_lock(prediction):
```
This called when a prediction is locked and can no longer be modified.
##### Parameters:
:   * `prediction` ([Prediction][twitch.prediction.Prediction]) - The prediction information.
##### Scopes:
:   * `channel:read:predictions`

---

```py
async def on_prediction_end(prediction):
```
This called when a prediction ends in the channel.
##### Parameters:
:   * `prediction` ([Prediction][twitch.prediction.Prediction]) - The prediction information.
##### Scopes:
:   * `channel:read:predictions`



## Goal
___
```py
async def on_goal_begin(goal):
```
This called when a goal begins in the channel.
##### Parameters:
:   * `goal` ([Goal][twitch.alerts.Goal]) - The goal information.
##### Scopes:
:   * `channel:read:goals`

---

```py
async def on_goal_progress(goal):
```
This called when the channel goal is updated or in progress.
##### Parameters:
:   * `goal` ([Goal][twitch.alerts.Goal]) - The goal information.
##### Scopes:
:   * `channel:read:goals`

---

```py
async def on_goal_end(goal):
```
This called when a goal ends in the channel.
##### Parameters:
:   * `goal` ([Goal][twitch.alerts.Goal]) - The goal information.
##### Scopes:
:   * `channel:read:goals`


## Charity
___
```py
async def on_charity_campaign_start(charity, started_at):
```
This called when a charity campaign starts in the channel.
##### Parameters:
:   * `charity` ([Charity][twitch.channel.Charity]) - The charity information.
* `started_at` ([Datetime][datetime.datetime]) - The charity start time.
##### Scopes:
:   * `channel:read:charity`

---

```py
async def on_charity_campaign_progress(charity):
```
This called when the charity is updated or in progress.
##### Parameters:
:   * `charity` ([Charity][twitch.channel.Charity]) - The charity information.
##### Scopes:
:   * `channel:read:charity`

---

```py
async def on_charity_campaign_stop(charity, stopped_at):
```
This called when the charity is updated or in progress.
##### Parameters:
:   * `charity` ([Charity][twitch.channel.Charity]) - The charity information.
* `stopped_at` ([Datetime][datetime.datetime]) - The charity end time.
##### Scopes:
:   * `channel:read:charity`

---

```py
async def on_charity_campaign_donate(charity, donor):
```
This called when a user donates to a charity campaign.
##### Parameters:
:   * `charity` ([Charity][twitch.channel.Charity]) - The charity information.
* `donor` ([CharityDonation][twitch.channel.CharityDonation]) - The user who donated to the charity.
##### Scopes:
:   * `channel:read:charity`



## HypeTrain
___
```py
async def on_hype_train_begin(train):
```
This called when a Hype Train begins in the channel.
##### Parameters:
:   * `train` ([HypeTrain][twitch.alerts.HypeTrain]) - The Hype Train information.
##### Scopes:
:   * `channel:read:hype_train`

---

```py
async def on_hype_train_progress(train):
```
This called when the Hype Train is updated or in progress.
##### Parameters:
:   * `train` ([HypeTrain][twitch.alerts.HypeTrain]) - The Hype Train information.
##### Scopes:
:   * `channel:read:hype_train`

---

```py
async def on_hype_train_end(train):
```
This called when a Hype Train ends in the channel.
##### Parameters:
:   * `train` ([HypeTrain][twitch.alerts.HypeTrain]) - The Hype Train information.
##### Scopes:
:   * `channel:read:hype_train`



## Stream
___
```py
async def on_stream_online(stream_type, started_at):
```
This called when the channel goes live.
##### Parameters:
:   * `stream_type` ([str][str]) - The stream type.
* `started_at` ([Datetime][datetime.datetime]) - The stream start time.

---

```py
async def on_stream_offline():
```
This called when the channel stops streaming


## Shoutout
___
```py
async def on_shoutout_create(to_user, created_by, viewer_count):
```
This called when the broadcaster sends a Shoutout.
##### Parameters:
:   * `to_user` ([BaseUser][twitch.user.BaseUser]) - The user that received the Shoutout.
* `created_by` ([BaseUser][twitch.user.BaseUser]) - The user who created the shoutout.
* `viewer_count` ([int][int]) - The number of users that were watching the broadcaster's stream.
##### Scopes:
:   * `moderator:read:shoutouts`

---

```py
async def on_shoutout_receive(from_user, viewer_count):
```
This called when the channel receives a shoutout from another channel.
##### Parameters:
:   * `from_user` ([BaseUser][twitch.user.BaseUser]) - The user that sent a Shoutout.
* `viewer_count` ([int][int]) - The number of users that were watching the broadcaster’s stream.
##### Scopes:
:   * `moderator:read:shoutouts`


</br></br></br>