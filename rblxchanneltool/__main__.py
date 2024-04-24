from .deployHistory import parseLine
from requests import get
import pickle
from .deployHistory import Deployment
from .download import download
import sys
if __name__ == "__main__":
    os = sys.argv[1].lower()
    channel = sys.argv[2].lower()
    if channel != "live":
        if os == "windows":
            r = get(f"https://setup.rbxcdn.com/channel/{channel}/DeployHistory.txt")
        else:
            r = get(f"https://setup.rbxcdn.com/channel/{channel}/mac/DeployHistory.txt")
    else:
        if os == "windows":
            r = get(f"https://setup.rbxcdn.com/DeployHistory.txt")
        else:
            r = get(f"https://setup.rbxcdn.com/mac/DeployHistory.txt")
    lines = r.content.splitlines()
    data = []
    for i in lines:
        data.append(parseLine(i.decode(), os, channel))
    for i in range(1,len(data)):
        d: Deployment = data[::-1][i]
        if d == None:
            pass
        else:
            print(f"{i}: Type: {d.BinaryType}, Version: {d.RobloxVersion}-{d.VersionHash}")
    inp = input("Version>")

    download(data[len(data) - 1 - int(inp)], "rblx")