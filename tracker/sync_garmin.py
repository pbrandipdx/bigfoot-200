#!/usr/bin/env python3
"""Pull Garmin Connect data into the bigfoot-200-training Supabase database.

Fills: garmin_daily (wellness), garmin_training (performance metrics),
       garmin_raw (every payload, verbatim, so nothing is lost to mapping bugs).

Credentials NEVER live in this repo. Put them in tracker/.env (gitignored):

    GARMIN_EMAIL=you@example.com
    GARMIN_PASSWORD=...            # only needed the first time; tokens cached after
    SUPABASE_URL=https://mwjprmuwdhfjlldrruhx.supabase.co
    SUPABASE_SERVICE_KEY=...       # service_role key - RLS is on, anon cannot write

Install once:
    pip3 install garminconnect requests

Usage:
    python3 tracker/sync_garmin.py discover              # which methods your version has
    python3 tracker/sync_garmin.py daily                 # yesterday + today
    python3 tracker/sync_garmin.py backfill 2024-09-01 2026-09-11
"""
import os, sys, json, time, datetime as dt

try:
    import requests
except ImportError:
    sys.exit("pip3 install requests")
try:
    from garminconnect import Garmin
except ImportError:
    sys.exit("pip3 install garminconnect")

HERE = os.path.dirname(os.path.abspath(__file__))
TOKENSTORE = os.path.expanduser("~/.garminconnect")

# ---------- config ----------
def load_env():
    p = os.path.join(HERE, ".env")
    if os.path.exists(p):
        for line in open(p):
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())
load_env()

SB_URL = os.environ.get("SUPABASE_URL", "").rstrip("/")
SB_KEY = os.environ.get("SUPABASE_SERVICE_KEY", "")
if not SB_URL or not SB_KEY:
    sys.exit("Set SUPABASE_URL and SUPABASE_SERVICE_KEY (see tracker/.env)")

SB_HEAD = {"apikey": SB_KEY, "Authorization": f"Bearer {SB_KEY}",
           "Content-Type": "application/json", "Prefer": "resolution=merge-duplicates"}

def upsert(table, rows, conflict):
    rows = [r for r in rows if r]
    if not rows:
        return 0
    r = requests.post(f"{SB_URL}/rest/v1/{table}?on_conflict={conflict}",
                      headers=SB_HEAD, data=json.dumps(rows), timeout=60)
    if r.status_code >= 300:
        print(f"  ! {table}: HTTP {r.status_code} {r.text[:300]}")
        return 0
    return len(rows)

# ---------- garmin ----------
def connect():
    try:
        g = Garmin()
        g.login(TOKENSTORE)
        return g
    except Exception:
        email, pw = os.environ.get("GARMIN_EMAIL"), os.environ.get("GARMIN_PASSWORD")
        if not email or not pw:
            sys.exit("No cached token. Put GARMIN_EMAIL and GARMIN_PASSWORD in tracker/.env for the first run.")
        g = Garmin(email, pw)
        g.login()
        g.garth.dump(TOKENSTORE)
        print(f"  token cached at {TOKENSTORE} - you can remove GARMIN_PASSWORD from .env now")
        return g

def call(g, names, *args):
    """Try several method names; return (name, value) for the first that works.
    Method names differ between library versions, so we probe rather than assume."""
    for n in names:
        fn = getattr(g, n, None)
        if not fn:
            continue
        try:
            return n, fn(*args)
        except Exception as e:
            print(f"    {n}: {type(e).__name__}")
    return None, None

WELLNESS = {
    "stats":              ["get_stats", "get_user_summary"],
    "sleep":              ["get_sleep_data"],
    "hrv":                ["get_hrv_data"],
    "training_readiness": ["get_training_readiness"],
}
PERFORMANCE = {
    "training_status":    ["get_training_status"],
    "max_metrics":        ["get_max_metrics"],
    "hill_score":         ["get_hill_score"],
    "endurance_score":    ["get_endurance_score"],
    "running_tolerance":  ["get_running_tolerance", "get_run_tolerance"],
    "race_predictions":   ["get_race_predictions"],
}

def num(d, *keys):
    for k in keys:
        if isinstance(d, dict) and d.get(k) is not None:
            return d[k]
    return None

