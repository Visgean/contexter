import datetime
import os.path
from datetime import timezone

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/calendar.events"]


class Calendar:
    def __init__(self):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
        self.service = build("calendar", "v3", credentials=creds)

    @staticmethod
    def make_token():
        """Create token file from credentials."""
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file("token.json", SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials.json", SCOPES
                )
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open("token.json", "w") as token:
                token.write(creds.to_json())

    def get_calendar_events(self, year, month):
        # Call the Calendar API
        start_date = datetime.datetime(
            year=year, month=month - 1, day=1, tzinfo=timezone.utc
        )
        end_date = start_date + datetime.timedelta(days=100)  # Roughly one month later

        events_result = (
            self.service.events()
            .list(
                calendarId="primary",
                timeMin=start_date.isoformat(),
                maxResults=100,
                timeMax=end_date.isoformat(),
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
        events = events_result.get("items", [])

        if not events:
            return []

        events_formatted = []

        # Prints the start and name of the next 10 events
        for event in events:
            start = event["start"].get("dateTime", event["start"].get("date"))

            date = datetime.datetime.fromisoformat(start)
            date_formatted = date.strftime("%A %Y-%m-%d")
            # attendees = ', '.join([a.get('displayName', a.get('email')) for a in event.get("attendees", [])])

            events_formatted.append(f"{date_formatted}: {event['summary']}")

        return events_formatted

    def add_event(self, summary, description, start_date, end_date, timezone):
        event = {
            "summary": summary,
            "description": description,
            "start": {
                "dateTime": start_date,
                "timeZone": timezone,
            },
            "end": {
                "dateTime": end_date,
                "timeZone": timezone,
            },
        }

        event = self.service.events().insert(calendarId="primary", body=event).execute()
        return event.get("htmlLink")


if __name__ == "__main__":
    Calendar.make_token()

    calendar = Calendar()
    events = calendar.get_calendar_events(2023, 10)
    print(events)
