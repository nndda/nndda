import requests, os
from bs4 import BeautifulSoup

urlpre = "https://simpleicons.org/icons/"
output_dir = "./icons/"
force_update = True # redownload every icons, regardless if the files already exist or not
icon_size = 28 #px

langs = {
    "heading" : "Languages",
    "col_1" : "#FCE217FF",
    "col_2" : "#E87415FF",
    "icons" : [
        # SimpleIcon slug, alt, url
        ["python",          "Python",],
        ["html5",           "HTML 5",],
        ["css3",            "CSS 3",],
        ["javascript",      "JavaScript",],
        ["sass",            "SASS",],
        ["csharp",          "C#",],
        ["cplusplus",       "C++",],
        ["wolframlanguage", "Wolfram Language",],
    ],
}
tools = {
    "heading" : "Tools & Frameworks",
    "col_1" : "#3BE6F9FF",
    "col_2" : "#287BEBFF",
    "icons" : [
        ["godotengine",         "Godot Engine",],
        ["medibangpaint",       "MediBang Paint",],
        ["aseprite",            "Aseprite",],
        ["inkscape",            "Inkscape",],
        ["sublimetext",         "Sublime Text",],
        ["visualstudiocode",    "Visual Studio Code",],
    ],
}
socials = {
    "heading" : "Links & Socials",
    "col_1" : "#FC3A78FF",
    "col_2" : "#A43FF5FF",
    "icons" : [
        ["itchdotio",   "itch.io",      "nnda.itch.io",],
        ["mastodon",    "Mastodon",     "mastodon.art/@nnda",],
        ["kofi",        "Ko-fi",        "ko-fi.com/nnda_",],
        ["instagram",   "Instagram",    "www.instagram.com/nnda.afrd",],
        ["artstation",  "ArtStation",   "www.artstation.com/nnda",],
        ["codepen",     "CodePen",      "codepen.io/nnda",],
    ],
}


def hex2rgba(hex):
    hex_f = hex.lstrip("#")
    if len(hex_f) <= 6:
        hex_f = hex_f.ljust(8, "f")

    output = [0, 0, 0, 0]
    for n in range(4):
        output[n] = int(hex_f[n*2:(n+1)*2], 16) / 255

    return output


def rgba2hex(rgb):
    output = "#"
    for n in rgb:
        output += hex(int(n * 255)).lstrip("0x").rjust(2, "0")

    return output


def gradient(length, col_1, col_2):
    output = []
    col_start = hex2rgba(col_1)
    col_end = hex2rgba(col_2)

    a = 0.0
    for n in range(length ):
        a += 1.0 / length
        if a > 1.0: a = 1.0

        c = [0, 0, 0, 0]
        for m in range(4):
            c[m] = col_start[m] * a + (1.0 - a) * col_end[m]

        output.append(rgba2hex(c))

    output.reverse()
    output[0] = output[0][0:-2] + "ff"
    return output


def icon_color(filepath, color):
    data = ""
    filename = output_dir + filepath + ".svg"

    if (not os.path.isfile(filename)) or force_update:
        i = requests.get(urlpre + filepath + ".svg")
        if i.status_code == 200:
            if i.headers["Content-Type"].startswith("image/svg+xml"):
                data = i.text
        else:
            print(i.status_code)
    else:
        file = open(filename, "r")
        data = file.read()
        file.close()

    soup = BeautifulSoup(data, "xml")
    soup.svg["fill"] = color

    file_write = open(filename, "w")
    file_write.write(soup.prettify())
    file_write.close()

markdown_output = ""

for n in [langs, tools, socials]:
    g = gradient(len(n["icons"]), n["col_1"], n["col_2"])

    markdown_output += "\n## %s\n\n&nbsp;\n" % n["heading"]

    for m in range(len(g)):
        icon = n["icons"][m][0]
        alt = n["icons"][m][1]
        url = ""

        if len(n["icons"][m]) >= 3:
            url = n["icons"][m][2]

        icon_color( icon, g[m] )

        if url != "":
            markdown_output += "<a href=\"https://%s\">" % url

        markdown_output += "<img height=\"%i\" width=\"%i\" src=\"icons/%s.svg\" alt=\"%s\"/>" % (icon_size, icon_size, icon, alt)

        if url != "":
            markdown_output += "</a>"

        markdown_output += " &nbsp;\n"

    markdown_output += "<br>\n"

print(markdown_output)
