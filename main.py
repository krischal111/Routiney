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

# format a routine according to the (list of times which divide two periods)
def routine_format(day_routine, times, word_for_day = '') -> str:
  if word_for_day == '':
    word_for_day = 'Today'

  Holiday='Holiday'
  if (day_routine == Holiday) :
    return str(
    f'''
    *************************
    {word_for_day+' is the holiday'}
         Enjoy your day!!
    ************************
    '''
    )

  else:
    routine_str = ""
    sameperiod = False
    period_str =""
    for i in range(len(day_routine)):
        start_time = times[i]
        end_time   = times[i+1]
        time_str = f"{start_time:5} - {end_time:5} : "
        period = day_routine[i]

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


# returning string for routine of the day
def routine_print(day_word) -> str:
  with open('default_routine.json') as routine_file:
    routine_json = json.load(routine_file)
    
    routine = routine_json['routine']
    times    = routine_json['times']
    days = routine_json["days"]
    relative_days = routine_json["relative_day"]
    day_number = (datetime.now().weekday()+1)%7
    

    def convert_daystring_to_daynumber(daystring):
      return (datetime.now().weekday()+1)%7

    if day_word in [day for listofdays in days for day in listofdays]:
      for i in range(7):
        if day_word in days[i]:
          day_number = i
          break;

    if day_word in relative_days:
      day_number += relative_days[day_word]

    today_routine = routine[day_number%7]
    # print(routine_format(today_routine,times))
    return routine_format(today_routine, times)


@client.event
async def on_message(message):
  bot_reply=''
  if message.author == client.user:
    return
    
  words = message.content[:].split()
  for word in words:
    # checking for banned words
    if word in banned_words:
      bot_reply = f'You have been warned. Do not use the word "{word}"'
      await message.channel.send(bot_reply)
      bot_reply = ''
  
  # overall command that starts with a bang (!)
  if message.content.startswith('!'):
    i_will_reply = True
    if words[0] == '!ban':
      bot_reply = f'Using "{words[1]}" is forbidden now.'
      banned_words.append(words[1])      
      Log(f'Added {words[1]} to banned_words.')

    # !unban command
    elif words[0] == '!unban':
      theword = words[1]
      if theword == '!everything':
        bot_reply = f'List of previously banned words were {banned_words}. They are no longer banned.'
        banned_words.clear()
      elif theword in banned_words:
        bot_reply = f'Using {theword} is no longer forbidden.'
        banned_words.remove(theword)
        Log(f'Removed {theword} from banned_words.')
    
    # !call command, practically useless
    elif words[0] == '!call':
      bot_reply = f'{message.author.display_name} mentions:'
      for u in message.mentions:
        bot_reply += '\n' + u.display_name

    # !sch command (routine command)
    elif words[0] in ['!routine','!sch','!schedule']:
      # routine_print()
      arg = ''
      if len(words) > 1:
        arg = words[1]
      bot_reply = f"```\n{routine_print(arg)}\n```"

    # !update command
    elif words[0] == "!update":
      await message.channel.send("Okay, updating myself. Just wait a moment... done.")
      exit()

    # !help command
    elif words[0] == "!help":
        with open('default_routine.json') as routine_file:
          help_text = json.load(routine_file)["help"]
          bot_reply+= '```'
          for line in help_text:
            bot_reply += '\n'+line
          print(bot_reply)
          bot_reply+= '```'
    else:
      i_will_reply = False
      bot_reply = ''

    if i_will_reply :
      if len(bot_reply):
        await message.channel.send(bot_reply)

# print(routine_print(''))
client.run(os.getenv('routiney_token'))

def routiney_cli():
  while True:
    print('routiney-cli > ',end='')

    async def process_message(message):
      await on_message()
    message = input()
    task = process_message(message=message)



# import os
# print(os.environ['routiney_token'])