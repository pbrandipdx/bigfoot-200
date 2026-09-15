# Plan revisions — what changed, and why

A running record of the substantive changes to this plan, so the reasoning
survives the conversation that produced it. Newest first.

---

## 2026-09-15 — Strawberry Fields Forever replaces Bighorn as the gate

**Bighorn 100 → Strawberry Fields Forever 100**, North Bonneville WA, **~June 19 2027**
(date estimated; 2026 ran June 20 and the 2027 calendar is not published).

Patrick questioned whether Bighorn was the right race, which it was not — for a **first**
hundred it is close to the worst available option.

| | Bighorn | Strawberry Fields |
|---|---|---|
| Getting there | flight to Sheridan WY, or 16 hr | **45 min** |
| Course | point-to-point mountain | **10K loop × 16** |
| Climbing | ~18,000 ft | **~3,200 ft** (32 ft/mile) |
| Altitude | to 9,000 ft | sea level |
| Bad day | DNF | **drop to 100K or 50K and still finish** |

That last row is the whole argument. It converts the worst case from a DNF eight weeks
before the A race into a completed 100K.

**It is not a Western States qualifier, and does not need to be.** Checked against the
official WSER list: **Gorge Waterfalls 100K in April is a qualifier**, and **Bigfoot 200
under 100 hours is itself one** — which confirms the premise the whole plan rests on.
Strawberry Fields, Pigtails and Lumberjack are all absent from the list; Hood Hundred is on
it but runs July 31, two weeks before Bigfoot.

**The flat course changes what the clock means.** Sub-28 was a Bighorn standard for 18,000 ft
of mountain. Here the signal is total aid time under 90 minutes across sixteen loop passes,
and a second half no worse than 25% slower. The gate's three outcomes were rewritten
accordingly, and the middle one now reads *"a costly finish, or a drop to 100K"* — because
with the drop-down rule a true DNF is nearly impossible, so **dropping to 100K is what a bad
day looks like** and should be read as one.

**Considered and rejected:** Pigtails Challenge (Renton, May 22, 9,000 ft, ~3 hr away) and
Lumberjack (Port Gamble, June 5, 12,000 ft, ~3.5 hr plus a ferry). Lumberjack is the most
fun of the three — 75% singletrack, 8 laps rather than 16, fire pits at the finish — and is
worth revisiting if sixteen laps of a ball-field loop turns out to be the thing that breaks
him. It is 10 weeks out rather than 8, which absorbs more of its extra climbing.

### And a third source of truth turned up

Fixing the Bighorn references exposed that **`tracker/template.html` — the Log page — carried
its own hardcoded copy of the entire block plan**, and it had drifted badly: pre-rescale
weekly hours (10→15, 17, 19, 21, 23 against the real 12/14/16/18/21), peak days from before
the 2026-09-15 revision, night totals matching nothing, and a Block 2 that claimed to end
with a 100-miler. The Log page had been showing a different plan from every other page for
days, and nobody had looked at it.

It now takes `BLOCKS` and `BLOCK_DISPLAY` from `schedule.json` through `build.py`, like the
race date and the block sections before it. That is the third hardcoded copy found today.

---

## 2026-09-15 (later the same day) — the race is August 2027, and it is fixed

Patrick: *"my race is 2027 make that change like i asked... everything revolves
around that race day."* Reverted. **Bigfoot 200, Friday August 13 2027.** Five
blocks, 49 weeks, Bighorn back on the ladder as the gate.

**The history correction stands and is not affected by the date.** No ultra
finished; longest single effort 3.0 hours. What that makes the 2027 ladder is
six firsts in eleven months, three of them in the final five — first 100K in
April, first 100-miler in June, first 200 in August. That is recorded here so
the difficulty is visible, not as an argument against the date. The date is
Patrick's call and it is made.

**Kept from the 2028 draft, because these were corrections rather than
strategy:**

- **Peak single efforts 6/8/10/14/16**, not 8/10/12/16/20, with the
  volume-vs-rehearsal split: 8 hours caps an aerobic long day, and Blocks 4 and
  5 each keep one longer overnight for the night and the sleep stop.
- **BURT at 55K** as the default, with the 110K and 100-mile explicitly still
  open — the 100-mile is 99 miles and 12,000 ft eight weeks after a first-ever
  50K, and the 110K gets most of the rehearsal value for two thirds of the cost.
