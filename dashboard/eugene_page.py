"""Render plan/eugene-int1.json as the "Eugene" page.

Standard library only (see dashboard/README.md). Returns an HTML fragment that
build.py wraps with doc_shell, so the page matches the other document pages.

The snapshot is exported from Supabase (training_plan_days, plan_name
'Marathon Intermediate 1 (Eugene)'). It is a fixed 18-week chart, so a snapshot
is enough; re-export it if the plan rows change.
"""
import datetime
import html

DOW = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

ROUTINES = [
    ("DWU1", "Before easy and long runs",
     "Arm swings 6–10 · Side bends 16–20 · Hip circles 10–12 each way · "
     "Half-squat 10–12 · Leg kicks 10–12 per leg · Leg swings 10–12 per leg"),
    ("DWU2", "After DWU1, before marathon-pace runs",
     "Slow skipping, High knees, Butt kicks, Cariocas, Bounders (each 30–50 m and back) · "
     "Sprints 4–6 × 75–100 m, 15 s or less"),
    ("LS", "After runs, never before",
     "Nine stretches, hold 20 s, 1–3 reps: Low back · Shoulder · Chest · Calves · "
     "Gluteal · Groin · Hamstrings · Hip flexors/quads · Hips"),
    ("BWM", "Mondays from week 5, on the cross-training day",
     "Back extension 12–15, hold 2–3 s · Superman 12–15 per side, hold 1–2 s · "
     "Squat · Bridge 12–15, hold 1–3 s"),
]

CSS = """
<style>
  .doc{max-width:1040px}
  .lede{font-size:15.5px;margin:6px 0 14px}
  .stats{display:flex;flex-wrap:wrap;gap:10px;margin:14px 0 6px}
  .stat{background:var(--white);border:1px solid var(--line);border-radius:8px;
    padding:9px 13px;min-width:112px}
  .stat b{display:block;font-size:20px;color:var(--forest);line-height:1.2}
  .stat span{font-size:12px;color:var(--ink-faint);letter-spacing:.03em;text-transform:uppercase}
  table.sched th,table.sched td{white-space:normal;text-align:center;padding:8px 7px;
    min-width:64px;font-size:13.5px;line-height:1.3}
  table.sched td.wk{text-align:left;white-space:nowrap;min-width:92px}
  table.sched td.wk b{display:block;color:var(--forest)}
  table.sched td.wk span{font-size:12px;color:var(--ink-faint)}
  table.sched td.tot{font-weight:650;color:var(--forest)}
  td .mi{display:block;font-weight:650;color:var(--ink)}
  td .lb{display:block;font-size:11.5px;color:var(--ink-faint);letter-spacing:.02em}
  td.rest,td.cross{color:var(--ink-faint)}
  td.rest .mi,td.cross .mi{font-weight:500;color:var(--ink-faint)}
  td.pace{background:#F2E6D3}
  td.pace .mi{color:var(--amber-deep)}
  td.long .mi{color:var(--forest)}
  td.race{background:var(--forest)}
  td.race .mi,td.race .lb{color:var(--white)}
  td.flag{box-shadow:inset 0 0 0 2px var(--amber)}
  td.race sup.f{color:#F2E6D3}
  sup.f{color:var(--amber-deep);font-weight:700;margin-left:1px}
  tr.now td{border-top:2px solid var(--amber);border-bottom:2px solid var(--amber)}
  tr.now td.wk b::after{content:" \\2022 this week";color:var(--amber-deep);font-weight:600;
    font-size:11.5px}
  @media (max-width:560px){
    table.sched{min-width:0;width:100%}
    table.sched th,table.sched td{padding:7px 2px;min-width:0;font-size:12.5px}
    table.sched th{font-size:10.5px;letter-spacing:0}
    table.sched td.wk{min-width:0;padding-left:6px}
    table.sched td.wk span{font-size:10.5px}
    td .lb{font-size:9.5px;letter-spacing:0}
    sup.f{font-size:9px}
    tr.now td.wk b::after{content:""}
  }
  .tw.sm table{min-width:0}
  .tw.sm td,.tw.sm th{white-space:normal;text-align:left}
  ol.fl{padding-left:1.4em;font-size:14.5px}
</style>
"""

NOW_JS = """
<script>
(function(){
  var d=new Date(), t=new Date(d.getFullYear(),d.getMonth(),d.getDate()).getTime();
  var rows=document.querySelectorAll('tr[data-start]');
  for(var i=0;i<rows.length;i++){
    var p=rows[i].getAttribute('data-start').split('-');
    var s=new Date(+p[0],+p[1]-1,+p[2]).getTime();
    if(t>=s && t<s+7*86400000){rows[i].className+=' now';}
  }
})();
</script>
"""


def _fmt_mi(m):
    return ("%g" % m) if m is not None else ""


