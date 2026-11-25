#!/usr/bin/env python3
"""Render the one-day news infographic for Tuesday 24 November 2026.

Offline PIL renderer. Every story string is baked in here from stories.md,
which was verified against dated 24 Nov 2026 coverage during the build
session. Output: image.png, 1024x1024. Deterministic: pure drawing, no
randomness, no network, no time dependence.
"""
import math

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
M = 16  # outer margin

PAPER = (247, 243, 234)
INK = (18, 26, 46)
NAVY = (16, 34, 74)
RED = (178, 34, 44)
GOLD = (196, 141, 26)
GRAY = (92, 96, 108)
CARD_BG = (255, 253, 247)
RULE = (198, 190, 172)
PANEL = (238, 231, 214)
BODY = (52, 56, 70)
FAINT = (170, 185, 220)
LIGHT = (225, 232, 248)

BADGE_FILL = {
    "CONFIRMED": (22, 110, 62),
    "OFFICIAL": (24, 78, 150),
    "REPORTED": (150, 96, 10),
}

BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


canvas = Image.new("RGB", (W, H), PAPER)
pen = ImageDraw.Draw(canvas)


def fit_lines(text, fnt, max_width):
    """Greedy word wrap returning a list of lines."""
    out, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if pen.textlength(trial, font=fnt) <= max_width:
            cur = trial
        else:
            if cur:
                out.append(cur)
            cur = word
    if cur:
        out.append(cur)
    return out


def put(x, y, s, fnt, fill=INK):
    pen.text((x, y), s, font=fnt, fill=fill)


def put_right(x, y, s, fnt, fill):
    put(x - pen.textlength(s, font=fnt), y, s, fnt, fill)


def badge(x, y, kind):
    fnt = font(BOLD, 8)
    w = pen.textlength(kind, font=fnt) + 8
    pen.rounded_rectangle([x, y, x + w, y + 13], 3, fill=BADGE_FILL[kind])
    pen.text((x + 4, y + 1), kind, font=fnt, fill=(255, 255, 255))
    return x + w


# ------------------------------------------------------------------ content
LEAD = {
    "kick": "LEAD STORY \u00b7 BUSINESS",
    "head": "SANOFI BUYS INSMED FOR $41 BILLION",
    "body": ("French drugmaker Sanofi agrees to buy US biotech Insmed in cash at "
             "$175 a share \u2014 the year's biggest biopharma deal, adding two lung "
             "drugs to its pipeline. Sanofi shares jump 5.6% at the open."),
    "src": "Sanofi \u00b7 WSJ \u00b7 Morningstar",
    "badge": "CONFIRMED",
}

# (icon, headline, summary, source, badge)
CARDS = [
    ("blast", "ISRAELI STRIKES KILL HAMAS SECURITY CHIEF IN GAZA",
     "Naeem Abu Nahel killed in Gaza City; six others dead, incl. two police officers.",
     "Reuters", "CONFIRMED"),
    ("blast", "RUSSIAN ATTACK ON ZAPORIZHZHIA KILLS 2, WOUNDS 40",
     "Overnight strike hits a flat block; four children among the wounded.",
     "Reuters", "CONFIRMED"),
    ("star", "MOST DISTANT QUASAR YET: 630M YEARS AFTER BIG BANG",
     "Euclid finds J1504+6252, 'Dun Aonghasa', a black hole of ~360m Suns.",
     "ESA \u00b7 Reuters", "CONFIRMED"),
    ("trophy", "USA TO HOST COPA AMERICA 2028",
     "16 teams, 9 June\u20139 July; second straight US edition. USMNT must qualify.",
     "Reuters \u00b7 CONMEBOL", "CONFIRMED"),
    ("ball", "REAL MADRID THRASH PSV 5-1 IN CHAMPIONS LEAGUE",
     "Mbappe scores twice after a Perisic penalty; Madrid's perfect run goes on.",
     "AllSports", "CONFIRMED"),
    ("quake", "MAGNITUDE 5.6 QUAKE HITS NEPAL NEAR CHINA BORDER",
     "07:17 local, Taplejung; felt in Kathmandu, India, Bhutan and Bangladesh.",
     "PTI \u00b7 Kathmandu Post", "CONFIRMED"),
    ("shield", "GERMANY FIRST TO GET UKRAINE'S DELTA WAR SYSTEM",
     "Berlin signs access deal; preliminary agreement on more interceptor missiles.",
     "Kyiv Independent", "REPORTED"),
    ("oil", "IRAQ PM ORDERS MINISTRY TO RUN KURDISH-AREA OILFIELDS",
     "Covers Diyala, Kirkuk, Salahuddin and Nineveh after a smuggling probe.",
     "Reuters", "CONFIRMED"),
    ("brain", "S. KOREA OFFERS $375,000 TO CATCH AI EXAM CHEATERS",
     "Rewards for tips on AI cheating in the college entrance test.",
     "Wall Street Journal", "CONFIRMED"),
    ("plane", "HASINA PLANS RETURN TO BANGLADESH ON 16 DECEMBER",
     "Ex-PM's spokesman confirms date; Dhaka minister: she will come 'in handcuffs'.",
     "Reuters \u00b7 BBC", "CONFIRMED"),
    ("scale", "JAPAN TO PAY FULL 2027 ICC BILL BY YEAR-END",
     "PM Takaichi acts as the court seeks early payment before US sanctions bite.",
     "Reuters", "CONFIRMED"),
    ("flag", "AMNESTY: TIGRAY STRIKES MAY BE WAR CRIMES",
     "Ethiopian artillery on towns in 2026; TPLF also accused over Alamata.",
     "Amnesty \u00b7 Reuters", "OFFICIAL"),
]

