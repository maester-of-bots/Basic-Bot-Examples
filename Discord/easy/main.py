import discord

# Bot token, get this from https://discord.com/developers
token = "put_discord_token_here"

# Initialize the bot
bot = discord.Client()

# Event listener, this fires whenever the bot detects a new message.  It provides the message as input.
@bot.event
async def on_message(message):

    # Don't do anything if the message is from the bot
    if message.author == bot.user:
        return

    # Read the message's content to see if they said nice things about Python
    elif message.content == "Python is awesome!":

        # Reply to the message expressing your support for Python
        await message.reply("Hell yeah brother")


    elif "goober" in message.content:

        await message.reply("Watch your language, this server is E for Everyone.")


# Event listener, this fires when the bot connects to Discord and is online
@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

# Start the bot
bot.run(token)