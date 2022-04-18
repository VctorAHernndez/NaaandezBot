import os
import logging

import dotenv

from Bot import Bot
from config.paths import APP_CREDENTIALS

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
	BOT_TOKEN = os.getenv('BOT_TOKEN')
	GOOGLE_CREDENTIALS = os.getenv('GOOGLE_CREDENTIALS')

	# Write credentials to a local file for easy access
	with open(APP_CREDENTIALS, 'w') as credentials_file:
		credentials_file.write(GOOGLE_CREDENTIALS)

	# Run Bot
	client = Bot()
	client.run(BOT_TOKEN)

if __name__ == '__main__':
	main()
