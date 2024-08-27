import requests, os
import urllib.parse
from bs4 import BeautifulSoup

# CONFIGURATIONS ==============================================================
# redownload icons and badges, regardless if the files already exist or not
force_update = True

# BADGES ----------------------------------------------------------------------
# use Shield.IO CDN instead of downloading the icons
badge_cdn = not force_update
# directory for the downloaded badges
badges_output_dir = "./badges/"
badge_template = "https://img.shields.io/badge/{text}-{textColor}"

badge_default = {
  "url"       : "",
  "style"     : "flat-square",
  "height"    : "",
  "width"    : "",
}

badge_stack = {
  "ko-fi" : {
    "url"         : "https://ko-fi.com/L3L536B9Z",
    "text"        : "Buy Me a Coffee",
    "textColor"   : "FF5E5B",
    "logo"        : "kofi",
    "logoColor"   : "FFFFFF",
  },
  "itchio" : {
    "url"         : "https://nnda.itch.io",
    "text"        : "Games I made",
    "textColor"   : "F82A2A",
    "logo"        : "itchdotio",
    "logoColor"   : "FFFFFF",
  },
  "discord" : {
    "text"        : "nnda.dev",
    "textColor"   : "FFFFFF",
    "logo"        : "discord",
    "logoColor"   : "FFFFFF",
    "label"       : "Discord",
    "labelColor"  : "101217",
    "height"      : 28,
  },
}

for n in badge_stack:
    badge_stack[n] = badge_default | badge_stack[n]

# ICONS -----------------------------------------------------------------------
# use SimpleIcons CDN instead of downloading the icons
icon_cdn = True
# icon size in pixels to be applied in "width" and "height" attributes
icon_size = 28
# directory for the downloaded icons
icons_output_dir = "./icons/"

icon_stack = [
{
    "heading" : "Languages",  # Heading text
    "col_1" : "#3BE6F9FF",  # Gradient start color
    "col_2" : "#287BEBFF",  # Gradient end color
    "icons" : [
        # SimpleIcons slug, alt, url
        ["python",          "Python",],
        ["html5",           "HTML 5",],
        ["css3",            "CSS 3",],
        ["javascript",      "JavaScript",],
        ["typescript",      "TypeScript",],
        ["sass",            "SASS",],
        # ["csharp",          "C#",], removed from simple-icons. microsoft is stinky poopy
        # ["cplusplus",       "C++",],
        # ["wolframlanguage", "Wolfram Language",],
    ],
},
{
    "heading" : "Tools & Frameworks",
    "col_1" : "#FC3A78FF",
    "col_2" : "#A43FF5FF",
    "icons" : [
        ["godotengine",         "Godot Engine",],
        ["medibangpaint",       "MediBang Paint",],
        ["aseprite",            "Aseprite",],
        ["inkscape",            "Inkscape",],
        # ["sublimetext",         "Sublime Text",],
        ["linux",               "Linux",],
        ["git",                 "Git",],
        ["nodedotjs",           "Node.js",],
        ["webpack",             "webpack",],
        # ["jekyll",              "Jekyll",],
    ],
},
]

for d in [icons_output_dir, badges_output_dir]:
    os.makedirs(d, exist_ok=True)

def fetch_data(url, filepath, output_dir, extension = "svg", content_type = "image/svg+xml"):
    data = ""
    filename = f"{output_dir}{filepath}.{extension}"

    if (not os.path.isfile(filename)) or force_update:
        i = requests.get(f"{url}")
        if i.status_code == 200:
            if i.headers["Content-Type"].startswith(content_type):
                data = i.text
        else:
            print(i.status_code)
    else:
        file = open(filename, "r")
        data = file.read()
        file.close()

    return data

def build_img_tag(src, width="", height="", alt="", url=""):
    output = ""

    if url != "":
        output += f"<a href=\"{url}\">"

    if width != "":
        width = f"width=\"{width}\""

    if height != "":
        height = f"height=\"{height}\""

    output += f"<img {height} {width} src=\"{src}\" alt=\"{alt}\"/>"

    if url != "":
        output += "</a>"

    return output

for n in badge_stack:
    badge = badge_stack[n]
    url = badge["url"]
    text = badge["text"]
    textColor = badge["textColor"]
    height = badge["height"]
    width = badge["width"]

    badge_url = badge_template.format(**{
        "text" : urllib.parse.quote(text,safe=""),
        "textColor" : urllib.parse.quote(textColor,safe=""),
    }) + "?"

    del badge["url"], badge["text"], badge["textColor"], badge["height"], badge["width"]

    badge_url = badge_url + urllib.parse.urlencode(badge)

    data = fetch_data(badge_url, n, badges_output_dir)

    soup = BeautifulSoup(data, "xml")

    filename = f"{badges_output_dir}{n}.svg"
    file_write = open(filename, "w")
    file_write.write(soup.prettify())
    file_write.close()

    src = badge_url if badge_cdn else filename

    alt = "" if not "label" in badge else (badge["label"] + " - ")
    alt += f"{text}"

    badge_stack[n]["compiled"] = build_img_tag(src, f"{width}", f"{height}", alt, url)

# Color utilities
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


# Generate gradient color in an array
def gradient(length, col_1, col_2):
    output = []
    col_start = hex2rgba(col_1)
    col_end = hex2rgba(col_2)

    a = 0.0
    for n in range(length):
        a += 1.0 / length
        if a > 1.0: a = 1.0

        c = [0, 0, 0, 0]
        for m in range(4):
            c[m] = col_start[m] * a + (1.0 - a) * col_end[m]

        output.append(rgba2hex(c))

    output.reverse()
    output[0] = output[0][0:-2] + "ff"
    return output

url_si = "https://cdn.simpleicons.org/"

# Generate icons
def icon_color(filepath, color):
    data = fetch_data(f"{url_si}{filepath}", filepath, icons_output_dir)

    if data != "":
        soup = BeautifulSoup(data, "xml")
        soup.svg["fill"] = color

        filename = f"{icons_output_dir}{filepath}.svg"
        file_write = open(filename, "w")
        file_write.write(soup.prettify())
        file_write.close()

md_icons = ""

for n in icon_stack:
    g = gradient(len(n["icons"]), n["col_1"], n["col_2"])

    md_icons += f"\n## {n['heading']}\n&nbsp;\n"

    for m in range(len(g)):
        icon = n["icons"][m][0]
        alt = n["icons"][m][1]
        url = ""

        if len(n["icons"][m]) >= 3:
            url = n["icons"][m][2]

        if icon_cdn:
            icon = f"https://cdn.simpleicons.org/{icon}/{g[m].removeprefix('#')}"
        else:
            icon_color(icon, g[m])
            icon = f"icons/{icon}.svg"

        md_icons += build_img_tag(icon, f"{icon_size}", f"{icon_size}", alt, url)

        md_icons += " &nbsp;\n"

    md_icons += "<br>"


# Apply to markdown
md_str = ""

with open("README.template.md", "r") as md_r:
    md_str = md_r.read()
    md_str = md_str.replace("<!-- <ICONS> -->", md_icons)
    for badge in badge_stack:
        md_str = md_str.replace(f"<!-- <{badge}> -->", badge_stack[badge]["compiled"])

with open("README.md", "w") as md_w:
    md_w.write(md_str)
    md_w.close()
