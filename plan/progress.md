# Week over week

Generated 2026-10-10 from Supabase `weekly_progress` — Strava activities plus Garmin daily and training metrics, Monday-start weeks.

Arrows compare with the previous week. {{up}} and {{down}} are moving the way you want, {{up-bad}} and {{down-bad}} the wrong way, {{level}} is unchanged. Hover any arrow for what it means.

## Finish odds

**18–26%** — *behind*, 96 weeks out.

That is the trajectory number: where the last eight weeks' rate of change lands on race day, measured against the final block's targets. Separately, you are at **79% of what Block 1 asks for right now** — that is a plan-adherence score, not a probability. Block 1 fitness would not finish this race; hitting Block 1 on time is what keeps the trajectory number climbing.

| Gate | Weight | vs Block 1 now | Projected race day |
|---|---|---|---|
| Vertical per week | 20% | `██████████` 100% | `██████████` 100% |
| Longest single day | 20% | `██████████` 98% | `█████████░` 90% |
| Time on feet per week | 15% | `██████████` 100% | `██████████` 100% |
| Run-specific capacity | 20% | `███░░░░░░░` 33% | `████░░░░░░` 44% |
| Night hours | 5% | `███░░░░░░░` 33% | `█░░░░░░░░░` 11% |
| Week-to-week consistency | 10% | `█████████░` 88% | `█████████░` 88% |
| Recovery headroom | 10% | `███████░░░` 75% | `███████░░░` 75% |
| **Readiness** | | **79%** | **79%** |

Biggest drags on the trajectory number: **Night hours** and **Recovery headroom**.

> **How this is built.** Seven gates, each measured from Strava and Garmin, weighted as shown, averaged into a readiness score. The *now* column compares the last four to eight weeks against the current block's targets. The *projected* column fits the slope of the last eight weeks and carries it AT MOST 26 weeks, then holds it flat, against the final block's targets — it assumes you keep improving at exactly the rate you have been, no faster and no slower, which is why a flat eight weeks shows up as a flat projection. The readiness score is entirely measured. Turning it into a percentage needs a field-wide finish rate, and that part is an assumption: base rate 45–65% assumed for the FIELD at a 200-mile mountain race — Destination Trail does not publish starter counts — then scaled by how much of the distance ladder has actually been raced. Read the gate breakdown and the direction as signal; read the percentage as a rough band.

> **The ladder you have actually raced.** Longest finish: **a marathon in ~2006; no ultra finished yet**, so the band above is scaled to **45%** of the field's. This is the one input no API can supply and the one the model was missing until 2026-09-15 — it read the training data, saw a solid block, and applied a finish rate belonging to a field of experienced 200-mile runners. It climbs on its own as races get finished: a 50K takes it to 60%, a 100K to 80%, a 100-miler to 100%. Update `LONGEST_FINISH_MI` in `tracker/odds.py` after each one.

## Last complete week — 2026-09-28

### Volume

| | This week | Prior | Target | At target |
|---|---|---|---|---|
| Hours | 23.8 {{up}} | 15.4 | 12 | 198% |
| Miles | 61.5 {{up}} | 46.1 | 45 | 137% |
| Vertical (ft) | 8990 {{up}} | 3273 | 3500 | 257% |
| Longest day (hr) | 5.9 {{up}} | 2 | 6 | 98% |
| Best back-to-back (hr) | 11.6 {{up}} | 5.7 | two consecutive days | — |
| Days on feet | 7 {{level}} | 7 | 5–6 | — |

### Race specificity

*Volume you can fake. This is the part that has to be real.*

| | This week | Prior | Target | At target |
|---|---|---|---|---|
| Vertical per hour | 377 {{up}} | 213 | 292 (race: 508) | 129% |
| Running share of miles (%) | 5 {{down-bad}} | 17 | 30 | 17% |
| Running miles | 3 {{down-bad}} | 8 | tolerance — | — |
| Night session hours | 0 | 0 | 3 cumulative this block | — |
| Avg HR on runs | 119 {{level}} | 121 | Z2 121–140 | — |

### Load and injury risk

| | This week | Prior | Target | At target |
|---|---|---|---|---|
| Acute load (7-day) | 221 {{down-bad}} | 296 | — | — |
| Acute:chronic ratio | 0.99 {{down-bad}} | 1.51 | 0.8–1.3 safe, >1.5 risky | — |
| Intensity minutes | 1453 {{up}} | 738 | — | — |

### Recovery

| | This week | Prior | Target | At target |
|---|---|---|---|---|
| HRV avg | 40 {{level}} | 39 | 41.6 baseline | 96% |
| Days HRV not balanced | 2 | 0 | 0 of 7 | — |
| Resting HR | 54.1 {{level}} | 53 | 51 baseline | — |
| Sleep (hr) | 8.1 {{down-bad}} | 8.6 | 7.5+ | — |
| Deep sleep (%) | 12 {{down-bad}} | 13 | 13–23 normal | — |
| Body battery low | 22 {{down-bad}} | 32 | how empty you get | — |
| Training readiness | 59 {{down-bad}} | 63 | — | — |
| Stress avg | 33 {{up-bad}} | 27 | under 35 | — |
| Respiration | 16.6 {{up-bad}} | 16.0 | a jump can precede illness | — |

### Fitness markers

| | This week | Prior | Target | At target |
|---|---|---|---|---|
| Endurance score | 4538 {{down-bad}} | 4597 | — | — |
| VO2 max | 42.0 {{level}} | 41.9 | — | — |
| Hill score | — | — | needs running on hills | — |

### What this changes

- **Running is 5% of your miles.** The long days are hikes. Run the runnable grades or run-specific fitness keeps sliding.
- **No night session.** Zero banked against 3 cumulative this block, and it is the cheapest gap you have — one headlamp lap counts.

## Last 13 weeks

| Week | Hr | Mi | Vert | ft/hr | Long | B2B | Run% | Night | ACWR | HRV | RHR | Sleep | Endur |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2026-10-05 *(partial)* | 7.4 | 23.2 | 787 | 106 | 1.6 | 3.8 | 26 | 0 | 0.74 | 36.7 | 56.3 | 7.5 | 4591 |
| 2026-09-28 | 23.8 | 61.5 | 8990 | 377 | 5.9 | 11.6 | 5 | 0 | 0.99 | 40 | 54.1 | 8.1 | 4538 |
| 2026-09-21 | 15.4 | 46.1 | 3273 | 213 | 2 | 5.7 | 17 | 0 | 1.51 | 39 | 53 | 8.6 | 4597 |
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

Refresh with `make progress` after `.venv/bin/python tracker/sync_garmin.py daily`.
