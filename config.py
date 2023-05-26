# Set up credentials
channel_name = 'il_nikk' # Channel from where to get messages
user_token = 'oauth:' # You can get oauth token form here here https://twitchapps.com/tmi/

#exlude bot or other user (streamelemetns, nightbot etc)
exlude_user = ['streamelements', 'nightbot']
#Banned words
banned_words = ['test1', 'testb', 'test3', 'testd']

# Set up for inject POST to MuvDriver
driver_domain = 'localhost'
driver_port = '51080'
driver_url = 'http://' + driver_domain + ':' + driver_port
driver_headers = "'Content-type' : 'application/json'"
fixgraph_l = "{"
fixgraph_r = "}"