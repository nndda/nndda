import requests
import os

urlpre = "https://simpleicons.org/icons/"

langs = [
    [
        "python",
        "html5",
        "css3",
        "javascript",
        "sass",
        "csharp",
        "cplusplus"
    ],
    ["#FCE217","#F6C917","#F0B018","#EA9819","#E47F1A","#DE661B","#D94E1C"]
]
tools = [
    [
        "godotengine",
        "medibangpaint",
        "aseprite",
        "sublimetext",
        "visualstudiocode",
        "bootstrap",
        "tailwindcss"
    ],
    ["#3BE6F9","#38CEF5","#35B7F1","#32A0EE","#2F89EA","#2C72E6","#2A5BE3"]
]
socials = [
    [
        "itchdotio",
        "instagram",
        "mastodon",
        "kofi",
        "codepen",
        "artstation",
        "deviantart"
    ],
    ["#FC3A78","#ED3A8D","#DE3BA2","#D03CB7","#C13DCC","#B23EE0","#A43FF5"]
]


for links in [ langs, tools, socials ]:
    for l in range( len( links[0] ) ):
        u = urlpre + links[0][l] + ".svg"
        i = requests.get( u )

        if i.status_code == 200:
            if i.headers["Content-Type"].startswith("image/svg+xml"):
                filename = os.path.basename( u )
                svg = "<svg " + "fill=\"" + links[1][l] + "\" " + i.text.removeprefix("<svg ")
                f = open( filename, "w" )
                f.write( svg )
                f.close()