# (headline, tail, source, badge)
MORE = [
    ("Wall Street's best day in over a year", "S&P 500 +4.73%, Nasdaq +6.51%; Nikkei +3.91%, Seoul +6%", "Horizon", "CONFIRMED"),
    ("Arsenal 1-1 Dortmund; Man City 2-2 Napoli", "Gyokeres scores early; Cherki rescues City; Villa lose 1-0", "AllSports", "CONFIRMED"),
    ("CAS restores Senegal's 2025 AFCON title", "overturns CAF ruling that gave Morocco a 3-0 win", "AllSports", "REPORTED"),
    ("UN mission in Libya urges Benghazi probe", "independent inquiry into Sunday's port attacks", "UN News", "OFFICIAL"),
    ("Russian aircraft enter S. Korea's defence zone", "Joint Chiefs correct earlier airspace-violation reports", "AP", "CONFIRMED"),
    ("Latvia: Ukraine war may hit tipping point in 2027", "Rinkevics cites Russia's worsening economy", "Reuters", "REPORTED"),
    ("Norway in dialogue with Ukraine on stability", "Defence chief: attacks stop 'if Russia stopped this war'", "Reuters", "REPORTED"),
    ("US discussing training Syrian soldiers in demining", "multinational plan faces US legal hurdles", "Reuters", "REPORTED"),
    ("Huckabee doubts US aid to Israel ends this year", "$3.8bn a year 'supposed to continue for two more years'", "Reuters", "REPORTED"),
    ("Report: Chinese AI campaign targets Taiwan vote", "Vanderbilt finds coordinated inauthentic activity", "NYT", "REPORTED"),
    ("FDA clears bezuclastinib combo for advanced GIST", "new treatment for gastrointestinal stromal tumours", "FDA", "OFFICIAL"),
    ("China opens Tiangong to first foreign astronaut", "Pakistani Zeeshan Ali to fly on Shenzhou-24", "Straits Times", "REPORTED"),
    ("Car bomb wrecks buildings in Villavicencio", "Colombia attack; no confirmed victims", "The Hindu", "REPORTED"),
    ("Houthis report dozens dead in Saudi airstrikes", "claim carried in Tuesday's roundups", "Horizon", "REPORTED"),
    ("Mexico to try 'El Chapo Isidro' itself", "despite a US extradition request", "Horizon", "REPORTED"),
    ("Tripoli demands answers from Kyiv", "over Ukraine's attack on Russian ships off Benghazi", "Horizon", "REPORTED"),
    ("Hernandez de Cos tipped to lead the ECB", "ex-Bank of Spain chief frontrunner to succeed Lagarde", "Horizon", "REPORTED"),
    ("Macron wants strategic rare-earth reserves", "France to stockpile critical minerals", "Horizon", "REPORTED"),
    ("Texas AG Paxton drops trans-care doctor cases", "ends 2024 lawsuits against two doctors", "AP", "REPORTED"),
    ("DOJ: US citizen deported after ICE error", "dual US-Mexican citizen Brian Morales Garcia", "The Hill", "REPORTED"),
    ("Pennsylvania records ninth measles death", "outbreak now spans 46 counties in the state", "Horizon", "REPORTED"),
]

