import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
import os
import random

from ron_swanson import quotes

intents = discord.Intents.all()

bot_owner_id = 'your_discord_id'

bot_description = "THC's General Bot"

class CustomClient(commands.Bot):
    def __init__(self, command_prefix, self_bot):

        commands.Bot.__init__(self, command_prefix=command_prefix, intents=intents, self_bot=self_bot)
        self.bot = commands.Bot(command_prefix=command_prefix, intents=intents, owner_id=bot_owner_id, description=bot_description)


        self.ron_quotes = quotes

        self.ron_triggers = ["lawns", "grilling", "beer", "women"]


    # OnMessage loop, this runs first, then executes commands
    async def on_message(self, message):

        # Ron Swanson Quote-Bot

        # Set this so we only respond once even if there are multiple trigger words
        responded = False

        # Iterate through Ron's trigger words and see if they exist in the message
        for trigger in self.ron_triggers:

            # If Ron hasn't responded and hears a trigger word...
            if responded is False and trigger in message.content.lower():

                # Generate the response.  "Women" only works 50% of the time.
                if trigger == "women" and random.randint(0,1):
                    break
                else:

                    # Used to give random some randomness.
                    random.seed()

                    # Choose a random qujote
                    num = random.randint(0,len(self.ron_quotes)-1)
                    response = self.ron_quotes[num]

                    # Send the quote
                    await message.reply(response)
                    responded = True

        if "i lost the game" in message.content.lower():
            await message.add_reaction('😡')

        elif "mario" in message.content.lower() or "pratt" in message.content.lower():
            await message.add_reaction('😡')
            await message.reply("There is no Mario movie in Ba Sing Se.", delete_after=10)
            await message.reply("https://tenor.com/bd1Da.gif", delete_after=10)
            await message.delete()

        await bot.process_commands(message)

    async def on_ready(self):
        print(f'{self.user.name} is connected to Discord.')

        # If the bot detected any cogs fail to load...
        if len(failed_cogs) > 0:

            # Generate an embed, make it green.
            color = discord.Colour.green()
            embeds = discord.Embed(title="Failed Cogs on {}".format(self.user.name), color=color)

            # Add cogs to the embed
            for cog in failed_cogs:
                cogname, error = cog.split('.py - ')
                embeds = embeds.add_field(name=cogname, value=error, inline=False)

            # Send the errors to an alert channel the bot can access
            channel = await self.fetch_channel('ID_for_an_alert_channel_here')
            await channel.send(embed=embeds)


# Get the token
load_dotenv()
token = os.getenv('token')

# Initialize the bot
bot = CustomClient(command_prefix="!", self_bot=False)

# Load in cogs
cogs = os.listdir('cogs')
failed_cogs = []

print("Loading in cogs.")
for cog in cogs:
    if ".py" in cog:
        bot.load_extension("cogs."+cog.replace(".py", ""))

print("Done loading cogs.")

# Run that bitch
bot.run(token)