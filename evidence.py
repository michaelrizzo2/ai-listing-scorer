"""Transparent fictional listing comparison with full editable cost assumptions."""
from app import LISTINGS
DEFAULT={'outbound_cents':2000,'labor_cents':1500,'returns_cents':1000,'overhead_cents':500}
def evaluate(scenario='all',weight=50,target='Northstar N14',assumptions=None):
 if scenario not in ['all','tested_only','missing_evidence']:raise ValueError('Unknown filter')
 if target not in ['Northstar N14','Meridian M2']:raise ValueError('Unknown target')
 if type(weight)!=int or not 0<=weight<=100:raise ValueError('Invalid weight')
 a={**DEFAULT,**(assumptions or {})}
 if set(a)!=set(DEFAULT) or any(type(v)!=int or not 0<=v<=100000 for v in a.values()):raise ValueError('Invalid assumptions')
 rows=[]
 for i in LISTINGS:
  missing=[] if i['id']=='a' else ['battery health not documented','charging function unknown'] if i['id']=='b' else ['charging and screen test records not supplied']
  if scenario=='tested_only' and missing or scenario=='missing_evidence' and not missing:continue
  match=i['title'].startswith(target);relevance=1 if match else .2
  flags=missing.copy()
  if not match:flags.append('Different device from selected target')
  if i['repair_cents']:flags.append('Repair reserve is an assumption')
  taxable=i['price_cents']+i['shipping_cents'];tax=(taxable*7+50)//100;landed=taxable+tax+i['repair_cents'];fee=(i['resale_cents']*13+50)//100
  lines=[{'label':'Purchase','cents':i['price_cents']},{'label':'Inbound shipping','cents':i['shipping_cents']},{'label':'Purchase tax (7%)','cents':tax},{'label':'Repair reserve','cents':i['repair_cents']},{'label':'Resale fee (13%)','cents':fee}]+[{'label':label,'cents':a[key]} for key,label in [('outbound_cents','Outbound shipping'),('labor_cents','Labor'),('returns_cents','Returns reserve'),('overhead_cents','Overhead')]]
  rows.append({'id':i['id'],'title':i['title'],'score':100*(weight/100*relevance+(1-weight/100)*i['condition']),'dimensions':{'target relevance':relevance,'condition':i['condition']},'reason':'; '.join(i['evidence']),'flags':flags,'matches_target':match,'evidence_complete':not missing,'eligible_for_review':match and not missing,'landed_cents':landed,'profit_cents':i['resale_cents']-sum(l['cents'] for l in lines),'resale_cents':i['resale_cents'],'cost_lines':lines})
 return {'kind':'listing','mode':'Rule-based comparison','synthetic':True,'target':target,'assumptions':a,'items':sorted(rows,key=lambda r:(-r['score'],r['id'])),'message':'Fictional listings. Target match, evidence and risk are separate. Projected margin includes all displayed assumptions; it is not guaranteed profit.'}
