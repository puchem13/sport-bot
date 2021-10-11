import slack
import os
from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime, timedelta, time
import schedule
import time as t

env_path = Path('.') / '.env'
load_dotenv(dotenv_path = env_path)
scheduleDict = {
    "Monday": {"time": "17:00", 
                "cancelled": False},
    "Thursday": {"time": "7:15", 
                "cancelled": False},
    "Friday": {"time": "17:00", 
                "cancelled": False},
    "Saturday": {"time": "10:00",
                "cancelled": False}
}

def post_message(message):
    client = slack.WebClient(token=os.environ['SLACK_TOKEN'])
    client.chat_postMessage(channel='#testing-sport-bot', text=message)

def get_message(day):
    if day in scheduleDict:
        TIME = scheduleDict[day]["time"]
        return (
            ":running::woman-running:*Will you be joining " 
            f"the running event on {day} at {TIME}?*:running_shirt_with_sash:\n"
            "Please react to this message with :thumbsup: :thumbsdown:"
            )

def check_event(day, startTime, endTime):
    if day in scheduleDict and not scheduleDict[day]["cancelled"]:
            eventTime = datetime.strptime(scheduleDict[day]["time"],'%H:%S')
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