def sync_day(g, day):
    iso = day.isoformat()
    raw_rows, payloads = [], {}
    for label, names in {**WELLNESS, **PERFORMANCE}.items():
        name, val = call(g, names, iso)
        if val is None:
            continue
        payloads[label] = val
        raw_rows.append({"day": iso, "endpoint": label, "payload": val})
    if not payloads:
        return 0, 0, 0

    s = payloads.get("stats") or {}
    slp = payloads.get("sleep") or {}
    slp_dto = (slp.get("dailySleepDTO") or {}) if isinstance(slp, dict) else {}
    hrv = payloads.get("hrv") or {}
    hrv_sum = (hrv.get("hrvSummary") or {}) if isinstance(hrv, dict) else {}
    tr = payloads.get("training_readiness")
    tr = (tr[0] if isinstance(tr, list) and tr else tr) or {}

    daily = {
        "day": iso,
        "resting_hr":        num(s, "restingHeartRate"),
        "stress_avg":        num(s, "averageStressLevel"),
        "max_stress":        num(s, "maxStressLevel"),
        "steps":             num(s, "totalSteps"),
        "active_calories":   num(s, "activeKilocalories"),
        "body_battery_high": num(s, "bodyBatteryHighestValue"),
        "body_battery_low":  num(s, "bodyBatteryLowestValue"),
        "avg_overnight_spo2":num(s, "averageSpo2"),
        "lowest_spo2":       num(s, "lowestSpo2"),
        "avg_respiration":   num(s, "avgWakingRespirationValue"),
        "sleep_score":       num((slp_dto.get("sleepScores") or {}).get("overall") or {}, "value"),
        "sleep_duration_s":  num(slp_dto, "sleepTimeSeconds"),
        "deep_sleep_s":      num(slp_dto, "deepSleepSeconds"),
        "rem_sleep_s":       num(slp_dto, "remSleepSeconds"),
        "light_sleep_s":     num(slp_dto, "lightSleepSeconds"),
        "awake_s":           num(slp_dto, "awakeSleepSeconds"),
        "hrv_overnight_avg": num(hrv_sum, "lastNightAvg"),
        "hrv_status":        num(hrv_sum, "status"),
        "training_readiness":num(tr, "score"),
        "readiness_level":   num(tr, "level"),
        "raw":               {"endpoints": list(payloads)},
    }
    bbc, bbd = num(s, "bodyBatteryChargedValue"), num(s, "bodyBatteryDrainedValue")
    if bbc is not None and bbd is not None:
        daily["body_battery_change"] = bbc - bbd
    mi, vi = num(s, "moderateIntensityMinutes"), num(s, "vigorousIntensityMinutes")
    if mi is not None or vi is not None:
        daily["intensity_minutes"] = (mi or 0) + (vi or 0)
    fa = num(s, "floorsAscended")
    if fa is not None:
        daily["floors_ascended"] = round(float(fa))
    daily = {k: v for k, v in daily.items() if v is not None}

    ts  = payloads.get("training_status") or {}
    mm  = payloads.get("max_metrics") or {}
    mm0 = (mm[0] if isinstance(mm, list) and mm else mm) or {}
    gen = (mm0.get("generic") or {}) if isinstance(mm0, dict) else {}
    training = {
        "day": iso,
        "hill_score":       num(payloads.get("hill_score") or {}, "overallScore", "hillScore"),
        "endurance_score":  num(payloads.get("endurance_score") or {}, "overallScore", "enduranceScore"),
        "running_tolerance":num(payloads.get("running_tolerance") or {}, "runningTolerance", "value"),
        "vo2max_running":   num(gen, "vo2MaxPreciseValue", "vo2MaxValue"),
        "training_status":  num(ts, "trainingStatus", "trainingStatusKey"),
        "raw":              {"endpoints": [k for k in payloads if k in PERFORMANCE]},
    }
    training = {k: v for k, v in training.items() if v is not None}

    n_raw = upsert("garmin_raw", raw_rows, "day,endpoint")
    n_day = upsert("garmin_daily", [daily] if len(daily) > 2 else [], "day")
    n_trn = upsert("garmin_training", [training] if len(training) > 2 else [], "day")
    return n_day, n_trn, n_raw

def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "daily"
    g = connect()
    print(f"connected as {g.get_full_name() if hasattr(g,'get_full_name') else 'garmin user'}")

    if mode == "discover":
        have = sorted(m for m in dir(g) if m.startswith("get_"))
        print(f"\n{len(have)} get_* methods available:")
        for m in have:
            print("  " + m)
        wanted = {n for names in {**WELLNESS, **PERFORMANCE}.values() for n in names}
        print("\nof the ones this script wants:")
        for n in sorted(wanted):
            print(f"  {'OK  ' if hasattr(g,n) else 'MISS'} {n}")
        return

    if mode == "backfill":
        start = dt.date.fromisoformat(sys.argv[2])
        end   = dt.date.fromisoformat(sys.argv[3])
    else:
        end = dt.date.today()
        start = end - dt.timedelta(days=1)

    day, tot = start, [0, 0, 0]
    while day <= end:
        d, t, r = sync_day(g, day)
        tot = [tot[0]+d, tot[1]+t, tot[2]+r]
        print(f"  {day}  daily:{d} training:{t} raw:{r}")
        day += dt.timedelta(days=1)
        time.sleep(1.0)          # be polite; this is an unofficial API
    print(f"\ndone: {tot[0]} daily, {tot[1]} training, {tot[2]} raw rows")

if __name__ == "__main__":
    main()