- **The odds model's experience input.** `LONGEST_FINISH_MI` scales the band by
  how much of the ladder has actually been raced. It climbs when a race is
  finished, not when a training week goes well.
- **The projection cap.** An eight-week slope is carried at most 26 weeks and
  then held flat. Without it the model reported "100% of race-day vertical" next
  to a readiness score of 53%.
- **The build guards** — the build fails if a block has no section in
  `block-targets.md`, or if any page shows a race date other than the configured
  one. Both were written because two files disagreed in public today.
- **The corrected course figures and max HR 196.**

**What came back:** Bighorn 100 on Jun 18 2027 as the gate and the first
hundred, Hagg Mud 50K on Feb 15 (nine days after BURT — check both before
entering either), and the five-block structure.

**What went away:** the Bigfoot 2027 volunteer entry, because he is running it.

---

## 2026-09-15 — the race moved to 2028, and then moved back (superseded)

**The correction.** `sub100-plan.md` said, in the passage arguing for BURT:
*"Your longest to date is Gorge Waterfalls 100K."* That is not true. Patrick's
actual racing history is **a marathon around 2006 and a few half marathons in
2026**. No ultra. The longest single effort in 208 logged activities is
**3.0 hours**.

Nobody checked it because it was written as an assertion rather than a
question, and everything downstream inherited it.

**What it was propping up.** Read against the true history, the ladder was:

| | |
|---|---|
| Nov 7 2026 | first trail race (25K) |
| Dec 12 2026 | **first ultra** (50K) |
| Feb 6 2027 | **99 miles**, eight weeks later |
| Apr 16 2027 | first 100K, 17-hour cutoff |
| Jun 18 2027 | first 100-miler |
| Aug 13 2027 | first 200, unsupported, four nights, sub-100 |

Six debuts in ten months, three of them in the final five. The plan had already
flagged the last two as *"two debuts stacked eight weeks apart"* — while
believing a 100K was in the bank. It was three, and nothing was.

**The decision: Bigfoot moves to August 2028.** Patrick chose this from four
options, the others being 2027-with-a-107-hour-goal, 2027-unchanged, and
defer-the-decision. 2027 becomes the year he learns to be an ultrarunner —
one debut at a time, each with months of consolidation behind it.

### The two-year shape

| Block | When | Weeks | Ends with |
|---|---|---|---|
| 1 — base + vertical intro | Sep 2026 – Dec 2026 | 14 | Frozen Trail 50K — **first ultra** |
| 2 — winter build | Dec 2026 – Feb 2027 | 9 | **BURT 55K** (was the 100-mile) |
| 3 — first 100K | Feb – Apr 2027 | 9 | Gorge Waterfalls 100K — **first 100K** |
| 4 — recover, base, recon | Apr – Aug 2027 | 17 | **Bigfoot 2027 as a volunteer** |
| 5 — first 100-mile build | Aug – Oct 2027 | 11 | **first 100-miler** — race TBD |
| 6 — winter base + night | Nov 2027 – Feb 2028 | 15 | no race |
| 7 — build + night running | Feb – Apr 2028 | 9 | tune-up — TBD |
| 8 — the gate | Apr – Jun 2028 | 9 | 100-miler — **the gate**, TBD |
| 9 — peak + taper | Jun – Aug 2028 | 8 | **BIGFOOT 200** |

101 weeks. Blocks 2–9 are marked **provisional** in `schedule.json` and carry a
*draft* tag on the Review page, because their races are not chosen yet.

**Working Bigfoot 2028 on a Friday August 11** — the 2028 calendar is not
published. 2026 ran Aug 14, 2027 runs Aug 13; it is the second Friday. Confirm
when Destination Trail posts it.

### The best thing on the new plan costs nothing

**Volunteer or crew at Bigfoot 2027.** Work an aid station or crew someone for
the race he will run a year later: see the course, see the aid stations, see
what people look like at mile 130 on night three. Free, zero injury risk, and
better education than any training block. It is the only entry in Block 4.

### Also changed: the odds model was flattering him

Every gate in `tracker/odds.py` is measured from training data, and none of them
can see a start list. It read a solid training block and applied a base rate
belonging to **the field** at a 200-mile race — people who mostly arrive with
several ultras behind them.

