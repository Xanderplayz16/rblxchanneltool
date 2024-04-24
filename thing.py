from requests import get
from json import load

with open("ChannelsAll.json") as f:
    j = load(f)

for i in j:
    r = get("https://clientsettings.roblox.com/v2/client-version/WindowsPlayer/channel/" + i)
    if r.status_code == 200:
        print(f"{i} sucessful!")
        print(r.json())
    #else:
    #    print(f"{i}: {r.status_code}")