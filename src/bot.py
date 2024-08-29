from discord.ext import commands, tasks
import discord
from twitch import checkIfLive, Stream
#client = discord.Client(intents=discord.Intents.all())

TOKEN = "" #put discord auth token here
CHANNEL_ID = "" #put discord channel id here

#isLive = True

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

@bot.event
async def on_ready():
    global channel
    print("Hello! Test bot is ready!")
    #print('We have logged in as {0.user}'.format(client))
    channel = bot.get_channel(CHANNEL_ID)
    twitchNotifications.start()




@tasks.loop(hours=3)
async def twitchNotifications():
    global isLive
    channelName = "" #put specific channel to check every 3 hours
    stream = checkIfLive(channelName)
    if stream != "OFFLINE":
            await channel.send(f"@everyone {channelName} is live at https://twitch.tv/" + channelName)
    else:
            await channel.send(f"{channelName} is offline")

@bot.command()
async def live(ctx, channelName):
    await ctx.send(f"Checking if {channelName} is live...")
    stream = checkIfLive(channelName)
    if stream != "OFFLINE":
        await ctx.send(f"{channelName} is live at https://twitch.tv/{channelName}")
    else:
        await ctx.send(f"{channelName} is offline")

bot.run(TOKEN)