def _cell(r, fnum):
    kind, sess, mi = r["kind"], r["session"], r.get("miles")
    cls, top, lab = [], "", ""
    if kind == "mobility":
        cls, top, lab = ["cross"], "Cross", "60 min"
    elif kind == "rest":
        cls, top = ["rest"], "Rest"
    elif kind == "race":
        cls, top, lab = ["race"], _fmt_mi(mi), ("Eugene" if "Eugene" in sess else "half")
    elif sess == "Marathon-pace run":
        cls, top, lab = ["pace"], _fmt_mi(mi), "pace"
    elif sess == "Long Run":
        cls, top, lab = ["long"], _fmt_mi(mi), "long"
    else:
        top, lab = _fmt_mi(mi), "easy"
    mark = ""
    if r.get("flag"):
        cls.append("flag")
        mark = '<sup class="f">%d</sup>' % fnum
    return ('<td class="%s"><span class="mi">%s%s</span><span class="lb">%s</span></td>'
            % (" ".join(cls), html.escape(top), mark, html.escape(lab)))


def render(doc):
    rows = doc["rows"]
    weeks = {}
    for r in rows:
        weeks.setdefault(r["week"], []).append(r)
    totals = {w: sum(x.get("miles") or 0 for x in rs) for w, rs in weeks.items()}
    peak_w = max(totals, key=totals.get)
    long_max = max((r["miles"] for r in rows if r["session"] == "Long Run"), default=0)

    flags, flag_no = [], {}
    for r in rows:
        if r.get("flag"):
            flags.append((r["date"], r["flag"]))
            flag_no[r["date"]] = len(flags)

    start = datetime.date.fromisoformat(doc["start"])
    race = datetime.date.fromisoformat(doc["race"])

    out = [CSS]
    out.append("<h1>%s</h1>" % html.escape(doc["title"]))
    out.append('<p class="lede">%d weeks from %s to the Eugene Marathon on %s. Goal %s, '
               "which is %s per mile. A run-only chart schedule, dated to finish at Eugene. "
               "It sits alongside your Eugene plan and does not replace it.</p>"
               % (len(weeks), start.strftime("%b %-d, %Y"), race.strftime("%a %b %-d, %Y"),
                  html.escape(doc["goal"]), html.escape(doc["goal_pace"])))
    out.append('<div class="stats">'
               '<div class="stat"><b>%d mi</b><span>Peak week (wk %d)</span></div>'
               '<div class="stat"><b>%g mi</b><span>Longest run</span></div>'
               '<div class="stat"><b>%d mi</b><span>Week 1</span></div></div>'
               % (totals[peak_w], peak_w, long_max, totals[1]))

    out.append("<h2>Week by week</h2>")
    out.append('<p>Amber cells are runs at goal marathon pace (%s per mile). Mondays are 60 minutes of '
               "low-impact cross-training. Outlined cells collide with a race or gate you already have; "
               "see the notes below the table.</p>" % html.escape(doc["goal_pace"]))
    out.append('<div class="tw"><table class="sched"><thead><tr><th>Week</th>%s<th>Miles</th></tr></thead><tbody>'
               % "".join("<th>%s</th>" % d for d in DOW))
    for w in sorted(weeks):
        rs = sorted(weeks[w], key=lambda x: x["dow"])
        s = datetime.date.fromisoformat(rs[0]["date"])
        out.append('<tr data-start="%s"><td class="wk"><b>Wk %d</b><span>%s</span></td>%s'
                   '<td class="tot">%s</td></tr>'
                   % (s.isoformat(), w, s.strftime("%b %-d"),
                      "".join(_cell(r, flag_no.get(r["date"], 0)) for r in rs),
                      _fmt_mi(totals[w])))
    out.append("</tbody></table></div>")

    if flags:
        out.append("<h3>Conflicts with your races</h3><ol class=\"fl\">")
        for d, text in flags:
            dd = datetime.date.fromisoformat(d)
            out.append("<li><strong>%s.</strong> %s</li>" % (dd.strftime("%a %b %-d"), html.escape(text)))
        out.append("</ol>")

    out.append("<h2>Warm-up, stretching and strength</h2>")
    out.append("<p>Where each routine goes in the schedule. Move names and counts are in the "
               "<code>ref_exercises</code> table in Supabase.</p>")
    out.append('<div class="tw sm"><table><thead><tr><th>Routine</th><th>When</th><th>Moves</th></tr></thead><tbody>')
    for code, when, moves in ROUTINES:
        out.append("<tr><td><strong>%s</strong></td><td>%s</td><td>%s</td></tr>"
                   % (code, html.escape(when), moves))
    out.append("</tbody></table></div>")

    out.append("<h2>Paces for a %s goal</h2>" % html.escape(doc["goal_pace"]))
    out.append("<p>From the book's pace chart, per mile.</p>")
    out.append('<div class="tw sm"><table><thead><tr><th>Effort</th><th>Pace</th></tr></thead><tbody>')
    for name, pace in doc["paces_for_goal"]:
        out.append("<tr><td>%s</td><td><strong>%s</strong></td></tr>" % (html.escape(name), html.escape(pace)))
    out.append("</tbody></table></div>")

    out.append('<p style="font-size:12.5px;color:var(--ink-faint)">Snapshot of the Supabase plan '
               "&ldquo;%s&rdquo; taken %s.</p>" % (html.escape(doc["plan_name"]), html.escape(doc["snapshot"])))
    out.append(NOW_JS)
    return "\n".join(out)
