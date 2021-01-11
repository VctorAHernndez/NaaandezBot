import datetime
import pickle
import os.path
import calendar
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# REFERENCE:
# https://developers.google.com/calendar/quickstart/python
# https://googleapis.github.io/google-api-python-client/docs/dyn/calendar_v3.events.html#list
# https://developers.google.com/calendar/concepts/events-calendars?hl=en

class CalendarHandler:

	SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

	def __init__(self, app_credentials, user_token_file):
		self.USER_TOKEN_FILE = user_token_file
		self.APP_CREDENTIALS = app_credentials
		self.service = None
		self.SCOPES = CalendarHandler.SCOPES


	def authenticate(self):
		creds = None

		if os.path.exists(self.USER_TOKEN_FILE):
			with open(self.USER_TOKEN_FILE, 'rb') as token:
				creds = pickle.load(token)

		if not creds or not creds.valid:

			if creds and creds.expired and creds.refresh_token:
				creds.refresh(Request())
			else:
				flow = InstalledAppFlow.from_client_secrets_file(
					self.APP_CREDENTIALS, self.SCOPES)
				creds = flow.run_local_server(port=0)

			with open(self.USER_TOKEN_FILE, 'wb') as token:
				pickle.dump(creds, token)

		self.service = build('calendar', 'v3', credentials=creds)


	def fetch_month_events(self):

		if self.service is None:
			raise Exception('You need to authenticate first!')

		# Extract today's info
		now = datetime.datetime.utcnow()
		month = now.month
		year = now.year
		_, num_days_in_month = calendar.monthrange(year, month)

		# Construct first and last days of the month
		first_day_of_month = datetime.datetime(year,
											month,
											1).isoformat() + 'Z'
		last_day_of_month =  datetime.datetime(year, 
											month, 
											num_days_in_month).isoformat() + 'Z'

		# Get (up to 250) events
		events_result = self.service.events().list(calendarId='primary', 
											timeMin=first_day_of_month,
											timeMax=last_day_of_month,
											singleEvents=True,
											orderBy='startTime').execute()
		events = events_result.get('items', [])

		return events


	def list_events(self, events):
		"""
		Returns list-formatted events.

		@param events: dict, event response from Google Calendar API
		@return: str, event list
		"""

		string = 'EVENTS:\n'

		# If no events, return early
		if not events:
			string += 'No upcoming events this month.'
			return string

		# List events one by one
		for i, event in enumerate(events):
			datestring = event['start'].get('dateTime', event['start'].get('date'))
			event_date = datetime.datetime.fromisoformat(datestring)
			if event['start'].get('dateTime', None):
				formatted_date = event_date.strftime('%b %d [%-I:%M %p %Z]')
			else:
				formatted_date = event_date.strftime('%b %d [All-Day]')
			string += f'{i+1}. {formatted_date} – {event["summary"]}\n'

		return string


	def get_event_list(self):
		"""Returns list-formatted events."""
		events = self.fetch_month_events()
		return self.list_events(events)

		
	def get_calendar(self, spaces=4, lines=2, highlight='*', syntax='C++', enlist=True, firstweekday=6):
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
		now = datetime.datetime.utcnow()
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
		# string += (lines - 1) * '\n'
		string += header
		for week in month:
			for date in week:
				for event in events:
					datestring = event['start'].get('dateTime', event['start'].get('date'))
					event_date = datetime.datetime.fromisoformat(datestring).date()
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

