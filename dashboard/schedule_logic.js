// Shared day-level schedule logic. Included verbatim into BOTH
// dashboard/template.html (Today) and dashboard/weeks_template.html (Every
// week) at build time, so the two pages can never drift on what a given day is.
//
// Expects these to already exist in the page: BLOCKS, DATA.longDays, today,
// toDate(), daysBetween().

function blockFor(d){
  for(const b of BLOCKS){
    if(d >= toDate(b.start) && d <= toDate(b.end)) return b;
  }
  if(d < toDate(BLOCKS[0].start)) return BLOCKS[0];
  return BLOCKS[BLOCKS.length-1];
}

function currentBlock(){ return blockFor(today); }

function weekOfBlock(block){
  return weekOfBlockOn(block, today);
}

// Week number of a block for an ARBITRARY date. weekOfBlock() answers for
// today, which is right for the header and wrong for anything that renders a
// future week — the same mistake blockFor() had to fix for scheduleFor().
function weekOfBlockOn(block, d){
  return Math.floor(daysBetween(toDate(block.start), d)/7) + 1;
}

// The race covering this date, if any. Multi-day races cover every day in range.
function raceOn(d){
  return (typeof RACES === 'undefined' ? [] : RACES)
    .find(r => d >= toDate(r.start) && d <= toDate(r.end)) || null;
}

function ordinalOfMonth(d){
  return Math.floor((d.getDate()-1)/7) + 1;
}

function fmtIso(d){
  return d.getFullYear()+'-'+String(d.getMonth()+1).padStart(2,'0')+'-'+String(d.getDate()).padStart(2,'0');
}

// The dated plan lives in plan/schedule.json "longDays" and is keyed by DATE,
// not by weekday: the weekly long day is Sunday, but a race keeps its real
// date and a multi-day trip keeps its real start, both of which are Saturdays.
function plannedFor(d){
  return (DATA.longDays||[]).find(s => s.date === fmtIso(d)) || null;
}

function fromPlanned(p){
  const showVert = p.vert && !/^(race|multi-day|—)$/.test(p.vert);
  return { title: p.title + (showVert ? '  ·  ' + p.vert : ''),
           desc: p.desc, vert: p.vert,
           link: p.link || null, linkLabel: p.linkLabel || null };
}

