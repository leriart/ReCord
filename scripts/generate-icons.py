#!/usr/bin/env python3
from pathlib import Path

SIZE = 16
OUT = Path(__file__).resolve().parent.parent / "assets" / "icons"
OUT.mkdir(exist_ok=True)

class Grid:
    def __init__(self):
        self.p = [[0] * SIZE for _ in range(SIZE)]

    def rect(self, x, y, w, h, v=1):
        for yy in range(y, y + h):
            for xx in range(x, x + w):
                if 0 <= xx < SIZE and 0 <= yy < SIZE:
                    self.p[yy][xx] = v

    def frame(self, x, y, w, h, v=1):
        self.rect(x, y, w, 1, v)
        self.rect(x, y + h - 1, w, 1, v)
        self.rect(x, y, 1, h, v)
        self.rect(x + w - 1, y, 1, h, v)

    def line(self, x1, y1, x2, y2, v=1):
        dx, dy = abs(x2 - x1), abs(y2 - y1)
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        err = dx - dy
        while True:
            if 0 <= x1 < SIZE and 0 <= y1 < SIZE:
                self.p[y1][x1] = v
            if x1 == x2 and y1 == y2:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x1 += sx
            if e2 < dx:
                err += dx
                y1 += sy

    def clear_line(self, x1, y1, x2, y2):
        self.line(x1, y1, x2, y2, 0)

    def pixels(self, *coords, v=1):
        for x, y in coords:
            if 0 <= x < SIZE and 0 <= y < SIZE:
                self.p[y][x] = v

    def circle(self, cx, cy, r, fill=False):
        for y in range(SIZE):
            for x in range(SIZE):
                d = (x + 0.5 - cx) ** 2 + (y + 0.5 - cy) ** 2
                if fill and d <= r * r:
                    self.p[y][x] = 1
                elif not fill and (r - 1) ** 2 < d <= r * r:
                    self.p[y][x] = 1

    def text3x5(self, text, x, y, scale=1):
        font = {
            "A": ["010", "101", "111", "101", "101"],
            "B": ["110", "101", "110", "101", "110"],
            "C": ["011", "100", "100", "100", "011"],
            "D": ["110", "101", "101", "101", "110"],
            "E": ["111", "100", "110", "100", "111"],
            "F": ["111", "100", "110", "100", "100"],
            "G": ["011", "100", "101", "101", "011"],
            "H": ["101", "101", "111", "101", "101"],
            "I": ["111", "010", "010", "010", "111"],
            "L": ["100", "100", "100", "100", "111"],
            "M": ["101", "111", "111", "101", "101"],
            "N": ["101", "111", "111", "111", "101"],
            "O": ["010", "101", "101", "101", "010"],
            "P": ["110", "101", "110", "100", "100"],
            "R": ["110", "101", "110", "101", "101"],
            "S": ["011", "100", "010", "001", "110"],
            "T": ["111", "010", "010", "010", "010"],
            "U": ["101", "101", "101", "101", "111"],
            "V": ["101", "101", "101", "101", "010"],
            "X": ["101", "101", "010", "101", "101"],
            "Y": ["101", "101", "010", "010", "010"],
        }
        cx = x
        for ch in text:
            rows = font.get(ch, ["000"] * 5)
            for yy, row in enumerate(rows):
                for xx, bit in enumerate(row):
                    if bit == "1":
                        self.rect(cx + xx * scale, y + yy * scale, scale, scale)
            cx += 4 * scale

    def save(self, name):
        cells = []
        for y, row in enumerate(self.p):
            for x, value in enumerate(row):
                if value:
                    cells.append(f'<rect x="{x}" y="{y}" width="1" height="1"/>')
        svg = (
            '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" '
            'shape-rendering="crispEdges"><g fill="#fff">'
            + "".join(cells)
            + "</g></svg>\n"
        )
        (OUT / f"{name}.svg").write_text(svg)

def make(name, fn):
    g = Grid()
    fn(g)
    g.save(name)

make("search", lambda g: (g.circle(6.5, 6.5, 5), g.line(10, 10, 13, 13), g.line(11, 10, 13, 12)))
make("inbox", lambda g: (g.frame(2, 4, 12, 9), g.line(2, 9, 5, 9), g.line(11, 9, 14, 9), g.line(5, 9, 7, 11), g.line(9, 11, 11, 9), g.line(5, 2, 11, 2)))
def help_icon(g):
    rows = [".###.", "#...#", "....#", "...##", "..#..", ".....", "..#.."]
    for y, row in enumerate(rows):
        for x, bit in enumerate(row):
            if bit == "#":
                g.rect(3 + x * 2, 1 + y * 2, 2, 2)

