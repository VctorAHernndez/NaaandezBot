import os
import logging

import dotenv

from Bot import Bot

def main():

	# Logging Setup
	logger = logging.getLogger('discord')
	logger.setLevel(logging.DEBUG)

	handler = logging.FileHandler(
		filename='discord.log',
		encoding='utf-8',
		mode='w',
	)
	handler.setFormatter(
		logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s')
	)

	logger.addHandler(handler)

	# Load Environment Variables
	dotenv.load_dotenv()

	# Run Bot
	client = Bot()
	client.run(os.getenv('BOT_TOKEN'))

if __name__ == '__main__':
	main()
