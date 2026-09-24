#!/usr/bin/env python3
"""Build the public site at ../../bigfoot200-training/ from this repo's plan + data.

  index.html   today / this week / race ladder   <- template.html + Supabase plan feed
  log.html     training log + charts             <- ../tracker/template.html + weeks.json
  blocks.html  block targets and monitors        <- ../plan/block-targets.md
  plan.html    the sub-100 race plan             <- ../plan/sub100-plan.md
  weeks.html   every week, plan vs actual        <- Supabase plan feed + weekly-actuals.json

DELIBERATELY NOT PUBLISHED: anything under plan/private/ — Destination Trail's
copyrighted runner manual lives there. It is gitignored and never rendered.
"""
import datetime
import json, os, re, sys
import md, nav, doc_shell

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
OUT  = os.environ.get("BF_OUT") or os.path.join(os.path.dirname(REPO), "bigfoot200-training")

# ---------------------------------------------------------------------------
# Where the plan comes from.
#
# Until 2026-09-24 the plan lived in plan/schedule.json and plan/odds.json.
# It now lives in Supabase so it can be changed from any device - by Claude, or
# from the training page - without editing a file or running a build. This
# section fetches it and hands the rest of this script the same shape
# schedule.json had, so nothing below had to change.
#
# The endpoint is a public, read-only Supabase edge function: no key, and it
# returns only plan data plus the aggregated weekly view, never raw activity or
# Garmin rows. Standard library only - the rebuild workflow runs no pip install.
# ---------------------------------------------------------------------------
import urllib.error
import urllib.request

PLAN_URL = os.environ.get(
    "BIGFOOT_PLAN_URL",
    "https://mwjprmuwdhfjlldrruhx.supabase.co/functions/v1/plan",
)
TIMEOUT = 20


def _fmt_ft(n):
    return "%s ft" % format(int(n), ",") if n is not None else ""


def _fmt_hours(n):
    if n is None:
        return ""
    n = float(n)
    return "%g hr/wk" % (int(n) if n == int(n) else n)


def _to_legacy(feed):
    """Map the Supabase payload onto the shape build.py already expects."""
    settings = feed.get("settings") or {}
    race = dict(settings.get("race") or {})

    blocks = []
    for b in feed.get("blocks") or []:
        blocks.append({
            "id": b["block_no"],
            "name": b["name"],
            "start": b["start_date"],
            "end": b["end_date"],
            "vert": _fmt_ft(b.get("vert_ft_per_week")),
            "hours": _fmt_hours(b.get("hours_per_week")),
            "endsWith": b.get("ends_with") or "",
            "targets": {
                "hoursPerWeek": b.get("hours_per_week"),
                "vertFtPerWeek": b.get("vert_ft_per_week"),
                "milesPerWeek": b.get("miles_per_week"),
                "peakDayHours": b.get("peak_day_hours"),
                "volumeDayCapHours": b.get("volume_day_cap_hours"),
                "nightHoursCumulative": b.get("night_hours_cumulative"),
            },
            **({"taper": True} if b.get("is_taper") else {}),
        })

    races = []
    for r in feed.get("races") or []:
        row = {
            "name": r["name"],
            "start": r["race_date"],
            "end": r.get("end_date") or r["race_date"],
            "tag": r.get("tag") or "",
            "taperDays": r.get("taper_days"),
            "recoveryDays": r.get("recovery_days"),
        }
        for src, dst in (("signup_url", "signup"), ("signup_label", "signupLabel"),
                         ("signup_status", "signupStatus"), ("signup_note", "signupNote")):
            if r.get(src):
                row[dst] = r[src]
        races.append(row)

    long_days = []
    for l in feed.get("long_days") or []:
        row = {
            "date": l["day_date"],
            "title": l["title"],
            "vert": l.get("vert_desc") or "",
            "desc": l.get("description") or "",
        }
        if l.get("url"):
            row["link"] = l["url"]
        if l.get("url_label"):
            row["linkLabel"] = l["url_label"]
        # status is new — the site shows it so a missed long day is visible
        if l.get("status") and l["status"] != "planned":
            row["status"] = l["status"]
        if l.get("actual_note"):
            row["statusNote"] = l["actual_note"]
        long_days.append(row)

    decisions = [{
        "date": d["decision_date"],
        "kind": d.get("kind") or "hard",
        "title": d["title"],
        "body": d.get("body") or "",
    } for d in feed.get("decisions") or [] if d.get("status") != "na"]

    schedule = {
        "_source": "Supabase (plan_* tables) via %s" % PLAN_URL,
        "race": race,
        "blocks": blocks,
        "races": races,
        "longDays": long_days,
        "decisions": decisions,
    }
    return schedule, (settings.get("odds") or {})