make("help", help_icon)
make("members", lambda g: (g.circle(5, 6, 2), g.circle(11, 6, 2), g.rect(2, 9, 7, 5), g.rect(7, 9, 7, 5)))
make("pin", lambda g: (g.rect(5, 2, 6, 4), g.rect(6, 6, 4, 6), g.rect(4, 12, 8, 2)))
make("bell", lambda g: (g.rect(6, 2, 4, 2), g.rect(4, 4, 8, 2), g.rect(3, 6, 10, 6), g.rect(2, 12, 12, 2), g.rect(7, 14, 2, 2)))
make("thread", lambda g: (g.rect(2, 3, 5, 5), g.rect(8, 8, 6, 5), g.line(7, 5, 8, 8), g.line(4, 8, 4, 12), g.line(4, 12, 7, 12)))
make("settings", lambda g: (g.rect(2, 4, 12, 2), g.rect(2, 10, 12, 2), g.rect(5, 2, 2, 6), g.rect(10, 8, 2, 6)))
make("mic", lambda g: (g.frame(6, 2, 4, 8), g.rect(5, 10, 6, 2), g.rect(7, 12, 2, 3), g.rect(5, 15, 6, 1)))
make("mic-off", lambda g: (g.frame(6, 2, 4, 8), g.rect(5, 10, 6, 2), g.rect(7, 12, 2, 3), g.rect(5, 15, 6, 1), g.clear_line(2, 2, 14, 14)))
def headphones_icon(g):
    g.rect(4, 2, 8, 2)
    g.rect(2, 4, 2, 8)
    g.rect(12, 4, 2, 8)
    g.rect(1, 8, 4, 6)
    g.rect(11, 8, 4, 6)
    g.rect(2, 10, 2, 2, 0)
    g.rect(12, 10, 2, 2, 0)

make("headphones", headphones_icon)
def headphones_off_icon(g):
    headphones_icon(g)
    g.clear_line(2, 2, 14, 14)

make("headphones-off", headphones_off_icon)
make("camera", lambda g: (g.frame(2, 5, 12, 8), g.rect(5, 3, 4, 2), g.rect(9, 7, 3, 3)))
make("screen", lambda g: (g.frame(2, 3, 12, 8), g.rect(7, 11, 2, 3), g.rect(4, 14, 8, 1)))
def phone_icon(g):
    for i in range(5):
        g.rect(2 + i * 2, 10 - i * 2, 4, 4)
    g.rect(1, 9, 3, 6)
    g.rect(10, 1, 6, 3)

make("phone", phone_icon)
def phone_off_icon(g):
    phone_icon(g)
    g.clear_line(2, 2, 14, 14)

make("phone-off", phone_off_icon)
make("gift", lambda g: (g.frame(2, 5, 12, 9), g.rect(7, 5, 2, 9), g.rect(2, 8, 12, 2), g.rect(4, 3, 3, 2), g.rect(9, 3, 3, 2)))
make("sticker", lambda g: (g.frame(2, 2, 11, 11), g.rect(10, 9, 4, 4), g.rect(11, 10, 2, 2, 0), g.rect(5, 5, 2, 2), g.rect(9, 5, 2, 2), g.rect(5, 9, 6, 1)))
make("emoji", lambda g: (g.circle(7.5, 7.5, 6), g.rect(5, 6, 2, 2), g.rect(9, 6, 2, 2), g.rect(4, 10, 8, 1), g.rect(5, 11, 6, 1)))
make("gif", lambda g: (g.frame(1, 3, 14, 10), g.text3x5("GIF", 2, 5)))
def attach_icon(g):
    g.line(9, 2, 4, 7)
    g.line(10, 3, 5, 8)
    g.line(4, 7, 7, 10)
    g.line(5, 8, 8, 11)
    g.rect(8, 11, 4, 2)
    g.rect(10, 9, 2, 4)
    g.rect(9, 2, 4, 2)

make("attach", attach_icon)
def send_icon(g):
    g.line(2, 13, 13, 2)
    g.line(3, 14, 13, 4)
    g.rect(11, 1, 4, 2)
    g.rect(13, 2, 2, 4)
    g.rect(3, 11, 2, 2)
    g.rect(4, 10, 2, 2)

make("send", send_icon)
def reply_icon(g):
    g.rect(2, 7, 9, 2)
    g.rect(2, 5, 2, 6)
    g.rect(4, 3, 2, 10)
    g.rect(11, 9, 2, 4)
    g.rect(9, 11, 2, 2)

