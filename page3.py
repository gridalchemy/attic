fonts=open('fonts.css',encoding='utf-8').read(); CSS=open('css3.txt',encoding='utf-8').read(); JS=open('js3.txt',encoding='utf-8').read()
data=open('data.json',encoding='utf-8').read()
H=f"""<!DOCTYPE html>
<html lang="en" data-pal="madder" data-mode="light" data-disp="newsreader" data-body="literata" data-sans="instrument" data-mono="spline">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Attic — a salvaged UX reading list</title>
<meta name="description" content="286 links of supplementary reading from a UX design curriculum that no longer exists, read again and written up. No tracking, no logins, no external requests.">
<style>{fonts}</style>
<style>{CSS}</style>
</head>
<body data-mode="browse" data-list="off">

<button class="menubtn" id="menubtn" aria-label="Open navigation">
  <svg width="15" height="15" viewBox="0 0 16 16" aria-hidden="true"><path d="M2 4h12M2 8h12M2 12h12" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg>
  Menu
</button>
<div class="scrim" aria-hidden="true"></div>

<aside class="nav">
  <div class="navtop">
    <button class="brand" aria-label="Back to start">
      <h1>Attic<span class="dot">.</span></h1>
      <small>A salvaged reading list</small>
    </button>
  </div>
  <div class="srch">
    <svg width="13" height="13" viewBox="0 0 16 16" fill="none" aria-hidden="true"><circle cx="7" cy="7" r="5" stroke="currentColor" stroke-width="1.7"/><path d="M11 11l3.5 3.5" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"/></svg>
    <input id="q" type="search" placeholder="Search…" aria-label="Search the archive">
  </div>
  <div class="navscroll" id="nav"></div>
  <div class="navfoot">
    <p class="counts">118 entries<br>286 links read</p>
    <div class="tools">
      <a class="stamp" id="stamp" href="https://icvc.framer.website/" target="_blank" rel="noopener noreferrer" aria-label="Peri — Lia's portfolio">
        <svg viewBox="0 0 32 32" width="24" height="24" fill="none" aria-hidden="true">
          <g stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round">
            <path d="M 7.83 10.54 A 4 4 0 0 1 10.63 9.4 L 21.37 9.4 A 4 4 0 0 1 24.17 10.54 L 26.5 12.83 A 5 5 0 0 1 28 16.4 L 28 19.63 A 5 5 0 0 1 27.48 21.85 L 24.67 27.56 A 2.6 2.6 0 0 0 24.4 28.71 L 24.4 29.05 A 0.95 0.95 0 0 1 23.45 30 L 20.5 30 A 1.3 1.3 0 0 1 19.22 28.91 L 19.2 28.8 A 1.44 1.44 0 0 0 17.78 27.6 L 14.22 27.6 A 1.44 1.44 0 0 0 12.8 28.8 L 12.78 28.91 A 1.3 1.3 0 0 1 11.5 30 L 8.55 30 A 0.95 0.95 0 0 1 7.6 29.05 L 7.6 28.71 A 2.6 2.6 0 0 0 7.33 27.56 L 4.52 21.85 A 5 5 0 0 1 4 19.63 L 4 16.4 A 5 5 0 0 1 5.5 12.83 Z"/>
            <path d="M 16 10.4 L 16 7.4"/>
            <path d="M 10.6 17 h 0.01 M 21.4 17 h 0.01" stroke-width="4.3"/>
          </g>
          <circle cx="16" cy="4.6" r="2.3" fill="var(--peri-bulb, #8E94F2)"/>
        </svg>
      </a>
      <span class="toolpair">
        <button class="icbtn" id="paltog" type="button" aria-label="Change accent colour">
          <svg viewBox="0 0 24 24" width="17" height="17" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 22a1 1 0 0 1 0-20 10 9 0 0 1 10 9 5 5 0 0 1-5 5h-2.25a1.75 1.75 0 0 0-1.4 2.8l.3.4a1.75 1.75 0 0 1-1.4 2.8z"/><circle cx="13.5" cy="6.5" r=".5" fill="currentColor"/><circle cx="17.5" cy="10.5" r=".5" fill="currentColor"/><circle cx="6.5" cy="12.5" r=".5" fill="currentColor"/><circle cx="8.5" cy="7.5" r=".5" fill="currentColor"/></svg>
        </button>
        <button class="icbtn" id="modetog" type="button" aria-label="Switch to dark mode">
          <svg class="i-moon" viewBox="0 0 24 24" width="17" height="17" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"/></svg>
          <svg class="i-sun" viewBox="0 0 24 24" width="17" height="17" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v2"/><path d="M12 20v2"/><path d="m4.93 4.93 1.41 1.41"/><path d="m17.66 17.66 1.41 1.41"/><path d="M2 12h2"/><path d="M20 12h2"/><path d="m6.34 17.66-1.41 1.41"/><path d="m19.07 4.93-1.41 1.41"/></svg>
        </button>
      </span>
    </div>
  </div>
</aside>

<section class="list">
  <div class="listhead" id="listhead"></div>
  <div class="listscroll" id="listscroll"></div>
</section>

<main id="scroller"><div class="pad" id="main"></div></main>


<script>window.__D__ = {data};</script>
<script>{JS}</script>
</body>
</html>"""
open('index.html','w',encoding='utf-8',newline='\n').write(H)
print('%.0f KB'%(len(H.encode())/1024))
