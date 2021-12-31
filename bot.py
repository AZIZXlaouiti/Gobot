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


print("ahla bik")
# client.chat_postMessage(
#     channel='#random',
#     text="happy new year!!"
#     )
if __name__ == "__main__":
    app.run(debug=True , port=5000 )    
