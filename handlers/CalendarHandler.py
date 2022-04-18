import calendar
import pickle
from datetime import datetime
from os import path
from typing import Any
from typing import Dict
from typing import List
from typing import Optional

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.discovery import Resource

# REFERENCE:
# https://developers.google.com/calendar/quickstart/python
# https://googleapis.github.io/google-api-python-client/docs/dyn/calendar_v3.events.html#list
# https://developers.google.com/calendar/concepts/events-calendars?hl=en

class CalendarHandler:
	SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

	def __init__(
		self,
		path_to_app_credentials_file: str,
		path_to_user_token_file: str,
	) -> None:
		self.USER_TOKEN_FILE = path_to_user_token_file
		self.APP_CREDENTIALS = path_to_app_credentials_file
		self.service: Optional[Resource] = None

	def authenticate(self) -> None:
		creds: Optional[Credentials] = None

		if path.exists(self.USER_TOKEN_FILE):
			with open(self.USER_TOKEN_FILE, 'rb') as token:
				creds = pickle.load(token)

		if creds is None or not creds.valid:

			if creds is not None and creds.expired and creds.refresh_token:
				creds.refresh(Request())
			else:
				flow = InstalledAppFlow.from_client_secrets_file(
					self.APP_CREDENTIALS,
					self.SCOPES,
				)
				creds = flow.run_local_server(port=0)

			with open(self.USER_TOKEN_FILE, 'wb') as token:
				pickle.dump(creds, token)

		self.service = build('calendar', 'v3', credentials=creds)

	def fetch_month_events(self) -> List[Dict[str, Dict[str, Any]]]:

		if self.service is None:
			raise Exception('You need to authenticate first!')

		# Extract today's info
		now = datetime.utcnow()
		month = now.month
		year = now.year
		_, num_days_in_month = calendar.monthrange(year, month)

		# Construct first and last days of the month
		first_day_of_month = datetime(year, month, 1).isoformat() + 'Z'
		last_day_of_month = datetime(year, month, num_days_in_month).isoformat() + 'Z'

		# Get (up to 250) events
		events_result: Dict[str, Any] = (
			self.service.events()
			.list(
				calendarId='primary', 
				timeMin=first_day_of_month,
				timeMax=last_day_of_month,
				singleEvents=True,
				orderBy='startTime',
			)
			.execute()
		)

		events = events_result.get('items', [])

		return events

	def list_events(
		self,
		events: List[Dict[str, Dict[str, Any]]],
	) -> str:
		"""
		Returns list-formatted events.

		@param events: dict, event response from Google Calendar API
		@return: str, event list
		"""

		string = 'EVENTS:\n'

		# If no events, return early
		if len(events) == 0:
			string += 'No upcoming events this month.'
			return string

		# List events one by one
		for i, event in enumerate(events):
			datestring = event['start'].get('dateTime', event['start'].get('date'))
			event_date = datetime.fromisoformat(datestring)

			if event['start'].get('dateTime', None):
				formatted_date = event_date.strftime('%b %d [%-I:%M %p %Z]')
			else:
				formatted_date = event_date.strftime('%b %d [All-Day]')

			string += f'{i+1}. {formatted_date} – {event["summary"]}\n'

		return string

	def get_event_list(self) -> str:
		"""Returns list-formatted events."""
		events = self.fetch_month_events()
		return self.list_events(events)

	def get_calendar(
		self,
		spaces: int = 4,
		lines: int = 2,
		highlight: str = '*',
		syntax: str = 'C++',
		enlist: bool = True,
		firstweekday: int = 6,
	) -> str:
		"""
		Return as calendar string in Discord ASCII format.

		@param spaces: int, number of spaces for each "cell" in the calendar table
		@param lines: int, number of lines for each "week" in the calendar table
		@param highlight: str, character to "highlight" calendar dates with
		@param syntax: str, Discord's syntax highlighting of... C++, Python, CSS, Apache, etc.
		@return: str, ASCII Calendar with event list below:
		"""

		# Get events
		# TODO: get previous/next month's events
		events = self.fetch_month_events()

		# Extract today's info
		now = datetime.utcnow()
		month = now.month
		year = now.year

		# Get meta info from TC (title and days)
		tc = calendar.TextCalendar()
		tc_string = tc.formatmonth(year, month, w=spaces, l=lines)
		meta = tc_string.split('\n')
		title = meta[0] + (lines - 1) * '\n'
		header = meta[lines] + (lines - 1) * '\n'

		# Construct Calendar
		cal = calendar.Calendar(firstweekday=firstweekday)
		month = cal.monthdatescalendar(year, month)
 		
 		# Construct string (with highlight applied)
		string = syntax + '\n'
		string += title
		string += header
	
		for week in month:
			for date in week:
				for event in events:
					datestring = event['start'].get('dateTime', event['start'].get('date'))
					event_date = datetime.fromisoformat(datestring).date()

					if date == event_date:
						detail = str(date.day) + highlight
						string += '{:^{}s}'.format(detail, spaces + 1)
						break

				else:
					# Triggered if no 'break' was executed
					string += '{:^{}d}'.format(date.day, spaces + 1) 

			string += lines * '\n'

		# Append events list
		if enlist:
			string += '\n'
			string += self.list_events(events)

		return string
