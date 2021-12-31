import os 
from slack import WebClient
from dotenv import load_dotenv
from pathlib import Path 
from slackeventsapi import SlackEventAdapter
from flask import Flask
env_path = Path('.')/'.env'
load_dotenv(dotenv_path = env_path)

app = Flask(__name__)

# adding a slack endpoint
slack_adapter = SlackEventAdapter(os.environ['SIGN_SECRET'],'/slack/events',app)

client = WebClient(token = os.environ['SLACK_TOKEN'])
# calling slack api and retrieving the slack_bot_id
BOT_ID = client.api_call("auth.test")["user_id"] 
# payload --> all message details
@slack_adapter.on('message')
def message(payload):
    event = payload.get('event' , {}) # look for the key ['event'] if not return {}
    channel_id = event.get('channel') # get message related channel
    client_id  = event.get('user') # get message related user(client)
    text = event.get('text') # get message content
    
    if BOT_ID != client_id : # avoiding message/recieve conflict
        client.chat_postMessage(
            channel=channel_id,
            text= f"text recieved : {text}"
            )

    
# print("ahla bik")
if __name__ == "__main__":
    app.run(debug=True , port=5000 )    
