---
icon: fontawesome/solid/turn-up
hide:
  - toc
---


To set up twitch.py and create an app on the Twitch Developer Console, follow these steps:

!!! Warning
    If you're currently using twitchify, please note that it will soon be moved to twitch.py on PyPI.

### Install twitch.py

Ensure you have `pip` installed, then run the following command in your terminal or command prompt:

#### On Windows

```bash
py -3 -m pip install -U twitchify
```

#### On Linux/macOS

```bash
python3 -m pip install -U twitchify
```

#### Clone

!!! Info
    Cloning the repository is for accessing beta releases.

```shell
git clone https://github.com/MrSniFo/twitch.py
```

### Create a Twitch Account
If you don't have a Twitch account, you need to [create](https://www.twitch.tv/signup) one.

### Create an App on the Twitch Developer Console

Go to [console](https://dev.twitch.tv/console) and sign in with your Twitch account

- Click on 'Applications' in the top navigation.
- Click on 'Register Your Application'.
- Fill in the required details for your app.
- Save your changes.

After creating the app on the Twitch Developer Console, you will receive a Client ID and Client Secret,
which you will use in your twitch.py client.