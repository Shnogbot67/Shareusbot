import pyrogram
from pyrogram import Client
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import bypasser
import os
from bypasser import ddllist
import requests
import threading
from texts import HELP_TEXT, ABOUT_TEXT
# Follow on GitHub @BotCreator99

# Update key and token 
bot_token = os.environ.get("TOKEN", "5825894034:5802122071:AAGhwOoT3jvZx1al4BRsxCs6oi_kJx0ZAAo")
api_hash = os.environ.get("HASH", "3531771c0d58b9ffc44d12f38c5edbf5")
api_id = os.environ.get("ID", "13556430")
app = Client("my_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)


# loop thread
def loopthread(message):
  urls = []
  for ele in message.text.split():
    if "http://" in ele or "https://" in ele:
      urls.append(ele)
  if len(urls) == 0:
    return

  if bypasser.ispresent(ddllist, urls[0]):
    msg = app.send_message(message.chat.id,
                           "⚡ __generating...__",
                           reply_to_message_id=message.id)
  else:
    if urls[0] in "https://olamovies" or urls[0] in "https://psa.pm/":
      msg = app.send_message(message.chat.id,
                             "🔎 __this might take some time...__",
                             reply_to_message_id=message.id)
    else:
      msg = app.send_message(message.chat.id,
                             "😍 __Uploading...__",
                             reply_to_message_id=message.id)

  link = ""
  for ele in urls:
    if bypasser.ispresent(ddllist, ele):
      try:
        temp = ddl.direct_link_generator(ele)
      except Exception as e:
        temp = "**Error**: " + str(e)
    else:
      try:
        temp = bypasser.shortners(ele)
      except Exception as e:
        temp = "**Error**: " + str(e)
    print("bypassed:", temp)
    link = link + temp + "\n\n"

  try:
    app.edit_message_text(message.chat.id,
                          msg.id,
                          f'__{link}__',
                          disable_web_page_preview=True)
  except:
    app.edit_message_text(message.chat.id, msg.id, "__Failed to Bypass__")


# start command
@app.on_message(filters.command(["start"]))
def send_start(client: pyrogram.client.Client,
               message: pyrogram.types.messages_and_media.message.Message):
  app.send_message(
    message.chat.id,
    f"__👋 Hey **{message.from_user.mention}**,\n\n I Am Shareus Link Bypasser Robot, just send me any shareus links and i will you get you results.\n\n More Command You Can Use:- /help & /about \n\n<b>[This bot powered by @Worldofmovies8]</b>",
    reply_markup=InlineKeyboardMarkup([[
      InlineKeyboardButton(
        "Developer", url="https://t.me/royaldwip")
    ]]),
    reply_to_message_id=message.id)


# help command
@app.on_message(filters.command(["help"]))
def send_help(client: pyrogram.client.Client,
              message: pyrogram.types.messages_and_media.message.Message):
  app.send_message(message.chat.id,
                   HELP_TEXT,
                   reply_to_message_id=message.id,
                   disable_web_page_preview=True)

# hi command
@app.on_message(filters.command(["about"]))
def send_help(client: pyrogram.client.Client,
              message: pyrogram.types.messages_and_media.message.Message):
  app.send_message(message.chat.id,
                   ABOUT_TEXT,
                   reply_to_message_id=message.id,
                   disable_web_page_preview=True)
                
# links
@app.on_message(filters.text)
def receive(client: pyrogram.client.Client,
            message: pyrogram.types.messages_and_media.message.Message):
  bypass = threading.Thread(target=lambda: loopthread(message), daemon=True)
  bypass.start()


# doc thread
def docthread(message):
  if message.document.file_name.endswith("dlc"):
    msg = app.send_message(message.chat.id,
                           "😍 __Bypassing Your Link 🔗__",
                           reply_to_message_id=message.id)
    print("sent DLC file")
    sess = requests.session()
    file = app.download_media(message)
    dlccont = open(file, "r").read()
    link = bypasser.getlinks(dlccont, sess)
    app.edit_message_text(message.chat.id, msg.id, f'__{link}__')
    os.remove(file)


# doc
@app.on_message(filters.document)
def docfile(client: pyrogram.client.Client,
            message: pyrogram.types.messages_and_media.message.Message):
  bypass = threading.Thread(target=lambda: docthread(message), daemon=True)
  bypass.start()


# server loop
print("👍😍😍 Bot Started")
print("😎 follow on GitHub BotCreator99")
app.run()
