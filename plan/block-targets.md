# Bigfoot 200 — Block Targets & Monitoring

**Race:** **August 2028** (est. Friday Aug 11, unconfirmed) · **200.1 mi · 44,082 ft gain ·
45,563 ft loss** · 107-hour cutoff · sub-100 hr for WS qualification
**101 weeks · 9 blocks.** Last revised **2026-09-15**.

> **Moved from 2027 on 2026-09-15.** The plan was built on a race history that turned out to be
> wrong — it assumed a Gorge Waterfalls 100K finish; the real record is a marathon twenty years
> ago and a few halves this year, with no ultra at all. 2027 is now the apprenticeship year:
> first ultra in December, first 100K in April, first 100-miler in the autumn. Blocks 2–9 are
> drafts until their races are chosen. Full reasoning in `plan/plan-revisions.md`.

> Course figures corrected 2026-09-15. This page previously said 200–208 mi /
> 44,000–45,500 ft, which describes the **retired** version of the course with
> aid at Windy Ridge and Johnston Ridge. The numbers above come from the
> official manual and sum exactly — see `sub100-plan.md`.

---

## The long day is Sunday

Moved from Saturday on 2026-09-12. Saturday is now recovery — up to 6 miles,
easy — or day one of a back-to-back weekend. Races and the Three Sisters
multi-day keep their real dates, which are Saturdays; the Sunday after one of
those is recovery or day two, not a fresh long day. `plan/schedule.json` keys
the dated progression by DATE (`longDays`), not by weekday, so nothing has to
be re-dated if a weekend moves again.

---

## The week, rebuilt 2026-09-15

> The full argument behind this rebuild — what an outside review got right, what
> it got wrong, and what was rejected — is in `plan/plan-revisions.md`. The
> review itself is archived at `plan/reviews/`.

Five running days. Run-specific capacity is the weakest gate in the model —
**21% now, projecting 25%** — and Bigfoot is only a hiking race if you are
willing to walk the runnable two thirds of it. Sub-100 lives in the parts you
can still run on day four.

| Day | Session |
|---|---|
| **Monday** | **Full rest.** No running, no strength, no capped walk that becomes three miles. |
| **Tuesday** | **Uphill tempo + power strides.** 3×5 → 3×10 → 2×15 on a three-week ladder, Z3, then 5×20 sec strides at ~85% effort on a moderate grade. |
| **Wednesday** | **Easy Z2 run + eccentric strength.** Single-leg box step-downs 3×10, weighted step-ups with the pack 3×12, single-leg RDLs 3×10, loaded carries. |
| **Thursday** | **Sustained downhill.** 15 → 20 → 25 min of *continuous* descent, on rock, late in the day. |
| **Friday** | **Recovery jog**, Z1. |
| **Saturday** | Recovery, or day one of a back-to-back, or a race. |
| **Sunday** | **The long day.** |

Session length ramps by block — 45 min midweek in Block 1, up to 90 on
Thursdays by Block 4 — because **frequency, not one big day, is how running
tolerance rises.** Five short days already spends a 12 mi/week tolerance.

**The release valve, stated on every running day:** if the week's running miles
are at or over Garmin's current running tolerance, **Friday becomes a walk**
before anything else is cut.

### What this replaced, and why

- **Monday's incline intervals** were the only vertical-specific session and
  they never got harder. The uphill ladder on Tuesday progresses.
- **The LeBron ramp** was a fixed 10–12 reps, forever, described in the plan's
  own notes as "not a vertical-volume session." It is now the downhill day.
- **Sustained downhill did not exist.** `coaching-references.md` has named it as
  gap #1 since September 11 — *"the most race-specific session available and
  completely absent"* — while the course loses 45,563 ft, more than it climbs.
  The one measured descent gap, Sep 13, was **8 bpm against a ≥15 target**.
- **Strength was generic.** It is now eccentric and single-leg, which is the
  quality that fails on descent.

### The long day has two different jobs, and only one has a cap

A long day run for **aerobic stimulus** is capped at **8 hours**. Past that the
musculoskeletal damage and recovery debt climb faster than the aerobic return;
Koop's worked progression tops out near 8, and Burt prefers back-to-backs
precisely because they cost less than one enormous effort.

