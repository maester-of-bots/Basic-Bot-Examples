import json
import os
import discord
import requests
from discord.ext import commands
from dotenv import load_dotenv


class Gif_Cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        load_dotenv()

        # Tenor API Key
        self.apikey = os.getenv('tenor_api_key')

        # Gif return limit
        self.lmt = 1

        # Gif search URL
        self.searchURL = "https://api.tenor.com/v1/search?q=%s&key=%s&limit=%s&anon_id=%s"

        # Testing the key
        self.r = requests.get("https://api.tenor.com/v1/anonid?key=%s" % self.apikey)

        # Dunno, google it.
        if self.r.status_code == 200:
            self.anon_id = json.loads(self.r.content)["anon_id"]
        else:
            self.anon_id = ""

    @commands.command(name='gif', pass_context=True, usage='[search terms]', brief='Tenor gif searcher', description='Tenor gif searcher, clearly the favorite feature')
    async def gif(self, ctx, *args):
        if args == ():
            await ctx.send('Please provide some keywords to search with.')
        else:

            # Craft the query
            query = " ".join(args).replace("?", "")

            # Request the gifs
            r = requests.get(self.searchURL % (query, self.apikey, 1, self.anon_id))

            # Craft a response
            if r.status_code == 200:
                gif = json.loads(r.content)
                url = gif['results'][0]['media'][0]['gif']['url']
            else:
                url = "That's weird, I couldn't actually find something for that."

            # Send the response
            await ctx.send(url)


def setup(bot):
    bot.add_cog(Gif_Cog(bot))
