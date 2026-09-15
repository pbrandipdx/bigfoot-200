PAGES = [("index.html","Today"),("progress.html","Progress"),("log.html","Log"),("blocks.html","Blocks"),("plan.html","Race plan"),("weeks.html","Review")]

NAV_CSS = """
<style id="bf-nav-css">
  #bf-nav{position:sticky;top:0;z-index:999;display:flex;gap:0;background:#152B1D;
    border-bottom:1px solid rgba(255,255,255,.14);overflow-x:auto;-webkit-overflow-scrolling:touch}
  #bf-nav a{flex:1 0 auto;text-align:center;padding:13px 16px;font:600 13px/1
    -apple-system,BlinkMacSystemFont,"Segoe UI",system-ui,sans-serif;letter-spacing:.02em;
    color:#B9C6B4;text-decoration:none;white-space:nowrap;border-bottom:2px solid transparent}
  #bf-nav a[aria-current="page"]{color:#FBFBF8;border-bottom-color:#B0793A}
  @media (max-width:420px){#bf-nav a{padding:12px 11px;font-size:12px}}
</style>
"""

def nav_html(current):
    parts = []
    for h, t in PAGES:
        cur = ' aria-current="page"' if h == current else ''
        parts.append('<a href="%s"%s>%s</a>' % (h, cur, t))
    return NAV_CSS + '<nav id="bf-nav">' + "".join(parts) + '</nav>'

def inject(html, current):
    """Put the nav immediately after <body>."""
    nav = nav_html(current)
    low = html.lower()
    i = low.find("<body")
    if i == -1:
        return nav + html
    j = html.find(">", i)
    return html[:j+1] + "\n" + nav + html[j+1:]
