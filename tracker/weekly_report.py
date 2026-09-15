#!/usr/bin/env python3
"""Week-over-week progress report.

Reads the weekly_progress view from Supabase and writes plan/progress.md plus
plan/odds.json. Stdlib only, so it runs on any machine with the repo.

  python3 tracker/weekly_report.py            # last 12 weeks
  python3 tracker/weekly_report.py 26         # last 26 weeks

Credentials come from tracker/.env (gitignored): SUPABASE_URL, SUPABASE_SERVICE_KEY
"""
import json, os, sys, urllib.request, urllib.parse, datetime
import odds as odds_model

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
OUT  = os.path.join(REPO, "plan", "progress.md")
ODDS = os.path.join(REPO, "plan", "odds.json")
ACTUALS = os.path.join(REPO, "plan", "weekly-actuals.json")

HRV_BASELINE = 41.6      # 90-day baseline when the plan was written
HRV_DROP_PCT = 10.0      # ">10% below baseline: cut volume 30% that week"
RACE_FT_PER_HR = 508     # 44,082 ft over the 86:48 moving budget

NUMERIC = ("hours", "miles", "vert_ft", "ft_per_hour", "longest_day_hr", "sessions",
           "days_on_feet", "best_back_to_back_hr", "night_hours", "night_session_hours",
           "run_hours", "run_miles", "run_vert_ft", "run_share_pct", "run_avg_hr",
           "rel_effort", "hrv_avg", "hrv_off_days", "rhr_avg", "sleep_avg", "sleep_hr",
           "deep_pct", "rem_pct", "readiness_avg", "bb_low_avg", "stress_avg",
           "respiration", "spo2", "intensity_min", "endurance", "hill",
           "run_tolerance", "vo2max", "acute_load", "acwr")


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
    """{{trend}} token; md.py renders it as a coloured arrow."""
    if now is None or prev in (None, 0):
        return ""
    d = (now - prev) / abs(prev)
    if abs(d) < flat:
        return " {{level}}"
    up = d > 0
    good = up == higher_is_better
    return " {{%s%s}}" % ("up" if up else "down", "" if good else "-bad")


def row(label, key, a, b, target=None, better=True, fmt="%g", flat=0.03, note=""):
    """One metric line: value + trend, prior, target, % of target."""
    v, p = a.get(key), b.get(key)
    at = "—"
    if target and v is not None:
        at = "%d%%" % round(100.0 * v / target)
    tgt = note or (("%g" % target) if target else "—")
    return "| %s | %s%s | %s | %s | %s |" % (
        label, cell(v, fmt), arrow(v, p, better, flat), cell(p, fmt), tgt, at)


