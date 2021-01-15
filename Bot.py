import glob
import random
from asyncio import TimeoutError
from const.cats import CATS
from const.keywords import LIT
from const.prefixes import PIRU, REKT, CAL, UWU, WAVE
from const.actions import CAL_ACTIONS, REKT_ACTIONS, PIRU_ACTIONS
from const.signatures import PIRU_SIGNATURE, REKT_SIGNATURE, CAL_SIGNATURE, UWU_SIGNATURE
from const.messages import CALENDAR_UNAVAILABLE
from handlers.StringHandler import StringHandler
from handlers.CalendarHandler import CalendarHandler
from config.paths import USER_TOKEN_FILE, APP_CREDENTIALS, REKT_FOLDER, REKT_IMAGE
from discord import Client, Activity, ActivityType, File, utils
from owoify import owoify


class Bot(Client):

	def __init__(self, echo_back=False):

		act = Activity(type=ActivityType.listening,
					name='!rekt, !piru, !cal, !wave, !uwu & lit')

		super().__init__(activity=act)
		self.echo_back = echo_back

		# Instantiate Calendar Handler
		try:
			self.ch = CalendarHandler(APP_CREDENTIALS, USER_TOKEN_FILE)
			self.ch.authenticate()
		except:
			self.ch = None
			raise Exception(CALENDAR_UNAVAILABLE)


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
		elif message.content.startswith(UWU):
			await self._uwu(message)
		elif self.is_lit(message):
			await self._lit(message)


	def is_lit(self, message, thresh=5):
		"""Detects if a given message contains 'lit'"""

		# True if:
		# 1. message length is less than thresh, and
		# 2. message contains 'lit' separated by spaces
		cap = len(message.content) < thresh
		words = message.content.lower().split(' ')
		return cap and (LIT in words)


	async def _echo_back(self, message):
		"""Echo back user's message"""
		await message.channel.send('Message from `{.author}`: {.content}'.format(message))


	async def _lit(self, message):
		"""React with fire emoji and reply '^'"""

		emoji_exists = False

		# KORARU's server
		moving_fire1 = utils.get(message.guild.emojis, name='fueguito')
		if moving_fire1:
			await message.add_reaction(moving_fire1)
			emoji_exists = True

		# PilonSmash's server
		moving_fire2 = utils.get(message.guild.emojis, name='lit')
		if moving_fire2 and not emoji_exists:
			await message.add_reaction(moving_fire2)
			emoji_exists = True

		# Default Case
		if not emoji_exists:
			await message.add_reaction('🔥')

		await message.channel.send('^')


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


	async def _uwu(self, message):
		"""UWUify the given message"""

		arg = message.content.split(UWU)[1].strip()
		sh = StringHandler(arg=UWU, signature=UWU_SIGNATURE)

		# Help section
		if arg == 'help':
			return await message.channel.send(sh.uwu_help_text())
		elif message.content == UWU:
			return await message.channel.send(sh.confused_text())

		def uwuify_sentence(sentence):
			# Note: 
			# * Exclamation point includes kaomojis
			# * Levels: owo, uwu, uvu
			core = owoify(sentence, 'uvu')
			num = random.random()
			tail = '!' if num > 0.5 else '!)'
			tail = '\n' + owoify(tail, 'uvu')
			return core + tail

		# Send uwuified message
		text = uwuify_sentence(arg)
		await message.channel.send(text)


	async def _piru(self, message):
		"""Reply with cat ASCII art"""

		arg = message.content.split(PIRU)[1].strip()
		sh = StringHandler(arg=PIRU, signature=PIRU_SIGNATURE,
						actions=PIRU_ACTIONS, parameter=arg)
		
		# Help section
		if arg == 'help':
			return await message.channel.send(sh.help_text())
		elif message.content == PIRU:
			return await message.channel.send(sh.confused_text())

		# Parse valid arguments
		if arg in CATS:
			return await message.channel.send(f'```{CATS[arg]}```')
		else:
			return await message.channel.send(sh.oops_text())


	async def _rekt(self, message):
		"""Send REKT image"""

		arg = message.content.split(REKT)[1].strip()
		sh = StringHandler(arg=REKT, signature=REKT_SIGNATURE,
						actions=REKT_ACTIONS, parameter=arg)

		# Help section
		if arg == 'help':
			return await message.channel.send(sh.help_text())

		# Parse valid arguments
		if arg == '':
			files = glob.glob(REKT_FOLDER)
			index = random.randint(0, len(files) - 1)
			filename = files[index]
		elif arg in REKT_ACTIONS:
			filename = REKT_IMAGE.format(arg=arg)
		else:
			return await message.channel.send(sh.oops_text())

		# Open and send image
		with open(filename, 'rb') as f:
			picture = File(f, spoiler=False)
			await message.channel.send(file=picture)


	async def _calendar(self, message):
		"""Reply with calendar details"""

		arg = message.content.split(CAL)[1].strip()
		sh = StringHandler(arg=CAL, signature=CAL_SIGNATURE,
						actions=CAL_ACTIONS, parameter=arg)

		# Help section
		if arg == 'help':
			return await message.channel.send(sh.help_text())
		elif message.content == CAL:
			return await message.channel.send(sh.confused_text())

		# Check if CH is ok
		if self.ch is None:
			return await message.channel.send(CALENDAR_UNAVAILABLE)

		# Parse valid arguments
		if arg == 'events':
			string = self.ch.get_event_list()
			return await message.channel.send(f'```{string}```')
		elif arg == 'view':
			calendar_string = self.ch.get_calendar()
			return await message.channel.send(f'```{calendar_string}```')
		else:
			return await message.channel.send(sh.oops_text())

