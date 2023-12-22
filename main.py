import json
import time as time_module
import os
import argparse
from datetime import datetime, timedelta
import aiohttp
from bs4 import BeautifulSoup as html
import requests

start = time_module.perf_counter()

# root = os.getcwd()
root = (os.path.dirname(os.path.abspath(__file__)))
import utils.mylogger as mylogger
from classes.Station import Station
from classes.Route import Route
from classes.Itinerary import Itinerary
# os.chdir(root)


VERSION = "0.6a"
parser = argparse.ArgumentParser(prog=f"MyCpSkAPI V{VERSION}", description='My API for cp.sk', epilog="Written by theonlypeti.")  # TODO separate this and the functions into a separate file so i can import them without running this

# parser.add_argument("--minimal", action="store_true", help="Quiet mode.")
parser.add_argument("--depart", action="store", help="City from", required=True)
parser.add_argument("--to", action="store", help="City to", required=True)
parser.add_argument("--date", action="store", help="Date (dd.mm.yyyy) of departure")
parser.add_argument("--time", action="store", help="Time (hh:mm) of departure")
parser.add_argument("--force", action="store_true", help="Forces the program to use the exact station names provided by the user, even if they contain potential typos or mismatches.")
parser.add_argument("--autocorrect", action="store_true", help="Enables the program to automatically correct the station names provided by the user by guessing the most likely correct names.")
parser.add_argument("--debug", action="store_true", help="Enable debug mode.")
parser.add_argument("--profiling", action="store_true", help="Measures the runtime and outputs it to profile.prof.")
parser.add_argument("--logfile", action="store_true", help="Logs to a file.")
args = parser.parse_args()

mylogger.main(args)  # initializing the logger
from utils.mylogger import baselogger as logger
from utils.levenstein import recommend_words

with open(root + r"/data/stations.json", "r", encoding="utf-8") as f:
    stations = json.load(f).keys()
    logger.debug(f"{len(stations)=}")

# logger.warning(recommend_word("Levie", stations))  #assert Levice
# logger.warning(recommend_word("Podhajska", stations)) #assert Podhájska
# logger.warning(recommend_word("Pozb", stations)) #assert Pozba
# logger.warning(recommend_word("Trencsen", stations)) #assert Trenčín


def make_request(link: str, inputted_datetime: datetime):  # dont judge pls
    # async with aiohttp.ClientSession() as session: #TODO make it async again?
    #     async with session.get(link) as req:
    logger.debug(link)
    req = requests.get(link)
    stranka = req.text
    soup = html(stranka, 'html.parser')
    try:
        timeelem = soup.find("h2", attrs={"class": "reset date"}) or soup.find("h2", attrs={"class": "reset date color-red"}) or soup.find("h2")
        depart_time = timeelem.find("span").text
        time = timeelem.text.removesuffix(depart_time)
        depart_time = datetime.strptime(f"{datetime.now().year}.{depart_time.split(' ')[0]} {time}", "%Y.%d.%m. %H:%M")
        if depart_time < datetime.now() < inputted_datetime:
            depart_time = depart_time.replace(year=datetime.now().year+1)
        currdate = depart_time

        spoj = soup.find("div", attrs={"class": "connection-details"})
        allcities = spoj.find_all("a", attrs={"title": "Zobraziť detail spoja"})
        traintype = spoj.find("img").get("alt")
        logger.debug(allcities)
    except Exception as e:
        logger.error(e)
        return None
    try:
        links = []
        for vlak in allcities:
            links.append(vlak.get("href"))
        # links = a.get("href") #ez szokott errorozni mert nonetype az a
    except AttributeError as e:
        logger.error(e)
        return None

    routes = []
    for link in links:
        with requests.get(link) as req:
            stranka = req.text

        delay = soup.find("a", attrs={"class": "delay-bubble"})
        if delay and delay.contents[0].text.startswith("Aktuálne"):
            dly = delay.contents[0].text.split(" ")[2].strip()
            if dly == "meškania":
                delay = 0
            else:
                delay = dly
                try:
                    delay = int(delay)
                except ValueError:
                    delay = 0
        else:
            delay = 0

        soup = html(stranka, 'html.parser')
        allcities = soup.find_all("li", attrs={"class": "item"})
        othercities = soup.find_all("li", attrs={"class": "item inactive"})
        routecities = set(allcities).difference(set(othercities))
        routecities = [i for i in allcities if i in routecities]

        try:
            distance = int(routecities[-1].find("span", attrs={"class": "distance"}).text.strip("km ")) - int(routecities[0].find("span", attrs={"class": "distance"}).text.strip("km "))
        except ValueError:
            distance = 0

        cities = []
        for child in routecities:
            city = Station.from_soup(child, currdate)
            cities.append(city)
            if city.arrival and city.arrival < currdate: #rollover to the next day
                city.arrival += timedelta(days=1)
                city.departure += timedelta(days=1)
            if city.departure:
                currdate = city.departure

        rt = Route(cities, delay, traintype or None, distance)
        routes.append(rt)

    return Itinerary(routes)


