import pandas as pd
from datetime import datetime
from uuid import uuid4

EXCEL_FILE = "roster.xlsx"
OUTPUT_FILE = "andre_roster.ics"

df = pd.read_excel(EXCEL_FILE)

def make_datetime(date_value, time_value):
    date_part = pd.to_datetime(date_value).date()
    time_part = pd.to_datetime(str(time_value)).time()
    return datetime.combine(date_part, time_part)

lines = [
    "BEGIN:VCALENDAR",
    "VERSION:2.0",
    "PRODID:-//RosterCalendarTest//Andre//EN",
    "CALSCALE:GREGORIAN",
    "METHOD:PUBLISH",
]

for _, row in df.iterrows():
    start_dt = make_datetime(row["Date"], row["Start"])
    end_dt = make_datetime(row["Date"], row["End"])
    title = str(row["Title"])

    lines += [
        "BEGIN:VEVENT",
        f"UID:{uuid4()}",
        f"DTSTAMP:{datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')}",
        f"DTSTART:{start_dt.strftime('%Y%m%dT%H%M%S')}",
        f"DTEND:{end_dt.strftime('%Y%m%dT%H%M%S')}",
        f"SUMMARY:{title}",
        "END:VEVENT",
    ]

lines.append("END:VCALENDAR")

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print(f"Created {OUTPUT_FILE}")