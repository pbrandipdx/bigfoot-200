# Bigfoot 200 — Block Targets & Monitoring

**Race:** **Friday August 13, 2027** · **200.1 mi · 44,082 ft gain · 45,563 ft loss** ·
107-hour cutoff · sub-100 hr for WS qualification
**49 weeks · 5 blocks.** Last revised **2026-09-15**.

> **The race is August 2027 and that is fixed.** It was briefly moved to 2028 on 2026-09-15 and
> Patrick moved it back the same day — everything revolves around this date.
>
> **What stands regardless: the race history in this plan was wrong.** It assumed a Gorge
> Waterfalls 100K finish. The real record is **a marathon around 2006 and a few half marathons
> this year — no ultra**, and a longest single effort of 3.0 hours. So the ladder below is six
> firsts in eleven months: first trail race in November, first ultra in December, first 100K in
> April, first 100-miler in June, first 200 in August. That is a very aggressive progression and
> it is recorded as such in `plan/plan-revisions.md` — not as an argument against the date, but
> so nobody later mistakes it for a gentle one.

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

> Blocks 5, 7 and 8 have no race chosen yet and are marked *draft* on the Review page.
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
for it. Blocks 5 and 8 each keep one, at 14 and 16 hours. Neither is an aerobic
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

> **Rescaled 2026-09-11, revised 2026-09-15.** The original targets were scaled from a
> baseline 27–43% above what was actually being trained, so they were shifted down one
> rung. The peak single efforts were lowered again on 2026-09-15 — see the progression
> table. The numbers below are the current ones.

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

## Block 2 — build
*Dec 13 2026 to Feb 13 2027 (9 weeks)*
*Ends: BURT 55K, then Hagg Mud 50K*

| Target | Value |
|---|---|
| Time on feet | **14 hr/week** |
| Vertical | **5,000 ft/week** (357 ft/hr) |
| On-foot miles | **50/week** |
| Peak single effort | **8 hr** |
| Volume long day, capped | **8 hr** |
| Night hours, cumulative | **6** |

**Block question:** can you go out again on tired legs, in bad weather, when nothing about it is enjoyable? This is the motivation block, not the fitness one.

**BURT is at 55K here — one 33-mile loop.** The 110K and 100-mile options are open and
the decision is Patrick's; the case for each is in `plan-revisions.md`. Whatever the
distance, the loop format is the point: a drop bag every few hours and timed transitions,
which is the aid-station discipline sub-100 depends on.

**Hagg Mud is nine days after BURT.** Check both dates before entering either.

---

## Block 3 — night running
*Feb 14 2027 to Apr 16 2027 (9 weeks)*
*Ends: Gorge Waterfalls 100K — FIRST 100K*

| Target | Value |
|---|---|
| Time on feet | **16 hr/week** |
| Vertical | **6,500 ft/week** (406 ft/hr) |
| On-foot miles | **55/week** |
| Peak single effort | **10 hr** |
| Volume long day, capped | **8 hr** |
| Night hours, cumulative | **12** |

**Block question:** can you move competently in the dark for six hours? Arriving at Gorge having never run at night is the avoidable failure here.

**This is the first 100K, against a 17-hour cutoff**, four months after a first-ever 50K.
Treat it as a debut to be finished, not a checkpoint to be paced.

---

## Block 4 — the gate
*Apr 17 2027 to Jun 18 2027 (9 weeks)*
*Ends: Strawberry Fields Forever 100 — FIRST 100-MILER, the gate*

| Target | Value |
|---|---|
| Time on feet | **18 hr/week** |
| Vertical | **8,000 ft/week** (444 ft/hr) |
| On-foot miles | **60/week** |
| Peak single effort | **14 hr** |
| Volume long day, capped | **8 hr** |
| Night hours, cumulative | **20** |

**Block question:** can you run through a night and keep functioning the next day? Everything about Bigfoot's second and third nights is decided here.

**The gate, and the first 100-miler, eight weeks before a 200.**

**Strawberry Fields Forever, North Bonneville WA, ~June 19 2027** — chosen 2026-09-15 over
Bighorn. A 10K loop run 16 times, ~3,200 ft total, 30-hour limit, 45 minutes from home, and
**you can drop to 100K or 50K and still take an official finish**. That last clause is why it
beat Bighorn: it converts the worst case from a DNF eight weeks before the A race into a
completed 100K. Bighorn was 18,000 ft, 9,000 ft of altitude, a flight to Wyoming, and no way
down from a bad day.