Added `LONGEST_FINISH_MI`, entered by hand because no API knows it, scaling the
band by how much of the ladder has actually been raced: **no ultra 0.45 · 50K
0.60 · 100K 0.80 · 100-miler 1.00**.

The number went from **31–45% to 15–22%**. It climbs on its own as races get
finished, which is the right incentive: the December 50K moves it, not a good
training week.

### Kept, unchanged

The training is sound and none of it was built on the wrong premise. The week
rebuilt earlier today — five running days, the downhill session, eccentric
strength, the uphill ladder — all still applies. So does every page of race-day
pacing, sleep and aid strategy in `sub100-plan.md`; it is the same course.

**Three Sisters, Oct 2–5 2026, stays.** It is a backpacking trip, not a race —
multi-day time on feet at hiking pace is exactly the right first big experience,
and it carries almost none of the risk a 100-mile race does. Permit still
unresolved: 60% release seven days out, about Sep 26, recreation.gov.

### Still open, and Patrick's to decide

1. **Which 100-miler in autumn 2027**, and its date. Placeholder is Oct 16 2027.
2. **Which race is the 2028 gate**, 8–10 weeks out. Placeholder is May 20 2028.
3. **Gorge Waterfalls as the first 100K** — a 17-hour cutoff is tight for a
   debut, four months after a first 50K. A more forgiving first 100K may be the
   kinder choice, with Gorge as the second.
4. **Whether Bighorn returns at all.** It came off the 2027 ladder; it may be
   the right 2028 gate, or the right autumn-2027 first hundred.

---

## 2026-09-15 — the week rebuilt, against an outside review

Patrick brought in a second opinion: *Bigfoot 200 — Optimized Sub-100 Training
Reference*, written against published coaching consensus. Roughly half of it was
right. This records the whole verdict, including the parts that were rejected,
because a rejected proposal that is not written down comes back.

### Adopted

| Change | Why |
|---|---|
| **Sustained downhill gets its own day** (Thursday) | `coaching-references.md` named this gap #1 on 2026-09-11 — *"the most race-specific session available and completely absent"* — against a course that loses **45,563 ft**, more than it climbs. The one measured descent gap, Sep 13, was **8 bpm against a ≥15 target**. The plan had a monitor for a quality it never trained. |
| **Eccentric, single-leg strength** (Wednesday) | "Strength A" was a placeholder. Box step-downs and single-leg RDLs train the quality that actually fails on descent. |
| **Uphill tempo progression** 3×5 → 3×10 → 2×15 (Tuesday) | Gap #2 in the same doc. Replaces the fixed LeBron prescription, which never got harder. |
| **ACWR action rule** — over 1.45, cut the weekend long day 30% | The report printed acute:chronic and did nothing with it. It went **0.73 → 1.40 in a single week** at the start of Block 1. |
| **Block 1 peak day 8 hr → 6 hr** | Longest single effort across 208 recorded activities is **3.0 hours**, and zero sessions exceed four. An 8-hour target nothing was walking toward was decoration. |

### Adopted with changes

**Carbohydrate target.** The review said 70–90 g/hr; the plan said "up to 120"
(Holz). Neither is a starting point. Now a ramp: 60–70 in Block 1, 70–90 in
Blocks 2–3, 90–100 in Blocks 4–5, with 120 as a ceiling reached only if the gut
gets there. Gut tolerance is trained, not chosen.

**HRV rule.** The review said four unbalanced days → everything becomes Zone 1.
Four days is a real signal and seven was too late, but "everything" is a
sledgehammer. Adopted as a **downgrade** trigger (quality work becomes Z1) with
seven days kept as the **stop** trigger.

**The long-day cap.** The review capped every long day at 7–8 hours. Right for
aerobic sessions — Koop's worked progression tops out near 8, Burt prefers
back-to-backs precisely because one enormous day costs more than it returns.
But the review treats every long day as the same currency, and it is not: a
14–16 hour overnight exists for **night movement, a real sleep stop and aid
rehearsal**, and back-to-backs cannot substitute for those. Peak days went
8/10/12/16/20 → **6/8/10/14/16**, with an explicit 8-hour cap on *volume* days
and one long overnight retained in each of Blocks 4 and 5.

