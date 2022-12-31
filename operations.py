import subprocess
import re
import bot
import responses
async def addmedia(link,message):

    #run yt-dlp cmd
    return_code = None
    process = subprocess.Popen(['yt-dlp', link], 
                           stdout=subprocess.PIPE,
                           universal_newlines=True)

    live_logs = "Progress : :red_square:"
    #status_msg = await bot.send_message(message, False, live_logs)
    title = "Dowloading :musical_note:"
    status_embed = await responses.send_embed(message, title , link, live_logs, 0x6CCFF6)

    while True:

        #check task progress and update live status message
        
        output = process.stdout.readline()
        #print(output.strip())
        if re.search("\[download\] Downloading video",output.strip()):

            L = [int(s) for s in re.findall(r'\b\d+\b', output.strip())]
            
            bar = ""
            for i in range(L[0]):
                bar += ":green_square:"
            for i in range(L[0],L[1]):
                bar += ":red_square:"
            
            live_logs = "Progress : " + str(L[0]) + " out of " + str(L[1]) + "\n" + bar
            print(live_logs)
            
        if re.search("\[download\] Downloading playlist",output.strip()):
            buffer = re.split("\s", output.strip())
            title = "Downloading "
            for i in range(3,len(buffer)):
                title += " " + buffer[i] 
        
        status_embed = await responses.edit_embed(status_embed, title, link, live_logs, 0x6CCFF6)
        # Check if task ended if so exit and return exit code

        return_code = process.poll()
        if return_code is not None:
            print('RETURN CODE', return_code)
            # Process has finished, read rest of the output 
            for output in process.stdout.readlines():
                print(output.strip())
            break
    return return_code

def searchmedia(key):
    return "Your search request was taken into account !"