**It is not a Western States qualifier.** It does not need to be — Gorge Waterfalls in April
is, and Bigfoot under 100 hours is itself one.

**The flat course changes what the clock means.** Bighorn's "sub-28" standard was for
18,000 ft of mountain. On 3,200 ft of gravel and dirt trail, the equivalent signal is nearer
**sub-26**, and the time is the least interesting number anyway. Watch these instead:

| Read this | Not this |
|---|---|
| **Total aid time under 90 min** across 16 loop passes | the finish time on its own |
| **Second half no worse than 25% slower** than the first | how you felt at halfway |
| **Recovered in days, not weeks** | that you finished |

**Three outcomes, decided now while it is abstract:**

- **A hundred, controlled, aid under 90 min** → sub-100 at Bigfoot is live. Run the plan.
- **A hundred that cost you two weeks, or a drop to 100K** → Bigfoot is on, sub-100 is not.
  Race it to finish inside 107, enjoy it, qualify another way.
- **A drop to 50K, a DNF, or an injury finish** → defer Bigfoot. There is another one next
  year and there is only one of you.

Note the middle outcome. With the drop-down rule a true DNF is nearly impossible, so
**dropping to 100K is itself the signal** — it is what a bad day looks like here, and it should
be read as one rather than as a finish.

---

## Block 5 — peak + taper
*Jun 19 2027 to Aug 13 2027 (8 weeks)*
*Ends: BIGFOOT 200*

| Target | Value |
|---|---|
| Time on feet | **21 hr/week** |
| Vertical | **10,000 ft/week** (476 ft/hr) |
| On-foot miles | **65/week** |
| Peak single effort | **16 hr** |
| Volume long day, capped | **8 hr** |
| Night hours, cumulative | **30** |

**Block question:** nothing is asked of this block but arriving fresh.

| Weeks 1–2 | Full recovery from the first hundred. Walks only. |
|---|---|
| Weeks 3–5 | Peak: 20–22 hr/week, 10,000 ft/week, one 16 hr overnight |
| Week 6 | Reduce 40% |
| Weeks 7–8 | Taper. Legs fresh, sleep banked. |

Heat acclimation: 6 sessions — August in the Cascades is hot and exposed, and the
blast zone has no shade.

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
| 2 | 14 | 5,000 | 50 | 8 hr | 357 | 6 |
| 3 | 16 | 6,500 | 55 | 10 hr | 406 | 12 |
| 4 | 18 | 8,000 | 60 | 14 hr | 444 | 20 |
| 5 | 21 | 10,000 | 65 | 16 hr | 476 | 30 |
| *the race* | — | 44,082 total | 200.1 | 97 hr | **508 moving** | ~40 |

The **ft/hr** column is the one to watch: it climbs to just under race pace rather than
overshooting it. Cutting weekly hours without cutting vertical pushes it above 500 —
asking you to train steeper, every hour of every week, than you will ever race. Your last
complete week was **221**.

Cumulative vertical if every week is hit: **~304,500 ft** across 49 weeks, about **6.9×** the
race, or nearer **277,000** once deloads take their week in four.

**Peak single efforts were lowered on 2026-09-15** from 8/10/12/16/20 to **6/8/10/14/16**,
and the distinction that made that sensible still holds: a long day for *aerobic stimulus*
caps at 8 hours, while a long day for *night movement and a sleep stop* is a different
session and Blocks 4 and 5 keep one each. The lifetime longest single effort is 3.0 hours,
so an 8-hour Block 1 target was never going to be walked toward.

Generated from `plan/schedule.json` — if a number here disagrees with the site, the JSON
wins and this table needs regenerating.

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

Current **42.0**. Expect it to drift up as a byproduct of two years of volume. Not a target.

It will likely **decline during Blocks 8 and 9.** That is normal under high
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

- **7+ hr/night** through Blocks 1–8
- Sleep score 75+ on the two nights before any long day
- The deliberate sleep-deprived sessions in Blocks 7–8 are the *only* exception
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
| Blocks 2–4, 6–7 | **70–90 g/hr** | Build tolerance on every long day |
| Blocks 5, 8–9 | **90–100 g/hr** | Race rehearsal, with race food, from the pack |
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
2. **Strawberry Fields is a gate, not a formality** — and it is also the first 100-miler.
   A controlled hundred with aid under 90 min means sub-100 is live; a costly finish or a drop
   to 100K means race Bigfoot to finish inside 107; a drop to 50K or a DNF means defer.
   Decide it now, not in June.
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
