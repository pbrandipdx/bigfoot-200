# Week over week

Generated 2026-09-13 from Supabase `weekly_progress` (activities + garmin_daily + garmin_training, Monday-start weeks, America/Los_Angeles).

Arrows compare with the previous week. {{up}} and {{down}} are moving the way you want, {{up-bad}} and {{down-bad}} the wrong way, {{level}} is unchanged. Hover any arrow for what it means.

## Finish odds

**27–39%** — *behind*, 47 weeks out.

That is the trajectory number: where the last eight weeks' rate of change lands on race day, measured against Block 5's targets. Separately, you are at **51% of what Block 1 asks for right now** — that is a plan-adherence score, not a probability. Block 1 fitness would not finish this race; hitting Block 1 on time is what keeps the trajectory number climbing.

| Gate | Weight | vs Block 1 now | Projected race day |
|---|---|---|---|
| Vertical per week | 20% | `█████░░░░░` 49% | `████░░░░░░` 41% |
| Longest single day | 20% | `████░░░░░░` 38% | `████░░░░░░` 36% |
| Time on feet per week | 15% | `██████████` 100% | `████████░░` 76% |
| Run-specific capacity | 15% | `███░░░░░░░` 29% | `████░░░░░░` 38% |
| Night hours | 10% | `░░░░░░░░░░` 0% | `░░░░░░░░░░` 0% |
| Week-to-week consistency | 10% | `████████░░` 75% | `████████░░` 75% |
| Recovery headroom | 10% | `███████░░░` 74% | `███████░░░` 74% |
| **Readiness** | | **51%** | **47%** |

Biggest drags on the trajectory number: **Night hours** and **Run-specific capacity**.

> **How this is built.** Seven gates, each measured from Strava and Garmin, weighted as shown, averaged into a readiness score. The *now* column compares the last four to eight weeks against the current block's targets. The *projected* column fits the slope of the last eight weeks and carries it to race day against Block 5's targets — it assumes you keep improving at exactly the rate you have been, no faster and no slower, which is why a flat eight weeks shows up as a flat projection. The readiness score is entirely measured. Turning it into a percentage needs a field-wide finish rate, and that part is an assumption: base rate 45–65% assumed for a 200-mile mountain race — Destination Trail does not publish starter counts. Read the gate breakdown and the direction as signal; read the percentage as a rough band.

## Last complete week — 2026-08-31

| | This week | Prior week | Block 1 target | At target |
|---|---|---|---|---|
| Hours | 12.1 {{down-bad}} | 13.8 | 12 | 101% |
| Miles | 39.6 {{up}} | 33.7 | 45 | 88% |
| Vert (ft) | 2927 {{up}} | 1453 | 3500 | 84% |
| Longest day (hr) | 3 {{up}} | 1.7 | 8 | 38% |
| Running miles | 2 {{up}} | 1.7 | — | — |
| HRV avg | 36.5 {{down-bad}} | 42.3 | 41.6 baseline | 88% |
| Resting HR | 52.7 {{up-bad}} | 51.1 | — | — |
| Endurance score | 4883 {{down-bad}} | 4941 | — | — |

### What this changes

- **HRV rule fires.** 7-day avg 36.5 is 12.3% below the 41.6 baseline, past the 10% line. Cut next week's volume 30%.
- **Running share 5%** (2 of 39.6 miles). The Saturdays are hikes. Run the runnable grades or the run-specific fitness keeps sliding.
- **Endurance score down 136 over 4 weeks** (5019 -> 4883). Volume is not converting into aerobic fitness yet.

## Last 13 weeks

| Week | Hr | Mi | Vert | Run mi | Longest | HRV | RHR | Sleep | Endur | Hill |
|---|---|---|---|---|---|---|---|---|---|---|
| 2026-09-07 *(partial)* | 9.3 | 24.3 | 1434 | 3.8 | 1.7 | 38.9 | 52.1 | 80 | 4775 | — |
| 2026-08-31 | 12.1 | 39.6 | 2927 | 2 | 3 | 36.5 | 52.7 | 76 | 4883 | — |
| 2026-08-24 | 13.8 | 33.7 | 1453 | 1.7 | 1.7 | 42.3 | 51.1 | 80 | 4941 | — |
| 2026-08-17 | 9.4 | 23.8 | 915 | — | 1.9 | 51 | 49.9 | 85 | 4987 | — |
| 2026-08-10 | 12.7 | 34.1 | 1519 | — | 1.9 | 37.7 | 53.4 | 73 | 5019 | 43 |
| 2026-08-03 | 7.3 | 17.5 | 1742 | — | 1.8 | 47.5 | 49.6 | 77 | 5046 | 44 |
| 2026-07-27 | 12.7 | 28 | 2694 | — | 3 | 40.9 | 49.6 | 79 | 5063 | 44 |
| 2026-07-20 | 13.2 | 26.9 | 1119 | 4.5 | 1.4 | 37.8 | 52.9 | 75 | 5068 | 44 |
| 2026-07-13 | 10.9 | 32 | 1752 | 18.7 | 1.7 | 41.1 | 51.6 | 84 | 5065 | 44 |
| 2026-07-06 | 11.4 | 24.3 | 2103 | 1.3 | 2.1 | 40 | 52.6 | 77 | 5067 | 45 |
| 2026-06-29 | 11.8 | 34.6 | 1280 | 18.7 | 1.1 | 42.2 | 52 | 78 | 5080 | 47 |
| 2026-06-22 | 9 | 29.5 | 883 | 21.3 | 2.2 | 39.3 | 50 | 77 | 5084 | 48 |
| 2026-06-15 | 7.7 | 30.7 | 2011 | 20.5 | 2.1 | 48.4 | 48.9 | 83 | 5102 | 49 |

Refresh with `make progress` after `python3 tracker/sync_garmin.py daily`.