A long day run for **night movement, a real sleep stop, and aid rehearsal** is a
different session with a different purpose, and back-to-backs cannot substitute
for it. Blocks 4 and 5 each keep one, at 14 and 16 hours. Neither is an aerobic
workout — they exist so that hour 18, in the dark, alone, is not new information
on race day.

This is why the peak-day numbers dropped from 8/10/12/16/20 to **6/8/10/14/16**,
and it is worth being blunt about the consequence: *longest single day* is a
20%-weight gate in the odds model. Lowering the target raises that gate's
percentage without you having done anything. The number will move for a reason
that is not fitness.

---

## How to read this

**Targets** are things you train toward and either hit or miss.
**Monitors** are things you watch. They have thresholds, not goals. Chasing them
is how people overtrain.

Primary progression metrics are **time on feet** and **vertical gain**. Miles are
listed because you asked, but for a race that's 219 ft of climb per mile, they're
the least informative number here.

---

## Baseline — where you are today

| Metric | Current |
|---|---|
| Time on feet | **8.8 hr/week** as measured on 2026-09-11 (plan assumed ~12). **But across the full 15 weeks in the database, May 25 – Sep 6, the average is 11.0 hr** — see the Review tab. The 8.8 came from a shorter window, and the whole ladder was rescaled down from it. Worth deciding whether the rescale went one rung too far. |
| Vertical | **~1,700 ft/week measured** (plan assumed ~3,000) · 15-week average **1,659 ft**, which the 1,700 figure matches · 62,182 ft YTD 2026 |
| On-foot miles | **~29/week measured** (plan assumed 40–45) · 15-week average **30.0** |
| Longest single DAY | 5:03 across several activities, 18.26 mi, 1,985 ft |
| **Longest single EFFORT** | **3:00** — the largest `moving_time` in all 208 logged activities. This is the number that matters for a 200-mile race, and it is the one the peak-day targets ramp from. |
| Max HR | **196** — corrected 2026-09-14. Every reading above it (233, 210, 209, 207, 205) came on a day with no logged workout: optical-sensor artifact, not effort. Highest on a genuinely hard day is 196. Strava was using an age-derived ~185. |
| Zone 2 / Zone 3 | 121–140 / 141–163 |
| Resting HR | 51 (7-day avg 52) |
| VO2 max | 42.0 → **~42–43**, ticked up early September |
| Night hours | 0 |
| **Hill score** | **no data — Garmin has never computed one** |
| **Endurance score** | **4,758** (peak 5,088, 12-wk avg 4,999) — *falling* |
| **Running tolerance** | **12 mi/week**, actual 7-day 5.8 mi — "Low impact load" |
| HRV status | **Unbalanced since ~Sep 7** (balanced 42–50 through Sep 5) |

*Baselines measured 2026-09-11 from Strava and Garmin Connect; stored in the
`bigfoot-200-training` Supabase project (`garmin_daily`, `garmin_training`,
`activities`) with full provenance in each row's `raw`.*

> **The plan was written off an overstated baseline.** Time on feet, vertical and
> miles are all 27–43% below what the block targets were scaled from. Every
> target below inherits that error and should be read as aspirational rather
> than calibrated until rescaled.

---

## Block 1 — base + vertical intro
*Sep 7 2026 to Dec 12 2026 (14 weeks)*
*Ends: Frozen Trail Run Fest 50K — FIRST ULTRA*

| Target | Value |
|---|---|
| Time on feet | **12 hr/week** |
| Vertical | **3,500 ft/week** (292 ft/hr) |
| On-foot miles | **45/week** |
| Peak single effort | **6 hr** |
| Volume long day, capped | **8 hr** |
| Night hours, cumulative | **3** |

**Block question:** can you sustain a full day on feet and descend hard without wrecking your quads?

---

## Block 2 — winter build
*Dec 13 2026 to Feb 13 2027 (9 weeks)*
*Ends: BURT 55K — one loop, aid-station rehearsal* · **draft — race not chosen**

| Target | Value |
|---|---|
| Time on feet | **13 hr/week** |
| Vertical | **4,000 ft/week** (308 ft/hr) |
| On-foot miles | **45/week** |
| Peak single effort | **8 hr** |
| Volume long day, capped | **8 hr** |
| Night hours, cumulative | **6** |

**Block question:** can you go out again on tired legs, in bad weather, when nothing about it is enjoyable? This is the motivation block, not the fitness one.

---

