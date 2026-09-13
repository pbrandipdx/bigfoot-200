"""Wrap rendered markdown in a mobile-first page matching the dashboard palette."""

SHELL = """<!DOCTYPE html>
<html lang="en"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>__TITLE__ · Bigfoot 200</title>
<style>
  :root{--paper:#EFF1EA;--paper-2:#E4E7DD;--ink:#131C15;--ink-soft:#33402F;
    --ink-faint:#5C6B58;--forest:#20402C;--amber:#B0793A;--amber-deep:#7A521F;
    --line:#C7CCBE;--white:#FBFBF8;color-scheme:light}
  *{box-sizing:border-box}
  body{margin:0;background:var(--paper);color:var(--ink);
    font:16px/1.62 -apple-system,BlinkMacSystemFont,"Segoe UI",system-ui,sans-serif;
    -webkit-text-size-adjust:100%}
  .doc{max-width:760px;margin:0 auto;padding:22px 18px 72px}
  .doc>*:first-child{margin-top:0}
  h1{font-size:25px;line-height:1.22;letter-spacing:-.015em;color:var(--forest);margin:30px 0 6px}
  h2{font-size:19px;line-height:1.3;color:var(--forest);margin:34px 0 8px;
    padding-top:14px;border-top:1px solid var(--line)}
  h3{font-size:16px;color:var(--ink-soft);margin:22px 0 6px}
  p,li{color:var(--ink-soft)}
  strong{color:var(--ink);font-weight:650}
  em{color:var(--ink-faint)}
  a{color:var(--amber-deep);text-underline-offset:2px}
  ul,ol{padding-left:1.25em}
  li{margin:3px 0}
  hr{border:0;border-top:1px solid var(--line);margin:26px 0}
  blockquote{margin:16px 0;padding:12px 14px;background:var(--paper-2);
    border-left:3px solid var(--amber);border-radius:0 6px 6px 0}
  blockquote p{margin:6px 0;font-size:14.5px}
  code{background:var(--paper-2);padding:1px 5px;border-radius:4px;font-size:.88em}
  .trend{display:inline-block;width:1.1em;text-align:center;font-weight:700;
    line-height:1;cursor:help;font-size:1.05em}
  .trend-good{color:#2E7D46}
  .trend-bad{color:#A23B2C}
  .trend-level{color:#8A9585;font-weight:500}
  pre{background:var(--paper-2);padding:12px;border-radius:8px;overflow-x:auto}
  pre code{background:none;padding:0}
  .tw{overflow-x:auto;-webkit-overflow-scrolling:touch;margin:14px 0;
    border:1px solid var(--line);border-radius:8px;background:var(--white)}
  table{border-collapse:collapse;width:100%;min-width:max-content;font-size:14px}
  th,td{padding:8px 11px;text-align:left;border-bottom:1px solid var(--line);
    white-space:nowrap}
  thead th{background:var(--forest);color:var(--white);font-weight:600;
    font-size:12.5px;letter-spacing:.03em;text-transform:uppercase;position:sticky;top:0}
  tbody tr:last-child td{border-bottom:0}
  tbody tr:nth-child(even){background:var(--paper)}
  td strong{color:var(--forest)}
  .src{margin-top:40px;padding-top:14px;border-top:1px solid var(--line);
    font-size:12.5px;color:var(--ink-faint)}
  @media (max-width:420px){
    .doc{padding:18px 14px 64px}
    h1{font-size:22px} h2{font-size:17.5px} body{font-size:15.5px}
  }
</style>
</head><body>
<main class="doc">
__CONTENT__
<p class="src">Generated from <code>__SOURCE__</code> in the private
<code>bigfoot-200</code> repo. Don't edit this page — edit the source and run
<code>make dashboard</code>.</p>
</main>
</body></html>
"""

def render(title, content_html, source):
    return (SHELL.replace("__TITLE__", title)
                 .replace("__CONTENT__", content_html)
                 .replace("__SOURCE__", source))
