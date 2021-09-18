from flask import Flask
from threading import Thread


app=Flask('')

@app.route('/')
def home():
  return("I am awake")

def run():
  app.run(host='0.0.0.0',port=5000)

def keep_awake():
  l=Thread(target=run)
  l.start()
