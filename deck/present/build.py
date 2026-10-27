"""Build the coded presenter (present/index.html) from the deck's slide files.

usage: python build.py <slides_dir> <wildlife_override> <blobmap.json> <deck_root>
Writes present/index.html and copies the images it needs into present/assets/.
"""
import json
import os
import re
import shutil
import sys

ORDER = ["cover", "where", "habitat", "wildlife", "foodchain", "snowleopard",
         "condor", "threats", "protect", "summit", "thanks"]

slides_dir, wildlife, blobmap_path, deck_root = sys.argv[1:5]
here = os.path.dirname(os.path.abspath(__file__))
blobmap = json.load(open(blobmap_path))
os.makedirs(os.path.join(here, "assets"), exist_ok=True)

sections, notes, bases = [], [], []
for sid in ORDER:
    path = wildlife if sid == "wildlife" else os.path.join(slides_dir, sid + ".html")
    html = open(path, encoding="utf-8").read().strip()

    def swap(m):
        src = blobmap[m.group(1)]
        name = os.path.basename(src)
        shutil.copyfile(os.path.join(deck_root, src), os.path.join(here, "assets", name))
        return "assets/" + name

    html = re.sub(r"/_blob/([0-9a-f]{32})", swap, html)
    aside = re.search(r"<aside>([\s\S]*?)</aside>", html)
    notes.append(aside.group(1).strip() if aside else "")
    html = re.sub(r"\s*<aside>[\s\S]*?</aside>", "", html)
    # the slide's own ground colour drives the transition's gradient
    bg = re.search(r"<section[^>]*?background:\s*(#[0-9a-fA-F]{6})", html)
    bases.append(bg.group(1) if bg else "#0e1c26")
    html = html.replace("<section ", f'<section data-i="{len(sections)}" ', 1)
    sections.append(html)

template = open(os.path.join(here, "template.html"), encoding="utf-8").read()
out = (template
       .replace("<!--SLIDES-->", "\n".join(sections))
       .replace("/*NOTES*/[]", json.dumps(notes, ensure_ascii=False))
       .replace("/*BASES*/[]", json.dumps(bases)))
open(os.path.join(here, "index.html"), "w", encoding="utf-8").write(out)
print("built", len(sections), "slides", bases)
