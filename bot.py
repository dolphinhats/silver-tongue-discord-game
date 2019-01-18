import discord
import asyncio
import json
import re
import os
import time
import logging
import sys
import subprocess
import base64


logging.basicConfig(
#    filename="/var/log/bossdad.log",
    level=logging.DEBUG,
    format="[%(asctime)s] %(filename)s:%(lineno)s %(msg)s"
    )

log = logging.getLogger(__name__)
config = {}
with open("config.json","r") as f:
    config = json.load(f)

client = discord.Client()

@client.event
async def on_ready():
    log.info("Ready")

@client.event
async def on_message(message):
    #lets not bother with responding to other bots
    if message.author.bot:
        return

    if message.channel.name in ["silver_tongue","testing-3","bot_testing-grounds"]:
        if "```" in message.content[:3] and "```" in message.content[-3:]:
            testmsg = message.content[3:-3]
            log.debug("Checking message {0}".format(testmsg))
            p = subprocess.Popen([config["verification-script"], base64.b64encode(testmsg.encode()).decode()],stdout=subprocess.PIPE)
            out = ""
            for line in p.stdout:
                out += line.decode()
            await client.send_message(message.channel,"```{0}```\n\n{1}".format(testmsg,out))
        
client.run(config["token"])
