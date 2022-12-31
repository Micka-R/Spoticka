import discord
from discord.ext import commands
from discord import app_commands

import subprocess
import asyncio
import send
import re


def is_downloading(process):
    '''
    return True if download is still in progress else return False
    '''
    return_code = process.poll()
    if return_code is not None:
        return False
    return True

def get_progress(output):
    
    #find the last occurence of the line we want
    index = -1
    c = 0
    for line in output:
        if re.search("\[download\] Downloading video", line):
            index = c
        c +=1

    if index == -1:
        return "Progress : :red_square:"
    
    #isolate the line to lex it
    line = output[index]

    #extact the numeric values of the line 
    L = [int(s) for s in re.findall(r'\b\d+\b', line.strip())] 

    #generate the bar using the values extected
    bar = ""
    for i in range(L[0]):
            bar += ":green_square:"
            
    for i in range(L[0],L[1]):
        bar += ":red_square:"

    #concat text + bar 
    return "Progress : " + str(L[0]) + " out of " + str(L[1]) + "\n" + bar

def get_title(output):
    #find last occurence of the line we want

    index = -1
    c = 0
    for line in output:
        if re.search("\[download\] Downloading playlist:", line):
            index = c
            break
        c +=1
    
    #isolate the line
    line = output[index]
    
    #generating the title bar this the informations
    buffer = re.split("\s", line.strip())
    title = "Downloading"
    for i in range(3,len(buffer)):
        title += " " + buffer[i]
    
    return title

def download_status(process):
    '''
    parse the output of the process to extract usefill information and generate the title and the progress bar to send in the chat
    return a tuple (title,live_logs) if information found 
    If not found replace with loading
    '''
    #read all of the output
    print("fetch download status")
    output = process.stdout.readlines()
    print("I read the lines")
    title = get_title(output)
    print("I found the title :",title)
    live_logs = get_progress(output)
    
    return (title,live_logs)

async def download_media(interaction, link):
    #run yt-dlp cmd
    return_code = None
    process = subprocess.Popen(['yt-dlp', link],
                           stdout=subprocess.PIPE,
                           universal_newlines=True)

    live_logs = "Progress : :red_square:"
    title = "Dowloading :musical_note:"
    status_embed = await send.edit_response(interaction, title, link, live_logs,0x6CCFF6 )
    #status_embed = await send.send_embed(message, title , link, live_logs, 0x6CCFF6)

    while is_downloading(process):
        #await asyncio.sleep(1)
        print("downloading")
        title,live_logs = download_status(process)
        print(title)
        print(live_logs)
        status_embed = await send.edit_response(interaction, title, link, live_logs, 0x6CCFF6)
    print(is_downloading(process))

    return process.poll()


async def add_media(message,link):

    return_code = await download_media(message,link)
    
    if return_code is None:
        content = "A error occured contact the administrator"
        color = 0xff1b1c
    elif return_code == 0:
        content = "Media added!"
        color = 0x85ff9e
    else:
        content = "Mission failed sucessfully! Some musics may not be available in France "
        color = 0xff1b1c