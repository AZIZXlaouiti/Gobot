import os
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

# adding a slack endpoint
slack_adapter = SlackEventAdapter(os.environ['SIGN_SECRET'],'/slack/events',app)

client = WebClient(token = os.environ['SLACK_TOKEN'])
# calling slack api and retrieving the slack_bot_id
auth = client.api_call("auth.test")
BOT_ID = auth["user_id"]
# print(f"auth_response == {auth}")
# payload --> all message details
message_counts = {}
# store this in memory

class Message():
    TEXT = {

    }

    def __init__(self , channel):
        self.channel = channel 
        self.icon = ':robot_face:'
        self.timestamp = ''
        self.completed = False
    

@slack_adapter.on('message') # adding a new end-point
def message(payload):
    # print(f"payload == {payload}")
    event = payload.get('event' , {}) # look for the key ['event'] if not return {}
    channel_id = event.get('channel') # get message related channel
    user_id  = event.get('user') # get message related user(client)
    text = event.get('text') # get message content
    message_ts = event.get('ts')
    if user_id != None and  BOT_ID != user_id : # avoiding message/recieve conflict ensuring the bot did not send the message
        if user_id in message_counts:
            message_counts[user_id] += 1
        else :
            message_counts[user_id] = 1
        if text == f'<@{BOT_ID}> move':
            try: 
                # send direct message (DM)
                client.chat_postMessage(
                    channel=user_id,
                    text=f"<@{user_id}>, your post has been moved to a better channel! <#{channel_id}> Thanks for participating in Tech Career Growth community! :wave:"
                )

                # print(result)

            except :
                print(f"Error:")
        else : 
            # reply in thread
            client.chat_postMessage(
                channel=channel_id,
                thread_ts=message_ts,
                text=f"<@{user_id}> Hello again :robot_face:"
            )      
            print(f'text == {text}')

@app.route('/message-count' , methods=['POST']) 
def message_count():
    data = request.form
    user_id =  data.get('user_id')
    channel_id = data.get('channel_id')
    message_count = message_counts.get(user_id, 0)
    client.chat_postMessage(
        channel=channel_id , text= f'Message: {message_count}'
        )
    return Response() , 200


if __name__ == '__main__':
    app.run(debug=True , port=5000 )    
