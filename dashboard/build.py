#!/usr/bin/env python3
"""Build the public site at ../../bigfoot200-training/ from this repo's plan + data.

  index.html   today / this week / race ladder   <- template.html + plan/schedule.json
  log.html     training log + charts             <- ../tracker/template.html + weeks.json
  blocks.html  block targets and monitors        <- ../plan/block-targets.md
  plan.html    the sub-100 race plan             <- ../plan/sub100-plan.md

DELIBERATELY NOT PUBLISHED: anything under plan/private/ — Destination Trail's
copyrighted runner manual lives there. It is gitignored and never rendered.
"""
import json, os, re, sys
import md, nav, doc_shell

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
OUT  = os.path.join(os.path.dirname(REPO), "bigfoot200-training")

NEVER_PUBLISH = ("runner-manual",)

def read(*p):
    return open(os.path.join(REPO, *p), encoding="utf-8").read()

def write(name, html):
    for bad in NEVER_PUBLISH:
        if bad in html.lower() and name != "index.html":
            pass  # a passing mention is fine; the file itself is simply never read
    html = nav.inject(html, name)
    open(os.path.join(OUT, name), "w", encoding="utf-8").write(html)
    print("  %-12s %6d bytes" % (name, len(html)))

def inject_data(tpl, data, where):
    if "/*__DATA__*/" not in tpl:
        sys.exit("%s has no /*__DATA__*/ token" % where)
    return tpl.replace("/*__DATA__*/", json.dumps(data, ensure_ascii=False,
                                                  separators=(",", ":")))

def md_body(src):
    """Render a plan markdown file to an HTML fragment (stdlib only — see md.py)."""
    return md.render(read("plan", src))

def md_page(src, title):
    return doc_shell.render(title, md_body(src), "plan/" + src)

def main():
    if not os.path.isdir(OUT):
        sys.exit("sibling repo not found: %s\n  git -C %s clone "
                 "https://github.com/pbrandipdx/bigfoot200-training.git"
                 % (OUT, os.path.dirname(OUT)))

    schedule = json.loads(read("plan", "schedule.json"))
    schedule.pop("_source", None)
    weeks = json.loads(read("tracker", "weeks.json"))

    print("building %s" % OUT)

    # the Today page carries the full training plan inline, after the race ladder
    plan_html = md_body("block-targets.md")
    today_tpl = read("dashboard", "template.html")
    if "<!--__PLAN__-->" not in today_tpl:
        sys.exit("dashboard/template.html has no <!--__PLAN__--> token")
    today_tpl = today_tpl.replace("<!--__PLAN__-->", plan_html)
    write("index.html",  inject_data(today_tpl, schedule, "dashboard/template.html"))
    write("log.html",    inject_data(read("tracker", "template.html"), weeks, "tracker/template.html"))
    write("blocks.html", md_page("block-targets.md", "Block targets"))
    write("plan.html",   md_page("sub100-plan.md",  "Race plan"))

    leaked = [f for f in os.listdir(OUT)
              if any(b in f.lower() for b in NEVER_PUBLISH)]
    if leaked:
        sys.exit("REFUSING: private file(s) present in the public repo: %s" % leaked)

    print("\n%d blocks, %d races, %d logged weeks" %
          (len(schedule["blocks"]), len(schedule["races"]), len(weeks["weeks"])))
    print("push:  cd ../bigfoot200-training && git add -A && "
          "git commit -m 'Regenerate from bigfoot-200' && git push")

if __name__ == "__main__":
    main()
