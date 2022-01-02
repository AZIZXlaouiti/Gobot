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

env_path = Path('.')/'.env'
load_dotenv(dotenv_path = env_path)

app = Flask(__name__)

# setting event endpoint
slack_ev_adapter = SlackEventAdapter(os.environ['SIGN_SECRET'],'/slack/events',app)

slack_wb_client = WebClient(token=os.environ['SLACK_TOKEN_U']) # using the client

slack_wb_bot = WebClient(token = os.environ['SLACK_TOKEN_B']) # using the bot 

BOT_ID = slack_wb_bot.api_call("auth.test")["user_id"]

MODAL ={
	"title": {
		"type": "plain_text",
		"text": "Modal Title"
	},
	"submit": {
		"type": "plain_text",
		"text": "Submit"
	},
	"blocks": [
		{
			"type": "input",
			"element": {
				"type": "plain_text_input",
				"action_id": "title",
				"placeholder": {
					"type": "plain_text",
					"text": "What do you want to ask of the world?"
				}
			},
			"label": {
				"type": "plain_text",
				"text": "Title"
			}
		},
		{
			"type": "input",
			"element": {
				"type": "multi_channels_select",
				"action_id": "channels",
				"placeholder": {
					"type": "plain_text",
					"text": "Where should the poll be sent?"
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
MESSAGE_TO_MOVE = {}
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
    #print(f'message ==> {message_ts}') #1641161637.003000
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
    payload =  data.get('payload')
    p = json.loads(payload)
    message = ''
    if p["type"] == "view_submission":
        slack_wb_bot.chat_postMessage(
        channel='C02SBULS0G2',
        text='moving this post to another channel'
        )
        
        # channel_id = p['view']['state']['values']['OKr4']['channels']['selected_channels'][0]
        print(p['view']['state']['values'])
        
       
    elif p["type"] == "message_action":
        trigger_id = p['trigger_id']
        slack_wb_bot.views_open(
                trigger_id=trigger_id,
                view= MODAL
            )
        message = p['message']['blocks']  
           
    # print(p)    
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