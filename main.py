import discord
import json
import os
import requests
import random
from replit import db
from keep_awake import keep_awake

client = discord.Client()

TOKEN=os.environ['Disc_Token']

sad_words=["miserable", "sad", "depressed", "angry", "frustrated"]

perm_encouragements=["Hang in there, Buddy!", "Cheer up, you got this!","You can take on everything!", "Ah shit, thats rough, let it out bud",]

if "responding" not in db.keys():
  db["responding"]=True

def get_quote():
  response=requests.get("https://zenquotes.io/api/random")
  json_data=response.json()
  print(json_data)
  quote=json_data[0]['q']+" - "+json_data[0]['h']
  return(quote)

def update_encouragements(encouraging_message):
  if "encouragements" in db.keys():
    encouragements=db["encouragements"]
    encouragements.append(encouraging_message)
    db["encouragements"]=encouragements
  else:
    db["encouragements"]=[encouraging_message]

def delete_encouragements(index):
    encouragements=db["encouragements"]
    if len(encouragements)>index:
      del encouragements[index]
      db["encouragements"]=encouragements
    else:
      message.channel.send("Message index out of bounds")



@client.event
async def on_ready():
  print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
  if message.author==client.user:
    return


  if message.content.startswith("$inspire"):
    quote=get_quote()
    await message.channel.send(quote)
  if db["responding"]:
    options=perm_encouragements
    if "encouragements" in db.keys():
      options.extend(db["encouragements"])

    if any(word in message.content for word in sad_words):
      await message.channel.send(random.choice(options))

  if message.content.startswith("$new"):
    encouraging_message=message.content.split("new ",1)[1]
    update_encouragements(encouraging_message)
    await message.channel.send("New encouraging message added")

  if message.content.startswith("$del"):
    encouragements=[]
    if "encouragements" in db.keys():
      index=int(message.content.split("del",1)[1])
      delete_encouragements(index)
      encouragements=db["encouragements"].value
      await message.channel.send(encouragements)
  
  if message.content.startswith("$list"):
    encouragements=[]
    if "encouragements" in db.keys():
      encouragements=db["encouragements"].value
    await message.channel.send(encouragements)
  k=str(db["responding"])
  if message.content.startswith("$responding"):
    text=message.content.split("$responding ",1)[1]
    if text.lower()=="true":
      db["responding"]= True
      await message.channel.send("Responding is on")
    elif text.lower()=="false":
      db["responding"]=False
      await message.channel.send("Responding is off")
    else:
      await message.channel.send(f"Not a boolean value. Current status is {k}") 
keep_awake()
client.run(TOKEN)