def main():
    weeks = int(sys.argv[1]) if len(sys.argv) > 1 else 12
    all_rows = fetch(env(), max(weeks + 1, 14))
    if not all_rows:
        sys.exit("weekly_progress returned no rows")
    for r in all_rows:
        for k in NUMERIC:
            r[k] = num(r.get(k))
    rows = all_rows[:weeks + 1]

    schedule = json.load(open(os.path.join(REPO, "plan", "schedule.json"),
                              encoding="utf-8"))
    today = datetime.date.today()
    this_monday = today - datetime.timedelta(days=today.weekday())
    blk = odds_model.current_block(schedule["blocks"], today)
    T = blk["targets"]
    dens = round(T["vertFtPerWeek"] / float(T["hoursPerWeek"]))   # target ft/hour

    L = []
    L.append("# Week over week")
    L.append("")
    L.append("Generated %s from Supabase `weekly_progress` — Strava activities plus "
             "Garmin daily and training metrics, Monday-start weeks." % today.isoformat())
    L.append("")
    L.append("Arrows compare with the previous week. "
             "{{up}} and {{down}} are moving the way you want, "
             "{{up-bad}} and {{down-bad}} the wrong way, "
             "{{level}} is unchanged. Hover any arrow for what it means.")
    L.append("")

    odds_md, odds_data = odds_model.report(all_rows, schedule["blocks"], today)
    if odds_md:
        L.append(odds_md)
        json.dump(odds_data, open(ODDS, "w", encoding="utf-8"), indent=2)
        print("wrote %s (%d-%d%% on trajectory)"
              % (ODDS, odds_data["trajectory"]["low"], odds_data["trajectory"]["high"]))

    done = [r for r in rows
            if datetime.date.fromisoformat(r["week_start"])
               + datetime.timedelta(days=6) <= today]
    if len(done) >= 2:
        a, b = done[0], done[1]
        short = blk["name"].split("—")[0].strip()
        head = "| | This week | Prior | Target | At target |\n|---|---|---|---|---|"

        L.append("## Last complete week — %s" % a["week_start"])
        L.append("")
        L.append("### Volume")
        L.append("")
        L.append(head)
        L.append(row("Hours", "hours", a, b, T["hoursPerWeek"]))
        L.append(row("Miles", "miles", a, b, T["milesPerWeek"]))
        L.append(row("Vertical (ft)", "vert_ft", a, b, T["vertFtPerWeek"], fmt="%d"))
        L.append(row("Longest day (hr)", "longest_day_hr", a, b, T["peakDayHours"]))
        L.append(row("Best back-to-back (hr)", "best_back_to_back_hr", a, b,
                     note="two consecutive days"))
        L.append(row("Days on feet", "days_on_feet", a, b, note="5–6", fmt="%d"))
        L.append("")

        L.append("### Race specificity")
        L.append("")
        L.append("*Volume you can fake. This is the part that has to be real.*")
        L.append("")
        L.append(head)
        L.append(row("Vertical per hour", "ft_per_hour", a, b, dens, fmt="%d",
                     note="%d (race: %d)" % (dens, RACE_FT_PER_HR)))
        L.append(row("Running share of miles (%)", "run_share_pct", a, b, 30, fmt="%d",
                     note="30"))
        L.append(row("Running miles", "run_miles", a, b, note="tolerance %s"
                     % cell(a.get("run_tolerance"), "%g")))
        L.append(row("Night session hours", "night_session_hours", a, b,
                     note="%d cumulative this block" % T["nightHoursCumulative"]))
        L.append(row("Avg HR on runs", "run_avg_hr", a, b, fmt="%d", note="Z2 121–140"))
        L.append("")

        L.append("### Load and injury risk")
        L.append("")
        L.append(head)
        L.append(row("Acute load (7-day)", "acute_load", a, b, fmt="%d", note="—"))
        L.append(row("Acute:chronic ratio", "acwr", a, b, fmt="%.2f",
                     note="0.8–1.3 safe, >1.5 risky"))
        L.append(row("Intensity minutes", "intensity_min", a, b, fmt="%d", note="—"))
        L.append("")

        L.append("### Recovery")
        L.append("")
        L.append(head)
        L.append(row("HRV avg", "hrv_avg", a, b, HRV_BASELINE,
                     note="%g baseline" % HRV_BASELINE))
        L.append(row("Days HRV not balanced", "hrv_off_days", a, b, better=False,
                     fmt="%d", note="0 of 7"))
        L.append(row("Resting HR", "rhr_avg", a, b, better=False, note="51 baseline"))
        L.append(row("Sleep (hr)", "sleep_hr", a, b, note="7.5+"))
        L.append(row("Deep sleep (%)", "deep_pct", a, b, fmt="%d", note="13–23 normal"))
        L.append(row("Body battery low", "bb_low_avg", a, b, fmt="%d",
                     note="how empty you get"))
        L.append(row("Training readiness", "readiness_avg", a, b, fmt="%d", note="—"))
        L.append(row("Stress avg", "stress_avg", a, b, better=False, fmt="%d",
                     note="under 35"))
        L.append(row("Respiration", "respiration", a, b, better=False, fmt="%.1f",
                     note="a jump can precede illness"))
        L.append("")

        L.append("### Fitness markers")
        L.append("")
        L.append(head)
        L.append(row("Endurance score", "endurance", a, b, fmt="%d", flat=0.005,
                     note="—"))
        L.append(row("VO2 max", "vo2max", a, b, fmt="%.1f", flat=0.005, note="—"))
        L.append(row("Hill score", "hill", a, b, fmt="%d", flat=0.005,
                     note="needs running on hills"))
        L.append("")

        # ---- what actually changes next week ---------------------------------
        flags = []
        hrv = a.get("hrv_avg")
        if hrv is not None:
            drop = 100.0 * (HRV_BASELINE - hrv) / HRV_BASELINE
            if drop > HRV_DROP_PCT:
                flags.append("**HRV rule fires.** Week avg %.1f is %.1f%% below the %g "
                             "baseline. Your rule: cut next week's volume 30%%."
                             % (hrv, drop, HRV_BASELINE))
        if a.get("acwr") and a["acwr"] > 1.5:
            flags.append("**Acute:chronic %.2f — ramping too fast.** Above 1.5 is where "
                         "injuries come from. Hold volume flat for a week."
                         % a["acwr"])
        elif a.get("acwr") and a["acwr"] > 1.3:
            flags.append("**Acute:chronic %.2f, elevated.** Not dangerous, but do not add "
                         "on top of it." % a["acwr"])
        if a.get("ft_per_hour") is not None and a["ft_per_hour"] < 0.75 * dens:
            flags.append("**%d ft per hour against a %d target** (race demands %d). Your "
                         "hours are there; they are flat hours. Same time, steeper ground."
                         % (a["ft_per_hour"], dens, RACE_FT_PER_HR))
        if a.get("run_share_pct") is not None and a["run_share_pct"] < 25:
            flags.append("**Running is %d%% of your miles.** The long days are hikes. Run "
                         "the runnable grades or run-specific fitness keeps sliding."
                         % a["run_share_pct"])
        if a.get("night_session_hours") == 0 and T["nightHoursCumulative"] > 0:
            flags.append("**No night session.** Zero banked against %d cumulative this "
                         "block, and it is the cheapest gap you have — one headlamp lap "
                         "counts." % T["nightHoursCumulative"])
        if a.get("longest_day_hr") and a["longest_day_hr"] < 0.5 * T["peakDayHours"]:
            flags.append("**Longest day %g hr against an %g-hour block peak.** Single-day "
                         "duration is the gap volume does not close."
                         % (a["longest_day_hr"], T["peakDayHours"]))
        if a.get("hrv_off_days") and a["hrv_off_days"] >= 5:
            flags.append("**HRV unbalanced %d of 7 days.** One bad night is noise; five is "
                         "a signal." % a["hrv_off_days"])
        es = [r["endurance"] for r in done[:4] if r["endurance"] is not None]
        if len(es) == 4 and es[0] < es[3]:
            flags.append("**Endurance score down %d over 4 weeks** (%d → %d). Volume is "
                         "not converting into aerobic fitness yet."
                         % (es[3] - es[0], es[3], es[0]))

        L.append("### What this changes")
        L.append("")
        if flags:
            for f in flags:
                L.append("- " + f)
        else:
            L.append("- Nothing fired. Carry on as planned.")
        L.append("")

    # ---- the long table ------------------------------------------------------
    L.append("## Last %d weeks" % len(rows))
    L.append("")
    L.append("| Week | Hr | Mi | Vert | ft/hr | Long | B2B | Run% | Night | ACWR | HRV | RHR | Sleep | Endur |")
    L.append("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    for r in rows:
        tag = "" if (datetime.date.fromisoformat(r["week_start"])
                     + datetime.timedelta(days=6) <= today) else " *(partial)*"
        L.append("| %s%s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s |" % (
            r["week_start"], tag,
            cell(r["hours"], "%g"), cell(r["miles"], "%g"), cell(r["vert_ft"], "%d"),
            cell(r["ft_per_hour"], "%d"), cell(r["longest_day_hr"], "%g"),
            cell(r["best_back_to_back_hr"], "%g"), cell(r["run_share_pct"], "%d"),
            cell(r["night_session_hours"], "%g"), cell(r["acwr"], "%.2f"),
            cell(r["hrv_avg"], "%g"), cell(r["rhr_avg"], "%g"),
            cell(r["sleep_hr"], "%g"), cell(r["endurance"], "%d")))
    L.append("")
    L.append("Refresh with `make progress` after `.venv/bin/python tracker/sync_garmin.py daily`.")
    L.append("")

    # per-week actuals for the Every week page - finished weeks only, so a
    # week in progress never shows as a miss.
    act = {}
    for r in all_rows:
        if (datetime.date.fromisoformat(r["week_start"])
                + datetime.timedelta(days=6)) > today:
            continue
        act[r["week_start"]] = {
            "hours": r["hours"], "miles": r["miles"],
            "vert_ft": int(r["vert_ft"]) if r["vert_ft"] is not None else 0,
            "ft_per_hour": r["ft_per_hour"], "run_share_pct": r["run_share_pct"],
        }
    json.dump(act, open(ACTUALS, "w", encoding="utf-8"), indent=2)
    print("wrote %s (%d finished weeks)" % (ACTUALS, len(act)))

    open(OUT, "w", encoding="utf-8").write("\n".join(L))
    print("wrote %s (%d weeks)" % (OUT, len(rows)))


if __name__ == "__main__":
    main()
