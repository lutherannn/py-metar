import requests
import json

#Characters for formatting output later
chars = "[]'"

#Get API Key
with open("key.txt", "r") as f:
    key = f.read()
f.close()

#Get airport and uppercase input
station = input("Enter ICAO Code: ").upper()

#Set url
url = f"https://api.checkwx.com/metar/{station}?x-api-key={key}"
req = requests.get(url)

#Get metar data
try:
    req.raise_for_status()
    resp = json.loads(req.text)
    #print(json.dumps(resp, indent=1))
except requests.exceptions.HTTPError as e:
    print(e)
#Get the metar from the JSON
result = str(resp["data"])

#Format the metar to get rid of non-needed characters
for x in chars:
    result = result.replace(x, "")

#Print final result
print(result)