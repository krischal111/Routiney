import os
import discord
import json
from datetime import datetime

client = discord.Client()
banned_words = []
def Log(msg):
  now = datetime.now()
  print(f'[{now}]: ', msg)
@client.event
async def on_ready():
  Log(f'Logged in as {client.user}')

def routine_print():
  with open('default_routine.json') as routine_file:
    routine = json.load(routine_file)
    print(routine)
  

@client.event
async def on_message(message):
  bot_reply=''
  if message.author == client.user:
    return
    
  words = message.content[:].split()
  for word in words:
    if word in banned_words:
      bot_reply = f'You have been warned. Do not use the word "{word}"'
      await message.channel.send(bot_reply)
      bot_reply = ''
  
  if message.content.startswith('!'):
    i_will_reply = True
    if words[0] == '!ban':
      bot_reply = f'Using "{words[1]}" is forbidden now.'
      banned_words.append(words[1])      
      Log(f'Added {words[1]} to banned_words.')

    elif words[0] == '!unban':
      theword = words[1]
      if theword == '!everything':
        bot_reply = f'List of previously banned words were {banned_words}. They are no longer banned.'
        banned_words.clear()
      elif theword in banned_words:
        bot_reply = f'Using {theword} is no longer forbidden.'
        banned_words.remove(theword)
        Log(f'Removed {theword} from banned_words.')
      
    elif words[0] == '!call':
      bot_reply = f'{message.author.display_name} mentions:'
      for u in message.mentions:
        bot_reply += '\n' + u.display_name

    elif words[0] in ['!routine','!sch','!schedule']:
      routine_print()
        
      bot_reply = f"I am printing today's routine"


      
    else:
      i_will_reply = False
      bot_reply = ''

    if i_will_reply :
      await message.channel.send(bot_reply)

# routine_print()
client.run('OTg2MjgzODY5NzM1MTE2OTAy.Gpyc0S.ocNlu3aACeRZ_2r5c_x19-Xi0wlPUdaLoSYE7I')



# import os
# print(os.environ['routiney_token'])