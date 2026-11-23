"""Draw the front page for Sunday 22 November 2026.

One self-contained renderer: a newspaper front page at 1024x1024 that sums
up 48 verified stories from a single day. No network, no clock, no random
input, so two runs write byte-identical output.
"""

import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024

PAPER = (246, 239, 220)
INK = (26, 26, 26)
SOFT_INK = (74, 68, 58)
RULE = (26, 26, 26)
RED = (179, 38, 30)
TEAL = (20, 82, 74)
NAVY = (38, 58, 92)
GOLD = (198, 152, 40)
FIELD = (46, 110, 62)
PANEL = (232, 224, 200)
MAPDOT = (120, 110, 88)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        try:
            return ImageFont.truetype(SANS, size)
        except Exception:
            return ImageFont.load_default()


# ---------------------------------------------------------------- data ---

MASTHEAD_TITLE = "THE WORLD IN ONE DAY"
MASTHEAD_LEFT = "SUNDAY 22 NOVEMBER 2026"
MASTHEAD_RIGHT = "48 STORIES \u00b7 ONE DAY"
MASTHEAD_SUB = "The world's news, verified against the day's reporting"

NUMBERS = [
    ("35\u201310", "49ERS OVER VIKINGS"),
    ("\u22128.6%", "S&P 500'S WEEK"),
    ("258", "DEMOCRATS' HOUSE SEATS"),
    ("98.79%", "HONG KONG TURNOUT"),
    ("$120m", "HUNGER GAMES OPENING"),
    ("32h 03m", "SPACEX PAD RECORD"),
]

HEROES = [
    {
        "kicker": "CLIMATE \u00b7 ANTALYA",
        "title": "COP31 COLLAPSES \u2014 NO DEAL ON FOSSIL FUELS",
        "deck": "After two weeks, the longest climate summit ever ends in failure \u2014 the first COP with no deal since Copenhagen in 2009.",
        "art": "cop",
    },
    {
        "kicker": "NFL \u00b7 MEXICO CITY",
        "title": "49ERS CRUSH VIKINGS 35\u201310 IN MEXICO RETURN",
        "deck": "Brock Purdy throws for 255 yards and three touchdowns as San Francisco win the NFL's first international Sunday night game.",
        "art": "nfl",
    },
    {
        "kicker": "MARKETS \u00b7 NEW YORK",
        "title": "WALL STREET'S WORST WEEK SINCE COVID",
        "deck": "The S&P 500 falls 8.6% in a week and enters correction territory; the Nasdaq wipes out its 2026 gains.",
        "art": "market",
    },
]

MEDIUMS = [
    ("WORLD", "Trump warns Iran: new strikes after New Year",
     "Strikes after the New Year if no deal, he tells Fox News."),
    ("LIBYA", "Russian warship hit in Benghazi port",
     "A suspected drone strike leaves the corvette Merkury mostly sunk, bow showing."),
    ("UKRAINE", "Russian strikes kill 15; Zelenskyy pleads for Patriots",
     "Ten die in Dymer as a strike collapses a block; Kyiv urges the US to release Patriots."),
    ("GULF", "Iran: two tankers hit mines in Hormuz",
     "IRGC: the tankers hit naval mines; a fourth US drone downed in 24 hours."),
    ("USA", "Democrats win 258 House seats \u2014 most since 1992",
     "Chuck Hubbard beats Rep. Virginia Foxx by 330 votes after a recount; Foxx concedes."),
    ("TENNIS", "Alcaraz wins first ATP Finals crown",
     "He beats world No. 1 Zverev 6\u20132, 7\u20136 in Turin and completes a perfect 5\u20130 week."),
    ("CRYPTO", "Bitcoin bounces back above $60,000",
     "After a two-year low near $55,130 on Saturday, it recovers $5,000 in hours."),
    ("ASIA", "Hong Kong vote hits record 98.79% turnout",
     "5,640 of 5,709 electors vote; 856 candidates chase 723 seats."),
    ("EUROPE", "NATO emergency talks after missiles hit Poland",
     "Warsaw: all three objects that crashed on Friday were Russian Kh-101 missiles."),
    ("FILM", "Hunger Games roars back with $120m opening",
     "It tops the box office in 81 countries; $225m worldwide in its first weekend."),
    ("AFRICA", "Nigeria boat disaster \u2014 at least 24 dead",
     "A boat of mourners capsizes in Bayelsa State; 24 rescued, hundreds feared aboard."),
]