def fetch_plan(repo_root):
    """Return (schedule, odds). Falls back to the frozen JSON on any failure."""
    try:
        req = urllib.request.Request(PLAN_URL, headers={"Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            feed = json.loads(resp.read().decode("utf-8"))
        if not feed.get("blocks"):
            raise ValueError("feed carried no blocks")
        schedule, odds = _to_legacy(feed)
        print("  plan: Supabase, %d blocks / %d races / %d long days"
              % (len(schedule["blocks"]), len(schedule["races"]), len(schedule["longDays"])))
        return schedule, odds
    except (urllib.error.URLError, ValueError, KeyError, TimeoutError, OSError) as e:
        # Deliberately no fallback to plan/schedule.json. That file is frozen at
        # 2026-09-24 and still lists Gorge Waterfalls 100K, so building from it
        # would quietly republish a plan that is no longer true. Failing leaves
        # the last good site in place, which is the better wrong answer.
        sys.exit(
            "REFUSING: could not reach the plan endpoint.\n"
            "  %s\n"
            "  %s\n"
            "  The plan lives in Supabase; plan/schedule.json is frozen and would\n"
            "  republish a stale race ladder. Leaving the published site as it is.\n"
            "  Check the project is not paused, then re-run this workflow."
            % (PLAN_URL, e))

# ---------------------------------------------------------------------------

BLOCK_QUESTIONS = {
    1: "Can you sustain a full day on feet and descend hard without wrecking your quads?",
    2: "Can you go out again on tired legs, in bad weather, when nothing about it is enjoyable?",
    3: "Can you move competently in the dark for six hours, and clear a 17-hour cutoff?",
    4: "Can you go a hundred miles, controlled, with aid under 90 minutes? Sub-100 at Bigfoot is decided here.",
    5: "Recover, peak once, then arrive fresh with sleep banked and heat in the legs.",
}

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

def odds_pill(o):
    """The finish-odds chip in the header. Empty if the model hasn't run yet."""
    if not o or not o.get("trajectory"):
        return ""
    t = o["trajectory"]
    return ('<a class="odds" href="progress.html" title="Chance of finishing on '
            'current trajectory, %d weeks out. %s. Tap for the breakdown.">'
            '<span class="dot" style="background:%s"></span>'
            '<span class="pct">%d\u2013%d%%</span>'
            '<span class="word">finish odds</span></a>'
            % (o["weeksToRace"], o["baseNote"].replace('"', "'"),
               o.get("color", "#5C6B58"), t["low"], t["high"]))


def main():
    guard_source()
    if not os.path.isdir(OUT):
        sys.exit("sibling repo not found: %s\n  git -C %s clone "
                 "https://github.com/pbrandipdx/bigfoot200-training.git"
                 % (OUT, os.path.dirname(OUT)))

    schedule, odds = fetch_plan(REPO)
    schedule.pop("_source", None)
    weeks = json.loads(read("tracker", "weeks.json"))

    # block-targets.md carries a hand-written section per block, and schedule.json
    # carries the numbers the site renders. On 2026-09-15 they disagreed for an
    # hour - the doc's header said 9 blocks and 2028 while its body still
    # described 5 blocks ending at Bigfoot 2027, and it was live that way. Fail
    # the build rather than publish two answers to the same question.
    bt = read("plan", "block-targets.md")
    missing = [b["name"] for b in schedule["blocks"]
               if ("## " + b["name"]) not in bt]
    if missing:
        sys.exit("REFUSING: plan/block-targets.md has no section for: %s\n"
                 "  schedule.json defines %d blocks; the doc must describe all of them."
                 % (", ".join(missing), len(schedule["blocks"])))
    stale = [b["name"] for b in schedule["blocks"]
             if b["endsWith"].split("—")[0].strip() and
             b["endsWith"].split("—")[0].strip() not in bt]
    if stale:
        print("  WARNING: block-targets.md may not mention what these blocks end with: %s"
              % ", ".join(stale))

    # The race date used to be typed into three page templates and a JS
    # constant. When it moved to 2028 the pages kept saying "Aug 13, 2027" and
    # the Log page went on counting weeks to it, so the site showed three
    # different answers at once. One source now, substituted here.
    _rd = datetime.date.fromisoformat(schedule["race"]["date"])
    RACE_LABEL = _rd.strftime("%b %-d, %Y") + (
        " (est.)" if schedule["race"].get("dateEstimated") else "")
    RACE_SUB = "Mount St. Helens, WA &middot; %s &middot; goal: %s" % (
        RACE_LABEL, schedule["race"]["goal"])

    # The Log page carried its own hardcoded copy of the block plan and it had
    # drifted to pre-rescale numbers. Build both structures it needs from
    # schedule.json so there is one source.
    _base = datetime.date.fromisoformat(schedule["blocks"][0]["start"])
    _log_blocks, _log_display = [], {}
    for _b in schedule["blocks"]:
        _s = datetime.date.fromisoformat(_b["start"])
        _e = datetime.date.fromisoformat(_b["end"])
        _t = _b["targets"]
        _log_blocks.append({
            "n": _b["id"],
            "start": (_s - _base).days // 7,
            "end": (_e - _base).days // 7,
            "ends": _b["endsWith"],
            "peak": [_t["peakDayHours"], _t["peakDayHours"]],
            "nightCum": _t["nightHoursCumulative"],
            "q": BLOCK_QUESTIONS.get(_b["id"], ""),
        })
        _log_display[str(_b["id"])] = {
            "h": str(_t["hoursPerWeek"]),
            "v": "{:,}".format(_t["vertFtPerWeek"]),
            "m": str(_t["milesPerWeek"]),
        }

    def race_tokens(html):
        return (html.replace("<!--__RACE_SUB__-->", RACE_SUB)
                    .replace("<!--__RACE_DATE__-->", RACE_LABEL)
                    .replace("/*__RACE_UTC__*/", "%d, %d, %d" % (_rd.year, _rd.month - 1, _rd.day))
                    .replace("/*__RACE_LABEL__*/", RACE_LABEL)
                    .replace("/*__BLOCKS__*/", json.dumps(_log_blocks, ensure_ascii=False))
                    .replace("/*__BLOCK_DISPLAY__*/", json.dumps(_log_display, ensure_ascii=False)))

    print("building %s" % OUT)

    # the Today page carries the full training plan inline, after the race ladder
    plan_html = md_body("block-targets.md")
    today_tpl = inject_schedule_js(read("dashboard", "template.html"))
    if "<!--__PLAN__-->" not in today_tpl:
        sys.exit("dashboard/template.html has no <!--__PLAN__--> token")
    today_tpl = today_tpl.replace("<!--__PLAN__-->", plan_html)
    today_tpl = today_tpl.replace("<!--__ODDS__-->", odds_pill(odds))
    write("index.html",  race_tokens(inject_data(today_tpl, schedule, "dashboard/template.html")))
    write("log.html",    race_tokens(inject_data(read("tracker", "template.html"), weeks, "tracker/template.html")))
    # Every week: the whole campaign, plan against actual, one row per week.
    weeks_tpl = inject_schedule_js(read("dashboard", "weeks_template.html"))
    ap = os.path.join(REPO, "plan", "weekly-actuals.json")
    actuals = json.loads(open(ap, encoding="utf-8").read()) if os.path.exists(ap) else {}
    dp = os.path.join(REPO, "plan", "daily-actuals.json")
    daily = json.loads(open(dp, encoding="utf-8").read()) if os.path.exists(dp) else {}
    if not daily:
        print("  daily-actuals.json missing - day rows will show the plan only")
    write("weeks.html", race_tokens(inject_data(weeks_tpl, {
        "blocks": schedule["blocks"], "longDays": schedule.get("longDays", []),
        "races": schedule["races"], "race": schedule["race"], "actuals": actuals,
        "decisions": schedule.get("decisions", []),
        "daily": daily,
    }, "dashboard/weeks_template.html")))

    if os.path.exists(os.path.join(REPO, "plan", "progress.md")):
        write("progress.html", md_page("progress.md", "Week over week"))
    else:
        print("  progress.md missing - run: python3 tracker/weekly_report.py")
    write("blocks.html", md_page("block-targets.md", "Block targets"))
    write("plan.html",   md_page("sub100-plan.md",  "Race plan"))

    # A page that prints the race date must print the current one. A stale
    # hardcode shows up as the label being absent, which is what happened on
    # 2026-09-15 and was live on three pages.
    for page in ("index.html", "weeks.html", "log.html"):
        body = open(os.path.join(OUT, page), encoding="utf-8").read()
        if RACE_LABEL not in body:
            sys.exit("REFUSING: %s does not show the race date %s. Something is "
                     "still hardcoded." % (page, RACE_LABEL))

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
