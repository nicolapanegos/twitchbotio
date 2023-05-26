##########################################################
#             -= TwitchBotIO version 1.0 =-              #        
#    This bot is made to integrate twitch to the Driver  #
#                                                        #
# This bot need TwitchIO version 2.6.0 installed         #
# https://twitchio.dev/                                  #
# pip install -U twitchio                                #
#                                                        #
# Git https://github.com/nicolapanegos/twitchbotIO       #
##########################################################

import re
from colorama import Fore, Back, Style
from twitchio.ext import commands
import requests
from requests.structures import CaseInsensitiveDict

# Set up credentials
channel_name = "channel name"
user_token = "oauth:" # You can get oauth token form here https://twitchapps.com/tmi/

#exlude user (streamelemetns, nightbot etc)
exlude_user = ["streamelements", "nightbot"]
#Banned worlds
banned_words = ['test1', 'testb', 'test3', 'testd']

# Set up for inject POST to MuvDriver
driver_url = 'http://localhost:51080/'
driver_headers = "'Content-type' : 'application/json'"
fixgraph_l = "{"
fixgraph_r = "}"
headers = CaseInsensitiveDict()
headers["Content-Type"] = "application/json"

# Utils
def prRed(skk): print("\033[91m {}\033[00m" .format(skk))
def prGreen(skk): print("\033[92m {}\033[00m" .format(skk))
def prYellow(skk): print("\033[93m {}\033[00m" .format(skk))
def prLightPurple(skk): print("\033[94m {}\033[00m" .format(skk))
def prPurple(skk): print("\033[95m {}\033[00m" .format(skk))
def prCyan(skk): print("\033[96m {}\033[00m" .format(skk))
def prLightGray(skk): print("\033[97m {}\033[00m" .format(skk))
def prBlack(skk): print("\033[98m {}\033[00m" .format(skk))

#TwitchBot
class TwitchBot(commands.Bot):
    def __init__(self):
        # Login
        super().__init__(token=user_token, prefix='?', initial_channels=[channel_name])

    async def event_ready(self):
        # Start up log
        prCyan(f'Ready')

    async def event_message(self, message):
        # utf-8 to be fix
        pattern = r'[\{\}\[\]@*\'"]'
        filtered_message_re = re.sub(pattern, '', message.content)
        #filtered_message = filtered_message_re.encode('utf-8')
        filtered_message = filtered_message_re

        # exlude user
        if message.author.name in exlude_user:
            print('---------------------------------------------------------------------------')
            prYellow(message.author.name + ' is on exlude list. Ignored...')
        # exlude ban words
        elif filtered_message and any(word in filtered_message for word in banned_words):
            print('---------------------------------------------------------------------------')
            prRed(message.author.name + ' say a banned word. Ignored...')
        # approved messages
        elif filtered_message:
            message_data =  f'{fixgraph_l}"author":"{message.author.name}", "content":"{filtered_message}"{fixgraph_r}'
            response = requests.post(driver_url, message_data, headers=headers) # Send to the Driver
            # debug prints
            print('---------------------------------------------------------------------------')
            if response.status_code == 200:
                prGreen('Message sent to the driver')
                print("\033[94m {}\033[00m" .format(message.author.name), end=": ")
                print("\033[98m {}\033[00m" .format(filtered_message))
                #prLightGray(message_data)
            else:
                prRed('Error '+ response.status_code)
        
twitchbot = TwitchBot()
twitchbot.run()
