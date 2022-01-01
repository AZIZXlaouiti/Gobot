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

BOT_ID = slack_wb_bot.api_call("auth.test")["user_id"]

MESSAGE_BLOCK = {
    "type": "section",
    "text":{
        "type":"mrkdwn",
        "text":""
    }
}
# print(f"channel ==> {slack_wb_bot.conversations_list()}")
# https://api.slack.com/events  ---> api events methods
# https://api.slack.com/methods ---> api methods
@slack_ev_adapter.on("message")
def message(payload):
    event = payload.get("event", {})
    user_id = event.get("user")
    channel_id = event.get("channel")
    text = event.get("text") # listen for every message posted
    message_ts = event.get('ts')
    if f'<@{BOT_ID}> move' in text:
        message = f"<@{user_id}>, your post has been moved to a better channel! <#{channel_id}> Thanks for participating in Tech Career Growth community! :wave:"
        
        MESSAGE_BLOCK["text"]["text"] = message       
        
        message_to_send = {"channel": user_id, "blocks":[MESSAGE_BLOCK]}
        
        return slack_wb_bot.chat_postMessage(
           **message_to_send 
        )
    elif  BOT_ID != user_id : 
        
        message = f"<@{user_id}> Hello again :robot_face:"
        MESSAGE_BLOCK["text"]["text"] = message       
        
        message_to_send = {"channel": channel_id,"thread_ts":message_ts, "blocks":[MESSAGE_BLOCK]}
        
        return slack_wb_bot.chat_postMessage(
           **message_to_send 
        )

@app.route('/')
def welcome():
    return 'There is nothing here for you to see!!'

if __name__ == '__main__':
    app.run(debug=True , port=5000 )  