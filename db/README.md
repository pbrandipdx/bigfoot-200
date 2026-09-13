# db/ — Supabase schema

Project **`bigfoot-200-training`** (`mwjprmuwdhfjlldrruhx`). Applied migrations are recorded in
`supabase_migrations.schema_migrations`.

Files here are a **copy for review and version control**. Applying them is a separate act — they
are already live. If you change one, apply it to Supabase too, or the repo and the database
disagree and you will not be able to tell which is right.

## Applied, newest first

| Version | What it does | In this folder |
|---|---|---|
| `20260913214636` | `data_health` view | yes |
| `20260913214549` | `activities_units_guard` trigger | yes |
| `20260910212220` | `bigfoot200_historical_data` | **no — Supabase only** |
| `20260907013738` | `add_routes_and_weekly_plan` | **no — Supabase only** |
| `20260906190917` | `add_garmin_raw_capture` | **no — Supabase only** |
| `20260906190316` | `create_training_schema` | **no — Supabase only** |

The four earlier migrations exist only in Supabase. **The database cannot be rebuilt from this
repo yet.** To export them:

    select version, name, array_to_string(statements, E'\n;\n') as sql
    from supabase_migrations.schema_migrations order by version;

## The invariants these protect

Two columns carry units or a timezone convention that is not obvious from the value, and both
have already caused a real error:

**`activities.elevation_gain_m` and `distance_m` are METRES.** Strava sends both in metres.
`weekly_progress` converts gain to feet, once, with `×3.28084`. Nothing else converts.
On 2026-09-13 Claude read `total_elevation_gain` as feet in a chat and under-reported climbing
by 3.28×; Patrick caught it because he knew what Wildwood feels like. The trigger in
`20260913214549` now compares the stored columns against the row's own `raw` payload and raises
if they disagree by more than 1% — a converted number cannot match its own source. It catches
both directions, which a plausibility ceiling alone cannot: dividing by 3.28 makes the number
too *small*, which looks fine.

`raw` is therefore **load-bearing, not decorative**. Always populate it. Never drop it to get a
write past the trigger. The 200 rows loaded before this date have it empty, which is why the
2026-09-13 investigation had to argue from plausibility instead of reading what Strava sent.

**`activities.start_local` holds LOCAL wall-clock time under a UTC label.** Read it
`at time zone 'UTC'`. Converting it to `America/Los_Angeles` shifts everything back 7 hours and
buckets every morning session into the previous day — which it silently did until 2026-09-12.
**This one has no trigger yet.** It is enforced only by comments and by the daily check-in's
prompt, which is the weaker kind of protection — the kind that failed above.

## Checking health

    select * from data_health;

`unit_guard_installed = 0` means the trigger is gone and the numbers are unprotected.
`unit_guard_violations` should be 0. `max_ft_per_mile` has been 322 across 122 measured
activities; a 3.28× inflation would push it past 1,000.