make("reply", reply_icon)
make("react", lambda g: (g.circle(7, 8, 5), g.rect(5, 7, 2, 2), g.rect(9, 7, 2, 2), g.rect(4, 10, 6, 1), g.rect(12, 2, 2, 6), g.rect(10, 4, 6, 2)))
make("more", lambda g: (g.rect(2, 7, 3, 3), g.rect(6, 7, 3, 3), g.rect(10, 7, 3, 3)))
make("edit", lambda g: (g.line(3, 12, 11, 4), g.line(4, 13, 12, 5), g.rect(10, 3, 3, 3), g.rect(2, 13, 3, 2)))
make("trash", lambda g: (g.rect(3, 4, 10, 1), g.rect(4, 5, 8, 9), g.rect(6, 2, 4, 2), g.rect(7, 7, 1, 5), g.rect(9, 7, 1, 5)))
make("copy", lambda g: (g.frame(2, 2, 8, 8), g.frame(6, 6, 8, 8)))
make("link", lambda g: (g.frame(2, 4, 6, 8), g.frame(8, 4, 6, 8), g.rect(7, 7, 2, 2)))
make("download", lambda g: (g.rect(7, 2, 2, 8), g.rect(4, 8, 8, 2), g.rect(5, 10, 6, 2), g.rect(3, 14, 10, 2)))
make("plus", lambda g: (g.rect(7, 2, 2, 12), g.rect(2, 7, 12, 2)))
make("close", lambda g: (g.line(3, 3, 12, 12), g.line(4, 3, 13, 12), g.line(12, 3, 3, 12), g.line(13, 3, 4, 12)))
make("chevron-down", lambda g: (g.rect(4, 6, 2, 2), g.rect(6, 8, 2, 2), g.rect(8, 10, 2, 2), g.rect(10, 8, 2, 2), g.rect(12, 6, 2, 2)))
make("chevron-right", lambda g: (g.rect(6, 3, 2, 2), g.rect(8, 5, 2, 2), g.rect(10, 7, 2, 2), g.rect(8, 9, 2, 2), g.rect(6, 11, 2, 2)))
def arrow_left_icon(g):
    for i in range(4):
        g.rect(2 + i, 7 - i, 2, 2)
        g.rect(2 + i, 7 + i, 2, 2)
    g.rect(4, 7, 11, 2)

make("arrow-left", arrow_left_icon)
def arrow_right_icon(g):
    for i in range(4):
        g.rect(13 - i, 7 - i, 2, 2)
        g.rect(13 - i, 7 + i, 2, 2)
    g.rect(1, 7, 11, 2)

