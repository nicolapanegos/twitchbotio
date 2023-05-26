##########################################################
#             -= TwitchBotIO version 1.1 =-              #        
#    This bot is made to integrate twitch to the Driver  #
#                                                        #
# This bot need TwitchIO version 2.6.0 installed         #
# https://twitchio.dev/                                  #
# pip install -U twitchio                                #
#                                                        #
# Git https://github.com/nicolapanegos/twitchbotIO       #
##########################################################

import modules
import config

headers = modules.CaseInsensitiveDict()
headers["Content-Type"] = "application/json"

# Pretty logs
def prRed(skk): print("\033[91m {}\033[00m" .format(skk))
def prGreen(skk): print("\033[92m {}\033[00m" .format(skk))
def prYellow(skk): print("\033[93m {}\033[00m" .format(skk))
def prLightPurple(skk): print("\033[94m {}\033[00m" .format(skk))
def prPurple(skk): print("\033[95m {}\033[00m" .format(skk))
def prCyan(skk): print("\033[96m {}\033[00m" .format(skk))
def prLightGray(skk): print("\033[97m {}\033[00m" .format(skk))
def prBlack(skk): print("\033[98m {}\033[00m" .format(skk))

class TwitchBot(modules.commands.Bot):
    def __init__(self):
        # Login
        super().__init__(token=config.user_token, prefix='?', initial_channels=[config.channel_name])

    async def event_ready(self):
        # Start up log
        prCyan(f'Ready')

    async def event_message(self, message):
        # utf-8 to be fix
        pattern = r'[\{\}\[\]@*\'"]'
        filtered_message_re = modules.re.sub(pattern, '', message.content)
        #filtered_message = filtered_message_re.encode('utf-8')
        filtered_message = filtered_message_re

        # exlude user check
        if message.author.name in config.exlude_user:
            print('---------------------------------------------------------------------------')
            prYellow(message.author.name + ' is on exlude list. Ignored...')
        # exlude ban words
        elif filtered_message and any(word in filtered_message for word in config.banned_words):
            print('---------------------------------------------------------------------------')
            prRed(message.author.name + ' say a banned word. Ignored...')
        # approved messages
        elif filtered_message:
            message_data =  f'{config.fixgraph_l}"author":"{message.author.name}", "content":"{filtered_message}"{config.fixgraph_r}'
            response = modules.requests.post(config.driver_url, message_data, headers=headers) # Send to the Driver
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

def Driver_connection(host, port):
    sock = modules.socket.socket(modules.socket.AF_INET, modules.socket.SOCK_STREAM)
    sock.settimeout(5) 
    while True:
        try:
            sock.connect((host, int(port)))
            prCyan(f'Connected to ' + host + ':' + config.driver_port)
            prCyan('TwitcBotIO starting...')
            twitchbot.run()
            #sock.close()
            break
        except (modules.socket.timeout, ConnectionRefusedError):
                prRed( config.driver_domain + ':' + config.driver_port + ' unreachable... I\'ll try again in 5 seconds...')
                modules.time.sleep(5)

Driver_connection(config.driver_domain, config.driver_port)
