import os
import discord
import requests
import json
import random
from replit import db
from keep_alive import keep_alive


client = discord.Client()

if "responding" not in db.keys():
  db["responding"] = True


def get_quote():
  response = requests.get('https://zenquotes.io/api/random') 
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + ' -' + json_data[0]['a']
  return(quote)

def update_bro_talks(bro_talk):
  if "bro_talks" in db.keys():
    bro_talks = db["bro_talks"]
    bro_talks.append(bro_talk)
    db["bro_talks"] = bro_talks 
  else:
    db["bro_talks"] = [bro_talk]

def delete_bro_talks(index):
  bro_talks = db["bro_talks"]
  if len(bro_talks) > index:
    del bro_talks[index]
    db["bro_talks"] = bro_talks


sad_words = ["unhappy","sad","hzn","kahar",
"depressed","suicide","fuck me","I hate myself",
"Im beta male","Im black pilled","Im blue pilled",]

starter_talks = ["shut the fuck up","man up","Don't be a beta","stop this bullshit","fuck that shit bro","stop bitching","stop fucking around","stop this bullshit and get your shit togther"]


@client.event
async def on_ready():
  print('logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  msg = message.content

  if msg.startswith('$stats'):
    await message.channel.send('ONLINE')

  if msg.startswith('$whoami'):
    await message.channel.send('Just a chad with an internet access')

  if msg.startswith('$help'):
    await message.channel.send('you can find the manual on how to use this bot at https://www.google.com/search?client=firefox-b-e&q=your+mom')

  if msg.startswith('$inspire'):
    quote = get_quote()
    await message.channel.send(quote)

  if db["responding"]:
    bro_response = starter_talks
    if "bro_talks" in db.keys():
      bro_response = bro_response.extend(db["bro_talks"])


    if any(word in msg for word in sad_words):
      await message.channel.send(random.choice(starter_talks))


  if msg.startswith("$add_bro_talk"):
    bro_talk = msg.split("$add_bro_talk ",1)[1]
    update_bro_talks(bro_talk)
    await message.channel.send("New bro message added!,Thanks king for the new message")

  if msg.startswith("$del_bro_talk"):
    bro_talks = []
    if "bro_talks" in db.keys():
      index = int(msg.split("$del_bro_talk",1 )[1])
      delete_bro_talks(index)
      bro_talks = db["bro_talks"]
    await message.channel.send(bro_talks)


  if msg.startswith("$list"):
    bro_talks = []
    if "bro_talks" in db.keys():
      bro_talks = db["bro_talks"]
    await message.channel.send(bro_talks)



  if msg.startswith("$responding"):
    value = msg.split("$responding ",1)[1]

    if value.lower() == "on":
      db["responding"] = True
      await message.channel.send("Responding is ON.")
    else:
      db["responding"] = False
      await message.channel.send("Responding is OFF.")


keep_alive()
client.run(os.environ['TOKEN'])
