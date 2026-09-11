#!/usr/bin/env python3
"""Generate the public phone dashboard from plan/schedule.json.

Writes ../bigfoot200-training/index.html. That repo is a VIEW — never edit its
index.html directly, it is overwritten from here.
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
OUT  = os.path.join(os.path.dirname(REPO), "bigfoot200-training", "index.html")

data = json.load(open(os.path.join(REPO, "plan", "schedule.json")))
data.pop("_source", None)
tpl = open(os.path.join(HERE, "template.html")).read()

if "/*__DATA__*/" not in tpl:
    sys.exit("template.html has no /*__DATA__*/ token")

out = tpl.replace("/*__DATA__*/", json.dumps(data, ensure_ascii=False, separators=(",", ":")))

if not os.path.isdir(os.path.dirname(OUT)):
    sys.exit(f"sibling repo not found: {os.path.dirname(OUT)}\n"
             f"clone it:  git -C {os.path.dirname(os.path.dirname(OUT))} clone "
             f"https://github.com/pbrandipdx/bigfoot200-training.git")

open(OUT, "w").write(out)
print(f"built {OUT} ({len(out)} bytes, {len(data['blocks'])} blocks, {len(data['races'])} races)")
print("now: cd ../bigfoot200-training && git add -A && git commit -m 'Regenerate from bigfoot-200' && git push")
