#!/opt/python3.5/bin/python

import asyncio
import praw
import time
import discord
import logging
import random
import re
import os
import io

try:
    import creds
except:
    print("Need valid creds.py to login")
    exit()


logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='error.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)
client = discord.Client()
client.login(creds.discordid, creds.discordpw)
user_agent = "Rolebot by BassGNT/jBASSr."
thing_limit = 25
last_summons = time.time()
script_root = os.path.dirname(os.path.realpath(__file__))

with io.open(os.path.join(script_root, 'quotes.txt'),'r',encoding='utf8') as f:
    quotes = f.readlines()
with io.open(os.path.join(script_root, 'helpmessage.txt'),'r',encoding='utf8') as f:
    helpmessage = f.read()
with io.open(os.path.join(script_root, 'rags.txt'),'r',encoding='utf8') as f:
    rags = f.readlines()
with io.open(os.path.join(script_root, '8ball.txt'),'r',encoding='utf8') as f:
    ball = f.readlines()
with io.open(os.path.join(script_root, 'rules.txt'),'r',encoding='utf8') as f:
    rules = f.read()


ignore = [
      'WoWbot',
      'RH1-N0',
      ]

roles = [
      'dk',
      'druid',
      'hunter',
      'mage',
      'monk',
      'paladin',
      'priest',
      'rogue',
      'shaman',
      'warlock',
      'warrior',
      ]


lockroles = ["Moderator", "Chat Moderator", "Twitterbot"]
cannotset = """Sorry I could not set your class because I did not
            recognize the class you chose. Type `@WoWbot help` for
            more information."""

# blank reddit account :)
r = praw.Reddit(client_id='',
                client_secret='',
                password='',
                user_agent=user_agent,
                username=''
                )
# r.login(creds.redditid,creds.redditpw) #replace with OAuth soon


wowsub = r.subreddit('WoW') #wowsub = r.get_subreddit('WoW')
print(r.read_only) # Output state of reddit instance.

if not client.is_logged_in:
    print('Login fail but continuing')
    # exit(1)


# def say_reddit_submission(submission, message):
#     saythis = submission.short_link
#     client.send_message(message.channel,saythis)
# 
# 
# def random_reddit_submission(subtype):
#     if subtype == 'hot':
#         submissions = wowsub.get_hot(limit = 27)
#     elif subtype == 'rising':
#         submissions = wowsub.get_rising(limit = 25)
#     elif subtype == 'new':
#         submissions = wowsub.get_new(limit = 25)
#     elif subtype =='controversial':
#         submissions = wowsub.get_controversial(limit = 25)
#     else:
#         print("Not a valid submission type")
#         return(False)
#     top_submissions = []
#     for sub in submissions:
#         top_submissions.append(sub)
#     random_submission = random.choice(top_submissions)
#     return(random_submission)


@client.event
def on_ready():
    print('Connected!')
    print('Username: ' + client.user.name)
    print('ID: ' + client.user.id)
    print('--Server List--')
    for server in client.servers:
        print(server.name)


@client.event
def on_message(message):
    if message.author.name not in ignore:
        if message.author.id == "113097494489006080":
            if '!roles' in message.content.lower():
                print(message.author.name + ': ' + message.content)
                for server in client.servers:
                    if server.name == 'wow':
                        wowroles = ''
                        for role in server.roles:
                            wowroles += '`'
                            wowroles += role.name
                            wowroles += '`'
                            wowroles += ': '
                            wowroles += role.id
                            wowroles += '\n'
                        client.send_message(message.channel, wowroles[1:])
            if '!colour' in message.content.lower():
                try:
                    myrole = next(role for role in roles if role in
                                    message.content.lower().split())
                except:
                    myrole = 'unrecognized'
                    print(myrole)
                octothorpe = message.content.lower().index("#")
                end = octothorpe + 7
                rolecolour = message.content.lower()[octothorpe:end]
                print('Setting ' + myrole + ' to ' + rolecolour)
                for role in server.roles:
                    if (myrole ==role.name):
                        client.edit_role(message.server, role, colour=rolecolour)


        if message.author.id == "77511942717046784":
            if '!butts' in message.content.lower():
                client.send_message(message.channel, '<3')


        if '!help' in message.content.lower():
            client.send_message(message.channel, helpmessage)


        elif '!id' in message.content.lower():
            print(message.author.name + ': ' + message.author.id)


        elif '!class' in message.content.lower():
            print(' class is true')
            doit = True
            for role in message.author.roles:
                if role.name in lockroles:
                    doit = False
            if 'remove' in message.content.lower() and doit:
                client.replace_roles(message.author,client.servers[1].roles[0])
                print('setting ' + message.author.name + ' to have no class')
            try:
                myrole = next(role for role in roles if role in message.content.lower().split())
                print(myrole)
            except:
                myrole = "unrecognized"
                doit = False
                client.send_message(message.author, cannotset)
            print('setting ' + message.author.name + ' as ' + myrole)
            for server in client.servers:
                if server.name == 'wow' and doit:
                    for role in server.roles:
                        if (myrole == role.name):
                            client.replace_roles(message.author,role)
                            client.delete_message(message)

        elif '!purge' in message.content.lower():
            for server in client.servers:
                if server.name == 'wow':
                    purged = random.choice(server.members)
                    ragnarquote = random.choice(rags)
                    saythis = ragnarquote + '\n'
                    saythis += purged.name + ' has been purged.'
                    client.send_message(message.channel,saythis)

        elif '!8ball' in message.content.lower():
            question = message.content
            question = re.sub('!8ball', '', question)
            saythis = message.author.name + ' asked: _' + question + '_\n'
            saythis += 'The 8 Ball says: ' + random.choice(ball)
            client.send_message(message.channel, saythis)


        #elif '!avatar' in message.content.lower():
        #    pass

        elif '!faq' in message.content.lower():
            saythis = "Check out the faq at: http://wowgfaq.neocities.org/"
            client.send_message(message.channel, saythis)

        elif '!rules' in message.content.lower():
            client.send_message(message.author, rules)
               


        elif '!aphoenix' in message.content.lower():
            global last_summons
            time_passed = time.time() - last_summons 
            print(time_passed)
            if time_passed > 3600:
                saythis = message.author.name + ' wants you in Discord'
                try:
                    r.send_message('aphoenix', 'Discord Summons', saythis)
                    client.send_message(message.channel, 'Aphoenix has been summoned.')
                    last_summons = time.time()
                except:
                    pass
            else:
                client.send_message(message.channel, 'You are doing too much aphoenix summoning.')


while(True):
    try:
        client.run()
    except Exception as e:
        print(e)
        time.sleep(300)

