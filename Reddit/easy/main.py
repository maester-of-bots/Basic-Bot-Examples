import praw

# Create a Reddit object using authentication info for the bot.  This is used to interact with Reddit as the bot.
reddit = praw.Reddit(
    client_id="bot_client_id",
    client_secret="bot_client_secret",
    user_agent="bot_user_agent",
    username="bot_reddit_account_username",
    password="bot_reddit_account_password"
)

# Create a Subreddit object using the subs you want the bot to watch.
# Use a "+" sign to add multiple subs, "testingground4bots+bots"
subreddit = reddit.subreddit("testingground4bots")

# Set what phrase the bot will
trigger_phrase = "python is awesome"

# Create a comment stream object.  This reads all the recent comments in the sub, then reads new comments as they come in.
comment_stream = subreddit.stream.comments()

# Open history.txt to get a list of comments the bot has replied to already
with open("history.txt", "r") as file:
    data = file.read()
    history = data.split("\n")

# Read through comments
for comment in comment_stream:

    # If the bot sees the trigger phrase, and hasn't commented yet
    if trigger_phrase in comment.body.lower() and comment.id not in history:
        # Make a reply to the comment
        comment.reply(body="It's super awesome!")

        # Upvote the comment
        comment.upvote()

        # Add the comment ID to the history list
        history.append(comment.id)

        # Write the new ID to the history file for persistance
        with open("history.txt", "a") as file:
            data = file.write(comment.id)
            file.close()