make("arrow-right", arrow_right_icon)
make("hash", lambda g: (g.rect(4, 2, 2, 12), g.rect(10, 2, 2, 12), g.rect(2, 5, 12, 2), g.rect(2, 10, 12, 2)))
make("volume", lambda g: (g.rect(2, 6, 3, 4), g.rect(5, 4, 2, 8), g.rect(7, 2, 2, 12), g.rect(11, 4, 2, 2), g.rect(13, 6, 2, 4), g.rect(11, 10, 2, 2)))
make("volume-mute", lambda g: (g.rect(2, 6, 3, 4), g.rect(5, 4, 2, 8), g.rect(7, 2, 2, 12), g.line(11, 5, 14, 11), g.line(14, 5, 11, 11)))
make("folder", lambda g: (g.rect(1, 4, 14, 10), g.rect(2, 2, 6, 2), g.rect(1, 3, 8, 2)))
make("compass", lambda g: (g.circle(7.5, 7.5, 6), g.rect(7, 4, 2, 8), g.rect(5, 7, 6, 2)))
make("home", lambda g: (g.rect(3, 7, 10, 7), g.rect(5, 3, 6, 2), g.rect(7, 1, 2, 2), g.rect(6, 11, 4, 3, 0), g.rect(7, 11, 2, 3)))
make("spark", lambda g: (g.rect(7, 1, 2, 14), g.rect(1, 7, 14, 2), g.rect(5, 5, 2, 2), g.rect(9, 5, 2, 2), g.rect(5, 9, 2, 2), g.rect(9, 9, 2, 2)))
make("shop", lambda g: (g.frame(3, 6, 10, 8), g.rect(4, 3, 8, 2), g.rect(5, 1, 2, 2), g.rect(9, 1, 2, 2), g.rect(6, 9, 4, 1)))
make("missions", lambda g: (g.rect(4, 2, 2, 12), g.rect(6, 2, 8, 6), g.rect(6, 4, 6, 2, 0), g.rect(6, 8, 6, 2)))
make("friends", lambda g: (g.circle(5, 5, 2), g.circle(11, 5, 2), g.rect(2, 8, 7, 6), g.rect(7, 8, 7, 6), g.rect(4, 10, 2, 2), g.rect(10, 10, 2, 2)))
make("shield", lambda g: (g.rect(3, 2, 10, 2), g.rect(2, 4, 12, 4), g.rect(3, 8, 10, 3), g.rect(5, 11, 6, 2), g.rect(7, 13, 2, 2)))
make("crown", lambda g: (g.rect(2, 6, 12, 2), g.rect(3, 8, 10, 4), g.rect(2, 3, 2, 4), g.rect(7, 2, 2, 5), g.rect(12, 3, 2, 4), g.rect(4, 12, 8, 2)))
make("bot", lambda g: (g.frame(2, 4, 12, 10), g.rect(5, 7, 2, 2), g.rect(9, 7, 2, 2), g.rect(5, 11, 6, 1), g.rect(7, 1, 2, 3), g.rect(1, 8, 1, 3), g.rect(14, 8, 1, 3)))
make("music", lambda g: (g.rect(9, 2, 2, 9), g.rect(4, 9, 7, 2), g.rect(4, 11, 3, 3), g.rect(9, 2, 5, 2)))
make("gamepad", lambda g: (g.frame(1, 5, 14, 8), g.rect(3, 7, 4, 2), g.rect(4, 6, 2, 4), g.rect(10, 7, 2, 2), g.rect(12, 9, 2, 2)))
make("clock", lambda g: (g.circle(7.5, 7.5, 6), g.rect(7, 4, 2, 5), g.rect(7, 7, 4, 2)))
make("user", lambda g: (g.circle(7.5, 5, 3), g.rect(3, 9, 10, 6), g.rect(5, 10, 6, 5)))
make("check", lambda g: (g.rect(3, 8, 2, 2), g.rect(5, 10, 2, 2), g.rect(7, 8, 2, 2), g.rect(9, 6, 2, 2), g.rect(11, 4, 2, 2)))
make("warning", lambda g: (g.rect(7, 2, 2, 2), g.rect(6, 4, 4, 2), g.rect(5, 6, 6, 2), g.rect(4, 8, 8, 2), g.rect(3, 10, 10, 2), g.rect(2, 12, 12, 2), g.rect(7, 6, 2, 4), g.rect(7, 11, 2, 2)))
make("info", lambda g: (g.circle(7.5, 7.5, 6), g.rect(7, 4, 2, 2), g.rect(7, 7, 2, 5)))
make("lock", lambda g: (g.frame(3, 7, 10, 7), g.rect(5, 3, 6, 2), g.rect(5, 5, 2, 3), g.rect(9, 5, 2, 3), g.rect(7, 9, 2, 3)))
make("diamond", lambda g: (g.rect(7, 2, 2, 2), g.rect(5, 4, 6, 2), g.rect(3, 6, 10, 2), g.rect(5, 8, 6, 2), g.rect(7, 10, 2, 2), g.rect(7, 12, 2, 2)))
make("dot", lambda g: g.rect(6, 6, 4, 4))


def announcement_icon(g):
    g.rect(2, 5, 8, 6)
    g.rect(4, 4, 4, 8)
    g.rect(10, 4, 2, 8)
    g.rect(12, 6, 2, 4)
    g.rect(5, 11, 2, 3)

make("announcement", announcement_icon)

def forum_icon(g):
    g.frame(2, 3, 9, 7)
    g.rect(4, 10, 3, 3)
    g.frame(8, 6, 6, 7)
    g.rect(9, 7, 4, 3)
    g.rect(10, 10, 4, 1)

make("forum", forum_icon)

def art(name, rows):
    g = Grid()
    for y, row in enumerate(rows):
        for x, bit in enumerate(row):
            if bit == "#":
                g.rect(x * 2, y * 2, 2, 2)
    g.save(name)