## Block 3 — first 100K
*Feb 14 2027 to Apr 17 2027 (9 weeks)*
*Ends: Gorge Waterfalls 100K — FIRST 100K* · **draft — race not chosen**

| Target | Value |
|---|---|
| Time on feet | **14 hr/week** |
| Vertical | **5,000 ft/week** (357 ft/hr) |
| On-foot miles | **50/week** |
| Peak single effort | **10 hr** |
| Volume long day, capped | **8 hr** |
| Night hours, cumulative | **10** |

**Block question:** can you cover 100 km, in one push, inside a cutoff? This is the first real gate of the apprenticeship year.

---

## Block 4 — recover, base, recon
*Apr 18 2027 to Aug 15 2027 (17 weeks)*
*Ends: Bigfoot 200 2027 — as a volunteer, not a runner* · **draft — race not chosen**

| Target | Value |
|---|---|
| Time on feet | **11 hr/week** |
| Vertical | **3,500 ft/week** (318 ft/hr) |
| On-foot miles | **40/week** |
| Peak single effort | **8 hr** |
| Volume long day, capped | **8 hr** |
| Night hours, cumulative | **12** |

**Block question:** can you recover properly, hold a base through summer, and learn the course with your own eyes rather than a map?

**August 2027: work Bigfoot as a volunteer, not a runner.** Crew someone, or take an
aid-station shift. You see the course, the aid stations, and what people look like at
mile 130 on night three — a year before you run it. It is free, it carries no injury
risk, and it is better education than any training block in this document.

---

## Block 5 — first 100-mile build
*Aug 16 2027 to Oct 31 2027 (11 weeks)*
*Ends: First 100-miler — race TBD* · **draft — race not chosen**

| Target | Value |
|---|---|
| Time on feet | **15 hr/week** |
| Vertical | **6,000 ft/week** (400 ft/hr) |
| On-foot miles | **50/week** |
| Peak single effort | **14 hr** |
| Volume long day, capped | **8 hr** |
| Night hours, cumulative | **16** |

**Block question:** can you go a hundred miles? Everything in year two assumes the answer is yes.

**The race is not chosen yet.** October 2027 is a placeholder. Wanted: supported,
forgiving cutoff, reachable from Portland, and not technical. This is a first hundred —
the goal is to finish one, not to race one.

---

## Block 6 — winter base + night
*Nov 1 2027 to Feb 13 2028 (15 weeks)*
*Ends: no race — night hours and durability* · **draft — race not chosen**

| Target | Value |
|---|---|
| Time on feet | **13 hr/week** |
| Vertical | **5,000 ft/week** (385 ft/hr) |
| On-foot miles | **45/week** |
| Peak single effort | **10 hr** |
| Volume long day, capped | **8 hr** |
| Night hours, cumulative | **20** |

**Block question:** can you keep a base through a second PNW winter without a race to point at? This block has no finish line, which is its difficulty.

---

## Block 7 — build + night running
*Feb 14 2028 to Apr 16 2028 (9 weeks)*
*Ends: a 100K or 50-miler tune-up — TBD* · **draft — race not chosen**

| Target | Value |
|---|---|
| Time on feet | **16 hr/week** |
| Vertical | **6,500 ft/week** (406 ft/hr) |
| On-foot miles | **55/week** |
| Peak single effort | **12 hr** |
| Volume long day, capped | **8 hr** |
| Night hours, cumulative | **26** |

**Block question:** can you move competently in the dark, for hours, repeatedly?

---

## Block 8 — the gate
*Apr 17 2028 to Jun 18 2028 (9 weeks)*
*Ends: 100-miler — THE GATE, race TBD* · **draft — race not chosen**

| Target | Value |
|---|---|
| Time on feet | **18 hr/week** |
| Vertical | **8,000 ft/week** (444 ft/hr) |
| On-foot miles | **60/week** |
| Peak single effort | **16 hr** |
| Volume long day, capped | **8 hr** |
| Night hours, cumulative | **32** |

**Block question:** can you run a hundred miles WELL — controlled, disciplined at aid, recovered in days rather than weeks?

**The gate.** A controlled finish with disciplined aid means sub-100 at Bigfoot is live.
A finish that costs two weeks means Bigfoot is on and sub-100 is not. A DNF or an injury
finish means defer. Written down now, while it is abstract.

---

## Block 9 — peak + taper
*Jun 19 2028 to Aug 11 2028 (8 weeks)*
*Ends: BIGFOOT 200* · **draft — race not chosen**

