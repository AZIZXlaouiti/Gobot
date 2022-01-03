![Discord](https://user-images.githubusercontent.com/79036942/147900523-0007d251-fe8f-4f1e-bf24-188c49134021.png)
## description 
Sample Python Slackbot app for App Platform
### how to use 
#### in development: 
- run `pip install -r requirements.txt`
- run `pip3 script.py` to run the flask server
#### in production : 
- coming soon ...
#### common bugs : 
- do not try and double post a post that was already posted by the GoBot , doing so will result in `This content can't be displayed.` message ,this is made intentionally by slack API to avoid bot conflict
## Technologies 
- Flask
- Ngrok
### Authorizations
On behalf of users, Gobot can:
- View information about a user’s identity, granted by 1 team member
- View basic information about public channels in a workspace, granted by 1 team member
- Send messages on a user’s behalf, granted by 1 team member

On behalf of the app, Gobot can:
- View messages and other content in public channels that Gobot has been added to
- Send messages as @slackbotv1
- Add shortcuts and/or slash commands that people can use
- View messages and other content in private channels that Gobot has been added to
- View messages and other content in direct messages that Gobot has been added to
- Start direct messages with people
- Send messages to channels @slackbotv1 isn't a member of
- View messages that directly mention @slackbotv1 in conversations that the app is in
- View basic information about public channels in a workspace
