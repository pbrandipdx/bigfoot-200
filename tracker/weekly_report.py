#!/usr/bin/env python3
"""Week-over-week progress report.

Reads the weekly_progress view from Supabase and writes plan/progress.md.
Stdlib only, same as dashboard/md.py, so it runs on any machine with the repo.

  python3 tracker/weekly_report.py            # last 12 weeks
  python3 tracker/weekly_report.py 26         # last 26 weeks

Credentials come from tracker/.env (gitignored):
  SUPABASE_URL, SUPABASE_SERVICE_KEY
"""
import json, os, sys, urllib.request, urllib.parse, datetime
import odds as odds_model

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
OUT  = os.path.join(REPO, "plan", "progress.md")
ODDS = os.path.join(REPO, "plan", "odds.json")

# Block 1 targets, from plan/block-targets.md. Keep these in step with that file.
TARGET = {"hours": 12.0, "vert_ft": 3500, "miles": 45.0, "peak_day_hr": 8.0}

# Patrick's own monitor rules, from plan/block-targets.md.
HRV_BASELINE = 41.6      # 90-day baseline at the time the plan was written
HRV_DROP_PCT = 10.0      # ">10% below baseline: cut volume 30% that week"


def env():
    path = os.path.join(HERE, ".env")
    if not os.path.exists(path):
        sys.exit("no tracker/.env — copy tracker/.env.example and fill it in")
    out = {}
    for line in open(path, encoding="utf-8"):
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        out[k.strip()] = v.strip().strip('"').strip("'")
    for k in ("SUPABASE_URL", "SUPABASE_SERVICE_KEY"):
        if not out.get(k):
            sys.exit("tracker/.env is missing %s" % k)
    return out


