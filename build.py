# -*- coding: utf-8 -*-
import json,os,shutil,sys,html,re,glob
SITE=sys.argv[1].rstrip('/'); OUT=sys.argv[2]
SITE_PRE=SITE
FB="https://www.facebook.com/share/1FDAMTnfQQ/"; WEB="https://awiu.net"
shutil.rmtree(OUT,ignore_errors=True); os.makedirs(OUT+'/news')
shutil.copytree('img',OUT+'/img')
if os.path.isdir('admin'):
    shutil.copytree('admin',OUT+'/admin')
    _c=open(OUT+'/admin/config.yml',encoding='utf-8').read().replace('SITE_URL_PLACEHOLDER',SITE)
    open(OUT+'/admin/config.yml','w',encoding='utf-8').write(_c)
MON={'يناير':1,'فبراير':2,'مارس':3,'أبريل':4,'مايو':5,'يونيو':6,'يوليو':7,'أغسطس':8,'سبتمبر':9,'أكتوبر':10,'نوفمبر':11,'ديسمبر':12}
MONR={v:k for k,v in MON.items()}
BASE=["اتحاد_المستثمرات_العرب","د_هدى_يسى"]
def dkey(i):
    iso=i.get('date_iso')
    if iso:
        y,m,d=map(int,str(iso)[:10].split('-')); return (y,m,d)
    d=i['date']; y=int(re.search(r'\d{4}',d).group()); m=[v for k,v in MON.items() if k in d][0]
    dm=re.search(r'(\d{1,2})\s+[^\s\d]+\s+\d{4}',d); dd=int(dm.group(1)) if dm else 15
    return (y,m,dd)
M=json.load(open('data/misc.json',encoding='utf-8')); YT=[tuple(x) for x in M['YT']]; FBV=[tuple(x) for x in M['FBV']]
items=[]
for f in glob.glob('content/*.json'):
    o=json.load(open(f,encoding='utf-8'))
    o.setdefault('cats',None); o['cats']=o['cats'] or [o['cat']]
    if o.get('date_iso'):
        y,m,d=map(int,str(o['date_iso'])[:10].split('-')); o['date']=f"{d} {MONR[m]} {y}"
    else: o['date']=o.get('date_text') or ''
    o['ar']=[p for p in (o.get('ar') or []) if p]; o['en']=[p for p in (o.get('en') or []) if p]
    o['tags']=[t.strip().lstrip('#').replace(' ','_') for t in (o.get('tags') or []) if t and t.strip()]
    for t in reversed(BASE):
        if t not in o['tags']: o['tags'].insert(0,t)
    o['tag']=o.get('tag') or ''
    o['en_title']=o.get('en_title') or ''
    o['img']=os.path.basename(o['image'])[:-4] if o.get('image') else None
    if o.get('draft'): continue
    items.append(o)
