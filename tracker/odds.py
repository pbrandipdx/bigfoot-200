#!/usr/bin/env python3
"""Finish-odds model for the Bigfoot 200.

Two numbers, both recomputed from measured data every time `make progress` runs:

  NOW         readiness against the CURRENT block's targets, i.e. how the last
              eight weeks stack up against what this block asks for.
  TRAJECTORY  where the current rate of change lands on race day, measured
              against Block 5's targets.

Readiness is a weighted average of seven gates, each clipped to 0..1. It is then
mapped to a finish-probability range. The mapping's base rate is an ASSUMPTION,
not a measurement — Destination Trail does not publish starter counts, so the
field-wide finish rate for the Bigfoot 200 is not in our data. It is stated
openly wherever the number is displayed. Everything to the left of the base
rate — the readiness score itself — is entirely measured.

No third-party imports: see the note in dashboard/md.py.
"""
import datetime

# Field-wide finish rate for a 200-mile mountain race. ASSUMPTION. Replace the
# moment we have real starters-vs-finishers data for the Bigfoot 200.
BASE_LOW, BASE_HIGH = 0.45, 0.65
BASE_NOTE = ("base rate 45–65% assumed for a 200-mile mountain race — "
             "Destination Trail does not publish starter counts")

RACE_DATE = datetime.date(2027, 8, 13)
HRV_BASELINE = 41.6

GATES = [
    # key,        label,                  weight
    ("vert",      "Vertical per week",       20),
    ("long_day",  "Longest single day",      20),
    ("hours",     "Time on feet per week",   15),
    ("run",       "Run-specific capacity",   15),
    ("night",     "Night hours",             10),
    ("consistency", "Week-to-week consistency", 10),
    ("recovery",  "Recovery headroom",       10),
]
WEIGHT = dict((k, w) for k, _, w in GATES)
LABEL = dict((k, l) for k, l, _ in GATES)


def clip(x, lo=0.0, hi=1.0):
    return lo if x < lo else hi if x > hi else x


def mean(xs):
    xs = [x for x in xs if x is not None]
    return sum(xs) / len(xs) if xs else None


def slope_per_week(xs):
    """Least-squares slope of xs (oldest first) per index step."""
    pts = [(i, v) for i, v in enumerate(xs) if v is not None]
    n = len(pts)
    if n < 3:
        return 0.0
    mx = sum(p[0] for p in pts) / n
    my = sum(p[1] for p in pts) / n
    den = sum((p[0] - mx) ** 2 for p in pts)
    if den == 0:
        return 0.0
    return sum((p[0] - mx) * (p[1] - my) for p in pts) / den


def current_block(blocks, on):
    iso = on.isoformat()
    for b in blocks:
        if b["start"] <= iso <= b["end"]:
            return b
    return blocks[0] if iso < blocks[0]["start"] else blocks[-1]


def gates(recent, tgt, night_total, endurance_series):
    """recent = last complete weeks, newest first. tgt = a block's targets dict."""
    last4 = recent[:4]
    last8 = recent[:8]

    g = {}
    g["hours"] = clip((mean([w["hours"] for w in last4]) or 0) / tgt["hoursPerWeek"])
    g["vert"] = clip((mean([w["vert_ft"] for w in last4]) or 0) / tgt["vertFtPerWeek"])
    g["long_day"] = clip(max([w["longest_day_hr"] or 0 for w in last8] or [0])
                         / tgt["peakDayHours"])

    # Run-specific: share of mileage actually run, plus the direction of the
    # endurance score. Hiking vertical does not build this.
    mi = sum(w["miles"] or 0 for w in last8)
    rmi = sum(w["run_miles"] or 0 for w in last8)
    share = (rmi / mi) if mi else 0.0
    es = [e for e in endurance_series if e is not None]
    trend = 1.0 if len(es) < 3 else (
        1.0 if slope_per_week(es) > 2 else 0.5 if slope_per_week(es) > -2 else 0.15)
    g["run"] = clip(0.6 * clip(share / 0.30) + 0.4 * trend)

    g["night"] = clip(night_total / tgt["nightHoursCumulative"])

    hit = [1 for w in last8 if (w["hours"] or 0) >= 0.8 * tgt["hoursPerWeek"]]
    g["consistency"] = clip(len(hit) / float(len(last8) or 1))

    # last two weeks, not four — a four-week mean hides the drop that the HRV
    # rule is firing on right now
    hrv = mean([w["hrv_avg"] for w in recent[:2]])
    # full credit at baseline, zero at 20% below it
    g["recovery"] = 1.0 if hrv is None else clip((hrv / HRV_BASELINE - 0.80) / 0.20)
    return g


def readiness(g):
    return sum(WEIGHT[k] * g[k] for k in WEIGHT) / 100.0


def odds(r):
    """Readiness -> finish-probability range. See BASE_NOTE."""
    adj = clip(0.15 + 0.95 * r, 0.0, 1.10)
    return round(100 * BASE_LOW * adj), round(100 * BASE_HIGH * adj)


def band(lo, hi):
    """Label from the midpoint of the range, not its optimistic end."""
    mid = (lo + hi) / 2.0
    if mid >= 50:
        return "strong", "#2E7D46"
    if mid >= 36:
        return "on track", "#6B8E3D"
    if mid >= 22:
        return "behind", "#B0793A"
    return "well behind", "#A23B2C"


