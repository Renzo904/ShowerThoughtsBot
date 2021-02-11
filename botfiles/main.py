import discord
import os
import asyncpraw
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
                   
r = asyncpraw.Reddit(client_id=os.getenv("CLIENT_ID"),
                client_secret=os.getenv("CLIENT_SECRET"),
                user_agent='Showathrougs')


# region Commands
@bot.command(pass_context=True)
async def shower(ctx):
    page = await r.subreddit('Showerthoughts')
    submission_list = [submission async for submission in page.hot(limit=prefs.postlimits.manual) if
                       not submission.stickied and not submission.over_18 and not submission.spoiler]
    await bot.get_channel(prefs.loopchannel).send(random.choice(submission_list).title)


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
    page = await r.subreddit('Showerthoughts')
    submission_list = [submission async for submission in page.hot(limit=prefs.postlimits.manual) if
                       not submission.stickied and not submission.over_18 and not submission.spoiler]
    await bot.get_channel(prefs.loopchannel).send(f"AUTO:{random.choice(submission_list).title}")


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