items.sort(key=lambda i:(dkey(i),i.get('order',0)),reverse=True)
CATS=[("visits","زيارات","Visits"),("forums","ملتقيات","Forums"),("summit","أخبار القمة","Summit News"),("intl","مشاركات دولية","International"),("agreements","اتفاقيات وبروتوكولات","Agreements & Protocols")]
E=html.escape
css=open('base.css').read()
extra='''
body{font-size:19px}
.hero{padding:44px 0 34px}.hero h1{font-size:38px}
nav{display:flex!important;flex-wrap:wrap;justify-content:flex-end;align-items:center}
nav a{text-align:center;margin-inline-start:16px;font-size:17px;color:var(--mute)}
nav a i{display:block;font-style:normal;font-size:12px;direction:ltr;opacity:.7;line-height:1.2}
nav a.on{color:var(--gold);border-bottom:2px solid var(--gold)}
.btn{background:#1877f2;color:#fff!important;border-radius:8px;padding:2px 12px;display:inline-block}.btn.web{background:var(--gold);color:#111!important}
.pagehead{padding:36px 0 6px}.pagehead h1{font-size:38px;color:var(--gold);line-height:1.5}.pagehead h2{font-size:19px;color:var(--mute);font-weight:400;direction:ltr;text-align:right}
.cards{display:grid;grid-template-columns:repeat(3,1fr);gap:22px;margin-top:20px}
.nc{background:var(--card);border:1px solid var(--line);border-radius:14px;overflow:hidden;display:flex;flex-direction:column;transition:.15s}
.nc:hover{border-color:var(--gold);transform:translateY(-2px)}
.nc .ph{aspect-ratio:16/10;background:#10151d center/cover no-repeat}
.nc .ph.logo{background-size:40%;background-color:#10151d}
.nc .tx{padding:16px 18px 20px}.nc h4{font-size:20px;line-height:1.7;margin:4px 0 6px}.nc .e{direction:ltr;text-align:left;color:var(--mute);font-size:14.5px;line-height:1.5}
.nc.big{grid-column:1/-1;flex-direction:row}.nc.big .ph{flex:1.2;aspect-ratio:auto;min-height:320px}.nc.big .tx{flex:1;padding:28px}.nc.big h4{font-size:28px}.nc.big .e{font-size:16px}
.empty{margin-top:20px}
.art{max-width:860px;margin:0 auto;padding:30px 24px 60px}
.art h1{font-size:34px;line-height:1.6;margin:8px 0}.art .en-h{direction:ltr;text-align:left;color:var(--mute);font-size:20px;line-height:1.5;margin-bottom:18px}
.art img.hero-i{width:100%;border-radius:14px;margin:12px 0 20px;max-height:520px;object-fit:cover}
.art p{margin-bottom:14px;font-size:21px}.art .en-t{font-size:17px;margin-top:22px;padding-top:18px;border-top:1px solid var(--line)}
.vid{aspect-ratio:16/9;margin:18px 0}.vid iframe{width:100%;height:100%;border:0;border-radius:12px}
.share{display:flex;flex-wrap:wrap;gap:8px;margin:22px 0;align-items:center;font-size:15px;color:var(--mute)}
.share a,.share button{background:#222b3a;color:var(--text);border:1px solid var(--line);border-radius:20px;padding:2px 14px;font:inherit;font-size:15px;cursor:pointer}
.share a:hover,.share button:hover{border-color:var(--gold);color:var(--gold)}
.back{display:inline-block;color:var(--gold);margin-bottom:10px}
.vh{font-size:24px;color:var(--gold);margin:30px 0 14px}.vh span{color:var(--mute);font-size:16px;direction:ltr;margin-inline-start:10px}
.vg{display:grid;grid-template-columns:repeat(3,1fr);gap:20px}
.vc{background:var(--card);border:1px solid var(--line);border-radius:12px;overflow:hidden}
.vt{position:relative;aspect-ratio:16/9;background:#000 center/cover no-repeat;cursor:pointer}
.vt:after{content:"\\25B6";position:absolute;inset:0;display:flex;align-items:center;justify-content:center;font-size:44px;color:#fff;background:rgba(0,0,0,.35)}
.vt.play:after{display:none}.vt iframe{position:absolute;inset:0;width:100%;height:100%;border:0}
.vc p{padding:10px 14px;font-size:16px;line-height:1.6}
@media(max-width:800px){.cards,.vg{grid-template-columns:1fr}.nc.big{flex-direction:column}.nc.big .ph{min-height:220px}.hero h1{font-size:28px}.art h1{font-size:26px}nav a{margin-inline-start:10px;font-size:15px}.nav{flex-wrap:wrap}}
'''
NAV=[("home","الرئيسية","Home","/#home")]+[(c,a,e,f"/#{c}") for c,a,e in CATS]+[("media","تغطيات القنوات والإعلام","Media Coverage","/#media"),("videos","فيديوهات","Videos","/#videos"),("about","عن الاتحاد","About","/#about")]
def ticker():
    top=sorted(items,key=dkey,reverse=True)[:10]
    a=''.join(f'<a href="/news/{i["id"]}/"><b>●</b> {E(i["title"])}</a>' for i in top)
    return f'<div class="tk" dir="rtl"><span class="tl">آخر الأخبار<i>Latest</i></span><div class="tv"><div class="tt">{a}{a}</div></div></div>'