def makeLink(fromcity: str, tocity: str, date: str, time: str) -> str:
    fromcity = fromcity.replace(" ", "%20")
    tocity = tocity.replace(" ", "%20")  # this is not strictly needed as it seems to work fine but let's keep it here
    return f"https://cp.hnonline.sk/vlakbus/spojenie/vysledky/?"+(f"date={date}&" if date else "") + (f"time={time}&" if time else "") +f"f={fromcity}&fc=100003&t={tocity}&tc=100003&af=true&&trt=150,151,152,153" #direct=true


def main():
    inputted_date = datetime.strptime(args.date, "%d.%m.%Y") if args.date else datetime.now()
    inputted_time = datetime.strptime(args.time, "%H:%M") if args.time else datetime.now()
    inputted_datetime = datetime.combine(inputted_date, inputted_time.time())
    if not args.force:
        if args.depart not in stations:
            recdepart = autocomplete_stations(args.depart)
            if not recdepart:
                recdepart = find_stations(args.depart)
            if not args.autocorrect:
                logger.warning(f"{args.depart} is an unknown station. Did you mean {recdepart}")
                logger.warning(f"Supress this warning with --force or autocorrect with --autocorrect")
                return -1
            else:
                args.depart = recdepart[0]
        if args.to not in stations:
            recto = autocomplete_stations(args.to)
            if not recto:
                recto = find_stations(args.to)
            if not args.autocorrect:
                logger.warning(f"{args.to} is an unknown station. Did you mean {recto}")
                logger.warning(f"Supress this warning with --force or autocorrect with --autocorrect")
                return -1
            else:
                args.to = recto[0]
    link = makeLink(args.depart, args.to, args.date, args.time)
    cesta = make_request(link, inputted_datetime)
    print(cesta)
    cesta.pprint()


def get_itinerary(departure: str, destinaton: str, depart_time: datetime = None):
    """Returns an Itinerary object with the given parameters."""
    if not depart_time:
        depart_time = depart_time.now()
    link = makeLink(departure, destinaton, depart_time.strftime("%d.%m.%Y"), depart_time.strftime("%H:%M"))
    return make_request(link, depart_time)


def find_stations(name: str):
    """Returns a list of stations that closely match the name."""
    return recommend_words(name, stations)  # TODO merge these two functions


def autocomplete_stations(name: str):
    """Returns a list of stations whose name begin with name."""
    return [st for st in stations if len(name) > 2 and st.startswith(name)]


if __name__ == "__main__":
    # args = parser.parse_args()
    if args.profiling:
        import cProfile
        import pstats
        with cProfile.Profile() as pr:
            main()
        logger.info(f"{time_module.perf_counter() - start} run time")
        stats = pstats.Stats(pr)
        # stats.sort_stats(pstats.SortKey.TIME)
        # stats.print_stats()
        stats.dump_stats(filename="profile.prof")
        os.system("snakeviz profile.prof")
    else:
        main()


"""Usage:
python main.py --depart "Bratislava" --to "Podhajska" --date 13.01.2024 --time 12:00 --autocorrect
        or
.\.venv\Scripts\python.exe main.py --depart "Bratislava" --to "Podhajska" --date 13.01.2024 --time 12:00 --autocorrect
"""

