import operations
import bot
import discord
import re


async def handle_response(message):
    msg = re.split("\s", message.content)

    if msg == "Hey Spoticka!":
        content =  "What can I do for you @" + str(message.author) + " ?"
        await bot.reply_message(message, False, content)

    elif msg[0] == "//":
        
        if msg[1] == "add":

            return_code = await operations.addmedia(msg[2],message)
            
            if return_code is None:
                content = "A error occured contact the administrator"
                color = 0xff1b1c
            elif return_code == 0:
                content = "Media added!"
                color = 0x85ff9e
            else:
                content = "Mission failed sucessfully! Some musics may not be available in France "
                color = 0xff1b1c

            #await bot.send_message(message, False, content)
            await send_embed(message, "Task finished", msg[2], content, color)
        
        elif msg[1] == "search":
            buffer = ""
            for i in range(2,1,len(msg)):
                buffer += msg[i]
            return operation.searchmedia(buffer)
        else:
            return "Unknown request :sob:\n try:\n// add <<https://music.youtube.....>>\n// search <key words>"