TKCSS=".tk{display:flex;align-items:stretch;background:#0b1018;border-bottom:1px solid var(--line);border-top:1px solid var(--line);direction:rtl}.tl{flex:none;background:var(--gold);color:#111;font-weight:700;font-size:18px;padding:8px 18px;line-height:1.2;text-align:center}.tl i{display:block;font-style:normal;font-size:11px;direction:ltr}.tv{flex:1;overflow:hidden;white-space:nowrap}.tt{display:inline-block;padding-inline-end:0;animation:tkm 140s linear infinite;will-change:transform}.tt:hover{animation-play-state:paused}.tt a{display:inline-block;color:var(--text);font-size:19px;padding:10px 28px;line-height:1.5}.tt a b{color:var(--gold);font-size:12px;margin-inline-end:8px}.tt a:hover{color:var(--gold)}@keyframes tkm{from{transform:translateX(0)}to{transform:translateX(50%)}}@media(max-width:800px){.tl{font-size:15px;padding:6px 10px}.tt a{font-size:16px}}@media(prefers-reduced-motion:reduce){.tt{animation:none}.tv{overflow-x:auto}}"
def header(active):
    n=''.join(f'<a href="{h}" data-p="{p}"{" class=on" if p==active else ""}>{a}<i>{e}</i></a>' for p,a,e,h in NAV)
    n+=f'<a class="btn" href="{FB}" target="_blank" rel="noopener">فيسبوك<i>Facebook</i></a><a class="btn yt" href="https://www.youtube.com/@ArabWomenInvestorsUnion" target="_blank" rel="noopener">يوتيوب<i>YouTube</i></a><a class="btn web" href="{WEB}" target="_blank" rel="noopener">الموقع الرسمي<i>awiu.net</i></a>'
    return f'<header><div class="wrap nav"><a class="brand" href="/#home"><img src="/img/logo.jpg" alt="شعار اتحاد المستثمرات العرب"><div><b>اتحاد المستثمرات العرب</b><small>Arab Women Investors Union</small></div></a><nav>{n}</nav></div></header>'+ticker()
