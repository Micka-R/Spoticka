import discord

async def send_message(message, is_private,content):
    try:
        if content is None :
            return
        if is_private:
            return await message.author.send(content) 
        else:
            return await message.channel.send(content)
    except Exception as e:
        print(e)

async def reply_message(message, is_private,content):
    try:
        if content is None :
            return
        if is_private:
            return await message.author.send(content = content, reference = message) 
        else:
            return await message.channel.send(content = content, reference = message)
    except Exception as e:
        print(e)
    
async def send_embed(message,title,url,description,color):
    '''
    send an embed in the channel of message
    '''
    embed=discord.Embed(title=title, 
                        url=url, 
                        description=description,
                        color=color)
    return await message.channel.send(embed=embed)


async def edit_embed(message,title,url,description,color):
    '''
    replace embed in message by new embed
    '''
    embed=discord.Embed(title=title, 
                        url=url, 
                        description=description,
                        color=color)
    return await message.edit(embed = embed)

async def edit_response(interaction,title,url,description,color):
    embed=discord.Embed(title=title, 
                        url=url, 
                        description=description,
                        color=color)
    while True:
            try:
                return await interaction.edit_original_response (embed = embed,content = "")
            except discord.errors.Any as e:
                print("discord.errors.HTTPException retrying ...")
    