| Target | Value |
|---|---|
| Time on feet | **20 hr/week** |
| Vertical | **10,000 ft/week** (500 ft/hr) |
| On-foot miles | **60/week** |
| Peak single effort | **18 hr** |
| Volume long day, capped | **8 hr** |
| Night hours, cumulative | **40** |

**Block question:** nothing is asked of this block but arriving fresh.

---

## Deload weeks

Every fourth week runs at **60–70% of that block's targets** — volume down, intensity
down, the long day cut in half. Adaptation happens during the easy week, not the hard one.

**Block 1's deloads are anchored to races rather than a rigid count**, which puts them
where the fatigue actually lands:

| Week | Date | Why |
|---|---|---|
| 5 | Oct 11 | Recovery from the Three Sisters multi-day |
| 10 | Nov 15 | Recovery from Run the Rock |
| 13 | Dec 6 | Taper into Frozen Trail 50K, Dec 12 |

**Blocks 2–9:** weeks 4 and 8 of each block, same 60–70% rule. The site detects a deload
from the Sunday long day's own title where one is dated, and falls back to every fourth
week where none is — so the uphill ladder pauses on the right weeks either way.

A deload is not a rest week — keep the frequency, cut the duration. Miss the deload and
the following block starts on a deficit.

## Progression at a glance

| Block | Hr/wk | Vert/wk | Miles/wk | Peak effort | ft/hr | Night hrs |
|---|---|---|---|---|---|---|
| Now (measured) | 11.0 | 1,659 | 30 | **3.0 hr** | 221 | 0 |
| 1 | 12 | 3,500 | 45 | 6 hr | 292 | 3 |
| 2 | 13 | 4,000 | 45 | 8 hr | 308 | 6 |
| 3 | 14 | 5,000 | 50 | 10 hr | 357 | 10 |
| 4 | 11 | 3,500 | 40 | 8 hr | 318 | 12 |
| 5 | 15 | 6,000 | 50 | 14 hr | 400 | 16 |
| 6 | 13 | 5,000 | 45 | 10 hr | 385 | 20 |
| 7 | 16 | 6,500 | 55 | 12 hr | 406 | 26 |
| 8 | 18 | 8,000 | 60 | 16 hr | 444 | 32 |
| 9 | 20 | 10,000 | 60 | 18 hr | 500 | 40 |
| *the race* | — | 44,082 total | 200.1 | 97 hr | **508 moving** | ~40 |

The **ft/hr** column is the one to watch: it climbs to just under race pace rather than
overshooting it. Cutting weekly hours without cutting vertical pushes it above 500 —
asking you to train steeper, every hour of every week, than you will ever race. Your last
complete week was **221**.

Cumulative vertical if every week is hit: **~541,000 ft** across 101 weeks, or nearer
**490,000** once deloads take their week in four. Do not read that as a multiple of the race —
the old plan's "6.2×" was over one year and this is over two, so the ratio changed without the
training changing. The number that matters is the **weekly** one, and week for week this is a
gentler plan than the 2027 version, not a bigger one.

**Rebuilt 2026-09-15** when the race moved to August 2028 and the plan went from 5 blocks
to 9. Blocks 2–9 are drafts until their races are chosen. Generated from
`plan/schedule.json` — if a number here disagrees with the site, the JSON wins and this
table needs regenerating.

# Monitors — thresholds, not goals

## Aerobic durability (the real predictor)

**Descent HR gap.** On any long day, average HR on sustained descent versus
sustained climb.
- Baseline: 15–20 bpm
- **Measured Sep 5 (hike, 3.0 hr): 15 bpm** — climb 138, descent 122. Passing.
- **Measured Sep 13 (trail run, 1.9 hr): 8 bpm** — climb 122, descent 114.
  Failing, on a short day that should have been comfortable.
- July 19 comparison: 2 bpm — the fatigued pattern
- **Watch:** gap under 10 bpm on a day that should be comfortable means
  under-recovery. Two in a row, cut the week.
- This is the monitor Thursday's sustained-downhill session exists to move.

**Aerobic decoupling.** Pace-to-HR ratio, first half vs second half of long days.
- Target: **under 5%** on aerobic efforts
- Above 8% consistently means the day was too hard or you're under-recovered

**Zone discipline.** Long days should sit **125–140 bpm** (mid-Z2).
- Over 15% of a long day above 150 means it was a workout, not a long day

