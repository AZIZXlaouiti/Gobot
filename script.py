import os
import random
import re
import json
from flask.helpers import make_response
from flask.wrappers import Response
from slack import WebClient 
from dotenv import load_dotenv
from pathlib import Path 
from slackeventsapi import SlackEventAdapter
from flask import Flask , request , Request
from slack_sdk.errors import SlackApiError

env_path = Path('.')/'.env'
load_dotenv(dotenv_path = env_path)

app = Flask(__name__)

# setting event endpoint
slack_ev_adapter = SlackEventAdapter(os.environ['SIGN_SECRET'],'/slack/events',app)

slack_wb_client = WebClient(token=os.environ['SLACK_TOKEN_U']) # using the client

slack_wb_bot = WebClient(token = os.environ['SLACK_TOKEN_B']) # using the bot 

BOT_ID = slack_wb_bot.api_call("auth.test")["user_id"]

MODAL = {
	"title": {
		"type": "plain_text",
		"text": "Give Task"
	},
	"submit": {
		"type": "plain_text",
		"text": "Submit"
	},
	"blocks": [
		{
			"type": "input",
			"element": {
				"type": "multi_channels_select",
				"action_id": "channels",
				"placeholder": {
					"type": "plain_text",
					"text": "Where should the post be sent?"
				}
			},
			"label": {
				"type": "plain_text",
				"text": "Channel(s)"
			}
		},
		{
			"type": "actions",
			"elements": [
				{
					"type": "button",
					"action_id": "add_option",
					"text": {
						"type": "plain_text",
						"text": "Add another option  "
					}
				}
			]
		}
	],
	"type": "modal"
}
MESSAGE_BLOCK = {
    "type": "section",
    "text":{
        "type":"mrkdwn",
        "text":""
    }
}
message_to_move = []
message_ts = ''
user_id = ''
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
    message_ts = event.get('ts') # '1641181687.004200'
    # print(f"messag_id ==> {message_ts}") # essag_id ==> 1641181687.004200
#     if p.match(text):
#         # forword = '/[^]<#.*>[^]/gi'
        
#         message = f"<@{user_id}>, your post has been moved to a better channel! <#{channel_id}> Thanks for participating in Tech Career Growth community! :wave:"
        
#         MESSAGE_BLOCK["text"]["text"] = message       
        
#         message_to_send = {"channel": user_id, "blocks":[MESSAGE_BLOCK]}
        
#         return slack_wb_bot.chat_postMessage(
#            **message_to_send 
#         )
#     elif  BOT_ID != user_id : 
#         message = f"<@{user_id}> Hello again :robot_face:"
#         MESSAGE_BLOCK["text"]["text"] = message       
        
#         message_to_send = {"channel": channel_id,"thread_ts":message_ts, "blocks":[MESSAGE_BLOCK]}
        
#         return slack_wb_bot.chat_postMessage(
#            **message_to_send 
#         )

@app.route('/slack/move-post' , methods=['POST']) 
def move_post():
    data = request.form
    payload =  data.get('payload')
    p = json.loads(payload)
    global message_to_move , message_ts , user_id
    if p["type"] == "view_submission":
        channel_id = list(p['view']['state']['values'].values())[0]['channels']['selected_channels'][0]
        try:
            # posting the message to the specified channel in the modal 
            slack_wb_bot.chat_postMessage(
            channel=channel_id,
            blocks=[
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text":f'<@{user_id}> {message_to_move}'
                }
            },
            
            ]
            )
            # sending DM to notify the original owner
            slack_wb_bot.chat_postMessage(
                channel=user_id ,
                text=f"<@{user_id}>, your post has been moved to a better channel! <#{channel_id}> Thanks for participating in Tech Career Growth community! :wave:"
            )
            slack_wb_bot.chat_delete(
                channel=channel_id ,
                ts='1641181687.004200',
            )
        except SlackApiError as e:
            print(f'Error: {e}')


    elif p["type"] == "message_action":
        trigger_id = p['trigger_id']
        message_ts = p['message_ts']
        user_id = p['message']['user']

        slack_wb_bot.views_open(
                trigger_id=trigger_id,
                view= MODAL
            )
        message_to_move = p['message']['text']
         
        # print(f"user_id ==> {user_id}") 
        print(p)  
    return make_response("", 200)


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