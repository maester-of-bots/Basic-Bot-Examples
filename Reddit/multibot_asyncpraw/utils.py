import os
import json
import asyncpraw
from dotenv import load_dotenv

def makeBots():
    """Loads in bot data from the bots folder"""

    # Initial empty dictionary for bots
    bots = {}

    # Empty list for a list of subreddits to crawl
    subs = []

    # Read through all the bots in the bots folder
    for dir in os.listdir('bots'):

        # Skip the example
        if dir == 'botname':
            pass

        else:

            # Grab the json filename
            file = os.path.join('bots', dir, f"{dir}.json")

            # Read it!
            with open(file,'r') as lines:
                char_lines = lines.read()
                data = json.loads(char_lines)

            # Dump it to the bots dict!
            bots[dir] = data

    # Load in credentials
    load_dotenv()

    # Iterate through all the bots you've made
    for bot in bots.keys():
        print(f"Loading {bot}")

        # Initialize a Reddit object for each bot
        bots[bot]['r'] = asyncpraw.Reddit(
            client_id=os.getenv(bots[bot]['envs'][0]),
            client_secret=os.getenv(bots[bot]['envs'][1]),
            password=os.getenv(bots[bot]['envs'][2]),
            user_agent=os.getenv(bots[bot]['envs'][3]),
            username=os.getenv(bots[bot]['envs'][4])
        )

        # Add all the subs to the list of subs, no duplicates
        for sub in bots[bot]['subs']:
            if sub.lower() not in subs:
                subs.append(sub.lower())

    return bots, subs


def isPost(obj):
    """Check if a Reddit object is a Submission"""
    return isinstance(obj,asyncpraw.models.Submission)

def isComment(obj):
    """Check if a Reddit object is a Comment"""
    return isinstance(obj,asyncpraw.models.Comment)
