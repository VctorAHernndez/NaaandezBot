import os
import dotenv
import logging
from Bot import Bot

def main():

	# Logging Setup
	logger = logging.getLogger('discord')
	logger.setLevel(logging.DEBUG)
	handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
	handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
	logger.addHandler(handler)

	# Load Environment Variables
	dotenv.load_dotenv()

	# Run Bot
	client = Bot()
	client.run(os.getenv('BOT_TOKEN'))

if __name__ == '__main__':
	main()


# USEFUL INIT PARAMETERS:
# status - busy, offline, online, etc.
# activity - "playing pubg", "listening to spotify", etc.

# USEFUL ATTRIBUTES:
# users

# USEFUL METHODS:
# get_channel(id)
# get_user(id)
# get_all_channels() # returns all channels from all guilds
# get_all_members()
# wait_for(event) # 


# USEFUL LISTENERS:
# on_user_update
# on_member_update/join/remove
# on_typing
