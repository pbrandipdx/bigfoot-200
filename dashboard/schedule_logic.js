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
  return Math.floor(daysBetween(toDate(block.start), today)/7) + 1;
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
           desc: p.desc, vert: p.vert };
}

// SUNDAY is the long day.
function sundayWorkout(block, d){
  const p = plannedFor(d);
  if(p) return fromPlanned(p);
  // If Saturday carried a dated entry — a race, or a multi-day start — Sunday
  // belongs to it. Do not hand back a fresh long day the morning after a 50K.
  const sat = new Date(d); sat.setDate(sat.getDate()-1);
  const satPlan = plannedFor(sat);
  if(satPlan){
    if(/multi-day/i.test(satPlan.vert || '')){
      return { title: satPlan.title + ' — day two', desc:'The trip continues. Time on feet is the point; let the terrain set the pace.' };
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

function thursdayWorkout(block){
  if(block.id === 1){
    return { title:'LeBron ramp repeats', desc:'10–12 reps, run up / walk down, 150–160 bpm. Real vertical here is modest (~250–300 ft) \u2014 Monday\u2019s incline intervals are the actual vertical-volume session; this one is about real-terrain movement.' };
  }
  const wk = weekOfBlock(block);
  if(wk % 2 === 0){
    return { title:'LeBron ramp — down-focus', desc:'Walk up conservatively, run down under control at race effort. Builds the eccentric quad durability the course\u2019s 45,563 ft of descent demands \u2014 the point isn\u2019t vertical volume, it\u2019s the descent itself.' };
  }
  return { title:'LeBron ramp — up-focus', desc:'Run up, walk down, 150–160 bpm. Real-terrain movement, not a vertical-volume session \u2014 Monday\u2019s incline intervals cover that.' };
}

function scheduleFor(date){
  // Use the block that CONTAINS this date. Looking two weeks ahead can cross a
  // block boundary, and currentBlock() would hand back today's block instead.
  const block = blockFor(date);
  const dow = date.getDay(); // 0 Sun .. 6 Sat
  switch(dow){
    case 1: return { title:'Strength A + incline intervals', desc:'4×3 min, 150–160 bpm, 15–18% grade treadmill.' };
    case 2: return { title:'Rest + capped walk', desc:'Up to 3 miles / under 1 hour. Not training — doesn\u2019t count toward compliance.' };
    case 3: return { title:'Easy run', desc:'25–30 min, Nike Jogging Trail.' };
    case 4: return thursdayWorkout(block);
    case 5: return { title:'Rest', desc:'Full rest day.' };
    case 6: return saturdayWorkout(block, date);
    case 0: return sundayWorkout(block, date);
  }
}

// Weeks run Monday -> Sunday, matching tracker/REFRESH.md and the block boundaries.
const DAY_NAMES = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'];
