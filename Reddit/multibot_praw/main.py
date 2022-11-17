from sql import *
from utils import *

import praw

import requests
import random
from dotenv import load_dotenv


class single_reddit_bot:
    def __init__(self):

        # Load in credentials from .env
        load_dotenv()

        # Set the bot's username in memory because it's slightly easier
        self.name = os.getenv('bot_main_name')

        # Initialize a Reddit object, use a master account (Or one of the bot accounts, I don't think it matters...)
        self.reddit = praw.Reddit(
            client_id=os.getenv('master-client_id'),
            client_secret=os.getenv('master-client_secret'),
            password=os.getenv('master-password'),
            user_agent=os.getenv('master-user_agent'),
            username=os.getenv('master-username')
        )

        # Load in webhooks for sending messages to Discord servers
        self.bofh = os.getenv('bofh_webhook')

        # Initialize all bots, Reddit objects, and get a list of subreddits to crawl
        self.all_bots, self.subs = makeBots()

    def send_webhook(self, body, bot):

        # Grab the webhook URL for this bot
        if bot == 'BOFH':
            url = self.bofh
        else:
            url = self.all_bots[bot]['webhook']

        # Craft the data
        data = {'content': body, 'username': bot}

        # Send it
        requests.post(url, data=data)

    def response_canon(self, c_dict, bot):
        """Sending a normal, random response"""

        bot_reddit = self.all_bots[bot]['r']

        # Initialize the comment using the provided bot
        new_comment = bot_reddit.comment(id=c_dict['id'])

        print(new_comment.id)

        # Seed randomness because stupid computer
        random.seed()

        # Get a random number based on the quote count
        num = random.randint(0, len(self.all_bots[bot]['quotes']) - 1)

        # Set response to a variable
        response = self.all_bots[bot]['quotes'][num]

        # Reply to the comment with the chosen response
        new_comment.reply(body=response)

        # Write the comment to the database, so we don't comment on it again.
        writeComment(c_dict['id'], bot)

        # Create a text body for the webhook
        body = f"{c_dict['text']}\nResponse: {response}\n{c_dict['link']}"

        return body

    def check_triggers(self, text):
        triggered = []

        for bot in self.all_bots:
            for trigger in self.all_bots[bot]['keywords']:
                if trigger in text and bot not in triggered:
                    triggered.append(bot)

        return triggered

    def run(self):

        # Set the subreddit to monitor
        self.subreddits = self.reddit.subreddit("+".join(self.subs))

        print("Crawling comments.")

        body = f"{self.name} has started."
        self.send_webhook(body, 'BOFH')

        # Iterate through all the comments in an asyncronous way
        for comment in self.subreddits.stream.comments():

            # Loading comment, getting author name
            try:

                # Load in the comment stuff
                comment.load()

                # It'll crash if someone deleted their comment or account, unless we do this check
                if comment.author == None:
                    author_name = 'None'

                else:
                    author_name = comment.author.name

                # c_dict, and triggers
                try:
                    # Grab comment info in case it gets deleted
                    c_dict = {
                        'text': comment.body.lower(),
                        'id': comment.id,
                        'user': author_name,
                        'link': f'https://www.reddit.com{comment.permalink}'
                    }

                    # Check if any bots are triggered
                    triggered = self.check_triggers(c_dict['text'])

                    # Process triggered bots, if none are triggered this does nothing
                    for bot in triggered:

                        # Try to respond for each triggered bot
                        try:

                            # See if this comment has already been responded to by the bot, and make sure the comment's author is not the bot
                            if not checkDB(c_dict['id'], bot) and c_dict['user'].lower() != bot.lower():
                                # Send a response for the bot
                                response = self.response_canon(c_dict, bot)

                                # Send a webhook to Discord
                                self.send_webhook(response, bot)

                        # Per-Bot catcher for trigger errors
                        except Exception as e:
                            body = f"**Error Report**\n\nGot an exception while processing a bot trigger.\nBot:  {bot}\nError: {e}\nComment: {c_dict['link']}"
                            self.send_webhook(body, 'BOFH')
                            pass

                # Catcher for c_dict / triggers
                except Exception as e:
                    body = f"**Error Report**\n\nGot an exception while making c_dict / checking triggers.\nError: {e}\nComment: {comment.id}"
                    self.send_webhook(body, 'BOFH')
                    pass

            # Catcher for comment loader
            except Exception as e:
                body = f"**Error Report**\n\nGot an exception while loading a comment\nError: {e}"
                self.send_webhook(body, 'BOFH')
                pass


def main():
    my_bot = single_reddit_bot()
    while True:
        try:
            my_bot.run()

        except Exception as e:
            body = f"**Error Report**\n\nGot an exception at the highest level.  Bot probably restarting.\nError: {e}"
            my_bot.send_webhook(body, 'BOFH')


if __name__ == "__main__":
    main()