## Training load — an action, not just a reading

**Acute:chronic workload ratio.** The weekly report has always printed this and
never told you to do anything with it.

- **0.8–1.3:** the band to live in
- **Above 1.45:** cut the weekend long day by 30%. Do not add on top of it.
- **Below 0.8 for three weeks:** you are detraining, not recovering

It went **0.73 → 1.40 in a single week** at the start of Block 1. A number that
moves that fast needs a rule attached to it. *(Added 2026-09-15.)*

## Running tolerance — the guardrail on five running days

Garmin computes this. It was **12 mi/week** at baseline with status *"Low impact
load."* The week is now built around five running days, which makes this the
binding constraint rather than a curiosity.

- **Weekly running miles stay at or under tolerance.** Over it repeatedly is the
  clearest overtraining signal available.
- **Raise it by frequency, not by one big day** — which is exactly what the five
  short midweek sessions are for.
- **Cap the ramp at 10%/week** (Holz). 12 → 14.5 → 17.6 → 21.3 → ~26 by Nov 7.
- **When running miles reach tolerance, Friday becomes a walk.** That is the
  release valve, and it is deliberately the smallest session of the week so that
  spending it costs nothing.

The reason this matters more than weekly hours: hours went to **126% of target**
in the week of Sep 7 while running was **10 miles against a 12-mile tolerance**
— up from 2 the week before. In hours that looks like a good week. In impact
load it is the steepest thing in the plan. *(Added 2026-09-15.)*

## VO2 max — monitor, do not chase

Current **42.0**. Expect 43–46 by Bighorn as a byproduct.

It will likely **decline during Blocks 4 and 5.** That is normal under high
volume and is not a warning sign. For a 105-hour race, VO2 max is close to
irrelevant. If you find yourself training to move this number, you are training
for the wrong race.

## HRV — trend only, never a single day

Establish a **30-day rolling baseline** once the Garmin backfill runs.

- Single low day: ignore
- **Status "Unbalanced" 4 consecutive days:** downgrade — Tuesday's intervals and
  Thursday's descent become easy Z1, everything else stands. Four days is a real
  signal, and seven was too late to act on. *(Added 2026-09-15.)*
- **7-day average down >10% from baseline:** cut volume 30% that week
- **Status "Unbalanced" for 7+ consecutive days:** take 3 full days off
- Rising or stable through a build block: the load is being absorbed

As of the week of 2026-09-07 this sat at **6 of 7 days unbalanced** — past the
new downgrade trigger, one day short of the stop trigger.

## Resting HR

- Establish baseline from backfill
- **+5 bpm sustained over 5 days:** back off
- **+8 bpm:** stop and check for illness

## Sleep — the counterintuitive one

Train **rested**, race deprived.

- **7+ hr/night** through Blocks 1–4
- Sleep score 75+ on the two nights before any long day
- The deliberate sleep-deprived sessions in Block 4 are the *only* exception
- Chronic under-sleeping during a build is how this goes wrong

## Body Battery

- **Morning of a long day: 70+.** Under 50, downgrade the session.
- Overnight recharge under 30 for three straight nights means accumulated fatigue

## Garmin performance metrics — baselined 2026-09-11

All three are now measured. All three say the same thing: **running-specific
capacity has gone backwards since running stopped in late July.**

### Hill score — **no data**

Garmin has never computed one. It is derived from running on hills, and there
has not been enough of that for the metric to exist. Your plan calls this "the
most Bigfoot-relevant number Garmin produces"; right now it is blank, and the
blankness *is* the finding.

- **Threshold:** get it to exist. One hilly run is enough to start it.
- Once it exists: should rise through every block. Flat or falling during a
  climbing block means the vert isn't being absorbed.

### Endurance score — **4,758, declining**

| Week | Score |
|---|---|
| Jul 25–31 | 5,059 |
| Aug 8–14 | 5,012 |
| Aug 15–21 | 4,984 |
| Aug 22–28 | 4,922 |
| Aug 29–Sep 4 | 4,873 |
| **Sep 5–11** | **4,758** |

Peak 5,088 → 4,758. Down 330 points (−6.5%) over twelve weeks, and accelerating
— the largest single drop was this week. Level: Intermediate.

- **Threshold:** stop the decline by the end of September. Back above 5,000 by
  the Dec 12 Frozen Trail checkpoint.