FOOT=f'<footer><div class="wrap">© 2026 اتحاد المستثمرات العرب<div class="en">Arab Women Investors Union</div><div style="margin-top:12px"><a class="btn" href="{FB}" target="_blank" rel="noopener">فيسبوك · Facebook</a> <a class="btn yt" href="https://www.youtube.com/@ArabWomenInvestorsUnion" target="_blank" rel="noopener">يوتيوب · YouTube</a> <a class="btn web" href="{WEB}" target="_blank" rel="noopener">awiu.net</a></div></div></footer>'
def head(title,desc,url,img,typ):
    return f'''<!DOCTYPE html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{E(title)}</title><meta name="description" content="{E(desc)}">
<meta property="og:type" content="{typ}"><meta property="og:site_name" content="اتحاد المستثمرات العرب"><meta property="og:locale" content="ar_AR"><meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}"><meta property="og:url" content="{url}"><meta property="og:image" content="{img}">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{E(title)}"><meta name="twitter:image" content="{img}"><link rel="icon" href="/img/logo.jpg"><style>{css}{extra}{extra2}{TKCSS}</style></head><body>'''
extra2='header nav a[data-p]{margin-inline-start:6px!important;font-size:12.5px!important}header nav a.btn{margin-inline-start:6px!important;padding:1px 6px!important;font-size:12px!important}header .brand img{width:44px;height:44px}header .brand b{font-size:14px!important}header .brand small{display:none}header nav{justify-content:flex-start!important}.btn.yt{background:#e62117!important;color:#fff!important}@keyframes lg{0%,100%{box-shadow:0 0 0 0 rgba(212,175,55,0);filter:brightness(1)}50%{box-shadow:0 0 18px 4px rgba(212,175,55,.45);filter:brightness(1.12)}}@keyframes sh{0%,70%{transform:translateX(-120%)}100%{transform:translateX(120%)}}@keyframes tb{0%{color:var(--gold);text-shadow:0 0 10px rgba(212,175,55,.8)}9%{color:var(--gold);text-shadow:0 0 10px rgba(212,175,55,.8)}13%,100%{text-shadow:none}}@keyframes ar{0%{opacity:0;transform:translateY(3px)}3%,9%{opacity:1;transform:none}13%,100%{opacity:0}}header .brand img{border-radius:50%;animation:lg 3.6s ease-in-out infinite}header nav a[data-p]{position:relative;padding-bottom:7px;animation:tb 8.1s linear infinite}header nav a[data-p]::after{content:"";position:absolute;left:50%;bottom:-3px;margin-left:-5px;width:0;height:0;border-left:5px solid transparent;border-right:5px solid transparent;border-bottom:6px solid #d4af37;opacity:0;animation:ar 8.1s linear infinite;animation-delay:inherit}header .brand{position:relative;overflow:hidden}header .brand::after{content:"";position:absolute;top:0;bottom:0;width:30%;left:0;background:linear-gradient(100deg,transparent,rgba(255,255,255,.14),transparent);animation:sh 5s ease-in-out infinite;pointer-events:none}header nav a[data-p]:nth-of-type(1){animation-delay:0.0s}header nav a[data-p]:nth-of-type(2){animation-delay:0.9s}header nav a[data-p]:nth-of-type(3){animation-delay:1.8s}header nav a[data-p]:nth-of-type(4){animation-delay:2.7s}header nav a[data-p]:nth-of-type(5){animation-delay:3.6s}header nav a[data-p]:nth-of-type(6){animation-delay:4.5s}header nav a[data-p]:nth-of-type(7){animation-delay:5.4s}header nav a[data-p]:nth-of-type(8){animation-delay:6.3s}header nav a[data-p]:nth-of-type(9){animation-delay:7.2s}@media(prefers-reduced-motion:reduce){header .brand img,header .brand::after,header nav a[data-p],header nav a[data-p]::after{animation:none!important}}header .nav{flex-wrap:nowrap!important;gap:10px}header .brand{flex:none}header .brand b{font-size:16px}header .brand small{font-size:11px}header nav{flex-wrap:nowrap!important;flex:1;justify-content:flex-end;overflow-x:auto;scrollbar-width:none;gap:0}header nav::-webkit-scrollbar{display:none}header nav a{white-space:nowrap;font-size:13.5px!important;margin-inline-start:9px!important;flex:none}header nav a i{font-size:9.5px!important}header nav a.btn{padding:1px 8px!important;font-size:13px!important;border-radius:6px}.wrap{max-width:1240px}@media(max-width:800px){header .brand div{display:none}header nav a{margin-inline-start:8px!important}}.ht{color:var(--gold);font-size:15px;line-height:1.9;margin:6px 0;word-break:break-word}.art .ht{font-size:18px;margin:10px 0}.ml{display:flex;flex-direction:column;gap:12px;margin-top:16px}.mi{display:flex;gap:14px;align-items:center;background:var(--card);border:1px solid var(--line);border-radius:12px;padding:14px 18px;color:var(--text)}.mi:hover{border-color:var(--gold)}.mi b{background:#222b3a;color:var(--gold);border-radius:8px;padding:2px 12px;white-space:nowrap;font-size:16px}.mi span{flex:1;font-size:18px;line-height:1.6}.mi em{font-style:normal;color:var(--mute);font-size:14px;white-space:nowrap}.vc a.fbv{display:block;padding:26px 14px;text-align:center;color:#fff;background:#1877f2;font-size:18px}.mh{font-size:22px;color:var(--gold);margin:26px 0 4px}\n'
def imgurl(i): return f"{SITE}/img/{i['img'] or 'logo'}.jpg"
def HT(i): return ' '.join('#'+t for t in i['tags'])
def card(i,big=False):
    ph=f'<div class="ph" style="background-image:url(/img/{i["img"]}.jpg)"></div>' if i['img'] else '<div class="ph logo" style="background-image:url(/img/logo.jpg)"></div>'
    return f'<a class="nc{" big" if big else ""}" href="/news/{i["id"]}/" data-cat="{" ".join(i["cats"])}">{ph}<div class="tx"><span class="tag">{i["tag"]}</span> <span class="date">{i["date"]}</span><h4>{E(i["title"])}</h4><div class="e">{E(i["en_title"])}</div><div class="ht">{HT(i)}</div></div></a>'
