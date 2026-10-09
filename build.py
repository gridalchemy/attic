import json, html, re

kb = json.load(open('kb.json',encoding='utf-8'))
principles = json.load(open('principles.json',encoding='utf-8'))
fonts = open('fonts.css',encoding='utf-8').read()

CATS = ['Foundations','Research & Discovery','Analysis & Insight','Architecture & Flows',
        'Prototyping & Fidelity','Visual Craft','Design Systems','Testing & Evaluation',
        'Accessibility','Practice & Career']

BLURB = {
 'Foundations':'What the discipline is, where it came from, and the definitions worth getting precise.',
 'Research & Discovery':'Finding out what is actually true about the people you are designing for.',
 'Analysis & Insight':'Turning what you found into something you can design from.',
 'Architecture & Flows':'How information is structured and how people move through it.',
 'Prototyping & Fidelity':'Making things real enough to learn from, and no more real than that.',
 'Visual Craft':'Perception, hierarchy, grids, colour and the long lineage behind them.',
 'Design Systems':'Documenting decisions so they survive the people who made them.',
 'Testing & Evaluation':'Finding out whether it works, and measuring how well.',
 'Accessibility':'Designing for the range of people who actually exist.',
 'Practice & Career':'Process, collaboration, persuasion, and getting the work shipped.',
}

def md(t):
    """minimal markdown -> html"""
    if not t: return ''
    t = html.escape(t)
    # tables
    def table(m):
        rows=[r for r in m.group(0).strip().split('\n') if r.strip()]
        cells=[[c.strip() for c in r.strip().strip('|').split('|')] for r in rows]
        if len(cells)<2: return m.group(0)
        head=cells[0]; body=[c for c in cells[2:]]
        h='<tr>'+''.join(f'<th>{c}</th>' for c in head)+'</tr>'
        b=''.join('<tr>'+''.join(f'<td>{c}</td>' for c in r)+'</tr>' for r in body)
        return f'<table>{h}{b}</table>'
    t = re.sub(r'(?:^\|.*\|[ \t]*\n)+', table, t, flags=re.M)
    t = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', t, flags=re.S)
    t = re.sub(r'(?<![\w*])\*([^*\n]+?)\*(?![\w*])', r'<em>\1</em>', t)
    t = re.sub(r'`([^`]+)`', r'<code>\1</code>', t)
    t = re.sub(r'^&gt; (.+)$', r'<blockquote>\1</blockquote>', t, flags=re.M)
    out=[]
    for block in re.split(r'\n\s*\n', t):
        b=block.strip()
        if not b: continue
        if b.startswith('<table') or b.startswith('<blockquote'): out.append(b); continue
        lines=b.split('\n')
        if all(re.match(r'^\s*[-•]\s+', l) for l in lines):
            items=''.join(f'<li>{re.sub(r"^\s*[-•]\s+","",l)}</li>' for l in lines)
            out.append(f'<ul>{items}</ul>'); continue
        if all(re.match(r'^\s*\d+\.\s+', l) for l in lines):
            items=''.join(f'<li>{re.sub(r"^\s*\d+\.\s+","",l)}</li>' for l in lines)
            out.append(f'<ol>{items}</ol>'); continue
        if b.startswith('### '): out.append(f'<h4>{b[4:]}</h4>'); continue
        if b.startswith('## '): out.append(f'<h4>{b[3:]}</h4>'); continue
        # mixed list + text
        if any(re.match(r'^\s*[-•]\s+', l) for l in lines):
            buf=[]; cur=[]
            for l in lines:
                if re.match(r'^\s*[-•]\s+', l): cur.append(re.sub(r'^\s*[-•]\s+','',l))
                else:
                    if cur: buf.append('<ul>'+''.join(f'<li>{c}</li>' for c in cur)+'</ul>'); cur=[]
                    buf.append(f'<p>{l}</p>')
            if cur: buf.append('<ul>'+''.join(f'<li>{c}</li>' for c in cur)+'</ul>')
            out.append(''.join(buf)); continue
        out.append('<p>'+b.replace('\n',' ')+'</p>')
    return ''.join(out)

