import datetime
from collections import namedtuple
from datetime import timezone

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build


def get_calendar_events(year, month):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    service = build("calendar", "v3", credentials=creds)

    # Call the Calendar API
    start_date = datetime.datetime(year=year, month=month - 1, day=1, tzinfo=timezone.utc)
    end_date = start_date + datetime.timedelta(days=100)  # Roughly one month later

    events_result = (
        service.events()
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


        events_formatted.append(
            f'{date_formatted}: {event["summary"]}'
        )

    return events_formatted


def add_event(summary, description, start_date, end_date, timezone):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    service = build("calendar", "v3", credentials=creds)

    event = {
        'summary': summary,
        'description': description,
        'start': {
            'dateTime': start_date,
            'timeZone': timezone,
        },
        'end': {
            'dateTime': end_date,
            'timeZone': timezone,
        },
    }

    event = service.events().insert(calendarId='primary', body=event).execute()
    return event.get('htmlLink')



