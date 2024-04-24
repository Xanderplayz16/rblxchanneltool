from dataclasses import dataclass
import datetime as dt
from requests import get
from time import sleep
@dataclass
class Timestamp:
    Timestamp: int
    Formatted: str

@dataclass
class Deployment:
    DeployType: str
    BinaryType: str
    VersionHash: str
    Time: Timestamp
    RobloxVersion: str
    GitHash: str
    OS: str
    Branch: str
    
def legacyParseLine(line:str, os:str, channel):
    if line == "":
        return None
    if not "file" in line:
        return None
    print(line)
    half = line.split("at")
    hashstring = half[0].split()
    if "file version" in line:
        timeverstring = half[1].split("file version:")
    else:
        timeverstring = half[1].split("file verion:")
    timestring = timeverstring[0]
    
    verstring = timeverstring[1][1:][:-7].replace(" ", "").split(",")


    DeployType = hashstring[0]
    BinaryType = hashstring[1]
    VersionHash = hashstring[2]
    Time = Timestamp(dt.datetime.strptime(timestring[1:][:-2], "%m/%d/%Y %I:%M:%S %p"), timestring[1:][:-2])
    RobloxVersion = f"{verstring[0]}.{verstring[1]}.{verstring[2]}.{verstring[3]}"
    return Deployment(DeployType, BinaryType, VersionHash, Time, RobloxVersion, "", os, channel)

def parseLine(line:str, os:str, channel:str):
    
    if ("git hash:" in line) == False:
        return legacyParseLine(line, os, channel)
    half = line.split("at")
    hashstring = half[0].split()
    timeverstring = half[1].split("file version:")
    timestring = timeverstring[0]
    verstring = timeverstring[1][1:][:-4].replace("git hash: ", "").replace(" ", "").split(",")


    DeployType = hashstring[0]
    BinaryType = hashstring[1]
    VersionHash = hashstring[2]
    Time = Timestamp(dt.datetime.strptime(timestring[1:][:-2], "%m/%d/%Y %I:%M:%S %p"), timestring[1:][:-2])
    RobloxVersion = f"{verstring[0]}.{verstring[1]}.{verstring[2]}.{verstring[3]}"
    GitHash = verstring[4]
    return Deployment(DeployType, BinaryType, VersionHash, Time, RobloxVersion, GitHash, os, channel)


    
if __name__ == "__main__":
    dep = parseLine("New Studio64 version-75a2aa06d5d443ef at 5/18/2022 12:25:38 PM, file version: 0, 527, 0, 5270372, git hash: b4b89e03c6608892edab51b1ca5c919a78008dad ...")
    print(dep)