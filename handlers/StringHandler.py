from const.messages import HELP_TEXT, OOPS_TEXT, CONFUSED_TEXT, UWU_HELP_TEXT

class StringHandler:

	def __init__(self, arg, signature, actions=None, parameter=None):
		self.arg = arg
		self.signature = signature
		self.actions = set(actions) if (actions is not None) else None
		self.parameter = parameter

	def help_text(self):
		return HELP_TEXT.format(arg=self.arg,
								actions=self.actions,
								signature=self.signature)

	def oops_text(self):
		return OOPS_TEXT.format(arg=self.arg,
								parameter=self.parameter,
								signature=self.signature)

	def confused_text(self):
		return CONFUSED_TEXT.format(arg=self.arg,
									signature=self.signature)

	def uwu_help_text(self):
		return UWU_HELP_TEXT.format(arg=self.arg,
									signature=self.signature)