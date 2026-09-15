#!/usr/bin/env python3
"""Build the public site at ../../bigfoot200-training/ from this repo's plan + data.

  index.html   today / this week / race ladder   <- template.html + plan/schedule.json
  log.html     training log + charts             <- ../tracker/template.html + weeks.json
  blocks.html  block targets and monitors        <- ../plan/block-targets.md
  plan.html    the sub-100 race plan             <- ../plan/sub100-plan.md
  weeks.html   every week, plan vs actual        <- schedule.json + weekly-actuals.json

DELIBERATELY NOT PUBLISHED: anything under plan/private/ — Destination Trail's
copyrighted runner manual lives there. It is gitignored and never rendered.
"""
import json, os, re, sys
import md, nav, doc_shell

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
OUT  = os.environ.get("BF_OUT") or os.path.join(os.path.dirname(REPO), "bigfoot200-training")

NEVER_PUBLISH = ("runner-manual",)

def guard_source():
    """Refuse to build if a NEVER_PUBLISH file is tracked in the source repo.

    plan/private/ is the one place these may live: it is gitignored. Anywhere
    else means a copy got committed, and this repo is meant to be public.
    """
    import subprocess
    try:
        tracked = subprocess.check_output(
            ["git", "-C", REPO, "ls-files"], stderr=subprocess.DEVNULL
        ).decode("utf-8", "replace").splitlines()
    except Exception:
        return                      # not a git checkout; nothing to police
    bad = [f for f in tracked
           if any(b in f.lower() for b in NEVER_PUBLISH)
           and not f.startswith("plan/private/")]
    if bad:
        sys.exit("REFUSING: copyrighted file(s) tracked in the source repo, "
                 "which is meant to be public: %s\n"
                 "  git rm --cached %s   (and purge it from history before "
                 "making the repo public)" % (bad, " ".join(bad)))


def read(*p):
    return open(os.path.join(REPO, *p), encoding="utf-8").read()

def write(name, html):
    for bad in NEVER_PUBLISH:
        if bad in html.lower() and name != "index.html":
            pass  # a passing mention is fine; the file itself is simply never read
    html = nav.inject(html, name)
    open(os.path.join(OUT, name), "w", encoding="utf-8").write(html)
    print("  %-12s %6d bytes" % (name, len(html)))

def inject_schedule_js(tpl):
    """Both page templates include dashboard/schedule_logic.js verbatim, so the
    Today page and the Every week page share one definition of what a day is."""
    if "/*__SCHEDULE_JS__*/" not in tpl:
        return tpl
    return tpl.replace("/*__SCHEDULE_JS__*/", read("dashboard", "schedule_logic.js"))


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

def odds_pill():
    """The finish-odds chip in the header. Empty if the model hasn't run yet."""
    path = os.path.join(REPO, "plan", "odds.json")
    if not os.path.exists(path):
        return ""
    o = json.load(open(path, encoding="utf-8"))
    t = o["trajectory"]
    return ('<a class="odds" href="progress.html" title="Chance of finishing on '
            'current trajectory, %d weeks out. %s. Tap for the breakdown.">'
            '<span class="dot" style="background:%s"></span>'
            '<span class="pct">%d\u2013%d%%</span>'
            '<span class="word">finish odds</span></a>'
            % (o["weeksToRace"], o["baseNote"].replace('"', "'"),
               o["color"], t["low"], t["high"]))


def main():
    guard_source()
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
    today_tpl = inject_schedule_js(read("dashboard", "template.html"))
    if "<!--__PLAN__-->" not in today_tpl:
        sys.exit("dashboard/template.html has no <!--__PLAN__--> token")
    today_tpl = today_tpl.replace("<!--__PLAN__-->", plan_html)
    today_tpl = today_tpl.replace("<!--__ODDS__-->", odds_pill())
    write("index.html",  inject_data(today_tpl, schedule, "dashboard/template.html"))
    write("log.html",    inject_data(read("tracker", "template.html"), weeks, "tracker/template.html"))
    # Every week: the whole campaign, plan against actual, one row per week.
    weeks_tpl = inject_schedule_js(read("dashboard", "weeks_template.html"))
    ap = os.path.join(REPO, "plan", "weekly-actuals.json")
    actuals = json.loads(open(ap, encoding="utf-8").read()) if os.path.exists(ap) else {}
    dp = os.path.join(REPO, "plan", "daily-actuals.json")
    daily = json.loads(open(dp, encoding="utf-8").read()) if os.path.exists(dp) else {}
    if not daily:
        print("  daily-actuals.json missing - day rows will show the plan only")
    write("weeks.html", inject_data(weeks_tpl, {
        "blocks": schedule["blocks"], "longDays": schedule.get("longDays", []),
        "races": schedule["races"], "race": schedule["race"], "actuals": actuals,
        "daily": daily,
    }, "dashboard/weeks_template.html"))

    if os.path.exists(os.path.join(REPO, "plan", "progress.md")):
        write("progress.html", md_page("progress.md", "Week over week"))
    else:
        print("  progress.md missing - run: python3 tracker/weekly_report.py")
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
