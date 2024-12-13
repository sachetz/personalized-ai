from typing import List

def create_event (
    service,
    summary: str,
    start_datetime: str,
    end_datetime: str,
    location: str = None,
    description: str = None,
    start_timezone: str = "America/Los_Angeles",
    end_timezone: str = "America/Los_Angeles",
    attendees: List[str] = None
):
    event = {
        "summary": summary,
        "start": {
            'dateTime': start_datetime,
            'timeZone': start_timezone,
        },
        "end": {
            "dateTime": end_datetime,
            "timeZone": end_timezone,
        }
    }
    if location:
        event["location"] = location
    if description:
        event["description"] = description
    if attendees:
        event["attendees"] = [{"email": lst} for lst in attendees]
    event = service.events().insert(calendarId="primary", body=event).execute()
    return "Event created: %s" % (event.get('htmlLink'))