SHARE_JS='''<script>var u=location.href.split("#")[0],t=document.querySelector("h1").textContent+"\n"+document.querySelector(".ht").textContent;document.getElementById("wa").href="https://wa.me/?text="+encodeURIComponent(t+"\n"+u);document.getElementById("fbs").href="https://www.facebook.com/sharer/sharer.php?u="+encodeURIComponent(u)+"&quote="+encodeURIComponent(t);document.getElementById("cp").onclick=function(){var b=this;(navigator.clipboard?navigator.clipboard.writeText(u):Promise.reject()).then(function(){b.textContent="تم النسخ ✓"},function(){prompt("انسخ الرابط",u)})}</script></body></html>'''
# article pages
for i in items:
    url=f"{SITE}/news/{i['id']}/"
    desc=i['ar'][0][:200]
    body=''.join(f'<p>{E(p)}</p>' for p in i['ar'])
    vid=f'<div class="vid"><iframe src="https://www.youtube.com/embed/{i["video"]}" allowfullscreen></iframe></div>' if i.get('video') else ''
    im=f'<img class="hero-i" src="/img/{i["img"]}.jpg" alt="">' if i['img'] and not i.get('video') else ''
    catn={c:a for c,a,e in CATS}[i['cat']]
    page=head(i['title']+' | اتحاد المستثمرات العرب',desc,url,imgurl(i),'article')+header(i['cat'])+f'''<div class="art"><a class="back" href="/#{i['cat']}">← {catn} · العودة للأخبار</a><div><span class="tag">{i['tag']}</span> <span class="date">{i['date']}</span></div><h1>{E(i['title'])}</h1><div class="en-h">{E(i['en_title'])}</div><div class="ht">{HT(i)}</div>{im}{body}{vid}<div class="en-t">{''.join('<p>'+E(p)+'</p>' for p in i['en'])}</div>
<div class="share"><span>مشاركة · Share:</span><a target="_blank" rel="noopener" id="wa">WhatsApp</a><a target="_blank" rel="noopener" id="fbs">Facebook</a><button type="button" id="cp">نسخ الرابط · Copy link</button></div></div>{FOOT}
'''+SHARE_JS
    os.makedirs(f"{OUT}/news/{i['id']}"); open(f"{OUT}/news/{i['id']}/index.html",'w',encoding='utf-8').write(page)
