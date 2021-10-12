import json

import slack
import os
from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime, timedelta, time
import schedule
import time as t
import yaml

env_path = Path('.') / '.env'
load_dotenv(dotenv_path = env_path)

def read_yaml(file_path):
    with open(file_path, "r") as f:
        return yaml.safe_load(f)

jsonEvents = read_yaml(os.environ['CONFIG_FILE'])

def post_message(message):
    client = slack.WebClient(token=os.environ['SLACK_TOKEN'])
    client.chat_postMessage(channel='#testing-sport-bot', text=message)

def get_message(day):
    for event in jsonEvents["EVENTS"].items():
        event_name, details = event
        event_day = details["DAY"]
        event_time = details["TIME"]
        print("Current processed event: "+ event_name)
        if (details["ACTIVE"]):
            print("event is active and can be checked")
            if (event_day == day):
                print("we need to announce this event in slack")
                return (
                    ":running::woman-running:*Will you be joining " 
                    f"the running event on {event_day} at {event_time}?*:running_shirt_with_sash:\n"
                    "Please react to this message with :thumbsup: :thumbsdown:"
                    )

def check_event(day, startTime, endTime):
    if day in jsonEvents and not jsonEvents[day]["cancelled"]:
            eventTime = datetime.strptime(jsonEvents[day]["time"], '%H:%S')
            if startTime < eventTime.time() and eventTime.time() < endTime:
                return True
    return False

def send_message():
    TODAY = datetime.now().date().strftime("%A")
    if check_event(TODAY, time(11,00), time(23,59)):
        MESSAGE = get_message(TODAY)
        post_message(message=MESSAGE)

    NEXTDAY = (datetime.now() + timedelta(days = 1)).strftime("%A")
    if check_event(NEXTDAY, time(00,00), time(11,00)):
        MESSAGE = get_message(NEXTDAY)
        post_message(message=MESSAGE)

schedule.every().day.at("14:04").do(send_message)

if __name__ == "__main__":
    while True:
        schedule.run_pending()
        t.sleep(1)