art("chat", [".######.", "#......#", "#.#..#.#", "#......#", ".######.", "..##....", ".#......", "........"])
art("more-vertical", ["...##...", "...##...", "........", "...##...", "...##...", "........", "...##...", "...##..."])
art("hash-lock", [".#.#....", "#####...", ".#.#....", "#####.#.", ".#.#.#.#", "....####", "....####", "....####"])
art("forward", ["....#...", "....##..", "#######.", "#...##..", "#...#...", "#.......", "#.......", "........"])
art("boost", ["...##...", "..####..", ".######.", "########", "..####..", "..####..", "..####..", "........"])
art("id", ["########", "#......#", "#.#.##.#", "#.#.#.##", "#.#.##.#", "#......#", "########", "........"])
art("calendar", [".#....#.", "########", "#......#", "#.#.#..#", "#......#", "#.#.#..#", "########", "........"])
art("browse", ["#####...", "........", "###.##..", "...#..#.", "##.#..#.", "....##..", "......#.", ".......#"])
art("book", ["#######.", "##....#.", "##.##.#.", "##....#.", "##....#.", "#######.", "##......", "#######."])
art("user-plus", ["..##....", ".####...", "..##....", "......#.", ".###.###", "#####.#.", "#####...", "........"])
art("trophy", ["########", ".######.", "#.####.#", ".######.", "..####..", "...##...", "...##...", ".######."])
art("flame", ["...#....", "..##....", "..###.#.", ".####.#.", ".######.", "########", ".######.", "..####.."])
art("external", ["..######", "......##", ".....#.#", "#...#..#", "#..#....", "#.#.....", "#.......", "#######."])
art("star", ["...##...", "...##...", "########", ".######.", "..####..", ".######.", ".##..##.", "##....##"])
art("plug", [".#....#.", ".#....#.", "########", "########", ".######.", "..####..", "...##...", "...##..."])
art("brush", ["......##", ".....###", "....###.", "...###..", "..###...", ".##.....", "###.....", "##......"])
art("cloud", ["........", "..###...", ".#####..", "#######.", "########", "########", ".######.", "........"])
art("sync", [".#####..", "#....#..", "#...###.", "#....#..", "..#....#", ".###...#", "..#....#", "..#####."])
art("wrench", [".....##.", "....##..", "....##.#", "...#####", "..###...", ".###....", "###.....", "##......"])
art("card", ["........", "########", "########", "#......#", "#.##...#", "#......#", "########", "........"])
art("globe", ["..####..", ".#.##.#.", "#..##..#", "########", "########", "#..##..#", ".#.##.#.", "..####.."])
art("code", ["........", "..#..#..", ".#....#.", "#......#", ".#....#.", "..#..#..", "........", "........"])
art("logout", ["#####...", "#.......", "#....#..", "#.######", "#....#..", "#.......", "#####...", "........"])
art("bookmark", [".######.", ".######.", ".######.", ".######.", ".######.", ".##..##.", ".#....#.", "........"])
art("apps", ["###.###.", "###.###.", "###.###.", "........", "###..#..", "###.###.", "###..#..", "........"])
art("unread", ["........", ".######.", ".#....#.", ".#.##.#.", ".#.##.#.", ".#....#.", ".######.", "........"])
art("flag", ["##......", "#######.", "#######.", "#######.", "#######.", "##......", "##......", "##......"])
art("chevron-up", ["........", "........", "...##...", "..####..", ".##..##.", "##....##", "........", "........"])
art("play", ["##......", "####....", "######..", "########", "########", "######..", "####....", "##......"])
art("poll", ["........", "##......", "##.####.", "........", "##......", "##.##...", "........", "........"])
art("eye", ["........", "..####..", ".#....#.", "#..##..#", "#..##..#", ".#....#.", "..####..", "........"])
art("status-online", ["########"] * 8)
art("status-idle", ["########", "#####...", "####....", "###.....", "###.....", "####....", "#####...", "########"])
art("status-dnd", ["########", "########", "########", "#......#", "#......#", "########", "########", "########"])
art("status-offline", ["########", "########", "##....##", "##....##", "##....##", "##....##", "########", "########"])
art("status-streaming", ["##......", "####....", "######..", "########", "########", "######..", "####....", "##......"])
art("status-mobile", [".######.", ".#....#.", ".#....#.", ".#....#.", ".#....#.", ".######.", ".##..##.", ".######."])
art("signal-3", ["......##", "......##", "...##.##", "...##.##", "##.##.##", "##.##.##", "##.##.##", "##.##.##"])
art("signal-2", ["........", "........", "...##...", "...##...", "##.##...", "##.##...", "##.##.##", "##.##.##"])
art("signal-1", ["........", "........", "........", "........", "##......", "##......", "##.##.##", "##.##.##"])
art("signal-0", ["#.#.....", ".#......", "#.#.....", "........", "........", "........", "##.##.##", "##.##.##"])

def bell_off_icon(g):
    g.rect(6, 2, 4, 2)
    g.rect(4, 4, 8, 2)
    g.rect(3, 6, 10, 6)
    g.rect(2, 12, 12, 2)
    g.rect(7, 14, 2, 2)
    for shift in (-1, 0, 1, 2):
        g.clear_line(1 + shift, 1, 14 + shift, 14)
    g.line(1, 1, 14, 14)

make("bell-off", bell_off_icon)

print(f"generated {len(list(OUT.glob('*.svg')))} icons in {OUT}")
