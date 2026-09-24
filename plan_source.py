"""Where the plan comes from.

Until 2026-09-24 the plan lived in plan/schedule.json and plan/odds.json in this
repo. It now lives in Supabase, so it can be changed from any device — by Claude,
or from the training page — without anyone editing a file or running a build.

This module fetches it and hands build.py the same shape schedule.json had, so
nothing downstream had to change.

The endpoint is a public, read-only Supabase edge function. It needs no key and
returns only plan data plus the aggregated weekly view — never raw activity or
Garmin rows. Standard library only: the rebuild workflow runs with no pip install.

If the fetch fails, the build falls back to the frozen JSON files and says so
loudly rather than publishing a half-built page.
"""

import json
import os
import sys
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
        sched_path = os.path.join(repo_root, "plan", "schedule.json")
        odds_path = os.path.join(repo_root, "plan", "odds.json")
        if not os.path.exists(sched_path):
            sys.exit("REFUSING: could not reach %s (%s) and there is no local "
                     "plan/schedule.json to fall back to." % (PLAN_URL, e))
        print("  WARNING: could not reach the plan endpoint (%s)." % e)
        print("  WARNING: falling back to the FROZEN plan/schedule.json — this site")
        print("  WARNING: will not show anything changed in Supabase since 2026-09-24.")
        schedule = json.loads(open(sched_path, encoding="utf-8").read())
        schedule.pop("_source", None)
        odds = (json.loads(open(odds_path, encoding="utf-8").read())
                if os.path.exists(odds_path) else {})
        return schedule, odds
