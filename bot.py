import discord
from discord.ext import commands
from discord import app_commands

import commands.add

#import and init queue to store multiple cmd
from queue import Queue
cmd_queue = Queue(maxsize=50)

def run_discord_bot():

    #get auth token from token.secret file
    f = open("token.secret","r")
    TOKEN = f.read()

    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)
    tree = app_commands.CommandTree(client)

    @tree.command(name = "plus", description = "simple addition")
    async def addition_cmd(ctx,a:int,b:int):
        await ctx.response.send_message(f"The calculation result is:\n***{a+b}***" )
    
    @tree.command(name = "add", description = "Add to Spoticka a music using a Youtube music link")
    async def add_cmd(interaction,link:str):
        await interaction.response.send_message("Fetching media info...")
        final = await commands.add.add_media(interaction,link)
        await interaction.channel.send(final)


    
    @client.event
    async def on_ready():
        await tree.sync()
        print(str(client.user) + " : Everything is ready, sir!")
    client.run(TOKEN)