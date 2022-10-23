import discord
from discord.ext import commands

class fun_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Basic command, literally just sends a gif in chat
    @commands.command(name='happydance', pass_context=True)
    async def happydance(self,ctx):
        tenorURL = 'https://tenor.com/view/happy-snoopy-dance-gif-26520972'
        await ctx.reply(tenorURL)

    @commands.command(name="slap", help="Tag a user after your command to slap them.")
    async def slap(self, ctx, user_to_be_slapped: discord.Member):
        if ctx.author == user_to_be_slapped:
            await ctx.send(f"{ctx.author.mention} was dumb and slapped himself", delete_after=20)
            await ctx.send("https://tenor.com/bd1Da.gif", delete_after=20)
        else:
            await ctx.send(f"{ctx.author.mention} slapped {user_to_be_slapped.mention}", delete_after=20)
            await ctx.send("https://tenor.com/bd1Da.gif", delete_after=20)
        if ctx.guild:
            await ctx.message.delete()


def setup(bot):
    bot.add_cog(fun_cog(bot))
