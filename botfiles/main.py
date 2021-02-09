import discord
import os
import praw
import random
from discord.ext import commands
from discord.ext import tasks
import requests

TOKEN = os.getenv("DISCORD_BOT_TOKEN")
intents = discord.Intents.all()
bot = commands.Bot(command_prefix = "/", intents = intents, description = "Bot made it by Renzo")
r = praw.Reddit(client_id=os.getenv("CLIENT_ID"),
                client_secret=os.getenv("CLIENT_SECRET"),
                user_agent='Showathrougs')
page = r.subreddit('Showerthoughts')


@bot.event
async def on_ready():
    print("Bot started")           

@bot.command(pass_context=True)
async def shower(ctx):
    top_posts = page.hot(limit=400)
    rnd=random.randint(1,199)
    i=0
    for post in top_posts:
        i=i+1
        if i==rnd:
            if i==rnd and not post.over_18:
                await ctx.channel.send(post.title)

    
@bot.command(pass_context=True)
async def prefix(ctx, prefix : str=None):
    bot.command_prefix=prefix
    await ctx.channel.send(f"Prefix changed to {bot.command_prefix}")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return await ctx.send(f"`Unknow command\nUse {bot.command_prefix}help to see all the commands`")
    raise error

bot.add_cog(bot_activity(bot))
bot.run(TOKEN)

