# Week over week

Generated 2026-09-28 from Supabase `weekly_progress` — Strava activities plus Garmin daily and training metrics, Monday-start weeks.

Arrows compare with the previous week. {{up}} and {{down}} are moving the way you want, {{up-bad}} and {{down-bad}} the wrong way, {{level}} is unchanged. Hover any arrow for what it means.

## Finish odds

**15–22%** — *well behind*, 46 weeks out.

That is the trajectory number: where the last eight weeks' rate of change lands on race day, measured against the final block's targets. Separately, you are at **67% of what Block 1 asks for right now** — that is a plan-adherence score, not a probability. Block 1 fitness would not finish this race; hitting Block 1 on time is what keeps the trajectory number climbing.

| Gate | Weight | vs Block 1 now | Projected race day |
|---|---|---|---|
| Vertical per week | 20% | `████████░░` 78% | `████████░░` 84% |
| Longest single day | 20% | `█████░░░░░` 50% | `██░░░░░░░░` 23% |
| Time on feet per week | 15% | `██████████` 100% | `██████████` 100% |
| Run-specific capacity | 15% | `███░░░░░░░` 35% | `█████░░░░░` 48% |
| Night hours | 10% | `███░░░░░░░` 33% | `█░░░░░░░░░` 11% |
| Week-to-week consistency | 10% | `████████░░` 75% | `████████░░` 75% |
| Recovery headroom | 10% | `██████████` 100% | `██████████` 100% |
| **Readiness** | | **67%** | **62%** |

Biggest drags on the trajectory number: **Night hours** and **Longest single day**.

> **How this is built.** Seven gates, each measured from Strava and Garmin, weighted as shown, averaged into a readiness score. The *now* column compares the last four to eight weeks against the current block's targets. The *projected* column fits the slope of the last eight weeks and carries it AT MOST 26 weeks, then holds it flat, against the final block's targets — it assumes you keep improving at exactly the rate you have been, no faster and no slower, which is why a flat eight weeks shows up as a flat projection. The readiness score is entirely measured. Turning it into a percentage needs a field-wide finish rate, and that part is an assumption: base rate 45–65% assumed for the FIELD at a 200-mile mountain race — Destination Trail does not publish starter counts — then scaled by how much of the distance ladder has actually been raced. Read the gate breakdown and the direction as signal; read the percentage as a rough band.

> **The ladder you have actually raced.** Longest finish: **a marathon in ~2006; no ultra finished yet**, so the band above is scaled to **45%** of the field's. This is the one input no API can supply and the one the model was missing until 2026-09-15 — it read the training data, saw a solid block, and applied a finish rate belonging to a field of experienced 200-mile runners. It climbs on its own as races get finished: a 50K takes it to 60%, a 100K to 80%, a 100-miler to 100%. Update `LONGEST_FINISH_MI` in `tracker/odds.py` after each one.

## Last complete week — 2026-09-21

### Volume

| | This week | Prior | Target | At target |
|---|---|---|---|---|
| Hours | 15.4 {{down-bad}} | 16.5 | 12 | 128% |
| Miles | 46.1 {{down-bad}} | 47.7 | 45 | 102% |
| Vertical (ft) | 3273 {{up}} | 1332 | 3500 | 94% |
| Longest day (hr) | 2 {{up}} | 1.7 | 6 | 33% |
| Best back-to-back (hr) | 5.7 {{down-bad}} | 5.9 | two consecutive days | — |
| Days on feet | 7 {{level}} | 7 | 5–6 | — |

### Race specificity

*Volume you can fake. This is the part that has to be real.*

| | This week | Prior | Target | At target |
|---|---|---|---|---|
| Vertical per hour | 213 {{up}} | 81 | 292 (race: 508) | 73% |
| Running share of miles (%) | 17 {{down-bad}} | 38 | 30 | 57% |
| Running miles | 8 {{down-bad}} | 18.4 | tolerance — | — |
| Night session hours | 0 {{down-bad}} | 1 | 3 cumulative this block | — |
| Avg HR on runs | 120 {{up}} | 115 | Z2 121–140 | — |

### Load and injury risk

| | This week | Prior | Target | At target |
|---|---|---|---|---|
| Acute load (7-day) | 298 | — | — | — |
| Acute:chronic ratio | 1.52 | — | 0.8–1.3 safe, >1.5 risky | — |
| Intensity minutes | 210 | — | — | — |

### Recovery

| | This week | Prior | Target | At target |
|---|---|---|---|---|
| HRV avg | 45.5 | — | 41.6 baseline | 109% |
| Days HRV not balanced | 0 | — | 0 of 7 | — |
| Resting HR | 51 | — | 51 baseline | — |
| Sleep (hr) | 9 | — | 7.5+ | — |
| Deep sleep (%) | 11 | — | 13–23 normal | — |
| Body battery low | 52 | — | how empty you get | — |
| Training readiness | 68 | — | — | — |
| Stress avg | 19 | — | under 35 | — |
| Respiration | 14.5 | — | a jump can precede illness | — |

### Fitness markers

| | This week | Prior | Target | At target |
|---|---|---|---|---|
| Endurance score | 4592 | — | — | — |
| VO2 max | 41.9 | — | — | — |
| Hill score | — | — | needs running on hills | — |

### What this changes

- **Acute:chronic 1.52 — ramping too fast.** Above 1.5 is where injuries come from. Hold volume flat for a week.
- **213 ft per hour against a 292 target** (race demands 508). Your hours are there; they are flat hours. Same time, steeper ground.
- **Running is 17% of your miles.** The long days are hikes. Run the runnable grades or run-specific fitness keeps sliding.
- **No night session.** Zero banked against 3 cumulative this block, and it is the cheapest gap you have — one headlamp lap counts.
- **Longest day 2 hr against an 6-hour block peak.** Single-day duration is the gap volume does not close.

## Last 13 weeks

| Week | Hr | Mi | Vert | ft/hr | Long | B2B | Run% | Night | ACWR | HRV | RHR | Sleep | Endur |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2026-09-28 *(partial)* | 1 | 3.4 | 121 | 126 | 1 | 1 | 0 | 0 | — | — | — | — | — |
| 2026-09-21 | 15.4 | 46.1 | 3273 | 213 | 2 | 5.7 | 17 | 0 | 1.52 | 45.5 | 51 | 9 | 4592 |
| 2026-09-14 | 16.5 | 47.7 | 1332 | 81 | 1.7 | 5.9 | 38 | 1 | — | — | — | — | — |
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

Refresh with `make progress` after `.venv/bin/python tracker/sync_garmin.py daily`.
