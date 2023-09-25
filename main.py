import requests
import re
import sys

from bs4 import BeautifulSoup
from icalendar import Calendar, Event
from datetime import datetime

if len(sys.argv) < 2:
    print("Please provide UPRN as argument")
    print("Example: python main.py 123456789012")
    exit(1)

UPRN = sys.argv[1]
URL = "https://www.glasgow.gov.uk/forms/refuseandrecyclingcalendar/PrintCalendar.aspx?UPRN="

cal = Calendar()
cal.add('prodid', '-//nonPointer//Glasgow Bin Collection iCal//EN')
cal.add('version', '2.0')
cal.add('X-WR-CALNAME', 'Bins Collection')
cal.add('X-WR-TIMEZONE', 'Europe/London')
cal.add('X-WR-CALDESC', 'Events of bin collection in Glasgow area')

BINS_DESCRIPTION = {
    "BLUE": "Please use the blue bins to recycle card packaging, cardboard boxes, magazines, newspapers, comics, office paper, brochures, yellow pages, junk mail, envelopes, drinks cans, food tins, empty aerosols cans and plastic bottles. Please do not place any other items into the blue bins.",
    "BROWN": "All compostable garden waste such as - grass cuttings, leaves, hedge trimmings, plants and garden weeds.  Plastic bin liners or carriers bags should not be placed in the brown bin because they are not compostable and can negatively impact the quality of compost produced at the re-processing facility. All garden waste has to be placed loose in your brown bin. Food waste can also be placed within the brown bin using compostable food waste liners.",
    "PURPLE": "Wine Bottles, Beer bottles, Jam jars, Coffee jars, Sauce bottles. Bottle lids/caps can be kept on the bottles.  These are removed at the re-processing plant and recycled separate from the glass.",
    "GREY": "Food waste.",
    "GREEN": "Any items that cannot go into a recycling a blue, purple, brown bin or grey food caddy, can go into a general waste bin other than hazardous, bulky or electrical items and batteries."
}


def extract_dates(tds: list) -> list[int]:
    dates = []
    for td in tds:
        date = td.text.strip()
        if date:
            dates.append(int(date))
    return dates


try:
    page = requests.get(URL + UPRN).text
    soup = BeautifulSoup(page, 'html.parser')
    tables = soup.findAll("table", {"title": "Calendar"})

    month = 0
    events = []

    for table in tables:
        month += 1

        tds = table.findAll("td", {"class": "calendar-day"})

        blues = extract_dates(list(filter(lambda x: x.findAll("img", {"alt": "blue Bin"}), tds)))
        browns = extract_dates(list(filter(lambda x: x.findAll("img", {"alt": "brown Bin"}), tds)))
        purples = extract_dates(list(filter(lambda x: x.findAll("img", {"alt": "purple Bin"}), tds)))
        greys = extract_dates(list(filter(lambda x: x.findAll("img", {"alt": "grey Bin"}), tds)))
        greens = extract_dates(list(filter(lambda x: x.findAll("img", {"alt": "green Bin"}), tds)))

        print("Month: " + str(month))
        print("Blue - " + str(len(blues)) + ": " + str(blues))
        print("Brown - " + str(len(browns)) + ": " + str(browns))
        print("Purple - " + str(len(purples)) + ": " + str(purples))
        print("Grey - " + str(len(greys)) + ": " + str(greys))
        print("Green - " + str(len(greens)) + ": " + str(greens))

        for i in blues:
            event = Event()
            event.add('summary', "Bin collection - Blue")
            event.add('description', BINS_DESCRIPTION["BLUE"])
            event.add('dtstart', datetime(datetime.now().year, month, i).date())
            event.add('dtstamp', datetime(datetime.now().year, month, i))
            event.add('uid', str(datetime.now().year) + str(month) + str(i) + "@glasgowbins")

            events.append(event)

        for i in browns:
            event = Event()
            event.add('summary', "Bin collection - Brown")
            event.add('description', BINS_DESCRIPTION["BROWN"])
            event.add('dtstart', datetime(datetime.now().year, month, i).date())
            event.add('dtstamp', datetime(datetime.now().year, month, i))
            event.add('uid', str(datetime.now().year) + str(month) + str(i) + "@glasgowbins")

            events.append(event)

        for i in purples:
            event = Event()
            event.add('summary', "Bin collection - Purple")
            event.add('description', BINS_DESCRIPTION["PURPLE"])
            event.add('dtstart', datetime(datetime.now().year, month, i).date())
            event.add('dtstamp', datetime(datetime.now().year, month, i))
            event.add('uid', str(datetime.now().year) + str(month) + str(i) + "@glasgowbins")

            events.append(event)

        for i in greys:
            event = Event()
            event.add('summary', "Bin collection - Grey")
            event.add('description', BINS_DESCRIPTION["GREY"])
            event.add('dtstart', datetime(datetime.now().year, month, i).date())
            event.add('dtstamp', datetime(datetime.now().year, month, i))
            event.add('uid', str(datetime.now().year) + str(month) + str(i) + "@glasgowbins")

            events.append(event)

        for i in greens:
            event = Event()
            event.add('summary', "Bin collection - Green")
            event.add('description', BINS_DESCRIPTION["GREEN"])
            event.add('dtstart', datetime(datetime.now().year, month, i).date())
            event.add('dtstamp', datetime(datetime.now().year, month, i))
            event.add('uid', str(datetime.now().year) + str(month) + str(i) + "@glasgowbins")

            events.append(event)
        print("")
    list(map(lambda x: cal.add_component(x), events))

    with open('bin.ics', 'wb') as f:
        f.write(cal.to_ical())

except requests.exceptions.RequestException as e:
    print(e)
    exit()