BRIEFS = [
    "Bessent warns Fed: don't overtighten ahead of December meeting",
    "Trump: \u2018very hard\u2019 to work with Schumer as majority leader",
    "Poilievre moves to reject Canada's immigration plan",
    "Spy chief confirms Nvidia chip-smuggling probe",
    "Storm threatens Thanksgiving travel for 81m Americans",
    "Mexico: 11 dead in raid that caught \u2018El Chapo Isidro\u2019",
    "Santos: Colombia force-only plan is doomed to fail",
    "Cowboys score 51 in rout of Titans; Prescott 4 TDs",
    "Liverpool hammer Man Utd 4\u20130 at Anfield",
    "Barcelona rally from 2\u20130 to beat Villarreal 3\u20132",
    "Murray's 45, Jokic triple-double lift Nuggets in OT",
    "Pakistan A beat India A by 48 runs in Doha",
    "IDF: Gaza aid-truck dead were Islamic Jihad militants",
    "Gaza families protest as homes are destroyed",
    "West Bank arson branded \u2018Jewish terrorism\u2019",
    "Lebanon at 83: families return to ruined homes",
    "Khartoum drones kill four, damage UN building",
    "Mashaba set for Joburg mayor in ANC pact",
    "Zimbabwe preacher Uebert Angel arrested in church",
    "EU budget deal rejected by France and Germany",
    "Czech PM: no \u20ac100bn for Ukraine from EU budget",
    "India third in Asia power index; Modi ranked second",
    "China slams US ban on telecom firms' phone access",
    "Nepal PM begins first India visit, seeks $2bn aid",
    "Korean minister quits over AI exam-cheating chaos",
    "China, Vietnam complete 41st joint sea patrol",
    "China's second home-built cruise ship sets sail",
    "China cuts stock margin rule to 80% from 30 Nov",
    "Australia business slump worst in five years",
    "SpaceX sets 32-hour pad turnaround record",
    "China targets Moon water and oxygen by 2030",
    "Google unveils secure microVMs for AI agents",
    "Claude AI solves two black-hole puzzles",
    "Five-year lecanemab data brings Alzheimer's hope",
]

TIMELINE = [
    ("00:00", "Drones strike Khartoum"),
    ("12:23", "SpaceX launches NROL-136"),
    ("~17:00", "COP31 talks collapse"),
    ("~19:30", "Alcaraz lifts the trophy"),
]

