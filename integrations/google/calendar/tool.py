from typing import List, Optional

from langchain_core.tools import tool
from langchain_core.runnables.config import RunnableConfig

from integrations.google.calendar.auth import authenticate_google_calendar
from integrations.google.calendar.service import create_event

@tool(parse_docstring=True)
def calendar_event_create_tool(
    summary: str,
    start_datetime: str,
    end_datetime: str,
    config: RunnableConfig,
    location: Optional[str] = None,
    description: Optional[str] = None,
    start_timezone: Optional[str] = "America/Los_Angeles",
    end_timezone: Optional[str] = "America/Los_Angeles",
    attendees: Optional[List[str]] = None
):
    """Use this to create an event in user's google calendar.
    This is visible to the user.
    
    Args:
        summary: The title/summary of the calendar event,
        start_datetime: The start time, of format '2015-05-28T09:00:00-07:00',
        end_datetime: The end time, of format '2015-05-28T09:00:00-07:00',
        location: location name, optional,
        description: description of the event, optional,
        start_timezone: start time zone of the event, optional, default is 'America/Los_Angeles',
        end_timezone: start time zone of the event, optional, default is 'America/Los_Angeles',
        attendees: list of emails of attendees for the event, optional
    """

    try:
        user_id = config.get("configurable", {}).get("user_id")
        service = authenticate_google_calendar(user_id)
        return create_event(
            service, 
            summary, 
            start_datetime, 
            end_datetime, 
            location, 
            description, 
            start_timezone, 
            end_timezone,
            attendees
        )
    except BaseException as e:
        return f"Failed to execute. Error: {repr(e)}"
