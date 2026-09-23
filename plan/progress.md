# Week over week

Generated 2026-09-23 from Supabase `weekly_progress` — Strava activities plus Garmin daily and training metrics, Monday-start weeks.

Arrows compare with the previous week. {{up}} and {{down}} are moving the way you want, {{up-bad}} and {{down-bad}} the wrong way, {{level}} is unchanged. Hover any arrow for what it means.

## Finish odds

**9–13%** — *well behind*, 46 weeks out.

That is the trajectory number: where the last eight weeks' rate of change lands on race day, measured against the final block's targets. Separately, you are at **53% of what Block 1 asks for right now** — that is a plan-adherence score, not a probability. Block 1 fitness would not finish this race; hitting Block 1 on time is what keeps the trajectory number climbing.

| Gate | Weight | vs Block 1 now | Projected race day |
|---|---|---|---|
| Vertical per week | 20% | `██████░░░░` 59% | `█░░░░░░░░░` 13% |
| Longest single day | 20% | `█████░░░░░` 50% | `██░░░░░░░░` 19% |
| Time on feet per week | 15% | `██████████` 97% | `████░░░░░░` 44% |
| Run-specific capacity | 15% | `██░░░░░░░░` 24% | `███░░░░░░░` 30% |
| Night hours | 10% | `░░░░░░░░░░` 0% | `░░░░░░░░░░` 0% |
| Week-to-week consistency | 10% | `██████░░░░` 62% | `██████░░░░` 62% |
| Recovery headroom | 10% | `███████░░░` 68% | `███████░░░` 68% |
| **Readiness** | | **53%** | **30%** |

Biggest drags on the trajectory number: **Night hours** and **Vertical per week**.

> **How this is built.** Seven gates, each measured from Strava and Garmin, weighted as shown, averaged into a readiness score. The *now* column compares the last four to eight weeks against the current block's targets. The *projected* column fits the slope of the last eight weeks and carries it AT MOST 26 weeks, then holds it flat, against the final block's targets — it assumes you keep improving at exactly the rate you have been, no faster and no slower, which is why a flat eight weeks shows up as a flat projection. The readiness score is entirely measured. Turning it into a percentage needs a field-wide finish rate, and that part is an assumption: base rate 45–65% assumed for the FIELD at a 200-mile mountain race — Destination Trail does not publish starter counts — then scaled by how much of the distance ladder has actually been raced. Read the gate breakdown and the direction as signal; read the percentage as a rough band.

> **The ladder you have actually raced.** Longest finish: **a marathon in ~2006; no ultra finished yet**, so the band above is scaled to **45%** of the field's. This is the one input no API can supply and the one the model was missing until 2026-09-15 — it read the training data, saw a solid block, and applied a finish rate belonging to a field of experienced 200-mile runners. It climbs on its own as races get finished: a 50K takes it to 60%, a 100K to 80%, a 100-miler to 100%. Update `LONGEST_FINISH_MI` in `tracker/odds.py` after each one.

## Last complete week — 2026-09-14

### Volume

| | This week | Prior | Target | At target |
|---|---|---|---|---|
| Hours | 5.6 {{down-bad}} | 15.1 | 12 | 47% |
| Miles | 15.3 {{down-bad}} | 36.6 | 45 | 34% |
| Vertical (ft) | 528 {{down-bad}} | 3333 | 3500 | 15% |
| Longest day (hr) | 1.5 {{down-bad}} | 2.1 | 6 | 25% |
| Best back-to-back (hr) | 3.6 {{down-bad}} | 5.4 | two consecutive days | — |
| Days on feet | 3 {{down-bad}} | 7 | 5–6 | — |

### Race specificity

*Volume you can fake. This is the part that has to be real.*

| | This week | Prior | Target | At target |
|---|---|---|---|---|
| Vertical per hour | 94 {{down-bad}} | 221 | 292 (race: 508) | 32% |
| Running share of miles (%) | 44 {{up}} | 27 | 30 | 147% |
| Running miles | 6.7 {{down-bad}} | 10 | tolerance — | — |
| Night session hours | 0 | 0 | 3 cumulative this block | — |
| Avg HR on runs | 125 {{up}} | 120 | Z2 121–140 | — |

### Load and injury risk

