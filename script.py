import os
import random
import re
import json
from flask.wrappers import Response
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

# <#C02S91GQBGV|general> <#C02SBULS0G2|random> <#C02SE7XSS76|software-engineering>
CHANNELS = slack_wb_bot.conversations_list()["channels"] # [{}]


tmp = ''
for e in CHANNELS:
    if tmp == '' :
        tmp = "("+ f"{e['id']}"+ "\|" +f"{e['name']}"+")"
    else :    
        tmp = tmp + "|" + "("+ f"{e['id']}"+ "\|" +f"{e['name']}"+")"

ptr = f'^<.*> move <#({tmp})>'   
p = re.compile(ptr)   

# https://api.slack.com/events  ---> api events methods
# https://api.slack.com/methods ---> api methods
@slack_ev_adapter.on("message")
def message(payload):
    event = payload.get("event", {})
    user_id = event.get("user")
    channel_id = event.get("channel")
    text = event.get("text") # listen for every message posted
    message_ts = event.get('ts')
    print(f'text ==> {text}')
    if p.match(text):
        # forword = '/[^]<#.*>[^]/gi'
        
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

@app.route('/slack/move-post' , methods=['POST']) 
def move_post():
    data = request.form
    user_id =  data.get('payload')
    p = json.loads(user_id)
    print(p['trigger_id'])
    # slack_wb_bot.views_open(
    #         trigger_id=trigger_id,
    #         view={
    #             "type": "modal",
    #             "title": {"type": "plain_text", "text": "My App"},
    #             "close": {"type": "plain_text", "text": "Close"},
    #             "blocks": [
    #                 {
    #                     "type": "section",
    #                     "text": {
    #                         "type": "mrkdwn",
    #                         "text": "About the simplest modal you could conceive of :smile:\n\nMaybe <https://api.slack.com/reference/block-kit/interactive-components|*make the modal interactive*> or <https://api.slack.com/surfaces/modals/using#modifying|*learn more advanced modal use cases*>.",
    #                     },
    #                 },
    #                 {
    #                     "type": "context",
    #                     "elements": [
    #                         {
    #                             "type": "mrkdwn",
    #                             "text": "Psssst this modal was designed using <https://api.slack.com/tools/block-kit-builder|*Block Kit Builder*>",
    #                         }
    #                     ],
    #                 },
    #             ],
    #         },
    #     )
    return Response() , 200

@app.route('/message-count' , methods=['POST']) 
def message_count():
    data = request.form
    user_id =  data.get('user_id')
    channel_id = data.get('channel_id')
    print(data)
    return Response() , 200

@app.route('/')
def welcome():
    return 'There is nothing here for you to see!!'

if __name__ == '__main__':
    app.run(debug=True , port=5000 )  