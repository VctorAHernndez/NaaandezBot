import glob
import random
from asyncio import TimeoutError
from typing import List
from typing import Optional

from discord import Activity
from discord import ActivityType
from discord import Client
from discord import Emoji
from discord import File
from discord import Message
from discord import utils
from owoify import owoify

from config.paths import APP_CREDENTIALS
from config.paths import REKT_FOLDER
from config.paths import REKT_IMAGE
from config.paths import USER_TOKEN_FILE
from const.actions import CAL_ACTIONS
from const.actions import PIRU_ACTIONS
from const.actions import REKT_ACTIONS
from const.cats import CATS
from const.keywords import LIT
from const.messages import CALENDAR_UNAVAILABLE
from const.prefixes import CAL
from const.prefixes import PIRU
from const.prefixes import REKT
from const.prefixes import UWU
from const.prefixes import WAVE
from const.signatures import CAL_SIGNATURE
from const.signatures import PIRU_SIGNATURE
from const.signatures import REKT_SIGNATURE
from const.signatures import UWU_SIGNATURE
from handlers.CalendarHandler import CalendarHandler
from handlers.StringHandler import StringHandler

class Bot(Client):
	"""
	Class that represents the Discord Bot's behavior
	"""

	def __init__(self, echo_back: bool = False) -> None:
		act = Activity(
			type=ActivityType.listening,
			name='!rekt, !piru, !cal, !wave, !uwu & lit',
		)

		super().__init__(activity=act)
		self.echo_back = echo_back

		# Instantiate Calendar Handler
		try:
			self.ch = CalendarHandler(APP_CREDENTIALS, USER_TOKEN_FILE)
			self.ch.authenticate()
		except:
			self.ch = None
			raise Exception(CALENDAR_UNAVAILABLE)

	async def on_ready(self) -> None:
		print('Logged in as {}!'.format(self.user))

	async def on_message(self, message: Message) -> None:

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
		elif "68" in message.content:
			await self._69(message)
		elif self.is_lit(message):
			await self._lit(message)

	def is_lit(self, message: Message, thresh: int = 5) -> bool:
		"""Detects if a given message contains 'lit'"""

		# True if:
		# 1. message length is less than thresh, and
		# 2. message contains 'lit' separated by spaces
		cap = len(message.content) < thresh
		words: List[str] = message.content.lower().split(' ')
		return cap and (LIT in words)

	async def _69(self, message: Message) -> None:
		"""Send message in channel where '68' was found"""
		await message.channel.send('69 😎')

	async def _echo_back(self, message: Message) -> None:
		"""Echo back user's message"""
		formatted_message = 'Message from `{.author}`: {.content}'.format(message)
		await message.channel.send(formatted_message)

	async def _lit(self, message: Message) -> None:
		"""React with fire emoji and reply '^'"""

		# KORARU's server
		moving_fire1: Optional[Emoji] = utils.get(message.guild.emojis, name='fueguito')
		if moving_fire1 is not None:
			await message.add_reaction(moving_fire1)
			await message.channel.send('^')
			return

		# PilonSmash's server
		moving_fire2: Optional[Emoji] = utils.get(message.guild.emojis, name='lit')
		if moving_fire2 is not None:
			await message.add_reaction(moving_fire2)
			await message.channel.send('^')
			return

		# Default Case
		await message.add_reaction('🔥')
		await message.channel.send('^')

	async def _wave(self, message: Message) -> None:
		"""Blush on wave response or roll eyes if no wave"""

		channel = message.channel
		await channel.send('Care to wave at me? 😮')

		def check(m: Message) -> bool:
			return m.content.count('👋') and m.channel == channel

		try:
			await self.wait_for('message', check=check, timeout=15.0)
		except TimeoutError:
			await channel.send('🙄👎') # change to a reply or a reaction?
		else:
			await channel.send('☺️') # change to a reply or a reaction?

	async def _uwu(self, message: Message) -> None:
		"""UWUify the given message"""

		arg: str = message.content.split(UWU)[1].strip()
		sh = StringHandler(arg=UWU, signature=UWU_SIGNATURE)

		# Help section
		if arg == 'help':
			return await message.channel.send(sh.uwu_help_text())
		elif message.content == UWU:
			return await message.channel.send(sh.confused_text())

		def uwuify_sentence(sentence: str) -> str:
			# Note: 
			# * Exclamation point includes kaomojis
			# * Parenthesis includes sparkles + kaomojis
			# * Levels: owo, uwu, uvu
			core = owoify(sentence, 'uvu')
			num = random.random()
			tail = '!' if num > 0.5 else ')'
			tail = '\n' + owoify(tail, 'uvu')
			return core + tail

		# Send uwuified message
		text = uwuify_sentence(arg)
		await message.channel.send(text)

	async def _piru(self, message: Message) -> None:
		"""Reply with cat ASCII art"""

		arg: str = message.content.split(PIRU)[1].strip()
		sh = StringHandler(
			arg=PIRU,
			signature=PIRU_SIGNATURE,
			actions=PIRU_ACTIONS,
			parameter=arg,
		)
		
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

	async def _rekt(self, message: Message) -> None:
		"""Send REKT image"""

		arg: str = message.content.split(REKT)[1].strip()
		sh = StringHandler(
			arg=REKT,
			signature=REKT_SIGNATURE,
			actions=REKT_ACTIONS,
			parameter=arg,
		)

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

	async def _calendar(self, message: Message) -> None:
		"""Reply with calendar details"""

		arg: str = message.content.split(CAL)[1].strip()
		sh = StringHandler(
			arg=CAL,
			signature=CAL_SIGNATURE,
			actions=CAL_ACTIONS,
			parameter=arg,
		)

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
