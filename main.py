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
    ***************{'*' * len(word_for_day)}
    {word_for_day} is the holiday
         Enjoy your day!!
    ***************{'*' * len(word_for_day)}
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
          subject, period_type, teachers = period
          if period_type == 'L':
            period_str += "Lec  of"
          elif period_type == 'P':
            period_str += "Prac of"
          elif period_type == 'T':
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
    relative_days = routine_json["relative_days"]
    day_number = (datetime.now().weekday()+1)%7

    formal_days = routine_json["formal_days"]
    formal_relative_days = routine_json["formal_relative_days"]
    
    word_for_day = ''
    def convert_daystring_to_daynumber(daystring) -> int:
      split_day = daystring.split(' ',1)
      day_word = split_day[0]
      nonlocal day_number
      nonlocal word_for_day
      if day_word in [day for listofdays in days for day in listofdays]:
        for i in range(7):
          if day_word in days[i]:
            nonlocal day_number
            nonlocal word_for_day
            day_number = i
            word_for_day = formal_days[i]
            # print("i = ", i, "word_for_day = ", word_for_day)
            break;

      if day_word in relative_days:
        add_days = relative_days[day_word]
        day_number += add_days
        word_for_day = f"{formal_relative_days[str(add_days)]} of {word_for_day}"
        # print(f"day number = '{day_number}' and word_for_day = {word_for_day}")
      
      if len(split_day) == 2:
        return convert_daystring_to_daynumber(split_day[1])
      else:
        return day_number
    
    convert_daystring_to_daynumber(day_word)
    today_routine = routine[day_number%7]
    if word_for_day == '':
      word_for_day = 'Today'

    # print("day number = ", day_number, " word for day = ", word_for_day)
    retstr  = f"```The routine for {word_for_day} is:\n"
    retstr += f"{routine_format(today_routine, times, word_for_day)}```"
    # retstr += f"```The routine for the specific day can change. Consult CR for that```"
    return retstr


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
        arg = message.content[len(words[0]):]
      
      bot_reply += f"\n{routine_print(arg)}\n"

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

# cli for !sch command only
def routiney_cli():
  while True:
    print('routiney-cli > ',end='')

    message = input().split(' ',1)
    if(len(message) == 2):
      message = message[1]
    else:
      message = ''
    print(routine_print(message))

routiney_cli()

# import os
# print(os.environ['routiney_token'])