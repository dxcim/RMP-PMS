import requests

res = requests.get("https://api.thingspeak.com/channels/1426475/feeds.json?api_key=9FPG13PUBB18V8UU&results=2")
print(res.json())






