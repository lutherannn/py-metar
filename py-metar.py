import requests
import json
import sys
from math import floor


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


verbose = True
windShow = False
convertToFahrenheit = False

# Check for no args
if len(sys.argv) < 2:
    print("Not enough arguments, see --help")
    sys.exit()
if sys.argv[1] == "--help":
    print("USAGE: python py-metar.py <airport icao code 1> <2> <3> etc... -q -w -c")
    print("-q: disables verbose, shows only metar")
    print("-w: shows wind direction")
    print("-f: converts temperature to Fahrenheit")
    sys.exit()

# remove the "python py-metar.py" from the args list
sys.argv.pop(0)
if "-q" in sys.argv:
    verbose = False
    sys.argv.remove("-q")
if "-w" in sys.argv:
    windShow = True
    sys.argv.remove("-w")
if "-f" in sys.argv:
    convertToFahrenheit = True
    sys.argv.remove("-f")


# Characters for formatting output later
chars = "[]'"

# Get API Key
with open("key.txt", "r") as f:
    key = f.read().rstrip("\n")
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
    if verbose:
            print(f"METAR for: {colors.WARNING}{i.upper()}{colors.ENDC}")
            print(f"{colors.OKGREEN} {result} {colors.ENDC}")
            print(f"{colors.WARNING}Airport: {colors.OKBLUE}{result[0:4]}{colors.ENDC}")
            print(f"{colors.WARNING}Posted Time: {colors.OKBLUE}{result[7:11]}z{colors.ENDC}")
            print(f"{colors.WARNING}Wind: {colors.OKBLUE}{result[13:16]}@{result[16:20]}{colors.ENDC}")
            if windShow:
                print(f"{colors.OKCYAN}Wind from: {direction} {colors.ENDC}")
            print(f"{colors.WARNING}Visibility: {colors.OKBLUE}{result[21:25]}{colors.ENDC}")
            if convertToFahrenheit:
                temp = floor((int(result[33:35]) * 9.0/5.0) + 32.0)
                print(f"{colors.WARNING}Temperature: {colors.OKBLUE}{temp}{colors.ENDC}")
            else:
                print(f"{colors.WARNING}Temperature: {colors.OKBLUE}{result[33:35]}{colors.ENDC}")
            print(f"{colors.WARNING}Dewpoint: {colors.OKBLUE}{result[36:40]}{colors.ENDC}")
            print(f"{colors.WARNING}Altimeter: {colors.OKBLUE}{result[41:45]}{colors.ENDC}")
    else:
       print(f"METAR for: {colors.WARNING}{i.upper()}{colors.ENDC}")
       print(f"{colors.OKGREEN} {result} {colors.ENDC}")
       if windShow:
                print(f"{colors.OKCYAN}Wind from: {direction} {colors.ENDC}")