- Three consecutive falling weeks during a build block means the block is not
  being absorbed — rebuild it rather than stacking on top.

### Running tolerance — **12 mi/week**

Acute impact load 4.9 mi · actual 7-day distance 5.8 mi · status **"Low impact
load."** Garmin's own guidance: *"Your impact load has been low for several
weeks. Increase impact load gradually after a lighter period like this."*

- **Threshold:** weekly running miles stay under tolerance. Exceeding it
  repeatedly is the clearest overtraining signal available.
- **Why Run the Rock is the 25K, not the 50K.** At Holz's 10%/week ramp,
  tolerance goes 12 → 14.5 → 17.6 → 21.3 → **~26 mi by Nov 7**. The 50K is 31
  running miles with 5,000 ft and a 10-hour cutoff needing 3.11 mph held from
  the gun. You arrive under the requirement even on a perfect ramp. The 25K is
  ~4–5 hours, still a real Block 1 checkpoint, and costs days of recovery
  instead of weeks.
- Gorge Waterfalls in April is 62 miles against a 17-hour cutoff. That is the
  race the running ramp has to actually reach, and there are seven months for it.
- Raise it by frequency, not by one big day. Three easy midweek runs — which is
  what you were doing through Jul 21 — plus running the runnable parts of the
  weekly long day.

### Why all three moved together

Running stopped around Jul 22. Aerobic fitness is fine — VO2 max ticked *up* to
~42–43, sleep is good, body battery recovers to ~79. What has degraded is
running-specific capacity, which is a different thing and the thing the race
ladder actually requires.

### HRV — first real signal, 2026-09-11

Balanced at 42–50 ms inside the baseline band through ~Sep 5. **Unbalanced from
~Sep 7** at 35–38, below the band, with one Low day around Sep 9 — beginning
two days after Block 1 opened and acute training load climbed from ~200 to ~300
(top edge of optimal). Sleep and body battery are unaffected so far.

Under the HRV rules above, five days of Unbalanced is not yet the three-days-off
trigger, but a seventh consecutive day is.

---

## Missing sessions — adopted 2026-09-15

`coaching-references.md` named three gaps on 2026-09-11. All three are now in
the week rather than in a list of things to do:

1. **Sustained downhill, continuous.** ✅ Thursday, its own session, 15 → 20 →
   25 min of unbroken descent, on rock, late in the day. Was gap #1 for four
   days while nothing in the week descended on purpose.
2. **Uphill tempo intervals, progressed.** ✅ Tuesday, 3×5 → 3×10 → 2×15 on a
   three-week ladder that pauses for deloads rather than resetting.
3. **A carbohydrate number.** ✅ Ramp it rather than starting at the ceiling:

| When | Target | Why |
|---|---|---|
| Block 1 | **60–70 g/hr** | Start where your gut already is |
| Block 2–3 | **70–90 g/hr** | Build tolerance on every long day |
| Block 4–5 | **90–100 g/hr** | Race rehearsal, with race food, from the pack |
| Ceiling | 120 g/hr (Holz) | Only if the gut gets there — it is trained, not chosen |

Rehearse on **every** long day with the food you will actually carry. "Eat every
40 minutes" stays as the timer; the grams are what it is timing.

Also worth noting: Holz caps weekly progression at **10%**, and this plan steps
13–20% between blocks off a baseline that was already overstated. That cap now
has a rule attached for the metric where it bites hardest — see *Running
tolerance* above.

## Non-negotiables

1. **Night hours accumulate on schedule.** Zero today. This is the cheapest gap
   to close and the one most likely to be skipped.
2. **Bighorn is a gate, not a formality.** Decide the rule now.
3. **Descent training happens on rock**, not loam, and late in the day.
4. **Feet get managed from hour five**, not hour nine. Practice in training.
5. **Eat every 40 minutes** on every long day, including when you don't want to —
   and hit the gram target above, not just the timer.
6. **Friday is the release valve.** When running miles reach tolerance, it
   becomes a walk. Cutting Friday is cheap; cutting Thursday or Sunday is not.

---

## Review cadence

End of each block, against that block's targets:

1. Did time on feet, vertical, and peak day hit?
2. Did the descent HR gap hold?
3. Did night hours accumulate?
4. What did hill score and endurance score do?
5. Did the checkpoint race meet its pace target?

Three or more misses means the next block gets rebuilt, not stacked on top.
