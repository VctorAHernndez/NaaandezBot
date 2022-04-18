from typing import Iterable
from typing import Optional

from const.messages import CONFUSED_TEXT
from const.messages import HELP_TEXT
from const.messages import OOPS_TEXT
from const.messages import UWU_HELP_TEXT

class StringHandler:
	def __init__(
		self,
		arg: str,
		signature: str,
		actions: Optional[Iterable[str]] = None,
		parameter: Optional[str] = None,
	) -> None:
		self.arg = arg
		self.signature = signature
		self.actions = set(actions) if actions is not None else None
		self.parameter = parameter

	def help_text(self) -> str:
		return HELP_TEXT.format(
			arg=self.arg,
			actions=self.actions,
			signature=self.signature,
		)

	def oops_text(self) -> str:
		return OOPS_TEXT.format(
			arg=self.arg,
			parameter=self.parameter,
			signature=self.signature,
		)

	def confused_text(self) -> str:
		return CONFUSED_TEXT.format(
			arg=self.arg,
			signature=self.signature,
		)

	def uwu_help_text(self) -> str:
		return UWU_HELP_TEXT.format(
			arg=self.arg,
			signature=self.signature,
		)
