import discord
import os
import praw
import random
from discord.ext import commands
from discord.ext import tasks


class prefs:
    loopchannel = int(808913329481449513)
    looptime = 3600

    class postlimits:
        manual = 400
        auto = 800


TOKEN = os.getenv("DISCORD_BOT_TOKEN")
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="/",
                   intents=intents,
                   description="Bot made it by Renzo")
                   
r = praw.Reddit(client_id=os.getenv("CLIENT_ID"),
                client_secret=os.getenv("CLIENT_SECRET"),
                user_agent='Showathrougs')
page = r.subreddit('Showerthoughts')


# region Commands
@bot.command(pass_context=True)
async def shower(ctx):
    top_posts = page.hot(limit=prefs.postlimits.manual)
    rnd = random.randint(1, prefs.postlimits.auto - 1)
    i = 0
    for post in top_posts:
        i = i + 1
        if i == rnd and not post.over_18:
            await ctx.channel.send(post.title)
        elif i == rnd and post.over_18:
            await ctx.channel.send("The auto-shower thought selected for this message was a NSFW post so i cant show "
                                   "you it :(, since the developer is too lazy to repeat the search he put this "
                                   "message, Sorry!!!")


@bot.command(pass_context=True)
@commands.has_permissions(manage_channels=True)
async def prefix(ctx, prefx: str = None):
    bot.command_prefix = prefx
    await ctx.channel.send(f"`Prefix changed to {bot.command_prefix}`")
    await bot.change_presence(activity=discord.Game(f"Use {bot.command_prefix}help"), status=discord.Status.online)


@bot.command(pass_context=True)
@commands.has_permissions(manage_channels=True)
async def loop(ctx, time: int = None):
    send_msg.change_interval(seconds=time)
    await ctx.channel.send(f"`Loop time changed to {send_msg.seconds} seconds`")


@bot.command(pass_context=True)
@commands.has_permissions(manage_channels=True)
async def loophere(ctx):
    prefs.loopchannel = ctx.channel.id
    await ctx.channel.send("`Alright, i will send the auto-thoughts here`")


# endregion
# region Tasks
@tasks.loop(seconds=prefs.looptime)
async def send_msg():
    channel = bot.get_channel(prefs.loopchannel)
    top_posts = page.hot(limit=prefs.postlimits.auto)
    rnd = random.randint(1, prefs.postlimits.auto - 1)
    i = 0
    for post in top_posts:
        i = i + 1
        if i == rnd and not post.over_18:
            await channel.send(f"AUTO:{post.title}")
        elif i == rnd and post.over_18:
            await channel.send("The auto-shower thought selected for this message was a NSFW post so i cant show you it"
                               ":(, since the developer is too lazy to repeat the search he put this message, Sorry!!!")


# endregion
# region Events
@bot.event
async def on_ready():
    send_msg.start()
    await bot.change_presence(activity=discord.Game(f"Use {bot.command_prefix}help"), status=discord.Status.online)
    print("Bot started")


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return await ctx.send(f"`Unknown command\nUse {bot.command_prefix}help to see all the commands`")
    raise error
# endregion

bot.run(TOKEN)