# Dotted-map landmass: (row, first column, last column) on a 72 x 28 grid.
# Columns are 5 degrees of longitude from -180; rows are ~3.93 degrees of
# latitude from 65N down to 45S. Hand-drawn, deliberately simplified.
LAND = [
    (0, 2, 7), (0, 8, 22), (0, 24, 28), (0, 35, 38), (0, 39, 70),
    (1, 3, 6), (1, 7, 22), (1, 25, 28), (1, 33, 34), (1, 36, 38), (1, 39, 71),
    (2, 8, 21), (2, 26, 27), (2, 33, 33), (2, 35, 40), (2, 41, 71),
    (3, 9, 20), (3, 34, 41), (3, 42, 70),
    (4, 9, 19), (4, 34, 42), (4, 43, 66),
    (5, 8, 19), (5, 34, 40), (5, 44, 64),
    (6, 8, 18), (6, 34, 39), (6, 44, 62), (6, 66, 68),
    (7, 9, 17), (7, 35, 40), (7, 41, 48), (7, 52, 62), (7, 67, 67),
    (8, 10, 16), (8, 32, 38), (8, 41, 47), (8, 50, 61),
    (9, 9, 12), (9, 15, 16), (9, 31, 40), (9, 43, 47), (9, 50, 53), (9, 56, 60),
    (10, 10, 12), (10, 31, 41), (10, 44, 47), (10, 51, 53), (10, 57, 60),
    (11, 11, 13), (11, 31, 42), (11, 52, 52), (11, 57, 59),
    (12, 12, 13), (12, 32, 43), (12, 52, 52), (12, 58, 59),
    (13, 20, 24), (13, 33, 44), (13, 58, 60),
    (14, 20, 25), (14, 34, 44), (14, 56, 61),
    (15, 20, 26), (15, 35, 43), (15, 57, 62),
    (16, 21, 26), (16, 36, 42), (16, 58, 62),
    (17, 21, 25), (17, 36, 41), (17, 59, 62),
    (18, 22, 25), (18, 36, 40), (18, 60, 62),
    (19, 22, 24), (19, 36, 40), (19, 59, 65),
    (20, 22, 24), (20, 36, 39), (20, 42, 43), (20, 59, 65),
    (21, 23, 24), (21, 36, 39), (21, 42, 42), (21, 60, 64),
    (22, 23, 24), (22, 36, 38), (22, 60, 64),
    (23, 23, 24), (23, 36, 38), (23, 60, 63),
    (24, 23, 24), (24, 36, 38), (24, 61, 63), (24, 68, 69),
    (25, 23, 24), (25, 37, 37), (25, 61, 62), (25, 68, 68),
    (26, 23, 23), (26, 68, 68),
    (27, 23, 23),
]

PINS = [
    (36.9, 30.7), (50.45, 30.52), (32.1, 20.07), (26.5, 56.3),
    (19.43, -99.13), (38.9, -77.04), (45.07, 7.69), (22.32, 114.17),
    (28.61, 77.21), (37.57, 126.98), (15.6, 32.53), (4.77, 6.1),
    (-26.2, 28.05), (31.5, 34.47),
]

PIN_KEY = ("1 Antalya (COP31) \u00b7 2 Kyiv \u00b7 3 Benghazi \u00b7 4 Strait of Hormuz \u00b7 "
           "5 Mexico City \u00b7 6 Washington \u00b7 7 Turin \u00b7 8 Hong Kong \u00b7 9 New Delhi \u00b7 "
           "10 Seoul \u00b7 11 Khartoum \u00b7 12 Bayelsa \u00b7 13 Johannesburg \u00b7 14 Gaza City")


# ------------------------------------------------------------ helpers ---

def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_h(draw, lines, fnt):
    return sum(draw.textbbox((0, 0), line, font=fnt)[3] for line in lines)


def draw_lines(draw, x, y, lines, fnt, fill, leading=None):
    if leading is None:
        leading = int(fnt.size * 1.22)
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def centre(draw, cx, y, text, fnt, fill):
    w = draw.textlength(text, font=fnt)
    draw.text((cx - w / 2, y), text, font=fnt, fill=fill)


def hrule(draw, x0, x1, y, fill=RULE, width=1):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def section_head(draw, x, y, w, label):
    fnt = font(SANS_B, 13)
    draw.text((x, y), label, font=fnt, fill=RED)
    hrule(draw, x, x + w, y + 19, fill=RULE, width=2)
    return y + 26


# ------------------------------------------------------------ heroes ----

