#!/usr/bin/env python3
"""Deterministic source crawling; zero AI/API calls. No automatic journalism-fit exclusion."""
import urllib.request,urllib.parse,json,re,hashlib,datetime,sqlite3,concurrent.futures,time
from pathlib import Path
from html.parser import HTMLParser
ROOT=Path(__file__).parent; OUT=ROOT/'output';OUT.mkdir(exist_ok=True)
NOW=datetime.datetime.now(datetime.timezone.utc).isoformat()
SEEDS=[
('Fundo Brasil','https://www.fundobrasil.org.br/nosso-trabalho/apoio-a-sociedade-civil/editais-gerais-e-especificos/',r'/edital/'),
('Fundo Brasil','https://www.fundobrasil.org.br/nosso-trabalho/apoio-a-sociedade-civil/editais-gerais-e-especificos/editais-especificos/',r'/edital/'),
('Fundo Casa','https://casa.org.br/chamadas/',r'/chamadas/[^/]+'),
('Pulitzer Center','https://pulitzercenter.org/opportunities/grants-fellowships',r'/grants-fellowships/|/grant-application|reporting-grants'),
('Capitaai (agregador)','https://capitaai.com.br/editais-abertos/cultura',r'/editais/|/edital/'),
]
class Page(HTMLParser):
 def __init__(self):super().__init__();self.links=[];self.text=[];self.ignore=0;self.a=None;self.h=False;self.heading=[]
 def handle_starttag(self,t,a):
  d=dict(a)
  if t in ('script','style','nav','header','footer'):self.ignore+=1
  if t=='a':self.a=[d.get('href',''),'']
  if t=='h1':self.h=True
 def handle_endtag(self,t):
  if t in ('script','style','nav','header','footer'):self.ignore=max(0,self.ignore-1)
  if t=='a' and self.a:self.links.append(tuple(self.a));self.a=None
  if t=='h1':self.h=False
 def handle_data(self,d):
  if self.a:self.a[1]+=d+' '
  if self.h:self.heading.append(d)
  if not self.ignore and d.strip():self.text.append(d.strip())
def fetch(url):
 req=urllib.request.Request(url,headers={'User-Agent':'Codesinfo-Editais/0.2 public-source-research'})
 with urllib.request.urlopen(req,timeout=35) as r:
  raw=r.read(3000000); ct=r.headers.get('Content-Type','')
 if 'html' not in ct:raise ValueError('Non HTML source: '+ct)
 p=Page();p.feed(raw.decode('utf8','replace'));return p,hashlib.sha256(raw).hexdigest()
def inspect(item):
 org,url,label,seed=item
 try:
  p,h=fetch(url);text=' '.join(p.text);title=' '.join(p.heading).strip() or label.strip()
  # Status only from explicit adjacent page language; never infer eligibility or missing deadline.
  explicit=re.search(r'\bStatus\s+(Encerrado|Aberto)\b',text,re.I)
  status='A verificar';evidence=''
  if explicit:status='Encerrado' if explicit[1].lower()=='encerrado' else 'Aberto (fonte)';evidence=explicit[0]
  if not explicit:
   m=re.search(r'.{0,45}(?:inscri[çc][õo]es (?:encerradas|abertas)|chamada (?:encerrada|aberta)|applications? (?:are )?closed|no deadline for grant applications|rolling basis).{0,70}',text,re.I)
   if m:
    evidence=m[0];status='Encerrado' if re.search('encerrad|closed',m[0],re.I) else 'Fluxo contínuo' if re.search('no deadline|rolling basis',m[0],re.I) else 'Aberto (fonte; conferir prazo)'
  excerpts=re.findall(r'.{0,30}(?:prazo|período de submissão|inscri[çc][õo]es|deadline).{0,100}',text,re.I)[:3]
  return dict(title=title,url=url,organizer=org,source_index=seed,status=status,evidence=evidence,deadline_excerpts=excerpts,checked_at=NOW,hash=h,attachments=list(dict.fromkeys(urllib.parse.urljoin(url,a) for a,l in p.links if '.pdf' in a.lower()))[:12],collection='ok',journalism_fit='Não avaliado, sem exclusão automática',source_type='Agregador' if 'agregador' in org else 'Fonte oficial')
 except Exception as e:return dict(title=label or url,url=url,organizer=org,source_index=seed,status='Falha de coleta',error=str(e)[:180],checked_at=NOW,collection='error')
jobs={};logs=[]
for org,url,pat in SEEDS:
 try:
  p,h=fetch(url);found=0
  for href,label in p.links:
   full=urllib.parse.urljoin(url,href).split('#')[0].split('?')[0].rstrip('/')
   if urllib.parse.urlsplit(full).netloc!=urllib.parse.urlsplit(url).netloc:continue
   if re.search(pat,full) and full.rstrip('/')!=url.rstrip('/') and len(label.strip())>7:
    jobs.setdefault(full,(org,full,label.strip(),url));found+=1
  logs.append(dict(url=url,status='ok',links_matching=found,hash=h))
 except Exception as e:logs.append(dict(url=url,status='error',error=str(e)[:180]))
# Official continuous programme: linked from the official application page (seed has documented linkage).
url='https://pulitzercenter.org/grant-application'
try:
 p,h=fetch(url)
 for href,label in p.links:
  if 'applying-reporting-grant-frequently-asked-questions' in href:
   full=urllib.parse.urljoin(url,href);jobs[full]=('Pulitzer Center',full,'Reporting grants — critérios e fluxo contínuo',url)
 logs.append(dict(url=url,status='ok',hash=h))
except Exception as e:logs.append(dict(url=url,status='error',error=str(e)[:180]))
print('Discovered',len(jobs),'URLs',flush=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool: results=list(pool.map(inspect,jobs.values()))
# Review status semantics: rolling interviews do not imply rolling applications.
for r in results:
 if r.get('status')=='Fluxo contínuo' and 'interview' in r.get('evidence','').lower():
  r['status']='A verificar'
  r['evidence']='Fonte fala de entrevistas em fluxo contínuo, não inscrições; abertura não confirmada.'
 if 'frequently-asked-questions' in r['url']:
  r['status']='Referência de critérios'
dedup={}
for r in results:
 key=(r.get('organizer',''),r.get('title','').strip().lower())
 if key not in dedup:dedup[key]=r
 else:dedup[key].setdefault('alternate_urls',[]).append(r['url'])
results=list(dedup.values())
db=sqlite3.connect(OUT/'catalog.sqlite');db.execute('create table if not exists crawl_observations(url text,checked_at text,record text,primary key(url,checked_at))')
for r in results:db.execute('insert or replace into crawl_observations values(?,?,?)',(r['url'],NOW,json.dumps(r,ensure_ascii=False)))
db.commit()
report={'run_at':NOW,'method':'HTTP HTML link traversal + explicit source status extraction; no LLM, no OpenAI/API calls','source_logs':logs,'results':results,'schedule_active':False}
(OUT/'no-ai-run.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
print('DONE',len(results),'fetched',sum(r['collection']=='ok' for r in results),flush=True)
