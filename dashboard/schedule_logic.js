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
// A race flagged `backup:true` would be excluded here so it could not blank out
// a training week for a start that may never happen. Nothing carries that flag
// right now - SISU 100 is entered as a real second attempt - but the guard
// stays so adding one later does not silently erase a week.
function raceOn(d){
  return (typeof RACES === 'undefined' ? [] : RACES)
    .find(r => !r.backup && d >= toDate(r.start) && d <= toDate(r.end)) || null;
}

// Deferral decision points. Destination Trail calls it a transfer, it is a
// sliding scale by the date the EMAIL is sent, and it is one-shot and binding.
// The dates live in schedule.json because they are policy, not training, and
// because the important one (Mar 31) lands two weeks before the first 100K -
// the decision has to be made without the evidence, which is exactly the kind
// of thing a calendar has to say out loud rather than leave in a policy doc.
function decisionOn(d){
  const list = (typeof DECISIONS === 'undefined' ? [] : DECISIONS) || [];
  const iso = fmtIso(d);
  return list.find(x => x.date === iso) || null;
}
function decisionHtml(d){
  const x = decisionOn(d);
  if(!x) return '';
  const esc = t => String(t).replace(/&/g,'&amp;').replace(/</g,'&lt;');
  return '<div class="decision ' + (x.kind === 'hard' ? 'dec-hard' : 'dec-soft') + '">' +
         '<div class="dec-t">' + esc(x.title) + '</div>' +
         '<div class="dec-b">' + esc(x.body) + '</div></div>';
}

// Race shoulders. A race is not just its own day: the days before it have to
// be a taper and the days after it have to be recovery, and until this existed
// the calendar cheerfully printed 90-minute downhill quad sessions into the
// six-day gap between Strawberry Fields and SISU. Each race carries its own
// taperDays/recoveryDays in schedule.json - no distance guessing here.
// Recovery outranks taper: you cannot taper into a race you have not recovered
// from, and when the two overlap the honest answer is "you are still recovering".
function shoulderOn(d){
  const list = (typeof RACES === 'undefined' ? [] : RACES);
  // Recovery windows overlap: SISU ends six days after Strawberry Fields, so a
  // day in early July sits inside both. The MOST RECENT race is the one the legs
  // are actually recovering from, so take the smallest n, not the first match.
  let taper = null, recov = null;
  for(const r of list){
    if(r.backup) continue;
    const rec = r.recoveryDays || 0, tap = r.taperDays || 0;
    if(rec){
      const n = daysBetween(toDate(r.end), d);
      if(n >= 1 && n <= rec && (!recov || n < recov.n))
        recov = { kind: 'recovery', race: r, n: n, of: rec };
    }
    if(tap){
      const n = daysBetween(d, toDate(r.start));
      if(n >= 1 && n <= tap && (!taper || n < taper.n))
        taper = { kind: 'taper', race: r, n: n, of: tap };
    }
  }
  return recov || taper;
}

function shoulderSession(sh, date){
  const dow = date.getDay();
  if(sh.kind === 'recovery'){
    const easy = sh.n <= 2
      ? 'Nothing, or a flat walk under 30 min. No running.'
      : (sh.n <= 5
        ? 'Walk, or 20-30 min shuffle on flat ground if it feels genuinely good. Stop early.'
        : 'Easy Z2 only, flat, under an hour. No vertical, no intervals, no downhill.');
    return sess('Recovery - day ' + sh.n + ' after ' + sh.race.name, [
      { k: 'DO', v: easy },
      { k: 'DO NOT', v: 'No uphill intervals, no eccentric strength, no sustained downhill. '
        + 'The damage from ' + sh.race.name + ' is still being repaired and loading it now '
        + 'is how a finish turns into an injury.' },
      { k: 'WHY', v: 'Day ' + sh.n + ' of a ' + sh.of + '-day recovery window written into the plan '
        + 'for this race, not a rule of thumb.' }
    ]);
  }
  const body = (dow === 1)
    ? 'Full rest.'
    : (sh.n <= 2 ? 'Nothing, or 20-30 min very easy with 4 x 20 s strides to stay sharp.'
                 : 'Easy Z2, 30-45 min, flat. Legs stay fresh.');
  return sess('Taper - ' + sh.n + ' day' + (sh.n === 1 ? '' : 's') + ' to ' + sh.race.name, [
    { k: 'DO', v: body },
    { k: 'DO NOT', v: 'No vertical, no intervals, no downhill, no strength. '
      + 'Nothing you do this week makes you fitter for ' + sh.race.name + '; '
      + 'it can only make you more tired.' },
    { k: 'WHY', v: 'Day ' + sh.n + ' of a ' + sh.of + '-day taper set for this race.' }
  ]);
}

