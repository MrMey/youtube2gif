# youtube2gif

Hey, I am a great fan of animated Gifs and each time I watch a YouTube video I am thinking about a gif I could make from the video.  
That's why I create a Telegram bot for this purpose. Just send the link, the start time and stop time to the bot and it will send you back the gif.
It is also possible to use it without the Telegram bot just by a local command line (TODO)

## Getting started

### Important
For now, the bot is private and mono-user and still under development. If you want to use it, you will have to make it run on your own server/aws/heroku.

### Prerequisite
You will have to create first a telegram bot i.e get a token from the bot father (TODO).

As a python lib, you will need the great wrapper : Python-telegram-bot
```
pip install python-telegram-bot
```
You will need also the following packages under Ubuntu 16.04 : ffmpeg, ffprobe, (and gifsicle soon)


### Install
Clone the github and run setup.py (TODO)
Fill the bot_config.json file with your credential and telegram_id (TODO)

## Running the tests
TODO

## Run

### Server side
Just run the command line :  
```
python main.py
```

### User side
#### First time
Look up for the bot in the contact list and start conversation.
Send to the bot:
```
/start
```
Then it will ask you a YouTube link
(add screen shot)
Then it will ask you a start time 

Then it will ask you a stop time

Then it will process the gif and send it back.



# Acknowledgement
* Python-telegram-bot library
