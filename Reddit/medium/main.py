import datetime
import os
import praw
from dotenv import load_dotenv

from module_SQL import *


def init():
    """
    Load in credentials / bot data and initialize a reddit object, then return reddit and some other data.
    """

    # This has to be run in order for the os.getenv() statements to return any data
    load_dotenv()

    reddit = praw.Reddit(
        client_id=os.getenv('client_id'),
        client_secret=os.getenv('client_secret'),
        password=os.getenv('password'),
        user_agent=os.getenv('user_agent'),
        username=os.getenv('reddit_username')
    )

    # Set the bot username
    bot_username = os.getenv('reddit_username')

    # Set the subreddit to watch
    subreddit = reddit.subreddit('hotfuzz+hotfuzzgifs')

    # Configure Bot response
    response = "-angrily slams £{} into the swear box-\n\nThank you, {}!\n\n^(\[Total donations:  £{}.  All proceeds go to the church roof\])"

    return reddit, bot_username, subreddit, response


def analysis(comment):
    """
    Analyze a comment and determine how much the foul-mouthed user ought to be fined.

    All proceeds go to the church roof!

    :param str comment:  The text of the user's comment
    :return int: How much the user owes the swear jar.
    """

    # This is a list of the fines for swear words from Hot Fuzz
    wordList = {" nob ": .1, " nob": .1, "bastard": .2, "shit": .5, "fuck": 1, "cunt": 2}

    # Count how many bad words the user used, and then how much they owe
    cost = 0.0
    for key in wordList.keys():
        if comment.count(key) > 0:
            cost = cost + (comment.count(key) * wordList[key])

    # Return amount of user donation for swearing
    return cost


def run():
    """
    Start watching the HotFuzz subreddits.

    Read through the subreddits' comment stream (100 past comments, then watch current comments)

    If the comment is newer than two days, make sure it hasn't been responded to already and that it's not the bot
    Then calculate how much the foul-mouthed user ought to donate to the swear jar, reply to the user with that information,
    and add the post / charge to the database.
    """

    # Get necessery bot information
    reddit, bot_username, subreddit, response = init()

    # Iterate through comments
    for comment in subreddit.stream.comments():

        # Get the list of comments from the database
        readComments = getComments()

        # Ignore blank author comments
        if comment.author == None:
            pass

        # Ignore comments you've already written up, or comments from yourself
        elif comment.id in readComments or comment.author.name == bot_username:
            print("Skipping comment that was already in the database.\n\n")
            pass

        # Process the comment
        else:

            # Grab the comment body
            lower_body = comment.body.lower()

            # Grab comment direct link
            url = "https://reddit.com{}".format(comment.permalink)

            # Determine how much he needs to donate for his potty mouth
            charges = analysis(lower_body)

            if charges > 0.0:
                try:

                    # Record charges to database
                    writeCharges(comment.author.name, charges)

                    # Get user's total donations from the database
                    total = getCharges(comment.author.name)

                    # Craft comment text
                    commentText = response.format(charges, comment.author.name, round(total, 1))

                    # Reply to the user and upvote his comment
                    comment.reply(body=commentText)
                    comment.upvote()

                    # Record the comment ID
                    writeComment(comment.id)
                except Exception as e:

                    # If there's an error, send it to your main account as a message.
                    messageToSend = "{} - {}".format(url, str(e))
                    reddit.redditor('YourRedditUsernameHere').message('Log', messageToSend)


if __name__ == "__main__":
    run()
