from .deployHistory import Deployment
from requests import get
import zipfile as zf
import os
channelpath = f"https://roblox-setup.cachefly.net/"
player = {
        "RobloxApp.zip": "",
        "shaders.zip": "shaders/",
        "ssl.zip": "ssl/",

        "WebView2.zip": "",
        "WebView2RuntimeInstaller.zip": "WebView2RuntimeInstaller/",

        "content-avatar.zip": "content/avatar/",
        "content-configs.zip": "content/configs/",
        "content-fonts.zip": "content/fonts/",
        "content-sky.zip": "content/sky/",
        "content-sounds.zip": "content/sounds/",
        "content-textures2.zip": "content/textures/",
        "content-models.zip": "content/models/",

        "content-textures3.zip": "PlatformContent/pc/textures/",
        "content-terrain.zip": "PlatformContent/pc/terrain/",
        "content-platform-fonts.zip": "PlatformContent/pc/fonts/",

        "extracontent-luapackages.zip": "ExtraContent/LuaPackages/",
        "extracontent-translations.zip": "ExtraContent/translations/",
        "extracontent-models.zip": "ExtraContent/models/",
        "extracontent-textures.zip": "ExtraContent/textures/",
        "extracontent-places.zip": "ExtraContent/places/"
    }

studio = {
        "RobloxStudio.zip": "",
        "redist.zip": "",
        "Libraries.zip": "",
        "LibrariesQt5.zip": "",

        "WebView2.zip": "",
        "WebView2RuntimeInstaller.zip": "",

        "shaders.zip": "shaders/",
        "ssl.zip": "ssl/",

        "Qml.zip": "Qml/",
        "Plugins.zip": "Plugins/",
        "StudioFonts.zip": "StudioFonts/",
        "BuiltInPlugins.zip": "BuiltInPlugins/",
        "ApplicationConfig.zip": "ApplicationConfig/",
        "BuiltInStandalonePlugins.zip": "BuiltInStandalonePlugins/",

        "content-qt_translations.zip": "content/qt_translations/",
        "content-sky.zip": "content/sky/",
        "content-fonts.zip": "content/fonts/",
        "content-avatar.zip": "content/avatar/",
        "content-models.zip": "content/models/",
        "content-sounds.zip": "content/sounds/",
        "content-configs.zip": "content/configs/",
        "content-api-docs.zip": "content/api_docs/",
        "content-textures2.zip": "content/textures/",
        "content-studio_svg_textures.zip": "content/studio_svg_textures/",

        "content-platform-fonts.zip": "PlatformContent/pc/fonts/",
        "content-terrain.zip": "PlatformContent/pc/terrain/",
        "content-textures3.zip": "PlatformContent/pc/textures/",

        "extracontent-translations.zip": "ExtraContent/translations/",
        "extracontent-luapackages.zip": "ExtraContent/LuaPackages/",
        "extracontent-textures.zip": "ExtraContent/textures/",
        "extracontent-scripts.zip": "ExtraContent/scripts/",
        "extracontent-models.zip": "ExtraContent/models/"
    }
def extract(filename, dir):
    print(f"Extracting {filename} to {dir}...")
    os.makedirs(dir, exist_ok=True)
    with zf.ZipFile(filename) as archive:
        archive.extractall(dir)
    print(f"Extracted {filename} to {dir}!")
def fetch(url):
    print("Downloading " + url + "...")
    f = get(url).content
    print("Downloaded " + url+ "!")
    return f
def writefileb(path, data):
    with open(path, "wb") as f:
        f.write(data)

def download(deployment: Deployment, dir):
    if deployment.Branch != "LIVE":
        channelpath = f"https://roblox-setup.cachefly.net/channel/" + deployment.Branch + "/"
    print(deployment.BinaryType)
    if deployment.OS == "mac":
        versionPath = f"{channelpath}/mac/"
        if deployment.BinaryType == "Client":
            outputFileName = f"{deployment.VersionHash}-RobloxPlayer.zip"
        else:
            outputFileName = f"{deployment.VersionHash}-RobloxStudio.zip"
        print(versionPath + outputFileName)
        with open(outputFileName, "wb") as f:
            f.write(fetch(versionPath + outputFileName))
        extract(outputFileName, "rblx")
    else:
        versionPath = f"{channelpath}/{deployment.VersionHash}-"
        lines = fetch(versionPath + "rbxPkgManifest.txt").decode().splitlines()
        writefileb("rbxPkgManifest.txt", "\n".join(lines).encode())
        os.makedirs(dir, exist_ok=True)
        writefileb(dir + "/AppSettings.xml", b"""<?xml version="1.0" encoding="UTF-8"?>
<Settings>
	<ContentFolder>content</ContentFolder>
	<BaseUrl>http://www.roblox.com</BaseUrl>
</Settings>""")
        for i in lines:
            if not "." in i: 
                continue
            elif not ".zip" in i:
                continue
            blobUrl = versionPath + i
            writefileb(i, fetch(blobUrl))
            if deployment.BinaryType == "Studio64":
                extract(i, f"{dir}/{studio[i]}")
            else:
                extract(i, f"{dir}/{player[i]}")