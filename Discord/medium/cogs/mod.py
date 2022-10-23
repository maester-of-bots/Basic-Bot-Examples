import discord
from discord.ext import commands, tasks


class ModCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        # Color codes for rainbow role
        self.rainbow = [(255,0,0),(255,128,0),(255,255,0),(0,255,0),(0,255,255),(0,0,255),(127,0,255),(255,0,255)]
        self.colorNum = 0


    @tasks.loop(seconds=10)
    async def change_color(self):
        """
        Random fun loop to change the color of a specified role every ten seconds.  Makes a rainbow role.
        """

        # Iterate through the guilds the bot is a member of
        for guild in self.bot.guilds:

            # Get the "rainbow" role
            role = discord.utils.get(guild.roles, name="rainbow")

            # If the rainbow role exists:
            if role:

                # Set the color of the role
                color = discord.Color.from_rgb(self.rainbow[self.colorNum][0],self.rainbow[self.colorNum][1],self.rainbow[self.colorNum][2])

                # Color rollover
                if self.colorNum == 7:
                    self.colorNum = 0
                else:
                    self.colorNum += 1

                # Edit the role
                await role.edit(colour=color)


    @commands.Cog.listener()
    async def on_ready(self):
        """
        Detects when the bot is ready, and then starts the above task loop.

        self.change_color.start() must be put here, or it will usually fail.
        """

        self.change_color.start()

def setup(bot):
    bot.add_cog(ModCog(bot))
