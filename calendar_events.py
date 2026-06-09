import caldav
import os
from datetime import datetime, timedelta
from icalendar import Calendar


def get_todays_events() -> list[str]:
    client = caldav.DAVClient(
        url="https://caldav.icloud.com/",
        username=os.getenv("ICLOUD_USERNAME"),
        password=os.getenv("ICLOUD_APP_PASSWORD"),
    )

    principal = client.principal()
    calendars = principal.calendars()

    today = datetime.now().date()
    start = datetime.combine(today, datetime.min.time())
    end = start + timedelta(days=1)

    events = []  # list of (sort_minutes, display_string)
    for calendar in calendars:
        try:
            results = calendar.date_search(start=start, end=end, expand=True)
            for event in results:
                cal = Calendar.from_ical(event.data)
                for component in cal.walk():
                    if component.name != "VEVENT":
                        continue
                    summary = str(component.get("SUMMARY", "Untitled"))
                    dtstart = component.get("DTSTART")
                    if dtstart and hasattr(dtstart.dt, "hour"):
                        dt = dtstart.dt
                        sort_key = dt.hour * 60 + dt.minute
                        time_str = dt.strftime("%-I:%M%p").lower()
                        events.append((sort_key, f"{time_str} - {summary}"))
                    else:
                        # All-day event sorts to top
                        events.append((0, summary))
        except Exception:
            continue

    events.sort(key=lambda x: x[0])
    return [display for _, display in events]
