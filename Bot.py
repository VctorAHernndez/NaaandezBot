import discord
import calendar
from os.path import join
from asyncio import TimeoutError
from const.cats import CATS
from const.prefixes import PIRU, WAVE, REKT, CAL
from handlers.CalendarHandler import CalendarHandler


class Bot(discord.Client):

	def __init__(self, echo_back=False):
		super().__init__()
		self.echo_back = echo_back


	async def on_ready(self):
		print('Logged in as {}!'.format(self.user))


	async def on_message(self, message):

		# Omit reading the bot's own messages
		if message.author == self.user:
			return

		if self.echo_back:
			await self._echo_back(message)

		if message.content.startswith(PIRU):
			await self._piru(message)
		elif message.content.startswith(WAVE):
			await self._wave(message)
		elif message.content.startswith(REKT):
			await self._rekt(message)
		elif message.content.startswith(CAL):
			await self._calendar(message)


	async def _echo_back(self, message):
		"""Echo back user's message"""
		await message.channel.send('Message from `{.author}`: {.content}'.format(message))


	async def _piru(self, message):
		"""Reply with cat ASCII art"""

		arg = message.content.split(PIRU)[1].strip()
		
		# Help section
		if arg == 'help':
			return await message.channel.send(f'Try `{PIRU}` followed by any of the following:\n`{set(CATS.keys())}` 🐱')
		elif message.content == PIRU:
			return await message.channel.send(f'You seem confused, try `{PIRU} help` 🐱')

		# Parse valid arguments
		if arg in CATS:
			return await message.channel.send(f'```{CATS[arg]}```')
		else:
			return await message.channel.send(f'Oops! I don\'t know what `{PIRU} {arg}` means... 😥\nTry `{PIRU} help` 🐱')
		

	async def _wave(self, message):
		"""Blush on wave response or roll eyes if no wave"""

		channel = message.channel
		await channel.send('Care to wave at me? 😮')

		def check(m):
			return m.content.count('👋') and m.channel == channel

		try:
			msg = await self.wait_for('message', check=check, timeout=15.0)
		except TimeoutError:
			await channel.send('🙄👎') # change to a reply or a reaction?
		else:
			await channel.send('☺️') # change to a reply or a reaction?


	async def _rekt(self, message):
		"""Send REKT image"""

		# TODO: CHOOSE PICTURE AT RANDOM

		channel = message.channel
		filename = join('img', 'rekt.jpeg')

		with open(filename, 'rb') as f:
			picture = discord.File(f, spoiler=True)
			await channel.send(file=picture)


	async def _calendar(self, message):
		"""Reply with calendar details"""

		arg = message.content.split(CAL)[1].strip()

		# Supported actions
		CAL_ACTIONS = ['events, view']

		# Help section
		if arg == 'help':
			return await message.channel.send(f'Try `{CAL}` followed by any of the following:\n`{set(CAL_ACTIONS)}` 🗓')
		elif message.content == CAL:
			return await message.channel.send(f'You seem confused, try `{CAL} help` 🗓')

		# Instantiate Calendar Handler
		USER_TOKEN_FILE = join('config', 'token.pickle')
		APP_CREDENTIALS = join('config', 'credentials.json')
		ch = CalendarHandler(APP_CREDENTIALS, USER_TOKEN_FILE)
		ch.authenticate()

		# Parse valid arguments
		if arg == 'events':
			string = ch.get_event_list()
			return await message.channel.send(f'```{string}```')
		elif arg == 'view':
			calendar_string = ch.get_calendar()
			return await message.channel.send(f'```{calendar_string}```')
		else:
			return await message.channel.send(f'Oops! I don\'t know what `{CAL} {arg}` means... 😥\nTry `{CAL} help` 🗓')