// The A race is the last NON-backup race on the ladder.
function aRaceOf(list){
  const real = (list || []).filter(r => !r.backup);
  return real.length ? real[real.length - 1] : null;
}

// Signup links. Status drives the badge; a note explains anything non-obvious
// (a date that has not been published, a registration window that has not
// opened, a race that has already sold out).
var SIGNUP_BADGE = {
  'entered':      { t: 'You are in',     c: 'sg-in'    },
  'open':         { t: 'Register',       c: 'sg-open'  },
  'opens-later':  { t: 'Opens later',    c: 'sg-soon'  },
  'not-yet-open': { t: '2027 TBA',       c: 'sg-tba'   },
  'closed':       { t: 'Sold out',       c: 'sg-shut'  }
};
function signupHtml(r){
  if(!r || !r.signup) return '';
  const b = SIGNUP_BADGE[r.signupStatus] || SIGNUP_BADGE['open'];
  const lbl = String(r.signupLabel || 'Registration')
    .replace(/&/g,'&amp;').replace(/</g,'&lt;');
  let h = '<a class="signup ' + b.c + '" href="' + r.signup +
          '" target="_blank" rel="noopener noreferrer" title="' + lbl + '">' +
          b.t + '</a>';
  if(r.signupNote){
    h += '<div class="sg-note">' +
         String(r.signupNote).replace(/&/g,'&amp;').replace(/</g,'&lt;') +
         '</div>';
  }
  return h;
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
// Per-block session minutes. Block 1 is deliberately small: running tolerance
// was 12 mi/week when this was written, and five short days already spends it.
// Keyed for every block the plan has - when this table had five entries and the
// plan briefly had nine, blocks 6-9 silently fell back to Block 1's beginner
// 45 minutes, so the fallback is no longer the smallest entry.
const RUN_MINUTES = {
  1: { tue: 45, wed: 45, thu: 45, fri: 25 },
  2: { tue: 55, wed: 55, thu: 60, fri: 30 },
  3: { tue: 60, wed: 60, thu: 75, fri: 30 },
  4: { tue: 65, wed: 70, thu: 90, fri: 35 },
  5: { tue: 60, wed: 70, thu: 90, fri: 35 }
};
function runMin(block){
  const keys = Object.keys(RUN_MINUTES).map(Number);
  return RUN_MINUTES[block.id] || RUN_MINUTES[Math.max.apply(null, keys)];
}

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

// ---------------------------------------------------------------------------
// Sessions are structured, not prose. Each one can carry PARTS - a run
// portion, a workout portion with its own movement list, an indoor
// alternative - so the page can lay them out instead of printing a paragraph
// and hoping. desc stays as a flattened string for anything that still wants
// one.

// Demo videos, checked 2026-09-15. If one rots, replace the URL here and every
// page picks it up.
const DEMO = {
  stepDown:  'https://www.youtube.com/watch?v=Or4C-UQ63Xc',
  stepUp:    'https://www.youtube.com/watch?v=tqECKZxlCKE',
  slRdl:     'https://www.youtube.com/watch?v=Zfr6wizR8rs',
  carry:     'https://www.youtube.com/watch?v=lLAw6fUccKA',
  downhill:  'https://www.youtube.com/watch?v=md0vWMb8QrM',
  hillReps:  'https://www.youtube.com/watch?v=JZJk7lld69E',
  hillSprint:'https://www.youtube.com/watch?v=fZ85Ht6y8Vc'
};

function escHtml(t){
  return String(t).replace(/&/g,'&amp;').replace(/</g,'&lt;')
                  .replace(/>/g,'&gt;').replace(/"/g,'&quot;');
}

// Flatten parts to a single sentence-ish string, for the places that still
// take plain text.
function partsToText(parts){
  return (parts || []).map(p => {
    const items = (p.items || []).map(it =>
      it.n + (it.s ? ' ' + it.s : '')).join('; ');
    return p.k + ': ' + [p.v, items].filter(Boolean).join(' ');
  }).join('  ');
}

// One session, laid out. Used by the Today page and the Review tab, so they
// cannot drift.
function partsHtml(w){
  if(!w || !w.parts || !w.parts.length) return '';
  return '<div class="sparts">' + w.parts.map(p => {
    const items = (p.items || []).map(it =>
      '<li><span class="mv-n">' + escHtml(it.n) + '</span>'
      + (it.s ? '<span class="mv-s">' + escHtml(it.s) + '</span>' : '')
      + (it.u ? ' <a class="mv-d" href="' + escHtml(it.u) + '" target="_blank" '
              + 'rel="noopener noreferrer">demo</a>' : '')
      + '</li>').join('');
    return '<div class="spart spart-' + p.k.toLowerCase().replace(/[^a-z]/g,'') + '">'
         + '<div class="spart-k">' + escHtml(p.k) + '</div>'
         + '<div class="spart-v">' + (p.v ? escHtml(p.v) : '')
         + (items ? '<ul class="mvs">' + items + '</ul>' : '')
         + '</div></div>';
  }).join('') + '</div>';
}

// Build a session from parts, keeping desc in sync automatically.
function sess(title, parts){
  return { title: title, parts: parts, desc: partsToText(parts) };
}



// TUESDAY — uphill tempo on a four-week cycle: 3x5, 3x10, 2x15, easy. Holz's
// structure. Replaces the fixed LeBron prescription, which never got harder.
// Each rung carries its own WORK minutes, because the session length has to be
// computed from them. It used to print a fixed per-block total - 45 min in
// Block 1 - next to "3 x 10 min of intervals plus 20 min either side", which
// does not fit in 45 minutes and was wrong from week 2 of the ladder onward.
const UPHILL_LADDER = [
  { label: '3 \u00d7 5 min',  work: 15, rec: 6 },
  { label: '3 \u00d7 10 min', work: 30, rec: 6 },
  { label: '2 \u00d7 15 min', work: 30, rec: 4 }
];
const STRIDES_MIN = 6;   // 5 x 20 sec plus the walk back

function tuesdayWorkout(block, d){
  const m = runMin(block);
  const slot = Math.max(0, buildWeekOf(block, d) - 1) % 3;
  const ends = Math.max(16, Math.round(m.tue * 0.45));
  const half = Math.round(ends / 2);

  if(isDeloadWeek(block, d)){
    return sess('Uphill tempo \u2014 easy week', [
      { k: 'Run', v: half + ' min easy either side, about ' + (ends + 13) + ' min total.' },
      { k: 'Workout', v: '2 \u00d7 5 min at tempo, 3 min easy between. No strides. Deload '
          + 'week: keep the frequency, cut the intensity \u2014 the ladder pauses here rather '
          + 'than advancing, and next week picks up where it left off.' },
      { k: 'Indoors', v: 'Treadmill: 10 min flat warm-up, 2 \u00d7 5 min at 12\u201315% grade '
          + 'holding Z3, 10 min cool-down.' },
      { k: 'If over tolerance', v: TOLERANCE_NOTE }
    ]);
  }

  const rung = UPHILL_LADDER[slot];
  const total = ends + rung.work + rung.rec + STRIDES_MIN;
  return sess('Uphill tempo intervals + power strides', [
    { k: 'Run', v: half + ' min easy either side, about ' + total + ' min total.'
        + (slot > 0 ? ' The session grows with the ladder \u2014 longer than week 1.' : '') },
    { k: 'Workout', v: 'Week ' + (slot + 1) + ' of 3 on the ladder. It is meant to progress, '
        + 'so do not leave it at 3 \u00d7 5.',
      items: [
        { n: rung.label + ' uphill', s: 'Z3, 137\u2013157 bpm \u00b7 3 min easy between',
          u: DEMO.hillReps },
        { n: 'Power hill strides', s: '5 \u00d7 20 sec at ~85% on a moderate grade',
          u: DEMO.hillSprint }
      ] },
    { k: 'Indoors', v: 'Treadmill: 10 min flat warm-up, then ' + rung.label + ' at 12\u201315% '
        + 'grade holding Z3 \u2014 walk it fast rather than jogging badly, the grade is what '
        + 'matters \u2014 with 2\u20133 min flat easy between. Strides become 5 \u00d7 20 sec at '
        + '8\u201310% grade, stepping off the belt to recover. 10 min cool-down.' },
    { k: 'If over tolerance', v: TOLERANCE_NOTE }
  ]);
}


// WEDNESDAY — easy aerobic plus the eccentric strength that used to sit on
// Monday. Step-downs and single-leg RDLs are the quad armour; the loaded
// carries are the unsupported-specific part.
function wednesdayWorkout(block){
  const m = runMin(block);
  return sess('Easy run + eccentric strength', [
    { k: 'Run', v: m.wed + ' min easy Z2 (118\u2013137 bpm), on trail if you can get to it.' },
    { k: 'Workout', v: '30 min. The step-downs are the session \u2014 lower slowly; that slow '
        + 'lowering is the load the descent asks for.',
      items: [
        { n: 'Single-leg box step-downs', s: '3 \u00d7 10', u: DEMO.stepDown },
        { n: 'Weighted step-ups, with the pack', s: '3 \u00d7 12', u: DEMO.stepUp },
        { n: 'Single-leg RDLs', s: '3 \u00d7 10', u: DEMO.slRdl },
        { n: 'Loaded carries', s: '3 \u00d7 40 m', u: DEMO.carry }
      ] },
    { k: 'If over tolerance', v: TOLERANCE_NOTE }
  ]);
}


// THURSDAY — the session the plan was missing. Bigfoot loses 45,563 ft, more
// than it climbs, and nothing in the old week descended on purpose.
function thursdayWorkout(block, d){
  const m = runMin(block);
  const deload = isDeloadWeek(block, d);
  const cont = deload ? 10 : 15 + 5 * (Math.max(0, buildWeekOf(block, d) - 1) % 3);
  const mins = deload ? Math.round(m.thu * 0.7) : m.thu;
  return sess('Sustained downhill \u2014 quad armour', [
    { k: 'Run', v: mins + ' min, on rock rather than loam, and late in the day on legs that '
        + 'are already tired.' },
    { k: 'Workout', v: 'The most race-specific session of the week: the course descends more '
        + 'than it climbs, and Block 1\u2019s question is whether you can descend hard without '
        + 'wrecking your quads.',
      items: [
        { n: cont + ' min of CONTINUOUS descent', s: 'light feet, high cadence, no braking',
          u: DEMO.downhill }
      ] },
    { k: 'Watch', v: 'Descent HR gap \u2014 target is 15 bpm below climb HR. It was 8 on Sep 13.' },
    { k: 'Indoors', v: 'Treadmill only if yours declines: \u22124 to \u22126% at easy effort, '
        + 'cadence 175\u2013180. If it does not decline a treadmill cannot do this session at '
        + 'all \u2014 use the LeBron ramp, a parking garage ramp, or stadium steps, and note '
        + 'which, because repeats are not the same stimulus as one unbroken descent.' },
    { k: 'If over tolerance', v: TOLERANCE_NOTE }
  ]);
}


// FRIDAY — short, easy, and the first thing to become a walk when the running
// ramp is running hot.
function fridayWorkout(block){
  const m = runMin(block);
  return sess('Recovery jog', [
    { k: 'Run', v: m.fri + ' min at Z1 (98\u2013118 bpm), easy enough to hold a conversation '
        + 'the whole way.' },
    { k: 'If over tolerance', v: 'This is the release valve. If running miles are at or over '
        + 'tolerance this week, walk it instead. Saturday is recovery and Sunday is the long day.' }
  ]);
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
  const aRace = (typeof RACES === 'undefined') ? null : aRaceOf(RACES);
  if(aRace && date > toDate(aRace.end))
    return { title: '—', desc: 'After ' + aRace.name + '. Nothing scheduled.' };

  // A dated long day still wins inside a shoulder - those are deliberate, and a
  // race weekend trip is dated. Otherwise the taper/recovery window outranks the
  // weekly template, which knows nothing about what race is six days away.
  const sh = shoulderOn(date);
  if(sh && !plannedFor(date)) return shoulderSession(sh, date);

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