def trajectory(recent, block5, night_total, today):
    """Project the current 8-week slope forward to race day, against Block 5."""
    wks = max(1, (RACE_DATE - today).days // 7)
    old_first = list(reversed(recent[:8]))          # oldest -> newest

    def proj(key, cap):
        cur = mean([w[key] for w in recent[:4]]) or 0.0
        s = slope_per_week([w[key] for w in old_first])
        return clip((cur + s * wks) / cap)

    g = {}
    g["hours"] = proj("hours", block5["hoursPerWeek"])
    g["vert"] = proj("vert_ft", block5["vertFtPerWeek"])

    best = max([w["longest_day_hr"] or 0 for w in recent[:8]] or [0])
    sld = slope_per_week([w["longest_day_hr"] for w in old_first])
    g["long_day"] = clip((best + max(sld, 0) * wks) / block5["peakDayHours"])

    mi = sum(w["miles"] or 0 for w in recent[:8])
    rmi = sum(w["run_miles"] or 0 for w in recent[:8])
    g["run"] = clip((rmi / mi if mi else 0.0) / 0.30)

    per_wk = night_total / max(1, min(len(recent), 12))
    g["night"] = clip((night_total + per_wk * wks) / block5["nightHoursCumulative"])

    hit = [1 for w in recent[:8] if (w["hours"] or 0) >= 0.8 * 12]
    g["consistency"] = clip(len(hit) / float(len(recent[:8]) or 1))

    hrv = mean([w["hrv_avg"] for w in recent[:2]])
    g["recovery"] = 1.0 if hrv is None else clip((hrv / HRV_BASELINE - 0.80) / 0.20)
    return g, wks


def bar(v, width=10):
    """Filled/empty block characters - readable as a bar at a glance, where
    '#####.....' read as punctuation."""
    n = int(round(v * width))
    return "\u2588" * n + "\u2591" * (width - n)


def report(rows, blocks, today):
    """rows newest-first from weekly_progress. Returns (markdown, odds dict)."""
    this_monday = today - datetime.timedelta(days=today.weekday())
    recent = [r for r in rows if r["week_start"] != this_monday.isoformat()]
    if len(recent) < 3:
        return "", None

    blk = current_block(blocks, today)
    tgt = blk["targets"]
    b5 = blocks[-1]["targets"]
    night_total = sum(w["night_hours"] or 0 for w in recent[:12])
    es = list(reversed([w["endurance"] for w in recent[:8]]))

    gn = gates(recent, tgt, night_total, es)
    rn = readiness(gn)            # block readiness — progress against THIS block

    gt, wks = trajectory(recent, b5, night_total, today)
    rt = readiness(gt)            # projected race-day readiness
    t_lo, t_hi = odds(rt)

    label, color = band(t_lo, t_hi)
    short = blk["name"].split("—")[0].strip()

    L = []
    L.append("## Finish odds")
    L.append("")
    L.append("**%d–%d%%** — *%s*, %d weeks out." % (t_lo, t_hi, label, wks))
    L.append("")
    L.append("That is the trajectory number: where the last eight weeks' rate of "
             "change lands on race day, measured against Block 5's targets. "
             "Separately, you are at **%d%% of what %s asks for right now** — "
             "that is a plan-adherence score, not a probability. Block 1 fitness "
             "would not finish this race; hitting Block 1 on time is what keeps "
             "the trajectory number climbing." % (round(rn * 100), short))
    L.append("")
    L.append("| Gate | Weight | vs %s now | Projected race day |" % short)
    L.append("|---|---|---|---|")
    for k, lab, w in GATES:
        L.append("| %s | %d%% | `%s` %d%% | `%s` %d%% |"
                 % (lab, w, bar(gn[k]), round(gn[k] * 100),
                    bar(gt[k]), round(gt[k] * 100)))
    L.append("| **Readiness** | | **%d%%** | **%d%%** |"
             % (round(rn * 100), round(rt * 100)))
    L.append("")

    worst = sorted(WEIGHT, key=lambda k: gt[k] * WEIGHT[k])[:2]
    L.append("Biggest drags on the trajectory number: **%s** and **%s**." %
             (LABEL[worst[0]], LABEL[worst[1]]))
    L.append("")
    L.append("> **How this is built.** Seven gates, each measured from Strava and "
             "Garmin, weighted as shown, averaged into a readiness score. The "
             "*now* column compares the last four to eight weeks against the "
             "current block's targets. The *projected* column fits the slope of "
             "the last eight weeks and carries it to race day against Block 5's "
             "targets — it assumes you keep improving at exactly the rate you "
             "have been, no faster and no slower, which is why a flat eight "
             "weeks shows up as a flat projection. The readiness score is "
             "entirely measured. Turning it into a percentage needs a "
             "field-wide finish rate, and that part is an assumption: %s. Read "
             "the gate breakdown and the direction as signal; read the "
             "percentage as a rough band." % BASE_NOTE)
    L.append("")

    return "\n".join(L), {
        "generated": today.isoformat(),
        "weeksToRace": wks,
        "blockReadiness": round(rn * 100),
        "blockName": short,
        "trajectory": {"low": t_lo, "high": t_hi, "readiness": round(rt * 100)},
        "label": label, "color": color,
        "gates": dict((k, {"label": LABEL[k], "weight": WEIGHT[k],
                           "now": round(gn[k] * 100),
                           "raceDay": round(gt[k] * 100)}) for k in WEIGHT),
        "baseNote": BASE_NOTE,
    }
