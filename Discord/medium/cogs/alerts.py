from discord.ext import commands
import discord

"""
This is a basic cog for listening to events.   Ensure that a channel named "mod-alerts" is created in the server, or 
redirect the bot to another channel in order for this to work.
"""

class Alerts_Cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def makeEmbed(self,title,color,field,value):
        embed = discord.Embed(title=title,color=color)
        embed = embed.add_field(name=field, value=value, inline=False)
        return embed

    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):

        # Get the channel to respond to
        c = discord.utils.get(guild.channels, name="mod-alerts")

        # Generate an Embed
        embed = self.makeEmbed('Alert - User Ban', discord.Color.red(), "Details:",f'{user.name}-{user.id} was banned from {guild.name}-{guild.id}')

        # Send the embed
        await c.send(embed=embed)

    @commands.Cog.listener()
    async def on_invite_create(self, invite):
        c = discord.utils.get(invite.guild.channels, name="mod-alerts")
        embed = self.makeEmbed('Alert - Invite Created', discord.Color.blue(), "Details:",f"{invite.inviter} has created an invite to the server.")
        await c.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        c = discord.utils.get(channel.guild.channels, name="mod-alerts")
        embed = self.makeEmbed('Alert - Channel Created', discord.Color.yellow(), "Details:", '<#{}> was created.')
        await c.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        c = discord.utils.get(channel.guild.channels, name="mod-alerts")
        embed = self.makeEmbed('Alert - Channel Deleted', discord.Color.blurple(), "Details:", f'{channel.name}was deleted.')
        await c.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        c = discord.utils.get(member.guild.channels, name="mod-alerts")
        embed = self.makeEmbed('Alert - New Member Joined', discord.Color.gold(), "Details:", f'{member.name} joined the server')
        await c.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        c = discord.utils.get(member.guild.channels, name="mod-alerts")
        embed = self.makeEmbed('Alert - Somebody left!', discord.Color.fuchsia(), "Details:", f'{member.name} has left the server')
        await c.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_channel_update(self, before, after):
        c = discord.utils.get(before.guild.channels, name="mod-alerts")
        embed = self.makeEmbed('Alert - Channel Update!', discord.Color.fuchsia(), "Details:", f'{before} was updated to {after}')
        await c.send(embed=embed)

    @commands.Cog.listener()
    async def on_error(self, event, *args, **kwargs):
        c = discord.utils.get(event.guild.channels, name="mod-alerts")
        embed = self.makeEmbed('Alert - Error!', discord.Color.fuchsia(), "Details:", f'{event} - {args}')
        await c.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        c = discord.utils.get(guild.channels, name="mod-alerts")
        embed = self.makeEmbed('Alert - Guild Joined!', discord.Color.brand_green(), "Details:", f'Bot joined {guild}')
        await c.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_unban(self, guild, user):
        c = discord.utils.get(guild.channels, name="mod-alerts")
        embed = self.makeEmbed('Alert - User Unbanned!', discord.Color.fuchsia(), "Details:", f'{user.name} has been pardoned.')
        await c.send(embed=embed)

    @commands.Cog.listener()
    async def on_integration_create(self, integration):
        c = discord.utils.get(integration.guild.channels, name="mod-alerts")
        embed = self.makeEmbed('Alert - Somebody left!', discord.Color.fuchsia(), "Details:", f'{integration} was created')
        await c.send(embed=embed)

    @commands.Cog.listener()
    async def on_integration_update(self, integration):
        c = discord.utils.get(integration.guild.channels, name="mod-alerts")
        embed = self.makeEmbed('Alert - Somebody left!', discord.Color.fuchsia(), "Details:", f'{integration} was updated')
        await c.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_role_create(self, role):
        c = discord.utils.get(role.guild.channels, name="mod-alerts")
        embed = self.makeEmbed('Alert - Role Created!', discord.Color.fuchsia(), "Details:", f'{role} was created.')
        await c.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_role_update(self, before, after):
        c = discord.utils.get(after.guild.channels, name="mod-alerts")
        embed = self.makeEmbed('Alert - Role Updated!!', discord.Color.fuchsia(), "Details:", f'{before} was updated to {after}.')
        await c.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):
        c = discord.utils.get(role.guild.channels, name="mod-alerts")
        embed = self.makeEmbed('Alert - Role deleted!', discord.Color.fuchsia(), "Details:", f'{role.name} was deleted!')
        await c.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        c = discord.utils.get(message.guild.channels, name="mod-alerts")
        embed = self.makeEmbed('Alert - Message deleted!!', discord.Color.fuchsia(), "Details:", f'Content: ```{message.content}```\nAuthor: ```{message.author}```')
        await c.send(embed=embed)

# Setup function.  All cogs need one, they usually look just like this.
def setup(bot):
    bot.add_cog(Alerts_Cog(bot))