# home
MED=json.load(open('data/media.json',encoding='utf-8'))
def mi(o,k): return f'<a class="mi" href="{E(o[2])}" target="_blank" rel="noopener"><b>{E(o[0])}</b><span>{E(o[1])}</span><em>{k} ↗</em></a>'
CH=json.load(open('data/yt_final.json',encoding='utf-8')); chids={o['id'] for o in CH}
ytx=[(v,t,'') for v,t in YT if v not in chids]
YTALL=ytx+[(o['id'],o['title'],o['date']) for o in CH]
CHURL="https://www.youtube.com/@ArabWomenInvestorsUnion"
vids=[("يوتيوب · YouTube",t,f"https://www.youtube.com/watch?v={v}") for v,t,d in ytx]+[("قناة الاتحاد · Union channel","كل فيديوهات قناة اتحاد المستثمرات العرب على يوتيوب ("+str(len(CH))+" فيديو)",CHURL)]
fbs=[("فيسبوك · Facebook",a+" · "+e,u) for u,a,e in FBV]
press=[(m['outlet'].replace('www.politica-eg.com','بوليتيكا'),m['title'],m['url']) for m in MED if 'youtu.be' not in m['url']]
M2=json.load(open('data/media2.json',encoding='utf-8'))
def mi2(m): return f'<a class="mi" href="{E(m["url"])}" target="_blank" rel="noopener"><b>{E(m["outlet"])}</b><span>{E(m["title"])}</span><em>{E(m["date"])} ↗</em></a>'
MORE='<div class="mh">تغطيات إضافية وأرشيف <span style="color:var(--mute);font-size:15px;direction:ltr">More coverage and archive</span></div><div class="ml">'+''.join(mi2(m) for m in M2)+'</div>'
MEDIA='<section id="media" data-show="media"><div class="wrap"><div class="mh">تغطيات تلفزيونية وفيديو</div><div class="ml">'+''.join(mi(o,'شاهد · Watch') for o in vids+fbs)+'</div><div class="mh">تغطيات الصحف والمواقع <span style="color:var(--mute);font-size:15px;direction:ltr">Press &amp; online coverage</span></div><div class="ml">'+''.join(mi(o,'اقرأ · Read') for o in press)+'</div>'+MORE+'</div></section>'
YTH='<div class="vh">قناة الاتحاد على يوتيوب<span>Union YouTube channel · <a style="color:var(--gold)" href="'+CHURL+'" target="_blank" rel="noopener">@ArabWomenInvestorsUnion</a></span></div><div class="vg">'+''.join(f'<div class="vc"><div class="vt" data-yt="{v}" style="background-image:url(https://i.ytimg.com/vi/{v}/hqdefault.jpg)"></div><p>{E(t)}<br><small style="color:var(--mute)">{d}</small></p></div>' for v,t,d in YTALL)+'</div><div class="vh">فيسبوك (روابط)<span>Facebook links</span></div><div class="vg">'+''.join(f'<div class="vc"><a class="fbv" href="{u}" target="_blank" rel="noopener">▶ {a}<br><span style="font-size:14px">{e}</span></a></div>' for u,a,e in FBV)+'</div>'
V=open('videos.js',encoding='utf-8').read()
cards=''.join(card(i,k==0) for k,i in enumerate(items))
T=json.dumps({c:[a,e] for c,a,e in CATS},ensure_ascii=False)
home=head('اتحاد المستثمرات العرب | Arab Women Investors Union','الموقع الإخباري الرسمي لاتحاد المستثمرات العرب: أخبار الاتحاد وزياراته وملتقياته وقمته.',SITE+'/',f'{SITE}/img/logo.jpg','website')+header('home')+f'''
<div id="pagehead" class="wrap pagehead" style="display:none"><h1></h1><h2></h2></div>
<div class="hero" data-show="home"><div class="wrap"><h1>الموقع الإخباري الرسمي لاتحاد المستثمرات العرب</h1><h2>The official news page of the Arab Women Investors Union</h2><p>أخبار الاتحاد وزياراته وملتقياته وقمته في مكان واحد، برئاسة الدكتورة هدى يسى.</p><p class="en">Union news, visits, forums and summit in one place, under the presidency of Dr. Hoda Yassa.</p></div></div>
<section id="news" data-show="home visits forums summit intl agreements" style="border:0"><div class="wrap"><div class="sec-t"><h3 id="newsH">آخر الأخبار</h3><span id="newsE">Latest News</span></div><div class="cards" id="cards">{cards}</div>
<div class="empty" id="emptyNews" style="display:none">قريبًا: أخبار هذا القسم<br><span style="font-size:16px;direction:ltr;display:block">Coming soon: news for this section</span></div></div></section>
{MEDIA}
<section id="videos" data-show="videos"><div class="wrap"><div id="vids"></div></div></section>
<section id="about" class="about" data-show="about home"><div class="wrap"><div class="sec-t"><h3>عن الاتحاد</h3><span>About</span></div>
<p>اتحاد المستثمرات العرب تجمع للمستثمرين والمستثمرات، بدأت مسيرته من مقر جامعة الدول العربية بالقاهرة منذ عام 2005، ويعمل تحت مظلة الجامعة العربية، برئاسة الدكتورة هدى يسى.</p><p>ينظم الاتحاد سنويًا مؤتمر ومعرض الاستثمار العربي الأفريقي والتعاون الدولي.</p>
<p class="en-t">The Arab Women Investors Union is a community of investors, founded at the Arab League headquarters in Cairo in 2005 and led by Dr. Hoda Yassa. It organizes the annual Arab-African Investment and International Cooperation Conference and Exhibition.</p>
<div class="facts"><div class="fact"><b>2005</b><span>سنة التأسيس<br>Founded</span></div><div class="fact"><b>29</b><span>دورة للقمة<br>Summit editions</span></div><div class="fact"><b>45</b><span>دولة في الدورة 29<br>Countries in 2026</span></div><div class="fact"><b>19</b><span>دولة عربية أعضاء<br>Arab member countries</span></div></div></div></section>
{FOOT}<script>
var T={T};T.home=["",""];T.media=["تغطيات القنوات والإعلام","Media Coverage"];T.videos=["الفيديوهات","Videos"];T.about=["عن الاتحاد","About"];
function route(){{var p=(location.hash||"#home").slice(1);if(!T[p])p="home";
document.querySelectorAll("[data-show]").forEach(function(e){{e.style.display=e.dataset.show.split(" ").indexOf(p)>-1?"":"none"}});
var cat=["visits","forums","summit","intl","agreements"].indexOf(p)>-1,n=0;
document.querySelectorAll("#cards .nc").forEach(function(a){{var ok=p=="home"||(" "+a.dataset.cat+" ").indexOf(" "+p+" ")>-1;a.style.display=ok?"":"none";if(ok)n++}});
document.getElementById("newsH").textContent=cat?"الأخبار":"آخر الأخبار";document.getElementById("newsE").textContent=cat?"News":"Latest News";
document.getElementById("news").style.display=(p=="home"||cat)?"":"none";
var ph=document.getElementById("pagehead");if(p!="home"){{ph.style.display="";ph.querySelector("h1").textContent=T[p][0];ph.querySelector("h2").textContent=T[p][1]}}else ph.style.display="none";
document.getElementById("emptyNews").style.display=(cat&&n==0)?"":"none";
document.querySelectorAll("nav a[data-p]").forEach(function(a){{a.classList.toggle("on",a.dataset.p==p)}});window.scrollTo(0,0)}}
{V}
document.getElementById("vids").insertAdjacentHTML("beforeend",{json.dumps(YTH,ensure_ascii=False)});document.getElementById("vids").addEventListener("click",function(e){{var t=e.target.closest(".vt[data-yt]");if(t&&!t.querySelector("iframe")){{t.style.backgroundImage="none";t.className="vt play";t.innerHTML='<iframe src="https://www.youtube.com/embed/'+t.dataset.yt+'?autoplay=1" allow="autoplay; fullscreen" allowfullscreen></iframe>'}}}});
addEventListener("hashchange",route);route();
</script></body></html>'''
open(OUT+'/index.html','w',encoding='utf-8').write(home)

