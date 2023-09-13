---
hide:
  - toc
---

To set up Twitchify and create an app on the Twitch Developer Console, follow these steps:

### Install Twitchify

Ensure you have `pip` installed, then run the following command in your terminal or command prompt:

```shell
pip install twitchify
```

???+ Note
    Cloning the repository is for beta releases and not required for regular usage.

```shell
git clone https://github.com/MrSniFo/Twitchify
```

### Create a Twitch Account
If you don't have a Twitch account, you need to [create](https://www.twitch.tv/signup) one.

### Create an App on the Twitch Developer Console

Go to [console](https://dev.twitch.tv/console) and sign in with your Twitch account

- Click on 'Applications' in the top navigation.
- Click on 'Register Your Application'.
- Fill in the required details for your app.

???+ Note 
    Twitchify built-in authentication uses `http://localhost:3000` Redirect URL, you can customize the port when running the client.

- Set 'OAuth Redirect URLs' to your desired redirect URI.
- Save your changes.

After creating the app on the Twitch Developer Console, you will receive a Client ID and Client Secret,
which you will use in your Twitchify client. Additionally, make sure to set the correct Redirect URI for your app.