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
