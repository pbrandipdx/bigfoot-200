"""Minimal Markdown -> HTML for the plan docs. Python stdlib only.

Deliberately dependency-free: the build must produce byte-identical output on
the Mac mini, the MacBook and any sandbox, with no pip install anywhere.
Supports what plan/*.md actually uses: ATX headings, GFM tables, blockquotes,
lists, hr, bold/italic, inline code, links.
"""
import re, html as _html

# Trend markers. weekly_report.py emits {{up}} / {{down-bad}} etc.; they render
# as a coloured arrow so direction and verdict read at a glance instead of from
# a legend. This is the ONLY markup the renderer produces from document text -
# everything else stays escaped.
_TRENDS = {
    'up':       ('\u2191', 'good',  'up on last week - the direction you want'),
    'down':     ('\u2193', 'good',  'down on last week - the direction you want'),
    'up-bad':   ('\u2191', 'bad',   'up on last week - the wrong direction'),
    'down-bad': ('\u2193', 'bad',   'down on last week - the wrong direction'),
    'level':    ('\u2192', 'level', 'level with last week'),
}
_TREND_RE = re.compile(r'\{\{(' + '|'.join(_TRENDS) + r')\}\}')


def _trend(m):
    glyph, kind, title = _TRENDS[m.group(1)]
    return ('<span class="trend trend-%s" title="%s" aria-label="%s">%s</span>'
            % (kind, title, title, glyph))


def _inline(s):
    s = _html.escape(s, quote=False)
    s = _TREND_RE.sub(_trend, s)
    s = re.sub(r'`([^`]+)`', r'<code>\1</code>', s)
    s = re.sub(r'\[([^\]]+)\]\(([^)\s]+)\)', r'<a href="\2">\1</a>', s)
    s = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', s)
    s = re.sub(r'(?<![\w*])\*([^*\n]+)\*(?![\w*])', r'<em>\1</em>', s)
    return s

def _row(line):
    line = line.strip()
    if line.startswith('|'): line = line[1:]
    if line.endswith('|'): line = line[:-1]
    return [c.strip() for c in line.split('|')]

_DIV = re.compile(r'^\s*\|?\s*:?-{2,}:?\s*(\|\s*:?-{2,}:?\s*)*\|?\s*$')

def render(text):
    lines = text.replace('\r\n', '\n').split('\n')
    out, i, n = [], 0, len(lines)
    while i < n:
        line = lines[i]
        s = line.strip()

        if not s:
            i += 1; continue

        if re.match(r'^(---+|\*\*\*+|___+)$', s):
            out.append('<hr />'); i += 1; continue

        m = re.match(r'^(#{1,6})\s+(.*)$', s)
        if m:
            lv = len(m.group(1))
            out.append('<h%d>%s</h%d>' % (lv, _inline(m.group(2).strip()), lv))
            i += 1; continue

        # GFM table: header row, then a divider row
        if s.startswith('|') and i + 1 < n and _DIV.match(lines[i+1]):
            head = _row(s); i += 2
            body = []
            while i < n and lines[i].strip().startswith('|'):
                body.append(_row(lines[i])); i += 1
            t = ['<div class="tw"><table>', '<thead>', '<tr>']
            t += ['<th>%s</th>' % _inline(c) for c in head]
            t += ['</tr>', '</thead>', '<tbody>']
            for r in body:
                t.append('<tr>')
                t += ['<td>%s</td>' % _inline(c) for c in r]
                t.append('</tr>')
            t += ['</tbody>', '</table></div>']
            out.append('\n'.join(t)); continue

        if s.startswith('>'):
            buf = []
            while i < n and lines[i].strip().startswith('>'):
                buf.append(re.sub(r'^\s*>\s?', '', lines[i])); i += 1
            out.append('<blockquote>\n%s\n</blockquote>' % render('\n'.join(buf)))
            continue

        m = re.match(r'^([-*+]|\d+\.)\s+', s)
        if m:
            ordered = not m.group(1) in ('-', '*', '+')
            tag = 'ol' if ordered else 'ul'
            items = []
            while i < n:
                cur = lines[i]; c = cur.strip()
                mm = re.match(r'^([-*+]|\d+\.)\s+(.*)$', c)
                if mm:
                    items.append(mm.group(2))
                elif c and cur[:1] in ' \t' and items:
                    items[-1] += ' ' + c          # lazy continuation
                else:
                    break
                i += 1
            out.append('<%s>\n%s\n</%s>' % (
                tag, '\n'.join('<li>%s</li>' % _inline(x) for x in items), tag))
            continue

        # paragraph
        buf = []
        while i < n and lines[i].strip() and not re.match(
                r'^\s*(#{1,6}\s|>|[-*+]\s|\d+\.\s|\|)', lines[i]) and not re.match(
                r'^(---+|\*\*\*+|___+)$', lines[i].strip()):
            buf.append(lines[i].strip()); i += 1
        if buf:
            out.append('<p>%s</p>' % _inline(' '.join(buf)))
        else:
            i += 1
    return '\n'.join(out)
