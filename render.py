#!/usr/bin/env python3
"""Render THE WORLD TODAY — front page for 18 November 2026 (1024x1024).

Build-time script. The graded program is main.py, which only copies the
baked entry.png to /output/entry.png (deterministic, no network).
All 33 stories were verified against live reporting on 18 Nov 2026
(Reuters, AP, Al Jazeera, BBC, The Hindu, CSK, IMD, official statements).
One claim from the early brief was DROPPED after checking: no North
Korean ballistic launch on 18 Nov 2026 could be verified (the launches
in the news were 4-5 Nov) — it is not on this page.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
M = 26                      # margin
CW = W - 2 * M              # 972 content width
PAPER = (253, 252, 246)
INK = (17, 17, 17)
GREY = (90, 90, 84)
RED = (178, 24, 24)
LAND = (216, 214, 200)
LAND_EDGE = (120, 118, 105)
SEA = (223, 232, 240)
RULE = (17, 17, 17)


def font(name, size):
    cands = {
        "serif_b": ["/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf",
                    "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"],
        "serif": ["/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf",
                  "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"],
        "serif_i": ["/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf",
                    "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Italic.ttf"],
        "sans_b": ["/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
                   "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"],
        "sans": ["/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
                 "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"],
    }
    for p in cands[name]:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def wrap(draw, text, fnt, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= width:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_h(draw, lines, fnt):
    return sum(draw.textbbox((0, 0), l, font=fnt)[3] for l in lines) + \
        (len(lines) - 1) * 2


# ---------------------------------------------------------------- stories
LEAD = {
    "kicker": "LEAD STORY  •  DIPLOMACY  —  MANILA / SHENZHEN",
    "head": "Trump takes the Quad to Manila — then flies to meet Xi and Putin",
    "deck": ("First Quad summit in two years agrees a joint maritime watch and an $85m AI "
             "plan. The US president meets Marcos today, then heads to Shenzhen for APEC — "
             "and Thursday's first-ever trilateral with Xi and Putin."),
}

SECONDARY = [
    {"kicker": "EUROPE  •  WAR IN UKRAINE",
     "head": "Ukraine smashes the Kerch bridge",
     "deck": ("Road arch collapses into the strait on day two of the biggest drone attack "
              "of the war — 1,441 drones, two killed, traffic halted.")},
    {"kicker": "MIDDLE EAST  •  GULF",
     "head": "Iran's drones at US radar in Bahrain",
     "deck": ("Tehran claims a precision hit on Sheikh Isa base; the US says every drone "
              "was intercepted. Washington answers with strikes on Qeshm Island.")},
    {"kicker": "ASIA  •  TRADE",
     "head": "APEC opens in Shenzhen",
     "deck": ("21 leaders meet 18–19 Nov on trade, AI and supply chains — with the "
              "Trump–Xi–Putin trilateral looming on Thursday.")},
]

# (section, head, deck) — 29 items; lead + 3 secondary = 33 stories
GRID = [
    ("EUROPE", "Russia pounds Kyiv's bridges",
     "Northern and Southern bridges hit; power and water cut in parts of the capital"),
    ("EUROPE", "UK sanctions eight settlement firms",
     "West Bank builders targeted; group accused of blocking Gaza aid also listed"),
    ("EUROPE", "EU–Rwanda return-hub talks open",
     "Five states back Vienna plan; refused asylum seekers would go to Kigali"),
    ("EUROPE", "Serbian MiG-29 crashes, pilot killed",
     "Jet goes down near Stara Pazova; inquiry opened"),
    ("EUROPE", "Russian An-12 crashes in Siberia",
     "Military transport goes down in Kemerovo; 13 killed"),
    ("EUROPE", "Spain lifts minimum wage 5.3%",
     "Pay rises to €1,286 a month; election set for 29 November"),
    ("EUROPE", "France denies troops in Ukraine",
     "Paris rejects Moscow claim of French combat troops on the ground"),
    ("EUROPE", "Estonia to shut Russia border crossings",
     "Road crossings close from 1 December after sabotage bid on drone maker"),
    ("AFRICA", "Nigeria: US intel aids militant hunt",
     "Satellite help for 2027 vote; Zamfara police free 20 abducted"),
    ("AFRICA", "South Africa probes 17 shooting deaths",
     "Two mass shootings in Pretoria and KwaZulu-Natal"),
    ("AFRICA", "Sudan toll: 2,230 civilians dead",
     "UN confirms January–October toll; AU pushes Sudan and Congo peace"),
    ("AFRICA", "Guinea mining crackdown displaces thousands",
     "Illegal-mining ban sparks exodus and row with neighbours"),
    ("ASIA", "Putin lands in Shenzhen",
     "Arrives a day early for Thursday's trilateral with Trump and Xi"),
    ("ASIA", "Quad unveils maritime watch",
     "Joint P-8 patrols in 2027; $85m AI Accelerator and cable pact agreed"),
    ("ASIA", "ASEAN chair passes to Singapore",
     "100+ documents adopted; South China Sea code 85–90% settled"),
    ("ASIA", "Modi offers free e-visas to ASEAN",
     "Pitch at East Asia Summit; lays stone for Manila's oldest gurudwara"),
    ("ASIA", "Japan protests Russian airspace breach",
     "Two jets believed Russian entered airspace; Tokyo lodges protest"),
    ("ASIA", "Cyclone Akvan bears down on Andhra",
     "Landfall due 20 Nov, Nellore–Tuni; gusts to 145 km/h, red alert"),
    ("ASIA", "India re-elected to ITU Council",
     "Wins 2027–2030 term; Digital India pitch carries the vote"),
    ("ASIA", "Amazon to put $7bn into India renewables",
     "Solar and data centres by 2030; jobs in Rajasthan, Gujarat, Karnataka"),
    ("BUSINESS & TECH", "Canada and China cut tariffs",
     "C$400m relief on pork and seafood; steel waivers extended two years"),
    ("BUSINESS & TECH", "US extends AI-chip licence rules",
     "Data centres in Southeast Asia and Brazil now need licences"),
    ("BUSINESS & TECH", "Nvidia revenue doubles to $115.8bn",
     "Up 103%; guides $130bn for Q4 in first results since Huang exit"),
    ("BUSINESS & TECH", "Vulcan rocket fails; 40 satellites lost",
     "ULA failure grounds Amazon's Leo internet plan"),
    ("SPORT", "Dhoni retires from the IPL",
     "45, five titles, 5,439 runs; takes over as CSK mentor for 2027"),
    ("THE AMERICAS", "Costa Rica journalist murdered",
     "Shot dead after probing politicians' drug-trafficking links"),
    ("THE AMERICAS", "Pope Leo pleads for Amazon defenders",
     "Calls for justice on Peru visit"),
    ("THE AMERICAS", "US jails Asif Merchant for 27.5 years",
     "Sentenced over a plot against US officials"),
    ("OCEANIA", "Australia sanctions settlements",
     "Wong targets 'illegal' West Bank expansion"),
]

NUMBERS = [
    ("1,441", "drones in Ukraine's biggest overnight attack"),
    ("$115.8bn", "Nvidia revenue, up 103% on a year"),
    ("372", "civilians killed in Ukraine in October (UN)"),
    ("145 km/h", "Cyclone Akvan gusts at landfall"),
]

# lon/lat dots on the map
DOTS = [
    ("MANILA", 121.0, 14.6), ("SHENZHEN", 114.1, 22.5),
    ("KYIV", 30.5, 50.5), ("KERCH", 36.5, 45.3),
    ("BAHRAIN", 50.6, 26.2), ("KUWAIT", 48.0, 29.4),
    ("ANDHRA", 80.0, 14.4), ("PRETORIA", 28.2, -25.7),
    ("SAN JOSÉ", -84.1, 9.9), ("LIMA", -77.0, -12.0),
    ("LONDON", -0.1, 51.5), ("CANBERRA", 149.1, -35.3),
]

# coarse continent polygons (lon, lat)
NA = [(-168, 65), (-158, 58), (-152, 60), (-140, 60), (-135, 58), (-130, 54),
      (-125, 49), (-124, 42), (-120, 34), (-114, 29), (-110, 24), (-105, 20),
      (-97, 16), (-94, 17), (-90, 14), (-86, 12), (-83, 9), (-79, 9),
      (-81, 13), (-86, 15), (-90, 21), (-97, 26), (-93, 30), (-89, 30),
      (-84, 30), (-81, 26), (-80, 32), (-76, 35), (-74, 40), (-70, 42),
      (-68, 45), (-65, 44), (-60, 47), (-55, 52), (-60, 55), (-65, 58),
      (-68, 58), (-72, 62), (-78, 62), (-82, 66), (-88, 66), (-95, 69),
      (-110, 68), (-125, 70), (-140, 70), (-155, 71), (-165, 68), (-168, 66)]
GREENLAND = [(-58, 64), (-52, 60), (-43, 60), (-40, 64), (-32, 68), (-22, 70),
             (-20, 74), (-25, 76), (-35, 77), (-50, 76), (-58, 74), (-60, 70)]
SA = [(-79, 9), (-77, 7), (-77, 4), (-80, -3), (-81, -6), (-79, -9),
      (-76, -13), (-72, -18), (-70, -22), (-70, -28), (-72, -33), (-73, -38),
      (-73, -44), (-71, -50), (-68, -52), (-66, -55), (-68, -54), (-65, -48),
      (-64, -42), (-61, -37), (-57, -34), (-52, -32), (-48, -28), (-44, -23),
      (-40, -20), (-38, -15), (-35, -9), (-35, -6), (-38, -4), (-42, -2),
      (-46, 0), (-50, 1), (-53, 4), (-57, 6), (-61, 9), (-65, 11),
      (-70, 12), (-75, 11), (-77, 10)]
AFRICA = [(-17, 15), (-16, 21), (-14, 27), (-9, 31), (-5, 35), (0, 36),
          (9, 37), (11, 34), (15, 32), (20, 32), (25, 32), (30, 31),
          (32, 31), (34, 27), (35, 22), (37, 18), (39, 15), (43, 12),
          (48, 11), (51, 12), (49, 7), (45, 2), (41, -2), (40, -8),
          (40, -14), (38, -18), (35, -23), (33, -26), (30, -29), (27, -33),
          (22, -35), (19, -34), (17, -32), (15, -27), (13, -20), (12, -15),
          (13, -10), (12, -6), (9, -1), (9, 4), (5, 5), (0, 6), (-5, 5),
          (-8, 5), (-12, 8), (-15, 11)]
EURASIA = [(-9, 37), (-9, 43), (-4, 44), (-2, 47), (-4, 48), (-1, 49),
           (1, 51), (3, 53), (7, 55), (8, 57), (10, 59), (6, 60), (5, 62),
           (12, 65), (18, 69), (25, 71), (30, 70), (35, 68), (40, 67),
           (44, 68), (48, 69), (52, 69), (56, 69), (60, 69), (65, 70),
           (70, 72), (75, 73), (80, 73), (85, 74), (90, 75), (95, 76),
           (100, 77), (105, 77), (110, 76), (115, 74), (120, 73), (125, 72),
           (130, 72), (135, 72), (140, 72), (145, 72), (150, 71), (155, 70),
           (160, 69), (165, 67), (170, 66), (178, 65), (178, 62), (170, 60),
           (164, 60), (160, 56), (157, 52), (150, 59), (146, 59), (142, 54),
           (141, 50), (140, 45), (138, 40), (135, 34), (132, 33), (130, 31),
           (127, 32), (124, 30), (121, 28), (119, 25), (116, 23), (112, 22),
           (109, 20), (108, 18), (106, 10), (104, 9), (101, 7), (99, 10),
           (97, 15), (94, 17), (92, 21), (89, 22), (87, 21), (84, 19),
           (81, 16), (80, 13), (77, 8), (75, 11), (73, 16), (70, 20),
           (68, 22), (66, 25), (62, 25), (58, 26), (56, 27), (53, 26),
           (51, 28), (49, 30), (48, 29), (50, 26), (52, 25), (55, 24),
           (57, 22), (59, 22), (58, 20), (55, 17), (52, 15), (48, 14),
           (45, 12), (43, 12), (42, 15), (40, 20), (38, 24), (36, 28),
           (35, 29), (34, 31), (33, 31), (30, 36), (27, 37), (23, 36),
           (21, 38), (19, 40), (18, 40), (16, 38), (15, 40), (12, 44),
           (10, 44), (8, 44), (6, 43), (3, 43), (0, 38), (-1, 37),
           (-4, 36), (-6, 36), (-9, 37)]
UK = [(-5, 50), (-3, 53), (-5, 56), (-3, 58), (-1, 57), (0, 53), (1, 51), (-4, 50)]
JAPAN = [(130, 31), (132, 33), (135, 34), (137, 37), (139, 38), (140, 40),
         (141, 42), (142, 44), (144, 44), (145, 42), (142, 40), (140, 36),
         (138, 35), (136, 33), (133, 34), (131, 32)]
SUMATRA = [(95, 5), (98, 3), (101, 0), (104, -3), (106, -6), (104, -6),
           (100, -2), (97, 2)]
BORNEO = [(109, 1), (112, 3), (116, 6), (118, 2), (117, -2), (114, -3), (110, -3)]
JAVA = [(105, -6), (110, -7), (114, -8), (114, -7), (108, -6)]
NEWGUINEA = [(131, -1), (136, -2), (141, -3), (146, -6), (150, -8), (147, -9),
             (142, -8), (137, -6), (132, -4)]
AUSTRALIA = [(114, -22), (114, -30), (115, -34), (119, -35), (124, -33),
             (129, -32), (132, -32), (135, -35), (138, -35), (140, -38),
             (145, -38), (150, -37), (153, -32), (153, -27), (150, -23),
             (146, -19), (142, -15), (142, -11), (140, -17), (136, -15),
             (135, -12), (132, -11), (130, -13), (126, -14), (122, -17),
             (118, -20)]
NZ = [(167, -45), (170, -42), (173, -40), (175, -38), (177, -38),
      (175, -41), (172, -43), (168, -46)]
MADAGASCAR = [(44, -16), (47, -15), (50, -16), (49, -20), (47, -24),
              (45, -25), (43, -21), (44, -17)]
PHILIPPINES = [(120, 18), (122, 17), (122, 14), (121, 11), (123, 10), (121, 13)]
LAND_POLYS = [NA, GREENLAND, SA, AFRICA, EURASIA, UK, JAPAN, SUMATRA, BORNEO,
              JAVA, NEWGUINEA, AUSTRALIA, NZ, MADAGASCAR, PHILIPPINES]


def render():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    y = M

    # ---- top bar
    f_top = font("sans_b", 12)
    d.text((M, y), "WEDNESDAY, 18 NOVEMBER 2026", font=f_top, fill=INK)
    r = "No. 322  •  33 STORIES  •  6 CONTINENTS"
    d.text((W - M - d.textlength(r, font=f_top), y), r, font=f_top, fill=INK)
    y += 20
    d.line([(M, y), (W - M, y)], fill=RULE, width=2)
    y += 8

    # ---- masthead
    f_mast = font("serif_b", 66)
    name = "THE WORLD TODAY"
    d.text(((W - d.textlength(name, font=f_mast)) / 2, y), name,
           font=f_mast, fill=INK)
    y += 78
    f_tag = font("sans", 12)
    tag = "T H E   D A Y ' S   W O R L D   N E W S   —   I N   O N E   P A G E"
    d.text(((W - d.textlength(tag, font=f_tag)) / 2, y), tag, font=f_tag, fill=GREY)
    y += 20
    d.line([(M, y), (W - M, y)], fill=RULE, width=3)
    y += 3
    d.line([(M, y), (W - M, y)], fill=RULE, width=1)
    y += 10

    # ---- lead story
    f_kick = font("sans_b", 11)
    d.text((M, y), LEAD["kicker"], font=f_kick, fill=RED)
    y += 17
    f_lead = font("serif_b", 35)
    lines = wrap(d, LEAD["head"], f_lead, CW)
    for ln in lines:
        d.text((M, y), ln, font=f_lead, fill=INK)
        y += 40
    y += 2
    f_deck = font("serif", 15)
    for ln in wrap(d, LEAD["deck"], f_deck, CW):
        d.text((M, y), ln, font=f_deck, fill=(40, 40, 38))
        y += 19
    y += 8
    d.line([(M, y), (W - M, y)], fill=RULE, width=1)
    y += 9

    # ---- secondary row (3 columns)
    col_w = (CW - 2 * 16) // 3
    sec_top = y
    f_sk = font("sans_b", 9)
    f_sh = font("serif_b", 17)
    f_sd = font("serif", 11)
    max_y = sec_top
    for i, s in enumerate(SECONDARY):
        x = M + i * (col_w + 16)
        yy = sec_top
        d.text((x, yy), s["kicker"], font=f_sk, fill=RED)
        yy += 14
        for ln in wrap(d, s["head"], f_sh, col_w):
            d.text((x, yy), ln, font=f_sh, fill=INK)
            yy += 20
        yy += 2
        for ln in wrap(d, s["deck"], f_sd, col_w):
            d.text((x, yy), ln, font=f_sd, fill=(40, 40, 38))
            yy += 14
        max_y = max(max_y, yy)
        if i < 2:
            d.line([(x + col_w + 8, sec_top), (x + col_w + 8, yy)],
                   fill=(200, 200, 190), width=1)
    y = max_y + 6
    d.line([(M, y), (W - M, y)], fill=RULE, width=1)
    y += 8

    # ---- map
    f_mapt = font("sans_b", 11)
    d.text((M, y), "THE DAY ON THE MAP — 12 PLACES THAT MADE THE NEWS",
           font=f_mapt, fill=INK)
    d.text((W - M - d.textlength("EQUIRECTANGULAR • DOTS = STORY SITES",
                                 font=font("sans", 9)),
            y + 1), "EQUIRECTANGULAR • DOTS = STORY SITES",
           font=font("sans", 9), fill=GREY)
    y += 17
    map_x0, map_y0 = M, y
    map_w, map_h = CW, 122
    d.rectangle([map_x0, map_y0, map_x0 + map_w, map_y0 + map_h],
                fill=SEA, outline=(150, 150, 140), width=1)
    lon0, lon1, lat0, lat1 = -170, 190, 78, -58

    def proj(lon, lat):
        return (map_x0 + (lon - lon0) / (lon1 - lon0) * map_w,
                map_y0 + (lat0 - lat) / (lat0 - lat1) * map_h)

    for poly in LAND_POLYS:
        d.polygon([proj(lo, la) for lo, la in poly],
                  fill=LAND, outline=LAND_EDGE)
    f_lab = font("sans_b", 8)
    # per-dot label anchor: (dx, dy) from the dot; keeps the crowded
    # Europe / Gulf cluster readable instead of stacking labels.
    OFF = {"LONDON": (-34, -13), "KYIV": (-30, -13), "KERCH": (6, -13),
           "BAHRAIN": (-6, 6), "KUWAIT": (-8, -14), "ANDHRA": (-14, 6),
           "SHENZHEN": (6, 6), "MANILA": (-8, 6), "PRETORIA": (-20, 6),
           "SAN JOSÉ": (-24, -13), "LIMA": (-6, 6), "CANBERRA": (-26, 6)}
    for name_, lon, lat in DOTS:
        px, py = proj(lon, lat)
        d.ellipse([px - 4, py - 4, px + 4, py + 4], fill=RED,
                  outline=(255, 255, 255), width=1)
        dx, dy = OFF.get(name_, (0, -13))
        lx = min(max(px + dx, map_x0 + 2),
                 map_x0 + map_w - d.textlength(name_, font=f_lab) - 2)
        d.text((lx, py + dy), name_, font=f_lab, fill=INK)
    y = map_y0 + map_h + 8
    d.line([(M, y), (W - M, y)], fill=RULE, width=1)
    y += 8

    # ---- grid: 3 columns, sections in order
    cols = [[], [], []]
    # col1: EUROPE(7) + AFRICA(4); col2: ASIA(8); col3: BUSINESS(4)+SPORT(1)+AMERICAS(2)+OCEANIA(1)
    order = [("EUROPE", 0), ("AFRICA", 0), ("ASIA", 1),
             ("BUSINESS & TECH", 2), ("SPORT", 2), ("THE AMERICAS", 2),
             ("OCEANIA", 2)]
    by_sec = {}
    for sec, head, deck in GRID:
        by_sec.setdefault(sec, []).append((head, deck))
    for sec, ci in order:
        cols[ci].append((sec, by_sec[sec]))
    f_sec = font("sans_b", 10)
    f_h = font("sans_b", 11)
    f_dd = font("sans", 9)
    grid_top = y
    grid_bottom = grid_top
    col_w = (CW - 2 * 14) // 3
    for ci, col in enumerate(cols):
        x = M + ci * (col_w + 14)
        yy = grid_top
        for sec, items in col:
            d.text((x, yy), sec, font=f_sec, fill=RED)
            yy += 14
            d.line([(x, yy), (x + col_w, yy)], fill=RED, width=1)
            yy += 5
            for head, deck in items:
                for ln in wrap(d, head, f_h, col_w)[:2]:
                    d.text((x, yy), ln, font=f_h, fill=INK)
                    yy += 13
                for ln in wrap(d, deck, f_dd, col_w)[:1]:
                    d.text((x, yy), ln, font=f_dd, fill=GREY)
                    yy += 11
                yy += 3
            yy += 2
        if ci == 2:
            # numbers box fills the rest of column 3
            yy += 2
            d.text((x, yy), "THE DAY IN NUMBERS", font=f_sec, fill=RED)
            yy += 14
            d.line([(x, yy), (x + col_w, yy)], fill=RED, width=1)
            yy += 6
            f_n = font("serif_b", 14)
            f_nt = font("sans", 9)
            for num, txt in NUMBERS:
                d.text((x, yy), num, font=f_n, fill=RED)
                nw = d.textlength(num, font=f_n)
                for ln in wrap(d, txt, f_nt, col_w - nw - 8)[:1]:
                    d.text((x + nw + 8, yy + 2), ln, font=f_nt, fill=INK)
                yy += 15
        grid_bottom = max(grid_bottom, yy)
        if ci < 2:
            d.line([(x + col_w + 7, grid_top), (x + col_w + 7, yy)],
                   fill=(200, 200, 190), width=1)
    # footer rule goes below the TALLEST column (col 3 carries the numbers box)
    y = grid_bottom + 4
    d.line([(M, y), (W - M, y)], fill=RULE, width=1)
    y += 7

    # ---- footer
    f_f = font("sans", 9)
    tick = ("ALSO:  UN counts 372 civilians killed in Ukraine in October  •  Gaza: WFP down to one "
            "hot meal every two days  •  Latvia approves Kulbergs cabinet  •  Voyager 1 nears one light-day")
    for ln in wrap(d, tick, f_f, CW):
        d.text((M, y), ln, font=f_f, fill=INK)
        y += 12
    y += 2
    src = ("Sources: Reuters • AP • Al Jazeera • BBC • The Hindu • CSK • IMD • Compiled Wednesday 18 November 2026  •  "
           "33 stories, 6 continents")
    for ln in wrap(d, src, f_f, CW):
        d.text((M, y), ln, font=f_f, fill=GREY)
        y += 12
    print("content bottom y =", y, "of", H)
    return img


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img = render()
    img.save(out, optimize=True)
    print("saved", out, os.path.getsize(out), "bytes")
