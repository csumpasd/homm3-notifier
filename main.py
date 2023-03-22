import asyncio
import os
import discord
from dotenv import load_dotenv
from PIL import ImageGrab as ig

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
bot = discord.Bot()


class Player:
    def __init__(self, tag, clr):
        self.tag = tag
        self.clr = clr
        self.been_pinged = False


players = []
pixelCoords = (ig.grab().width/2, ig.grab().height/2+20)  # Middle of screen
prev_color = ""


@bot.event
async def on_ready():
    print(f'{bot.user} is ready and online!')


@bot.command(description="Add player")  # this decorator makes a slash command
async def add_player(ctx, member: discord.Member):  # a slash command will be created with the name "ping"
    screen = ig.grab()
    color = screen.getpixel(pixelCoords)
    players.append(Player(member, color))
    await ctx.respond(f"{member.display_name} has been added to the game with color: {color}")


@bot.command(description="Remove player")  # this decorator makes a slash command
async def rem_player(ctx, member: discord.Member):  # a slash command will be created with the name "ping"
    found = False
    for player in players:
        if player.tag == member:
            players.remove(player)
            found = True

    if not found:
        await ctx.respond(f"{member.display_name} is not in the list of players")
    else:
        await ctx.respond(f"{member.display_name} has been removed from the list of players")


@bot.command(description="List players")
async def list_players(ctx):
    if players.count == 0:
        await ctx.respond("Player list is empty")
    else:
        await ctx.respond("Players:")
        for player in players:
            await ctx.send(player.tag.display_name)


async def pinger(ctx):
    global prev_color
    while True:
        screen = ig.grab()
        color = screen.getpixel(pixelCoords)
        if color != prev_color:
            prev_color = color
            for player in players:
                if player.clr == color:
                    if not player.been_pinged:
                        for p in players:
                            p.been_pinged = False
                        player.been_pinged = True
                        await ctx.send(f"It's {player.tag.mention}'s turn.")

        await asyncio.sleep(5)


@bot.command(description="Start game")
async def start_game(ctx):
    await ctx.respond("Game has been started!")
    bot.loop.create_task(pinger(ctx))


@bot.command(description="Stop game")
async def stop_game(ctx):
    await ctx.respond("Game has been stopped!")
    bot.loop.stop()


@bot.command(description="Reset game")
async def reset_game(ctx):
    await ctx.respond("Game has been reset!")
    players.clear()
    bot.loop.stop()


bot.run(TOKEN)
