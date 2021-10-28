from slack_sdk import WebClient
import os
from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime, timedelta, time
import schedule
import time as t
import yaml

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)


def read_yaml(file_path):
    with open(file_path, "r") as f:
        return yaml.safe_load(f)


jsonEvents = read_yaml(os.environ['CONFIG_FILE'])
client = WebClient(token=os.environ['SLACK_TOKEN'])


def post_message(message):
    client.chat_postMessage(channel='#testing-sport-bot', text=message)


def get_messages(day):
    event_to_send_list = []
    for event in jsonEvents["events"].items():
        event_name, details = event
        event_day = details["day"]
        event_time = details["time"]
        print("Current processed event: " + event_name)
        if details["ative"]:
            print("event is active and can be checked")
            if event_day == day:
                print("we need to announce this event in slack")
                event_to_send_list.append(
                    ":running::woman-running:*Will you be joining "
                    f"the running event on {event_day} at {event_time}?*"
                    f":running_shirt_with_sash:\n"
                    "Please react to this message with :thumbsup: :thumbsdown:"
                    )
    return event_to_send_list


def send_message():
    today = datetime.now()
    tomorrow = today + timedelta(days=1)
    weekday_to_check = tomorrow.strftime("%A")
    if weekday_to_check == "Saturday":
        weekday_to_check = (tomorrow + timedelta(days=2)).strftime("%A")
    slack_messages = get_messages(weekday_to_check)
    for message in slack_messages:
        post_message(message=message)


schedule.every().day.at("14:04").do(send_message)

if __name__ == "__main__":
    while True:
        schedule.run_pending()
        t.sleep(1)
