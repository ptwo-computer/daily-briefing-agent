import caldav
import os
from datetime import datetime, timedelta


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

    events = []
    for calendar in calendars:
        try:
            results = calendar.date_search(start=start, end=end, expand=True)
            for event in results:
                vevent = event.vobject_instance.vevent
                summary = str(vevent.summary.value) if hasattr(vevent, "summary") else "Untitled"

                # Include time if not an all-day event
                if hasattr(vevent, "dtstart") and hasattr(vevent.dtstart.value, "hour"):
                    start_time = vevent.dtstart.value.strftime("%-I:%M%p").lower()
                    events.append(f"{start_time} – {summary}")
                else:
                    events.append(summary)
        except Exception:
            continue

    return sorted(events)
