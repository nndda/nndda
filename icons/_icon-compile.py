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
        "cplusplus",
        "wolframlanguage",
    ],
    ["#FCE217","#F8D217","#F4C217","#F0B218","#ECA218","#E89219","#E48219","#E17319"]
]
tools = [
    [
        "godotengine",
        "medibangpaint",
        "aseprite",
        "inkscape",
        "sublimetext",
        "visualstudiocode",
    ],
    ["#3BE6F9","#38D1F5","#35BCF2","#33A7EE","#3092EB","#2E7DE8"]
]
socials = [
    [
        "itchdotio",
        "mastodon",
        "kofi",
        "instagram",
        "artstation",
        "codepen",
    ],
    ["#FC3A78","#EA3B91","#D83CAA","#C73DC3","#B53EDC","#A43FF5"]
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