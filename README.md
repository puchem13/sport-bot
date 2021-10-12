# Sport Bot 🤖

Developing a [Slack Bot](https://slack.com/intl/en-in/help/articles/115005265703-Create-a-bot-for-your-workspace) that automatically posts messages to the Fitness Channel.


## Tools 🛠️

- [Slack API](https://api.slack.com/)
- [Python](https://www.python.org/)


## Environment Variables 🌎

To run this project, you will need to add a [`SLACK_TOKEN`](https://slack.dev/python-slack-sdk/web/index.html) to your .env file


## Run Locally 📝

Clone the project
```bash
  $ git clone https://github.com/puchem13/sport-bot.git
```

Go to the project directory
```bash
  $ cd sport-bot
```

Create a .env file and add `SLACK_TOKEN`
```bash
  $ cat > .env
```

Install dependencies
```bash
  $ pip install -r requirements.txt
```

Run the project
```bash
  $ python bot.py
```
