import os
import random
from slack import WebClient 
from dotenv import load_dotenv
from pathlib import Path 
from slackeventsapi import SlackEventAdapter
from flask import Flask , request , Request
env_path = Path('.')/'.env'
load_dotenv(dotenv_path = env_path)

app = Flask(__name__)
# setting event endpoint
slack_ev_adapter = SlackEventAdapter(os.environ['SIGN_SECRET'],'/slack/events',app)

slack_wb_client = WebClient(token=os.environ['SLACK_TOKEN_U']) # using the client

slack_wb_bot = WebClient(token = os.environ['SLACK_TOKEN_B']) # using the bot 

MESSAGE_BLOCK = {
    "type": "section",
    "text":{
        "type":"mrkdwn",
        "text":""
    }
}
# https://api.slack.com/events  ---> api events methods
@slack_ev_adapter.on("message")
def message(payload):
    event = payload.get("event", {})
    
    text = event.get("text") # listen for every message posted
    if "flip a coin" in text.lower():
        channel_id = event.get("channel")
        rand_int = random.randint(0 , 1)
        if rand_int == 0 : 
            result = "head"
        else :
            result = "tails"
        message = f"the result is {result}" 

        MESSAGE_BLOCK["text"]["text"] = message       
        message_to_send = {"channel": channel_id, "blocks":[MESSAGE_BLOCK]}
        return slack_wb_bot.chat_postMessage(**message_to_send)

@app.route('/')
def welcome():
    return 'There is nothing here for you to see!!'

if __name__ == '__main__':
    app.run(debug=True , port=5000 )  