**Bighorn at Zone 1.** The review turns the gate into a formality. Running
Bighorn flat-out eight weeks before Bigfoot is a real risk, so there is
something here — but the gate exists to give permission to defer, and you need
a number to read. **This is conditional on BURT 100 in February.** With BURT,
Bighorn's informational value drops and running it controlled is defensible.
Without it, Bighorn is the only 100-mile data point there is. Not changed;
the BURT decision is upstream of it.

### Rejected

**The sleep plan deletes the Twin Sisters stop.** The review lists two sleep
stops, RD 9327 and Chain of Lakes, and no Twin Sisters — while keeping a 97:00
finish that only closes *with* the 2:55 Twin Sisters stop included. It kept the
arithmetic and removed a row the arithmetic depends on. Its own numbers do not
agree either: the prose says 2.5 hr per stop, the table says 2:10.

Substantively, Twin Sisters is the sleep that converts into time: mile 171,
29 miles left, after both sections this race is known for, with 13 miles of road
at the end that must be **run at 3.8 mph at hour 94**. Sleeping early and
walking a finish you could have run is the most common way hours are lost here.

**Peak vertical above race pace.** The review cut weekly hours without cutting
weekly vertical, which pushes ft/hr past what the race itself demands:

| | Block 5 target | ft per hour |
|---|---|---|
| This plan | 10,000 ft / 21 hr | **476** |
| The review | 9,000 ft / 14–16 hr | **563–643** |
| The race | 44,082 ft / 86:48 moving | **508** |

It would have had him training steeper than he will ever race, every hour of
every week. A ft/hr column was added to the progression table so this cannot
happen silently again.

**Five running days — reversed by Patrick, and he was right.** The initial
concern was impact load: running tolerance is 12 mi/week at "low impact load",
and five running days is a large increase in impact even while hours fall.
Patrick overrode it: *"it's a hiking race but i need to be able to run as much
of it as possible."* That is correct — run-specific capacity is the weakest gate
in the model at **21%**, and frequency is precisely how Garmin raises the
tolerance number. Adopted, with the ramp governed instead of argued about:
sessions start at 45 minutes and lengthen by block, and **Friday becomes a walk
when running miles reach tolerance.**

### What the review left out, which was the real problem

It is a well-built *fitness* plan that dropped most of the *race* plan:

- **Night hours — entirely absent.** No session, no column, no progression,
  against roughly 40 hours of solo night across four nights. It is the model's
  single biggest drag at **0%** and the cheapest gap on the board.
- **Sleep-deprivation practice — gone.** The skill is the waking up.
- **Heat acclimation — gone.** Noon start, blast zone, no shade, no crew.
- **Unsupported-specific work — gone.** Filtering silty water at night, pack
  weight from Block 2, solo night navigation through two sections the official
  manual says the trail disappears in.

### The thing worth remembering

The review spent most of its energy arguing 14–16 hr/week versus 20–22. The
week of Sep 7 was **126% of the hours target, 26% of the peak-day target, and
0% of night hours.** Weekly volume is the gate already being passed. Single-day
duration and night hours are the ones at a quarter and zero. Optimising the
ceiling on a number that is already beaten, while dropping the two that are
failing, is optimising the wrong variable.

### Corrections made at the same time

- **Max HR 205 → 196** on `block-targets.md`. Established 2026-09-14: every
  reading above 196 (233, 210, 209, 207, 205) came on a day with no logged
  workout — optical-sensor artifact. Highest on a genuinely hard day is 196.
- **Course figures** on `block-targets.md`: 200–208 mi / 44,000–45,500 ft →
  **200.1 / 44,082 / 45,563**. The old range describes the retired course.
- **Treadmill versions** written for both terrain sessions, so weather or a dark
  weeknight costs the session's shape rather than the session.
- **The weekday template is versioned by date.** Days before 2026-09-15 still
  render the week as it stood then. Week 1 was trained and logged at 15.1 hr
  under the old template; showing it as uphill tempo and sustained downhill
  would claim he was told to do something he was never told to do.

### Consequence to expect

*Longest single day* is a **20%-weight gate** in the odds model, measured
against Block 5's peak-day target. Lowering that target from 20 to 16 hours
raises the gate's percentage without any change in fitness. When the next
weekly report moves, that is why.