| | This week | Prior | Target | At target |
|---|---|---|---|---|
| Acute load (7-day) | — | 263 | — | — |
| Acute:chronic ratio | — | 1.40 | 0.8–1.3 safe, >1.5 risky | — |
| Intensity minutes | — | 780 | — | — |

### Recovery

| | This week | Prior | Target | At target |
|---|---|---|---|---|
| HRV avg | — | 38.9 | 41.6 baseline | — |
| Days HRV not balanced | — | 6 | 0 of 7 | — |
| Resting HR | — | 52.1 | 51 baseline | — |
| Sleep (hr) | — | 8.7 | 7.5+ | — |
| Deep sleep (%) | — | 13 | 13–23 normal | — |
| Body battery low | — | 20 | how empty you get | — |
| Training readiness | — | 45 | — | — |
| Stress avg | — | 31 | under 35 | — |
| Respiration | — | 16.0 | a jump can precede illness | — |

### Fitness markers

| | This week | Prior | Target | At target |
|---|---|---|---|---|
| Endurance score | — | 4775 | — | — |
| VO2 max | — | 42.1 | — | — |
| Hill score | — | — | needs running on hills | — |

### What this changes

- **94 ft per hour against a 292 target** (race demands 508). Your hours are there; they are flat hours. Same time, steeper ground.
- **No night session.** Zero banked against 3 cumulative this block, and it is the cheapest gap you have — one headlamp lap counts.
- **Longest day 1.5 hr against an 6-hour block peak.** Single-day duration is the gap volume does not close.

## Last 13 weeks

| Week | Hr | Mi | Vert | ft/hr | Long | B2B | Run% | Night | ACWR | HRV | RHR | Sleep | Endur |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2026-09-14 | 5.6 | 15.3 | 528 | 94 | 1.5 | 3.6 | 44 | 0 | — | — | — | — | — |
| 2026-09-07 | 15.1 | 36.6 | 3333 | 221 | 2.1 | 5.4 | 27 | 0 | 1.40 | 38.9 | 52.1 | 8.7 | 4775 |
| 2026-08-31 | 12.1 | 39.6 | 2927 | 242 | 3 | 6.8 | 5 | 0 | 0.73 | 36.5 | 52.7 | 8.7 | 4883 |
| 2026-08-24 | 13.8 | 33.7 | 1453 | 105 | 1.7 | 5.4 | 5 | 0 | 0.98 | 42.3 | 51.1 | 7.8 | 4941 |
| 2026-08-17 | 9.4 | 23.8 | 915 | 98 | 1.9 | 5.5 | 0 | 0 | 0.92 | 51 | 49.9 | 8.3 | 4987 |
| 2026-08-10 | 12.7 | 34.1 | 1519 | 120 | 1.9 | 4.9 | 0 | 0 | 1.26 | 37.7 | 53.4 | 7 | 5019 |
| 2026-08-03 | 7.3 | 17.5 | 1742 | 240 | 1.8 | 4.2 | 0 | 0 | 0.70 | 47.5 | 49.6 | 7.5 | 5046 |
| 2026-07-27 | 12.7 | 28 | 2694 | 212 | 3 | 4.7 | 0 | 0 | 1.14 | 40.9 | 49.6 | 8.3 | 5063 |
| 2026-07-20 | 13.2 | 26.9 | 1119 | 85 | 1.4 | 5.3 | 17 | 0 | 1.04 | 37.8 | 52.9 | 7.8 | 5068 |
| 2026-07-13 | 10.9 | 32 | 1752 | 160 | 1.7 | 4 | 58 | 0 | 0.54 | 41.1 | 51.6 | 8.3 | 5065 |
| 2026-07-06 | 11.4 | 24.3 | 2103 | 185 | 2.1 | 4.9 | 5 | 0 | 0.63 | 40 | 52.6 | 7.8 | 5067 |
| 2026-06-29 | 11.8 | 34.6 | 1280 | 108 | 1.1 | 5.4 | 54 | 0 | 0.84 | 42.2 | 52 | 7.2 | 5080 |
| 2026-06-22 | 9 | 29.5 | 883 | 98 | 2.2 | 4.1 | 72 | 0 | 0.71 | 39.3 | 50 | 7.7 | 5084 |

Refresh with `make progress` after `.venv/bin/python tracker/sync_garmin.py daily`.
