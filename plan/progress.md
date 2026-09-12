# Week over week

Generated 2026-09-12 from Supabase `weekly_progress` (activities + garmin_daily + garmin_training, Monday-start weeks, America/Los_Angeles).

Read the arrows as direction, not verdict: `^` up, `v` down, `=` level, `!` means the direction is the wrong one.

## Last complete week — 2026-08-31

| | This week | Prior week | Block 1 target | At target |
|---|---|---|---|---|
| Hours | 12.1 v! | 12.9 | 12 | 101% |
| Miles | 39.6 ^ | 30.3 | 45 | 88% |
| Vert (ft) | 2927 ^ | 1348 | 3500 | 84% |
| Longest day (hr) | 3 ^ | 1.7 | 8 | 38% |
| Running miles | 2 ^ | 1.7 | — | — |
| HRV avg | 36.5 v! | 42.3 | 41.6 baseline | 88% |
| Resting HR | 52.7 ^! | 51.1 | — | — |
| Endurance score | 4883 v! | 4941 | — | — |

### What this changes

- **HRV rule fires.** 7-day avg 36.5 is 12.3% below the 41.6 baseline, past the 10% line. Cut next week's volume 30%.
- **Running share 5%** (2 of 39.6 miles). The Saturdays are hikes. Run the runnable grades or the run-specific fitness keeps sliding.
- **Endurance score down 136 over 4 weeks** (5019 -> 4883). Volume is not converting into aerobic fitness yet.

## Last 13 weeks

| Week | Hr | Mi | Vert | Run mi | Longest | HRV | RHR | Sleep | Endur | Hill |
|---|---|---|---|---|---|---|---|---|---|---|
| 2026-09-07 *(partial)* | 9.3 | 24.3 | 1434 | 3.8 | 1.7 | 37.2 | 52.4 | 80 | 4775 | — |
| 2026-08-31 | 12.1 | 39.6 | 2927 | 2 | 3 | 36.5 | 52.7 | 76 | 4883 | — |
| 2026-08-24 | 12.9 | 30.3 | 1348 | 1.7 | 1.7 | 42.3 | 51.1 | 80 | 4941 | — |
| 2026-08-17 | 10.3 | 27.1 | 1020 | — | 1.9 | 51 | 49.9 | 85 | 4987 | — |
| 2026-08-10 | 11.2 | 28.8 | 1299 | — | 1.9 | 37.7 | 53.4 | 73 | 5019 | 43 |
| 2026-08-03 | 8.7 | 22.8 | 1962 | — | 1.8 | 47.5 | 49.6 | 77 | 5046 | 44 |
| 2026-07-27 | 11.8 | 24.6 | 2562 | — | 3 | 40.9 | 49.6 | 79 | 5063 | 44 |
| 2026-07-20 | 13.1 | 26.8 | 1050 | 4.5 | 1.4 | 37.8 | 52.9 | 75 | 5068 | 44 |
| 2026-07-13 | 11.6 | 34.2 | 1880 | 18.7 | 1.7 | 41.1 | 51.6 | 84 | 5065 | 44 |
| 2026-07-06 | 10.7 | 22.2 | 1962 | 1.3 | 2.1 | 40 | 52.6 | 77 | 5067 | 45 |
| 2026-06-29 | 12.5 | 36.7 | 1398 | 18.7 | 1.1 | 42.2 | 52 | 78 | 5080 | 47 |
| 2026-06-22 | 9 | 29.5 | 883 | 21.3 | 2.2 | 39.3 | 50 | 77 | 5084 | 48 |
| 2026-06-15 | 7.7 | 30.7 | 2037 | 20.5 | 2.1 | 48.4 | 48.9 | 83 | 5102 | 49 |

Refresh with `make progress` after `python3 tracker/sync_garmin.py daily`.