// One escaped anchor, or ''. Every page that prints a session uses this, so a
// dated route can never render as a link on one page and bare text on another.
function routeLink(w){
  if(!w || !w.link) return '';
  const esc = t => String(t).replace(/&/g,'&amp;').replace(/</g,'&lt;')
                            .replace(/>/g,'&gt;').replace(/"/g,'&quot;');
  // "AllTrails · Dog Mountain Trail" -> the source is wrapped so a phone can
  // drop it and keep the part that identifies the route.
  const label = String(w.linkLabel || 'Route map');
  const i = label.indexOf(' \u00b7 ');
  const inner = i > 0
    ? `<span class="lsrc">${esc(label.slice(0, i + 3))}</span>${esc(label.slice(i + 3))}`
    : esc(label);
  return `<a class="routelink" href="${esc(w.link)}" target="_blank" ` +
         `rel="noopener noreferrer">${inner}</a>`;
}

// SUNDAY is the long day.
function sundayWorkout(block, d){
  const p = plannedFor(d);
  if(p) return fromPlanned(p);
  // If Saturday carried a dated entry — a race, or a multi-day start — Sunday
  // belongs to it. Do not hand back a fresh long day the morning after a 50K.
  const sat = new Date(d); sat.setDate(sat.getDate()-1);
  // A race that finished yesterday counts too. Bighorn is a Friday-Saturday
  // 100-miler and is not in longDays, so without this the Sunday after it came
  // back "long day, vertical-focused" - the morning after a hundred miles.
  const satRace = raceOn(sat);
  if(satRace && !plannedFor(sat)){
    return { title:'Recovery — the day after ' + satRace.name,
             desc:'Walk, or nothing. The long day already happened yesterday.' };
  }
  const satPlan = plannedFor(sat);
  if(satPlan){
    if(/multi-day/i.test(satPlan.vert || '')){
      // Same trip, so it keeps the same route map.
      return { title: satPlan.title + ' — day two',
               desc:'The trip continues. Time on feet is the point; let the terrain set the pace.',
               link: satPlan.link || null, linkLabel: satPlan.linkLabel || null };
    }
    return { title:'Recovery — the day after ' + satPlan.title,
             desc:'Walk, or nothing. The long day already happened yesterday.' };
  }
  const nth = ordinalOfMonth(d);
  if(!block.taper){
    if(nth === 1) return { title:'Overnight long day', desc:'Evening/night start (~9pm–3am) — night-running exposure, targeting the overnight fade window seen in the split data. (No dated plan for this Sunday yet.)' };
    if(nth === 3) return { title:'Back-to-back weekend — Sunday', desc:`The second and harder of the two days: target ${block.vert} of vertical on legs that are already tired. (No dated plan for this Sunday yet.)` };
  }
  return { title:'Long day, vertical-focused', desc:`Target ${block.vert} of vertical this block. (No dated plan for this Sunday yet.)` };
}

// SATURDAY is the recovery slot, or day one of a back-to-back — unless a race
// or a multi-day trip is dated on it.
function saturdayWorkout(block, d){
  const p = plannedFor(d);
  if(p) return fromPlanned(p);
  const sun = new Date(d); sun.setDate(sun.getDate()+1);
  if(!block.taper && ordinalOfMonth(sun) === 3 && !plannedFor(sun)){
    return { title:'Back-to-back weekend — Saturday', desc:'Day one of two. Long, but held back — Sunday is the day that has to hurt. (No dated plan for this weekend yet.)' };
  }
  return { title:'Flexible recovery', desc:'Up to 6 miles, easy. Sunday is the long day — arrive at it fresh enough to do it properly.' };
}

// ---------------------------------------------------------------------------
// The midweek week. Rewritten 2026-09-15.
//
// Five running days now: Tue, Wed, Thu, Fri and the Sunday long day. Run-
// specific capacity is the weakest gate in the model (21%), and Bigfoot is only
// a hiking race if you are willing to walk the runnable two thirds of it.
//
// Frequency, not one big day, is how Garmin's running tolerance rises, so these
// sessions start SHORT and lengthen by block rather than starting long. The
// guardrail is stated on every running day instead of being buried in a
// monitor: if the week's running miles are over tolerance, Friday becomes a
// walk. That is the release valve, and it is deliberately the smallest session.
//
// Monday is now a full rest day. The vertical-volume work it carried moved to
// Tuesday's uphill tempo, which progresses instead of sitting at a fixed
// prescription, and the strength moved to Wednesday and became eccentric.

// Per-block session minutes. Block 1 is deliberately small: running tolerance
// was 12 mi/week when this was written, and five short days already spends it.
const RUN_MINUTES = {
  1: { tue: 45, wed: 45, thu: 45, fri: 25 },
  2: { tue: 55, wed: 55, thu: 60, fri: 30 },
  3: { tue: 60, wed: 60, thu: 75, fri: 30 },
  4: { tue: 65, wed: 70, thu: 90, fri: 35 },
  5: { tue: 60, wed: 70, thu: 90, fri: 35 }
};
function runMin(block){ return RUN_MINUTES[block.id] || RUN_MINUTES[1]; }

// ---------------------------------------------------------------------------
// The week was rebuilt on 2026-09-15. Days BEFORE that date still render the
// week as it actually stood, because the Every week tab is a record as well as
// a plan: week 1 was trained and logged (15.1 hr, 126% of target) under the old
// template, and showing it as uphill tempo and sustained downhill would be
// claiming he was told to do something he was never told to do.
//
// Versioned by DAY rather than by week, because the change landed mid-week:
// Monday Sep 14 was the old week, Tuesday Sep 15 onward is the new one.
const TEMPLATE_V2_FROM = '2026-09-15';
function usesNewWeek(date){ return fmtIso(date) >= TEMPLATE_V2_FROM; }

const WAS = ' (the week as it stood before 2026-09-15)';

function legacyWeekday(block, d, dow){
  switch(dow){
    case 1: return { title:'Strength A + incline intervals',
      desc:'4 \u00d7 3 min, 150\u2013160 bpm, 15\u201318% grade treadmill.' + WAS };
    case 2: return { title:'Rest + capped walk',
      desc:'Up to 3 miles / under 1 hour. Not training \u2014 didn\u2019t count toward compliance.' + WAS };
    case 3: return { title:'Easy run',
      desc:'25\u201330 min, Nike Jogging Trail.' + WAS };
    case 4: {
      if(block.id === 1) return { title:'LeBron ramp repeats',
        desc:'10\u201312 reps, run up / walk down, 150\u2013160 bpm.' + WAS };
      const wk = weekOfBlockOn(block, d);
      return wk % 2 === 0
        ? { title:'LeBron ramp \u2014 down-focus', desc:'Walk up conservatively, run down under control at race effort.' + WAS }
        : { title:'LeBron ramp \u2014 up-focus',   desc:'Run up, walk down, 150\u2013160 bpm.' + WAS };
    }
    case 5: return { title:'Rest', desc:'Full rest day.' + WAS };
  }
}

// A week is a deload when its Sunday long day says so. Block 1's deloads are
// anchored to races (weeks 5, 10 and 13), not to a rigid count, so a modulo
// would put the easy week in the wrong place. Blocks with no dated long days
// fall back to weeks 4 and 8, which is what block-targets.md specifies.
function mondayOfWeek(d){
  const m = new Date(d); m.setDate(d.getDate() - ((d.getDay() + 6) % 7));
  m.setHours(0,0,0,0); return m;
}
function blockIsDated(block){
  return (DATA.longDays || []).some(s =>
    s.date >= block.start && s.date <= block.end);
}
function isDeloadWeek(block, d){
  const mon = mondayOfWeek(d);
  for(let i = 0; i < 7; i++){
    const day = new Date(mon); day.setDate(mon.getDate() + i);
    const p = plannedFor(day);
    if(p) return /deload|taper/i.test(p.title || '');
  }
  // A dated block has already answered: no marker anywhere in the week means a
  // build week. Only fall back to the every-fourth-week rule for blocks that
  // carry no dated long days at all - otherwise week 4 of Block 1, which is the
  // Three Sisters trip, was being called a deload.
  if(blockIsDated(block)) return false;
  return weekOfBlockOn(block, mon) % 4 === 0;
}

// Position in the three-week build ladder, counting only weeks that are not
// deloads - so a deload pauses the ladder rather than consuming a rung.
function buildWeekOf(block, d){
  const target = mondayOfWeek(d).getTime();
  let n = 0;
  for(let m = mondayOfWeek(toDate(block.start)); m.getTime() <= target; m.setDate(m.getDate() + 7)){
    if(!isDeloadWeek(block, m)) n++;
  }
  return n;
}

const TOLERANCE_NOTE = 'If the week’s running miles are at or over Garmin’s running ' +
  'tolerance, drop Friday to a walk before cutting anything else.';

// Indoor versions of the two terrain sessions. Portland in January, a dark
// weeknight, or no time to reach a trail should cost the session's shape, not
// the session. The treadmill numbers line up with the outdoor ones rather than
// being a vague "do something on a machine".
function treadmillUp(minutes, work){
  return ' TREADMILL VERSION: 10 min flat warm-up, then ' + work + ' at 12\u201315% grade '
       + 'holding Z3 (137\u2013157 bpm) \u2014 walk it fast rather than jogging badly, the grade '
       + 'is what matters \u2014 with 2\u20133 min flat easy between. Strides become 5 \u00d7 20 sec '
       + 'at 8\u201310% grade, stepping off the belt to recover. 10 min cool-down, '
       + minutes + ' min total.';
}
const TREADMILL_DOWN =
  ' TREADMILL VERSION: only if yours declines. Set \u22124 to \u22126% and run the continuous '
  + 'block at easy effort, cadence 175\u2013180, short quick steps, no heel braking \u2014 the '
  + 'point is the eccentric load, not the pace. If it does NOT decline, a treadmill cannot do '
  + 'this session at all: use the LeBron ramp instead (walk up easy, run down under control, '
  + 'repeat until the descent minutes add up), or a parking garage ramp, or stadium steps. '
  + 'Note which you did \u2014 ramp repeats are not the same stimulus as one unbroken descent, '
  + 'and the descent HR gap will show the difference.';

// TUESDAY — uphill tempo on a four-week cycle: 3x5, 3x10, 2x15, easy. Holz's
// structure. Replaces the fixed LeBron prescription, which never got harder.
const UPHILL_LADDER = ['3 × 5 min', '3 × 10 min', '2 × 15 min'];

function tuesdayWorkout(block, d){
  const m = runMin(block);
  const slot = Math.max(0, buildWeekOf(block, d) - 1) % 3;
  if(isDeloadWeek(block, d)){
    return { title: 'Uphill tempo — easy week',
      desc: '2 × 5 min at tempo, no strides, ' + Math.round(m.tue * 0.7) + ' min total. Deload '
          + 'week: keep the frequency, cut the intensity. The ladder pauses here rather than '
          + 'advancing \u2014 next week picks up where it left off.'
          + treadmillUp(Math.round(m.tue * 0.7), '2 \u00d7 5 min') + ' ' + TOLERANCE_NOTE };
  }
  return { title: 'Uphill tempo intervals + power strides',
    desc: UPHILL_LADDER[slot] + ' uphill at Z3 (137–157 bpm), then 5 × 20 sec power strides '
        + 'at about 85% effort on a moderate grade. Easy 20 min either side, ' + m.tue
        + ' min total. Week ' + (slot + 1) + ' of 3 on the ladder — it is meant to '
        + 'progress, so do not leave it at 3 \u00d7 5.'
        + treadmillUp(m.tue, UPHILL_LADDER[slot]) + ' ' + TOLERANCE_NOTE };
}

// WEDNESDAY — easy aerobic plus the eccentric strength that used to sit on
// Monday. Step-downs and single-leg RDLs are the quad armour; the loaded
// carries are the unsupported-specific part.
function wednesdayWorkout(block){
  const m = runMin(block);
  return { title: 'Easy run + eccentric strength',
    desc: m.wed + ' min easy Z2 (118–137 bpm), on trail if you can get to it, then 30 min of '
        + 'strength: single-leg box step-downs 3 × 10, weighted step-ups with the pack '
        + '3 × 12, single-leg RDLs 3 × 10, loaded carries. The step-downs are the session '
        + '— lower slowly; that slow lowering is the load the descent asks for. '
        + TOLERANCE_NOTE };
}

// THURSDAY — the session the plan was missing. Bigfoot loses 45,563 ft, more
// than it climbs, and nothing in the old week descended on purpose.
function thursdayWorkout(block, d){
  const m = runMin(block);
  const deload = isDeloadWeek(block, d);
  // 15 / 20 / 25 across the build ladder, back to 10 on a deload.
  const cont = deload ? 10 : 15 + 5 * (Math.max(0, buildWeekOf(block, d) - 1) % 3);
  const mins = deload ? Math.round(m.thu * 0.7) : m.thu;
  return { title: 'Sustained downhill — quad armour',
    desc: mins + ' min built around ' + cont + ' min of CONTINUOUS descent. Light feet, high '
        + 'cadence, no braking — let the legs absorb it rather than the joints. On rock '
        + 'rather than loam, and late in the day on legs that are already tired. This is the '
        + 'most race-specific session of the week: the course descends more than it climbs, '
        + 'and Block 1’s question is whether you can descend hard without wrecking your '
        + 'quads. Watch the descent HR gap — target is 15 bpm below climb HR; it was 8 on '
        + 'Sep 13.' + TREADMILL_DOWN + ' ' + TOLERANCE_NOTE };
}

// FRIDAY — short, easy, and the first thing to become a walk when the running
// ramp is running hot.
function fridayWorkout(block){
  const m = runMin(block);
  return { title: 'Recovery jog',
    desc: m.fri + ' min at Z1 (98–118 bpm), easy enough to hold a conversation the whole way. '
        + 'This is the release valve: if running miles are at or over tolerance this week, '
        + 'walk it instead. Saturday is recovery and Sunday is the long day.' };
}

function scheduleFor(date){
  // A race outranks the weekly template. Most races here fall on a Saturday and
  // are also dated in longDays, but the ones that matter most are not: Gorge
  // Waterfalls, Bighorn and Bigfoot itself are Fridays, and without this the
  // page printed "Rest — full rest day" on race day.
  const race = raceOn(date);
  if(race){
    // A dated longDay for this same date is the more specific entry - it is the
    // one carrying the route link and the day's own notes - so it wins.
    const p = plannedFor(date);
    if(p) return fromPlanned(p);
    // A Sunday inside a multi-day trip is "day two", not the race name again.
    // sundayWorkout already knows that, and it carries the route link across.
    const prev = new Date(date); prev.setDate(date.getDate() - 1);
    if(date.getDay() === 0 && plannedFor(prev)) return sundayWorkout(blockFor(date), date);
    return { title: race.name, desc: 'Race day. ' + race.tag + '.' };
  }

  // Nothing is planned past the A race. Without this the final week printed a
  // recovery Saturday and a long-day Sunday after Bigfoot had already finished.
  const aRace = (typeof RACES === 'undefined' || !RACES.length)
    ? null : RACES[RACES.length - 1];
  if(aRace && date > toDate(aRace.end))
    return { title: '—', desc: 'After ' + aRace.name + '. Nothing scheduled.' };

  // Use the block that CONTAINS this date. Looking two weeks ahead can cross a
  // block boundary, and currentBlock() would hand back today's block instead.
  const block = blockFor(date);
  const dow = date.getDay(); // 0 Sun .. 6 Sat
  // Weekdays before the rebuild show what was actually prescribed then.
  if(dow >= 1 && dow <= 5 && !usesNewWeek(date)) return legacyWeekday(block, date, dow);

  switch(dow){
    case 1: return { title:'Full rest', desc:'No running, no strength, no capped walk that turns into three miles. Yesterday was the long day and this is where it gets absorbed \u2014 one forced rest day a week is the single piece of published coaching every source agrees on.' };
    case 2: return tuesdayWorkout(block, date);
    case 3: return wednesdayWorkout(block);
    case 4: return thursdayWorkout(block, date);
    case 5: return fridayWorkout(block);
    case 6: return saturdayWorkout(block, date);
    case 0: return sundayWorkout(block, date);
  }
}

// Weeks run Monday -> Sunday, matching tracker/REFRESH.md and the block boundaries.
const DAY_NAMES = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'];
