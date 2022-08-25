import requests
import json
import sys


class colors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


windShow = False

# Check for no args
if len(sys.argv) < 2:
    print("Not enough arguments, see --help")
    sys.exit()
if sys.argv[1] == "--help":
    print("USAGE: python py-metar.py <airport icao code 1> <2> <3> etc...")
    sys.exit()

# remove the "python py-metar.py" from the args list
sys.argv.pop(0)
if "-w" in sys.argv:
    windShow = True
    sys.argv.remove("-w")


# Characters for formatting output later
chars = "[]'"

# Get API Key
with open("key.txt", "r") as f:
    key = f.read()
f.close()

for i in sys.argv:
    # Get airport and uppercase input
    station = sys.argv[sys.argv.index(i)].upper()

    # Set url
    url = f"https://api.checkwx.com/metar/{station}?x-api-key={key}"
    req = requests.get(url)

    # Get metar data
    try:
        req.raise_for_status()
        resp = json.loads(req.text)
    except requests.exceptions.HTTPError as e:
        print(e)
    # Get the metar from the JSON
    result = str(resp["data"])

    # Format the metar to get rid of non-needed characters
    for x in chars:
        result = result.replace(x, "")

    # Show wind in terms of cardinal directions
    if windShow:
        bearing = result[13:16]
        if bearing[0] == "0":
            bearing -= bearing[0]
        bearing = int(bearing)

        if bearing >= 350 and bearing <= 10:
            direction = "N"
        if bearing >= 20 and bearing <= 30:
            direction = "NNE"
        if bearing >= 40 and bearing <= 50:
            direction = "NE"
        if bearing >= 60 and bearing <= 70:
            direction = "ENE"
        if bearing >= 80 and bearing <= 100:
            bearing = "E"
        if bearing >= 110 and bearing <= 120:
            direction = "ESE"
        if bearing >= 130 and bearing <= 140:
            direction = "SE"
        if bearing >= 150 and bearing <= 160:
            direction = "SSE"
        if bearing >= 170 and bearing <= 190:
            direction = "S"
        if bearing >= 200 and bearing <= 210:
            direction = "SSW"
        if bearing >= 220 and bearing <= 230:
            direction = "SW"
        if bearing >= 240 and bearing <= 250:
            direction = "WSW"
        if bearing >= 260 and bearing <= 280:
            direction = "W"
        if bearing >= 290 and bearing <= 300:
            direction = "WNW"
        if bearing >= 310 and bearing <= 340:
            direction = "NW"
        if bearing >= 330 and bearing <= 340:
            direction = "NNW"

    # Print final result
    print(f"METAR for: {colors.WARNING}{i.upper()}{colors.ENDC}")
    print(f"{colors.OKGREEN} {result} {colors.ENDC}")
    if windShow:
        print(f"{colors.OKCYAN}Wind from: {direction} {colors.ENDC}\n")