def domain(u):
    m=re.match(r'https?://([^/]+)', u or '')
    return m.group(1).replace('www.','') if m else ''

live=[r for r in kb if r['tier']!='C']
dead=[r for r in kb if r['tier']=='C']
live.sort(key=lambda r:(r['cat'][0], r['title']))

entries=[]
for i,r in enumerate(live):
    links=[r['url']]+[u for u in r.get('extra_urls',[]) if u]
    entries.append({
      'i':i,'t':r['title'],'a':r.get('author',''),'s':r.get('source',''),'y':r.get('year'),
      'cat':r['cat'],'tier':r['tier'],'mod':r.get('module',''),'sub':r.get('submodule',''),
      'sum':md(r.get('summary','')),
      'kp':r.get('key_points',[]),'sr':md(r.get('still_relevant','')),
      'k':r['id'],
      'links':[{'u':u,'d':domain(u)} for u in links],
      'q':(r['title']+' '+r.get('author','')+' '+r.get('source','')+' '+' '.join(r.get('raw_topics',[]))+' '+' '.join(r.get('key_points',[]))).lower()
    })

deadl=[{'t':r['title'],'u':r['url'],'why':r.get('kill_reason',''),'mod':r.get('module','')} for r in dead]

# principles ship as themed groups; guard against dupes within and across groups
seen=set(); prin=[]
for grp in principles:
    items=[]
    for t in grp['items']:
        k=re.sub(r'[^a-z]','',t.lower())[:60]
        if k in seen: continue
        seen.add(k); items.append(t)
    if items: prin.append({'g':grp['g'],'d':grp['d'],'items':items})

# --- link accounting, derived from kb.json so it can never drift ---
def nlinks(r):
    # unlisted_urls were saved and count toward the total, but are not shown
    return (1 if r.get('url') else 0) + len(r.get('extra_urls') or []) + len(r.get('unlisted_urls') or [])

solo   = [r for r in live if nlinks(r) == 1]
clust  = [r for r in live if nlinks(r) > 1]
killct = {}
for r in dead:
    killct[r.get('kill_cat','weak')] = killct.get(r.get('kill_cat','weak'), 0) + nlinks(r)

def slugify(s):
    return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')

# deep-link keys. Published artifacts only pass a bare #token made of
# letters, digits and . _ ~ - so every key is checked against that charset.
tslug = {c: slugify(c) for c in CATS}
PAGE_IDS = ['principles', 'dead', 'about']
ekeys = [e['k'] for e in entries]
allkeys = ekeys + list(tslug.values()) + PAGE_IDS
assert len(allkeys) == len(set(allkeys)), 'deep-link key collision'
bad = [k for k in allkeys if not re.fullmatch(r'[a-z0-9][a-z0-9._~-]*', k)]
assert not bad, 'keys unusable as an artifact hash: %s' % bad

stats = {
  'links_total': sum(nlinks(r) for r in kb),
  'solo':   {'links': sum(nlinks(r) for r in solo),  'entries': len(solo)},
  'clust':  {'links': sum(nlinks(r) for r in clust), 'entries': len(clust)},
  'killed': {'links': sum(nlinks(r) for r in dead),  'entries': len(dead)},
  'biggest': max(nlinks(r) for r in clust),
  'kill': killct,
}
assert stats['solo']['links'] + stats['clust']['links'] + stats['killed']['links'] == stats['links_total']
assert sum(killct.values()) == stats['killed']['links']

data=json.dumps({'e':entries,'d':deadl,'p':prin,'cats':CATS,'blurb':BLURB,'s':stats,'slug':tslug}, ensure_ascii=False)
open('data.json','w',encoding='utf-8',newline='\n').write(data)
print('live',len(entries),'dead',len(deadl),'principles',sum(len(g['items']) for g in prin),'in',len(prin),'groups')
print('links', stats['links_total'], '=', stats['solo']['links'], 'solo +',
      stats['clust']['links'], 'clustered +', stats['killed']['links'], 'killed')
print('deep-link keys', len(allkeys), 'unique, all hash-safe')
print('data size %.0fKB' % (len(data)/1024))
