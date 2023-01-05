import discord
from discord.ext import commands
from discord import app_commands

from subprocess import Popen,PIPE,DEVNULL, CalledProcessError
import os
import send
import re

def get_progress(line,live_logs):

    if line[0:28] == "[download] Downloading video":

        L = [int(s) for s in re.findall(r'\b\d+\b', line)]
        gsCount = round(L[0] / L[1] * 20)
        
        bar = ""
        for i in range(gsCount):
            bar += ":green_square:"
        for i in range(gsCount, 20):
            bar += ":red_square:"

        live_logs = "Progress : " + str(L[0]) + " out of " + str(L[1]) + "\n" + bar
        return live_logs
    return live_logs

def get_title(line,title):
    if re.search("\[download\] Downloading playlist",line):
        buffer = re.split("\s", line)
        title = "Downloading "
        for i in range(3,len(buffer)):
            title += " " + buffer[i]
        return title
    return title


async def download_media(interaction, link):
    #run yt-dlp cmd
    return_code = None

    out = open("out.txt","w")
    err = open("err.txt","w")
    

    process = Popen(['yt-dlp', link], stdout=out, stderr=err, universal_newlines=True)
    out.close()
    err.close()
    out = open("out.txt","r")

    live_logs = "Progress : :red_square:"
    title = "Dowloading :musical_note:"
    status_embed = await send.edit_response(interaction, title, link, live_logs,0x6CCFF6 )

    #for line in logs try update progress bar
    while process.poll() is None:
        line = out.readline()
        print(line)
        if title == "Dowloading :musical_note:":
            title = get_title(line,title)
        live_logs = get_progress(line,live_logs)
        status_embed = await send.edit_response(interaction, title, link, live_logs, 0x6CCFF6)

    return_code = process.poll()
    out.close()
   # err.close()
    os.remove("out.txt")
    os.remove("err.txt")

    return (return_code,title)
'''
async def download_media(interaction, link):
    #run yt-dlp cmd
    return_code = None

    #process = Popen(['yt-dlp', link], stdout=DEVNULL,shell=True)
    process = Popen(['yt-dlp', link],stdout=PIPE, bufsize=64, universal_newlines=True)
    

    live_logs = "Progress : :red_square:"
    title = "Dowloading :musical_note:"
    #status_embed = await send.edit_response(interaction, title, link, live_logs,0x6CCFF6 )
    status_embed = await send.send_embed(interaction, title, link, live_logs,0x6CCFF6)

    #for line in logs try update progress bar
    for line in process.stdout:
        print(line)
        if title == "Dowloading :musical_note:":
            title = get_title(line,title)
        live_logs = get_progress(line,live_logs)
        status_embed = await send.edit_embed(status_embed, title, link, live_logs, 0x6CCFF6)

    return_code = process.poll()

    return (return_code,title)
'''

async def add_media(message,link):
    if link[0:25] == "https://music.youtube.com" and ' ' not in link:
        return_code,title = await download_media(message,link)
    else:
        return "Bad link"
    if return_code is None:
        content = "Your link is bullshit mate!"
        color = 0xff1b1c
    elif return_code == 0:
        content = "Finished downloading " + title
        color = 0x85ff9e
    else:
        content = "Mission failed sucessfully! Some musics may not be available in France "
        color = 0xff1b1c
    return content