NUMBERS = [
    ("34", "verified stories\non this page"),
    ("$41bn", "Sanofi's deal for\nInsmed, year's biggest"),
    ("+6.51%", "Nasdaq on Wall St's\nbest day in a year"),
    ("5.6", "magnitude of the\nNepal earthquake"),
    ("630m yrs", "after the Big Bang:\nrecord quasar's age"),
    ("5\u20131", "Real Madrid's win\nover PSV Eindhoven"),
]

TIMELINE = [
    ("01:32", "Nepal quake"),
    ("07:05", "Sanofi $41bn deal"),
    ("17:53", "Record quasar"),
    ("19:00", "UCL night: 5-1"),
]


# ------------------------------------------------------------------ icons
def draw_icon(name, x, y, s, col=NAVY):
    cx, cy = x + s // 2, y + s // 2
    lw = max(2, s // 16)
    if name == "blast":
        pen.rectangle([x + 6, y + s - 16, x + 22, y + s - 3], outline=col, width=lw)
        pen.rectangle([x + 24, y + s - 24, x + s - 8, y + s - 3], outline=col, width=lw)
        for dx, dy in [(0, -8), (8, -4), (-8, -4), (5, -10), (-5, -10)]:
            pen.line([cx + 8 + dx, y + 16 + dy, cx + 8 + dx * 2, y + 8 + dy],
                     fill=RED, width=lw)
    elif name == "star":
        pts = []
        for i in range(10):
            ang = -math.pi / 2 + i * math.pi / 5
            r = s // 2 - 2 if i % 2 == 0 else s // 5
            pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
        pen.polygon(pts, outline=col, width=lw)
    elif name == "trophy":
        pen.arc([x + 6, y + 4, x + s - 6, y + s - 14], 0, 180, fill=col, width=lw)
        pen.line([cx - 8, y + s - 14, cx + 8, y + s - 14], fill=col, width=lw)
        pen.line([cx, y + s - 14, cx, y + s - 4], fill=col, width=lw)
        pen.line([cx - 10, y + s - 4, cx + 10, y + s - 4], fill=col, width=lw + 1)
    elif name == "ball":
        pen.ellipse([x + 5, y + 5, x + s - 5, y + s - 5], outline=col, width=lw)
        pen.polygon([(cx - 5, cy - 5), (cx + 5, cy - 5), (cx + 7, cy + 3),
                     (cx, cy + 7), (cx - 7, cy + 3)], outline=col, width=lw)
    elif name == "quake":
        pen.line([x + 4, cy + 8, x + 12, cy - 8, x + 20, cy + 6, x + 28, cy - 10,
                  x + s - 6, cy + 4], fill=RED, width=lw + 1)
        pen.line([x + 4, y + s - 5, x + s - 4, y + s - 5], fill=col, width=lw)
    elif name == "shield":
        pen.polygon([(cx, y + 3), (x + s - 4, y + 10), (x + s - 4, cy + 4),
                     (cx, y + s - 4), (x + 4, cy + 4), (x + 4, y + 10)],
                    outline=col, width=lw)
        pen.line([cx - 6, cy, cx - 1, cy + 5, cx + 7, cy - 6], fill=RED, width=lw)
    elif name == "oil":
        pen.ellipse([cx - 10, y + 6, cx + 10, y + 26], outline=col, width=lw)
        pen.polygon([(cx - 10, y + 16), (cx + 10, y + 16), (cx + 14, y + s - 6),
                     (cx - 14, y + s - 6)], outline=col, width=lw)
    elif name == "brain":
        pen.ellipse([x + 6, y + 8, cx + 6, y + s - 8], outline=col, width=lw)
        pen.ellipse([cx - 6, y + 8, x + s - 6, y + s - 8], outline=col, width=lw)
        pen.line([cx, y + 8, cx, y + s - 8], fill=col, width=lw)
    elif name == "plane":
        pen.polygon([(x + 4, cy + 6), (x + s - 6, y + 8), (x + s - 12, cy - 8),
                     (x + s - 18, cy + 2), (x + 16, cy - 2)], outline=col, width=lw)
        pen.line([x + 6, y + s - 6, x + s - 8, y + s - 10], fill=col, width=lw)
    elif name == "scale":
        pen.line([cx, y + 4, cx, y + s - 8], fill=col, width=lw)
        pen.line([x + 6, y + 10, x + s - 6, y + 10], fill=col, width=lw)
        pen.polygon([(x + 2, y + 12), (x + 12, y + 12), (x + 7, y + 22)], outline=col, width=lw)
        pen.polygon([(x + s - 12, y + 12), (x + s - 2, y + 12), (x + s - 7, y + 22)],
                    outline=col, width=lw)
        pen.line([cx - 10, y + s - 4, cx + 10, y + s - 4], fill=col, width=lw + 1)
    elif name == "pill":
        pen.rounded_rectangle([x + 6, y + 12, x + s - 6, y + s - 12], s // 4,
                              outline=col, width=lw)
        pen.line([x + 12, y + s - 12, x + s - 12, y + 12], fill=RED, width=lw)
        pen.ellipse([x + s - 16, y + s - 16, x + s - 6, y + s - 6], fill=GOLD)
    elif name == "flag":
        pen.line([x + 8, y + 4, x + 8, y + s - 4], fill=col, width=lw)
        pen.polygon([(x + 8, y + 4), (x + s - 6, y + 10), (x + 8, y + 18)], fill=RED)


# ------------------------------------------------------------------ masthead
pen.rectangle([0, 0, W, 62], fill=NAVY)
put(M, 6, "THE WORLD IN ONE DAY", font(BOLD, 15), (255, 255, 255))
sub = "34 verified stories \u00b7 every one first reported on 24 Nov 2026"
put_right(W - M, 8, sub, font(REG, 12), (210, 220, 245))
put(M, 28, "TUESDAY 24 NOVEMBER 2026", font(BOLD, 27), (255, 255, 255))
tag = "ONE IMAGE \u00b7 ONE DAY \u00b7 THE WHOLE WORLD"
put_right(W - M, 40, tag, font(BOLD, 11), GOLD)

# ------------------------------------------------------------------ numbers
ny = 68
nw = (W - 2 * M - 5 * 6) // 6
for i, (num, lab) in enumerate(NUMBERS):
    x = M + i * (nw + 6)
    pen.rectangle([x, ny, x + nw, ny + 46], fill=PANEL, outline=RULE)
    put(x + 8, ny + 2, num, font(BOLD, 18), RED)
    for j, ln in enumerate(lab.split("\n")):
        put(x + 8, ny + 24 + j * 10, ln, font(REG, 9), GRAY)

# ------------------------------------------------------------------ lead
ly = 122
pen.rectangle([M, ly, W - M, ly + 86], fill=NAVY)
draw_icon("pill", M + 10, ly + 14, 56, (255, 255, 255))
lx = M + 78
put(lx, ly + 7, LEAD["kick"], font(BOLD, 11), GOLD)
put(lx, ly + 22, LEAD["head"], font(BOLD, 21), (255, 255, 255))
for j, ln in enumerate(fit_lines(LEAD["body"], font(REG, 12), W - lx - M - 8)):
    put(lx, ly + 50 + j * 14, ln, font(REG, 12), LIGHT)
bw = pen.textlength(LEAD["badge"], font=font(BOLD, 9)) + 8
pen.rounded_rectangle([W - M - bw, ly + 7, W - M, ly + 20], 3,
                      fill=BADGE_FILL[LEAD["badge"]])
pen.text((W - M - bw + 4, ly + 8), LEAD["badge"], font=font(BOLD, 9),
         fill=(255, 255, 255))
put_right(W - M, ly + 70, LEAD["src"], font(REG, 10), FAINT)

# ------------------------------------------------------------------ cards
gy = ly + 94
cw = (W - 2 * M - 2 * 8) // 3
ch = 86
for idx, (ic, head, summ, src, bd) in enumerate(CARDS):
    r, c = divmod(idx, 3)
    x, y = M + c * (cw + 8), gy + r * (ch + 6)
    pen.rectangle([x, y, x + cw, y + ch], fill=CARD_BG, outline=RULE)
    pen.rectangle([x, y, x + 4, y + ch], fill=RED if idx % 3 == 0 else NAVY)
    draw_icon(ic, x + 10, y + 10, 40)
    tx = x + 58
    for j, ln in enumerate(fit_lines(head, font(BOLD, 12), x + cw - tx - 6)[:2]):
        put(tx, y + 6 + j * 14, ln, font(BOLD, 12), INK)
    for j, ln in enumerate(fit_lines(summ, font(REG, 10), x + cw - tx - 6)[:3]):
        put(tx, y + 36 + j * 12, ln, font(REG, 10), BODY)
    bx = badge(x + 10, y + ch - 17, bd)
    put(bx + 5, y + ch - 15, src, font(REG, 9), GRAY)

# ------------------------------------------------------------------ timeline
ty = gy + 4 * (ch + 6) + 2
pen.rectangle([M, ty, W - M, ty + 58], fill=PANEL, outline=RULE)
put(M + 8, ty + 4, "THE DAY BY THE HOUR \u2014 FIRST REPORTED (UTC)",
    font(BOLD, 11), NAVY)
tl_y = ty + 34
pen.line([M + 14, tl_y, W - M - 14, tl_y], fill=NAVY, width=2)
n = len(TIMELINE)
for i, (hh, ev) in enumerate(TIMELINE):
    x = M + 14 + i * (W - 2 * M - 28) // (n - 1)
    pen.ellipse([x - 3, tl_y - 3, x + 3, tl_y + 3], fill=RED)
    tx_ = min(max(x - 17, M + 4), W - M - 40)
    put(tx_, tl_y - 16, hh, font(BOLD, 10), INK)
    ex = min(max(x - 40, M + 2), W - M - 90)
    put(ex, tl_y + 6 + (10 if i % 2 else 0), ev, font(REG, 8), BODY)

# ------------------------------------------------------------------ more list
sy = ty + 66
put(M, sy, "ALSO ON 24 NOVEMBER \u2014 21 MORE VERIFIED STORIES", font(BOLD, 13), NAVY)
pen.line([M, sy + 18, W - M, sy + 18], fill=RED, width=2)
colw = (W - 2 * M - 16) // 2
rowh = 26
for i, (head, tail, src, bd) in enumerate(MORE):
    c = 0 if i < 11 else 1
    r = i if i < 11 else i - 11
    x = M + c * (colw + 16)
    y = sy + 24 + r * rowh
    put(x, y, f"{i + 14:02d}", font(BOLD, 11), RED)
    hx = x + 26
    put(hx, y, fit_lines(head, font(BOLD, 11), colw - 26)[0], font(BOLD, 11), INK)
    put(hx, y + 13, f"{tail}  \u2014 {src}", font(REG, 9), GRAY)
    bw2 = pen.textlength(bd, font=font(BOLD, 7)) + 6
    pen.rounded_rectangle([x + colw - bw2, y + 1, x + colw, y + 11], 2,
                          fill=BADGE_FILL[bd])
    pen.text((x + colw - bw2 + 3, y + 2), bd, font=font(BOLD, 7),
             fill=(255, 255, 255))

# ------------------------------------------------------------------ footer
fy = sy + 24 + 11 * rowh + 8
pen.rectangle([0, fy, W, H], fill=NAVY)
put(M, fy + 7, "DATE CHECK \u2713", font(BOLD, 13), GOLD)
dc = ("Every story above was first reported on Tuesday 24 November 2026 (any "
      "time zone) and cross-checked against dated 24 Nov editions. Deliberately "
      "EXCLUDED as not of this day: the COP31 collapse and Nvidia's CEO return "
      "(both 23 Nov), the Grok lawsuits and Medvedev's nuclear warning (filed "
      "and published Monday 23 Nov), and the UN's Gaza 77-year report (23 Nov). "
      "Badges: CONFIRMED = 2+ outlets \u00b7 OFFICIAL = official source \u00b7 "
      "REPORTED = single outlet.")
for j, ln in enumerate(fit_lines(dc, font(REG, 11), W - 2 * M - 130)):
    put(M + 130, fy + 5 + j * 13, ln, font(REG, 11), LIGHT)

canvas.save("image.png", optimize=True)
print("saved image.png", canvas.size)