# ---- SEO ----
import datetime
ORG={"@context":"https://schema.org","@type":"Organization","name":"اتحاد المستثمرات العرب","alternateName":"Arab Women Investors Union","url":SITE+"/","logo":SITE+"/img/logo.jpg","foundingDate":"2005","sameAs":["https://www.youtube.com/@ArabWomenInvestorsUnion","https://www.facebook.com/share/1FDAMTnfQQ/","https://awiu.net"]}
WEB={"@context":"https://schema.org","@type":"WebSite","name":"اتحاد المستثمرات العرب - الموقع الإخباري","url":SITE+"/","inLanguage":["ar","en"]}
def ld(o): return '<script type="application/ld+json">'+json.dumps(o,ensure_ascii=False)+'</script>'
def inject(path,canon,extra):
    t=open(path,encoding='utf-8').read()
    if 'preview' in SITE: extra+='<meta name="robots" content="noindex,nofollow">'
    t=t.replace('</head>',f'<link rel="canonical" href="{canon}">'+extra+'</head>',1)
    open(path,'w',encoding='utf-8').write(t)
inject(OUT+'/index.html',SITE+'/',ld(ORG)+ld(WEB))
urls=[(SITE+'/',None)]
for i in items:
    y,m,d=dkey(i); iso=min(datetime.date(y,m,d),datetime.date.today()).isoformat(); urls.append((f"{SITE}/news/{i['id']}/",iso))
    art={"@context":"https://schema.org","@type":"NewsArticle","headline":i['title'][:110],"alternativeHeadline":i.get('en_title',''),"datePublished":iso,"dateModified":iso,"inLanguage":"ar","image":[imgurl(i)],"mainEntityOfPage":f"{SITE}/news/{i['id']}/","articleBody":' '.join(i['ar'])[:5000],"keywords":', '.join(i['tags']),"author":{"@type":"Organization","name":"اتحاد المستثمرات العرب"},"publisher":{"@type":"Organization","name":"اتحاد المستثمرات العرب","logo":{"@type":"ImageObject","url":SITE+"/img/logo.jpg"}}}
    inject(f"{OUT}/news/{i['id']}/index.html",f"{SITE}/news/{i['id']}/",ld(art)+ld(ORG))
sm='<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join(f'<url><loc>{u}</loc>'+(f'<lastmod>{d}</lastmod>' if d else '')+'</url>' for u,d in urls)+'</urlset>'
open(OUT+'/sitemap.xml','w',encoding='utf-8').write(sm)
open(OUT+'/robots.txt','w').write(f"User-agent: *\n{'Disallow' if 'preview' in SITE else 'Allow'}: /\n\nSitemap: {SITE}/sitemap.xml\n")
print(len(items),'items')

for _f in glob.glob("google*.html"): shutil.copy(_f,OUT+"/"+_f)
