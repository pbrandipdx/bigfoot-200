# Bigfoot 200 tracker — how the refresh works

Files here:

- `template.html` — the page. Contains the literal token `/*__DATA__*/` where the data block goes.
- `weeks.json`    — the synced data: `{synced, source, weeks:{ "YYYY-MM-DD(Monday)": {hours, vert, miles, longest, night, sessions, days} }}`
- `build.py`      — `python3 build.py` reads both and writes `bigfoot-tracker.html` beside them.

## Aggregation rules (keep these stable or the history breaks)

- Weeks run **Monday → Sunday**, keyed by the Monday's ISO date.
- **hours**   = sum of `moving_time` for sport types Walk, Hike, Run, TrailRun, StairStepper.
- **miles**   = sum of `distance` for Walk, Hike, Run, TrailRun only (StairStepper excluded — no distance).
- **vert**    = sum of `elevation_gain` (metres) × 3.280839895, rounded to whole feet.
- **longest** = the single largest `moving_time` in the week, in hours (not the daily total).
- **sessions**= count of qualifying activities. **days** = distinct calendar days with one.
- Excluded entirely: WeightTraining, Swim, Basketball, Soccer, and anything else not on the list above.
- **night**   = hours of qualifying activity falling between local sunset and sunrise for
  Lake Oswego, OR (45.42 N, 122.67 W). Currently 0 across all weeks.

## Weekly refresh

1. `mcp__Strava__list_activities` with `range_start` = the Monday of the last week already in
   `weeks.json`, `range_end` = now. Page until covered.
2. Recompute those weeks with the rules above and merge into `weeks.json` (overwrite, don't append —
   Strava activities get edited after the fact).
3. Set `synced` to today.
4. `python3 build.py`, then write `bigfoot-tracker.html` to the Desktop.

## The phone dashboard

The page Patrick reads on his phone is **https://pbrandipdx.github.io/bigfoot200-training/**,
served from the separate public repo `pbrandipdx/bigfoot200-training`.

That repo is a VIEW. It must never hold its own copy of block targets, race dates or
weekly-template rules — those live here, in `plan/block-targets.md`, and are generated
into the dashboard. If a number appears in both places, this repo is right.

Do not hand-edit `bigfoot-tracker.html` — it is generated and will be overwritten.

## Garmin sync

`sync_garmin.py` fills the Supabase tables `garmin_daily`, `garmin_training` and
`garmin_raw` — the monitors in `plan/block-targets.md` (HRV, resting HR, body
battery, sleep, hill score, endurance score, running tolerance) all read from there.

    python3 -m venv .venv
    .venv/bin/pip install garminconnect requests
    cp tracker/.env.example tracker/.env             # fill it in; it is gitignored
    .venv/bin/python tracker/sync_garmin.py discover # what your library version can reach
    .venv/bin/python tracker/sync_garmin.py backfill 2024-09-01 2026-09-11
    .venv/bin/python tracker/sync_garmin.py daily    # weekly from then on

Use `.venv/bin/python`, not `python3` — on macOS `pip3` and `python3` often point at
different interpreters, so packages installed with one are invisible to the other.

Notes:

- Credentials live only in `tracker/.env` on the Mac mini. They are never committed
  and never pass through Claude.
- `discover` first. The library's method names vary by version, and hill score and
  endurance score are not in every build — the script probes rather than assumes,
  and skips what is missing instead of failing.
- Every payload is stored verbatim in `garmin_raw`, so a mapping mistake loses nothing.
- It sleeps 1s between days. This is Garmin's private API, not a supported one:
  go gently, and expect it to need fixing whenever Garmin changes something.
- Metrics only exist from when Garmin started computing them on a device you owned.
  Hill score and endurance score date from ~2022 devices; running tolerance is newer
  still. A backfill earlier than the Fenix 8 will simply return nothing for those.