def art_cop(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=TEAL)
    cx, cy, r = x + w // 2, y + h // 2 - 4, 34
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(233, 224, 196))
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(120, 140, 120), width=2)
    draw.arc([cx - r + 6, cy - r + 4, cx + 2, cy + 6], 200, 330, fill=(120, 140, 120), width=3)
    draw.arc([cx - 4, cy + 2, cx + r - 4, cy + r - 6], 20, 150, fill=(120, 140, 120), width=3)
    draw.line([(cx - 8, cy - r + 2), (cx + 2, cy - 12), (cx - 6, cy + 2),
               (cx + 8, cy + 14), (cx - 2, cy + r - 2)], fill=RED, width=4)
    bx0, bx1 = x + 14, x + w - 14
    by = y + h - 26
    draw.polygon([(bx0, by), (bx1, by), (bx1 - 12, by + 16), (bx0 + 12, by + 16)],
                 fill=RED)
    fnt = font(SANS_B, 13)
    centre(draw, x + w // 2, by + 1, "NO DEAL", fnt, (255, 255, 255))


def art_nfl(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=FIELD)
    for i in range(1, 6):
        lx = x + i * w // 6
        draw.line([(lx, y), (lx, y + h)], fill=(255, 255, 255), width=1)
    draw.line([(x, y + h - 14), (x + w, y + h - 14)], fill=(255, 255, 255), width=2)
    px = x + w - 46
    draw.line([(px, y + 8), (px, y + h - 30)], fill=(240, 200, 60), width=4)
    draw.line([(px - 14, y + 8), (px, y + 8)], fill=(240, 200, 60), width=4)
    draw.line([(px, y + 8), (px + 14, y + 8)], fill=(240, 200, 60), width=4)
    draw.line([(px - 14, y + 8), (px - 14, y + 20)], fill=(240, 200, 60), width=3)
    draw.line([(px + 14, y + 8), (px + 14, y + 20)], fill=(240, 200, 60), width=3)
    bx, by = x + 52, y + h // 2 - 6
    draw.ellipse([bx - 34, by - 15, bx + 34, by + 15], fill=(122, 72, 32))
    draw.line([(bx - 22, by), (bx + 22, by)], fill=(255, 255, 255), width=2)
    for dx in (-14, -7, 0, 7, 14):
        draw.line([(bx + dx, by - 4), (bx + dx, by + 4)], fill=(255, 255, 255), width=2)
    fnt = font(SANS_B, 15)
    draw.text((x + 12, y + 8), "35\u201310", font=fnt, fill=(255, 255, 255))


def art_market(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=NAVY)
    bars = [48, 40, 44, 34, 38, 26, 28, 16]
    bw = (w - 40) // len(bars)
    for i, bh in enumerate(bars):
        bx0 = x + 20 + i * bw
        draw.rectangle([bx0, y + h - 12 - bh, bx0 + bw - 6, y + h - 12],
                       fill=(150, 165, 190))
    draw.line([(x + 16, y + 22), (x + w - 60, y + 40), (x + w - 34, y + h - 34)],
              fill=RED, width=6)
    draw.polygon([(x + w - 52, y + h - 52), (x + w - 18, y + h - 52),
                  (x + w - 30, y + h - 22)], fill=RED)
    fnt = font(SANS_B, 15)
    draw.text((x + 12, y + 8), "\u22128.6%", font=fnt, fill=(255, 255, 255))


ARTS = {"cop": art_cop, "nfl": art_nfl, "market": art_market}


def draw_masthead(draw):
    f_title = font(SERIF_B, 50)
    f_side = font(SANS_B, 11)
    f_sub = font(SERIF, 13)
    draw.text((20, 8), MASTHEAD_LEFT, font=f_side, fill=SOFT_INK)
    right_w = draw.textlength(MASTHEAD_RIGHT, font=f_side)
    draw.text((W - 20 - right_w, 8), MASTHEAD_RIGHT, font=f_side, fill=SOFT_INK)
    centre(draw, W // 2, 26, MASTHEAD_TITLE, f_title, INK)
    centre(draw, W // 2, 82, MASTHEAD_SUB, f_sub, SOFT_INK)
    hrule(draw, 20, W - 20, 102, width=3)
    hrule(draw, 20, W - 20, 106, width=1)


def draw_numbers(draw, y):
    cell_w = (W - 40) // 6
    f_num = font(SERIF_B, 26)
    f_lab = font(SANS_B, 9)
    for i, (num, lab) in enumerate(NUMBERS):
        x0 = 20 + i * cell_w
        if i:
            draw.line([(x0, y + 2), (x0, y + 34)], fill=(200, 190, 165), width=1)
        centre(draw, x0 + cell_w // 2, y, num, f_num, RED)
        centre(draw, x0 + cell_w // 2, y + 30, lab, f_lab, SOFT_INK)
    hrule(draw, 20, W - 20, y + 44, width=1)
    return y + 50


def draw_heroes(draw, y):
    gap, cw = 8, (W - 40 - 16) // 3
    f_kick = font(SANS_B, 10)
    f_head = font(SERIF_B, 19)
    f_deck = font(SANS, 12)
    art_h = 76
    for i, hero in enumerate(HEROES):
        x = 20 + i * (cw + gap)
        draw.rectangle([x, y, x + cw, y + 198], outline=(200, 190, 165), width=1)
        ARTS[hero["art"]](draw, x + 1, y + 1, cw - 2, art_h)
        ty = y + art_h + 8
        draw.text((x + 10, ty), hero["kicker"], font=f_kick, fill=RED)
        ty += 16
        lines = wrap(draw, hero["title"], f_head, cw - 20)
        ty = draw_lines(draw, x + 10, ty, lines[:3], f_head, INK, leading=22)
        deck = wrap(draw, hero["deck"], f_deck, cw - 20)
        draw_lines(draw, x + 10, ty + 2, deck[:3], f_deck, SOFT_INK, leading=15)
    return y + 206


def draw_mediums(draw, y):
    y = section_head(draw, 20, y, W - 40, "THE DAY'S TOP STORIES")
    col_w = (W - 40 - 16) // 2
    left, right = MEDIUMS[:6], MEDIUMS[6:]
    f_tag = font(SANS_B, 10)
    f_head = font(SANS_B, 13)
    f_deck = font(SANS, 10)
    max_y = y
    for ci, items in enumerate((left, right)):
        x = 20 + ci * (col_w + 16)
        cy = y
        for tag, head, deck in items:
            draw.text((x, cy), tag, font=f_tag, fill=RED)
            tag_w = draw.textlength(tag, font=f_tag)
            head_lines = wrap(draw, head, f_head, col_w - tag_w - 8)
            draw_lines(draw, x + tag_w + 8, cy - 1, head_lines[:1], f_head, INK, leading=15)
            cy += 15
            deck_lines = wrap(draw, deck, f_deck, col_w)
            cy = draw_lines(draw, x, cy, deck_lines[:1], f_deck, SOFT_INK, leading=12)
            cy += 3
        max_y = max(max_y, cy)
    return max_y + 2


def draw_briefs(draw, y):
    y = section_head(draw, 20, y, W - 40, "MORE OF THE DAY \u2014 IN BRIEF")
    col_w = (W - 40 - 16) // 3
    cols = [BRIEFS[i::3] for i in range(3)]
    size = 10
    while size >= 8:
        fnt = font(SANS, size)
        lead = size + 2
        heights = []
        for items in cols:
            total = 0
            for item in items:
                lines = wrap(draw, "\u2022  " + item, fnt, col_w)
                total += len(lines[:2]) * lead + 2
            heights.append(total)
        if max(heights) <= 156:
            break
        size -= 1
    fnt = font(SANS, size)
    lead = size + 2
    for ci, items in enumerate(cols):
        x = 20 + ci * (col_w + 8)
        cy = y
        for item in items:
            lines = wrap(draw, "\u2022  " + item, fnt, col_w)
            cy = draw_lines(draw, x, cy, lines[:2], fnt, INK, leading=lead)
            cy += 2
    return y + 172


def draw_timeline(draw, y):
    f_lab = font(SANS_B, 11)
    f_txt = font(SANS, 11)
    draw.text((20, y), "THROUGH THE DAY \u00b7 UTC", font=f_lab, fill=RED)
    line_y = y + 32
    x0, x1 = 110, W - 110
    hrule(draw, x0, x1, line_y, fill=(180, 168, 140), width=2)
    n = len(TIMELINE)
    for i, (t, label) in enumerate(TIMELINE):
        cx = x0 + (x1 - x0) * i / (n - 1)
        draw.ellipse([cx - 5, line_y - 5, cx + 5, line_y + 5], fill=RED)
        centre(draw, cx, line_y - 19, t, f_lab, INK)
        centre(draw, cx, line_y + 9, label, f_txt, SOFT_INK)
    return y + 48


def draw_map(draw, x, y, w, h):
    cell_w, cell_h = w / 72.0, h / 28.0
    for r, c0, c1 in LAND:
        for c in range(c0, c1 + 1):
            px = x + (c + 0.5) * cell_w
            py = y + (r + 0.5) * cell_h
            draw.ellipse([px - 1.6, py - 1.6, px + 1.6, py + 1.6], fill=MAPDOT)
    f_pin = font(SANS_B, 9)
    for i, (lat, lon) in enumerate(PINS, start=1):
        col = (lon + 180) / 5.0
        row = (65 - lat) / (110.0 / 28.0)
        px = x + col / 72.0 * w
        py = y + row / 28.0 * h
        draw.ellipse([px - 8, py - 8, px + 8, py + 8], fill=RED, outline=(255, 255, 255), width=1)
        label = str(i)
        lw = draw.textlength(label, font=f_pin)
        draw.text((px - lw / 2, py - 6), label, font=f_pin, fill=(255, 255, 255))
    f_cap = font(SANS, 9)
    key_lines = wrap(draw, PIN_KEY, f_cap, w)
    return draw_lines(draw, x, y + h + 4, key_lines[:3], f_cap, SOFT_INK, leading=11)


def draw_datecheck(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], outline=RULE, width=2)
    f_head = font(SANS_B, 12)
    f_body = font(SANS, 11)
    f_leg = font(SANS, 10)
    draw.text((x + 10, y + 8), "DATE CHECK", font=f_head, fill=RED)
    body = ("Every story on this page happened or was first reported on "
            "Sunday 22 November 2026, and was checked against the day's "
            "reporting. Nothing here is from another day.")
    by = draw_lines(draw, x + 10, y + 26, wrap(draw, body, f_body, w - 20),
                    f_body, INK, leading=14)
    hy = by + 6
    draw.text((x + 10, hy), "HOW SURE", font=f_head, fill=RED)
    legend = [
        ("\u25cf  CONFIRMED", "official or on the record"),
        ("\u25cf  REPORTED", "major outlet, same day"),
        ("\u25cb  DEVELOPING", "tolls and counts may rise"),
    ]
    ly = hy + 18
    for mark, note in legend:
        draw.text((x + 10, ly), mark, font=f_leg, fill=INK)
        draw.text((x + 118, ly), note, font=f_leg, fill=SOFT_INK)
        ly += 14
    f_cred = font(SANS, 9)
    draw.text((x + 10, y + h - 18),
              "Entry for make.fun bounty news-image-20261122 \u00b7 @obasiobo",
              font=f_cred, fill=SOFT_INK)
    return ly


def render(out_path):
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    draw_masthead(draw)
    y = draw_numbers(draw, 112)
    y = draw_heroes(draw, y + 6)
    y = draw_mediums(draw, y + 6)
    y = draw_briefs(draw, y + 2)
    y = draw_timeline(draw, y + 4)
    map_x, map_y, map_w, map_h = 20, y + 8, 560, 112
    f_map = font(SANS_B, 11)
    draw.text((map_x, map_y - 2), "WHERE THE DAY HAPPENED", font=f_map, fill=RED)
    draw_map(draw, map_x, map_y + 16, map_w, map_h)
    draw_datecheck(draw, 596, y + 8, W - 20 - 596, 168)
    out_dir = os.path.dirname(out_path)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
    img.save(out_path, format="PNG")
    return out_path


if __name__ == "__main__":
    import sys
    render(sys.argv[1] if len(sys.argv) > 1 else "/output/entry.png")
