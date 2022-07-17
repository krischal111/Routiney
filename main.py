import os
from tracemalloc import start

from pyparsing import delimited_list
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

def routine_format(today_routine, times) -> str:
  Holiday='Holiday'
  # print(type(Holiday))
  if (today_routine == Holiday) :
    return str(
    '''
    ********************
    Today is the holiday
      Enjoy your day!!
    ********************
    '''
    )

  else:
    routine_str = ""
    sameperiod = False
    period_str =""
    for i in range(len(today_routine)):
        start_time = times[i]
        end_time   = times[i+1]
        time_str = f"{start_time:5} - {end_time:5} : "
        period = today_routine[i]

        if period == "Same":
          routine_str += time_str+period_str
          continue
        else:
          period_str = ""

        if period in ["Break", ""]:
          routine_str += time_str + period + '\n'
        else:
          subject, type, teachers = period
          if type == 'L':
            period_str += "Lec  of"
          elif type == 'P':
            period_str += "Prac of"
          elif type == 'T':
            period_str += "Tut  of"
          
          period_str += f" {subject:17} by {str(teachers)}\n"
          routine_str +=  time_str+period_str




    return routine_str


def routine_print(day) -> str:
  with open('default_routine.json') as routine_file:
    routine_json = json.load(routine_file)
    routine = routine_json['routine']
    times    = routine_json['times']
    today = (datetime.now().weekday()+1)%7
    days = routine_json["days"]

    if day in days:
      today = days.index(day)

    today_routine = routine[today]
    # print(routine_format(today_routine,times))
    return routine_format(today_routine, times)
    
  

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
      # routine_print()
      arg = ''
      if len(words) > 1:
        arg = words[1]
      bot_reply = f"```\n{routine_print(arg)}\n```"


      
    else:
      i_will_reply = False
      bot_reply = ''

    if i_will_reply :
      await message.channel.send(bot_reply)

# print(routine_print(''))
# client.run(os.getenv('routiney_token'))
client.run('OTg2MjgzODY5NzM1MTE2OTAy.GEhZrK.uaXNlvh2cO--I50ntaTFCUey10QnPsD6-pV4Co')



# import os
# print(os.environ['routiney_token'])