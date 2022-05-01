import requests
import json
import sys

class colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def main():
    #Check for no args
    if len(sys.argv) < 2:
        print("Not enough arguments, see --help")
        return 0
    if sys.argv[1] == "--help":
        print("USAGE: python py-metar.py <airport icao code 1> <2> <3> etc...")
        return 0
    # remove the "python py-metar.py" from the args list
    sys.argv.pop(0)

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

        # Print final result
        print(f"METAR for: {colors.WARNING}{i.upper()}{colors.ENDC}")
        print(f"{colors.OKGREEN} {result} \n {colors.ENDC}")
main()