def fetch(cfg, weeks):
    url = cfg["SUPABASE_URL"].rstrip("/") + "/rest/v1/weekly_progress?" + \
        urllib.parse.urlencode({"select": "*", "order": "week_start.desc",
                                "limit": str(weeks)})
    req = urllib.request.Request(url, headers={
        "apikey": cfg["SUPABASE_SERVICE_KEY"],
        "Authorization": "Bearer " + cfg["SUPABASE_SERVICE_KEY"],
        "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def num(v):
    if v is None or v == "":
        return None
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def cell(v, fmt="%s"):
    return "—" if v is None else fmt % v


def arrow(now, prev, higher_is_better=True, flat=0.03):
    """Week-over-week marker as a {{trend}} token; md.py renders it as a
    coloured arrow. flat = fraction inside which we call it level."""
    if now is None or prev in (None, 0):
        return ""
    d = (now - prev) / abs(prev)
    if abs(d) < flat:
        return " {{level}}"
    up = d > 0
    good = up == higher_is_better
    return " {{%s%s}}" % ("up" if up else "down", "" if good else "-bad")


def pct(now, target):
    return "—" if now is None else "%d%%" % round(100.0 * now / target)


def main():
    weeks = int(sys.argv[1]) if len(sys.argv) > 1 else 12
    # the odds model wants 12 complete weeks of history regardless of how many
    # the table is asked to show
    all_rows = fetch(env(), max(weeks + 1, 14))
    if not all_rows:
        sys.exit("weekly_progress returned no rows")

    for r in all_rows:
        for k in ("hours", "miles", "vert_ft", "longest_day_hr", "night_hours",
                  "run_hours", "run_miles", "run_vert_ft", "hrv_avg", "rhr_avg",
                  "sleep_avg", "readiness_avg", "endurance", "hill",
                  "run_tolerance"):
            r[k] = num(r.get(k))
    rows = all_rows[:weeks + 1]

    schedule = json.load(open(os.path.join(REPO, "plan", "schedule.json"),
                              encoding="utf-8"))
    today = datetime.date.today()
    this_monday = today - datetime.timedelta(days=today.weekday())
    # The current week is still being written; report on it but mark it partial.
    L = []
    L.append("# Week over week")
    L.append("")
    L.append("Generated %s from Supabase `weekly_progress` "
             "(activities + garmin_daily + garmin_training, Monday-start weeks, "
             "America/Los_Angeles)." % today.isoformat())
    L.append("")
    L.append("Arrows compare with the previous week. "
             "{{up}} and {{down}} are moving the way you want, "
             "{{up-bad}} and {{down-bad}} the wrong way, "
             "{{level}} is unchanged. Hover any arrow for what it means.")
    L.append("")

    # ---- finish odds ---------------------------------------------------------
    odds_md, odds_data = odds_model.report(all_rows, schedule["blocks"], today)
    if odds_md:
        L.append(odds_md)
        json.dump(odds_data, open(ODDS, "w", encoding="utf-8"), indent=2)
        print("wrote %s (%d-%d%% on trajectory)"
              % (ODDS, odds_data["trajectory"]["low"],
                 odds_data["trajectory"]["high"]))

    # ---- headline: last complete week vs the one before it -------------------
    done = [r for r in rows if r["week_start"] != this_monday.isoformat()]
    if len(done) >= 2:
        a, b = done[0], done[1]
        L.append("## Last complete week — %s" % a["week_start"])
        L.append("")
        L.append("| | This week | Prior week | Block 1 target | At target |")
        L.append("|---|---|---|---|---|")
        for label, key, tgt, better in (
                ("Hours", "hours", TARGET["hours"], True),
                ("Miles", "miles", TARGET["miles"], True),
                ("Vert (ft)", "vert_ft", TARGET["vert_ft"], True),
                ("Longest day (hr)", "longest_day_hr", TARGET["peak_day_hr"], True)):
            L.append("| %s | %s%s | %s | %s | %s |" % (
                label, cell(a[key], "%g"), arrow(a[key], b[key], better),
                cell(b[key], "%g"), ("%g" % tgt), pct(a[key], tgt)))
        L.append("| Running miles | %s%s | %s | — | — |" % (
            cell(a["run_miles"], "%g"), arrow(a["run_miles"], b["run_miles"]),
            cell(b["run_miles"], "%g")))
        L.append("| HRV avg | %s%s | %s | %g baseline | %s |" % (
            cell(a["hrv_avg"], "%g"), arrow(a["hrv_avg"], b["hrv_avg"]),
            cell(b["hrv_avg"], "%g"), HRV_BASELINE, pct(a["hrv_avg"], HRV_BASELINE)))
        L.append("| Resting HR | %s%s | %s | — | — |" % (
            cell(a["rhr_avg"], "%g"), arrow(a["rhr_avg"], b["rhr_avg"], False),
            cell(b["rhr_avg"], "%g")))
        L.append("| Endurance score | %s%s | %s | — | — |" % (
            cell(a["endurance"], "%d"), arrow(a["endurance"], b["endurance"], True, 0.005),
            cell(b["endurance"], "%d")))
        L.append("")

        # ---- the three rules that actually change what he does next week ----
        flags = []
        if a["hrv_avg"] is not None:
            drop = 100.0 * (HRV_BASELINE - a["hrv_avg"]) / HRV_BASELINE
            if drop > HRV_DROP_PCT:
                flags.append("**HRV rule fires.** 7-day avg %.1f is %.1f%% below the "
                             "%g baseline, past the 10%% line. Cut next week's volume "
                             "30%%." % (a["hrv_avg"], drop, HRV_BASELINE))
        if a["miles"] and a["run_miles"] is not None:
            share = 100.0 * a["run_miles"] / a["miles"]
            if share < 25:
                flags.append("**Running share %.0f%%** (%g of %g miles). The Saturdays "
                             "are hikes. Run the runnable grades or the run-specific "
                             "fitness keeps sliding." % (share, a["run_miles"], a["miles"]))
        if len(done) >= 4 and all(r["endurance"] is not None for r in done[:4]):
            e = [r["endurance"] for r in done[:4]]
            if e[0] < e[3]:
                flags.append("**Endurance score down %d over 4 weeks** (%d -> %d). "
                             "Volume is not converting into aerobic fitness yet."
                             % (e[3] - e[0], e[3], e[0]))
        if a["hours"] is not None and a["hours"] < 0.8 * TARGET["hours"]:
            flags.append("**Under 80%% of the hour target** (%g vs %g). One more "
                         "midweek session, not a bigger Saturday."
                         % (a["hours"], TARGET["hours"]))
        if flags:
            L.append("### What this changes")
            L.append("")
            for f in flags:
                L.append("- " + f)
            L.append("")
        else:
            L.append("No monitor rule fired this week. Carry on as planned.")
            L.append("")

    # ---- the full table -----------------------------------------------------
    L.append("## Last %d weeks" % len(rows))
    L.append("")
    L.append("| Week | Hr | Mi | Vert | Run mi | Longest | HRV | RHR | Sleep | Endur | Hill |")
    L.append("|---|---|---|---|---|---|---|---|---|---|---|")
    for r in rows:
        tag = " *(partial)*" if r["week_start"] == this_monday.isoformat() else ""
        L.append("| %s%s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s |" % (
            r["week_start"], tag,
            cell(r["hours"], "%g"), cell(r["miles"], "%g"),
            cell(r["vert_ft"], "%d"), cell(r["run_miles"], "%g"),
            cell(r["longest_day_hr"], "%g"), cell(r["hrv_avg"], "%g"),
            cell(r["rhr_avg"], "%g"), cell(r["sleep_avg"], "%d"),
            cell(r["endurance"], "%d"), cell(r["hill"], "%d")))
    L.append("")
    L.append("Refresh with `make progress` after `python3 tracker/sync_garmin.py daily`.")
    L.append("")

    open(OUT, "w", encoding="utf-8").write("\n".join(L))
    print("wrote %s (%d weeks)" % (OUT, len(rows)))


if __name__ == "__main__":
    main()
