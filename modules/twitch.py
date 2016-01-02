import sopel.module
import requests
import os
import signal
from datetime import datetime
import time
import pickle

customs = {}
try:
    with open('customs.pickle', 'rb') as f:
        customs = pickle.load(f)
except Exception as e:
    print(e)

if customs != {}:
    @sopel.module.commands(*list(customs))
    def custom(bot, trigger):
        command = trigger.match.group(0)[1:]
        bot.say(bot.customs[command])

def setup(bot):
    bot.customs = customs
    bot.cap_req('twitch', ':twitch.tv/membership')

def save_customs(bot):
    with open('customs.pickle', 'wb') as f:
        pickle.dump(bot.customs, f)

@sopel.module.commands('kill')
def kill(bot, trigger):
    if trigger.admin:
        os.kill(os.getpid(), signal.SIGTERM)

@sopel.module.commands('addcommand')
def add_command(bot, trigger):
    if not trigger.admin:
        return
    message = trigger.match.group(0).split(maxsplit=2)
    try:
        command = message[1]
        content = message[2]
        bot.customs[command] = content
        save_customs(bot)
        bot.say('Added command !{}, which will output: \'{}\'. Will take effect when the bot is restarted.'.format(command, content))
    except Exception as e:
        print(e)
        bot.say('Failed to add command. Is the command formatted properly?')

@sopel.module.commands('removecommand')
def remove_command(bot, trigger):
    if not trigger.admin:
        return
    try:
        message = trigger.match.group(0).split(maxsplit=1)
        del bot.customs[message[1]]
        save_customs(bot)
        bot.say('Successfully removed command.')
    except Exception as e:
        print(e)
        bot.say('Failed to remove command. Is the command formatted properly?')

@sopel.module.commands('uptime')
def uptime(bot, trigger):
    try:
        response = requests.get('https://api.twitch.tv/kraken/streams/{}'.format(bot.config.twitch.streamer)).json()
        epoch = datetime.strptime(response['stream']['created_at'], '%Y-%m-%dT%H:%M:%SZ')
        delta = datetime.now() - epoch
        hours, remainder = divmod(delta.total_seconds(), 3600)
        minutes, seconds = divmod(remainder, 60)
        bot.say('The stream has been online for {} hours, {} minutes and {} seconds!'.format(int(hours), int(minutes), int(seconds)))
    except Exception as e:
        bot.say('The stream is offline!')
