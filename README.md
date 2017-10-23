# RoleBOT (Modification of WoWbot by aphoenix)

## What's it do?

WoWbot is a python bot that sits in /r/WoW's Discord and quotes Rick from Rick
and Morty and also sets class colours for people who have joined the channel.

## Install Instructions

Make sure you have installed the requirements

    pip install -r requirements.txt

Make sure you meet the non-code requirements of having existing accounts for
both reddit and discord. We don't help you out there, and if you don't this
will just fail. 

Copy `example.creds.py` and edit it appropriately with your account 
information.

Then just call the bot:

    python wowbot.py

It'll let you know if it's connected and what channels are connected.

## Plans

Modify the program to function solely as a role assignment bot.

Remove reddit creds requirements.

Remove other useless functionality.