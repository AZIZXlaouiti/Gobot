import slack 
import os 
from dotenv import load_dotenv
from pathlib import Path 
# print(os.environ.get("USER"))
env_path = Path('.')/'.env'
load_dotenv(dotenv_path = env_path)

client = slack.WebClient(token = os.environ['SLACK_TOKEN'])
print(os.environ['SLACK_TOKEN'])
