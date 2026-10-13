CONFIG = {'input_label': 'Evidence filter', 'boundary': 'All listings and judgments are fictional. This starter does not connect to eBay or Facebook Marketplace.', 'options': [{'id': 'all', 'label': 'Compare all listings'}, {'id': 'tested_only', 'label': 'Complete evidence only'}, {'id': 'missing_evidence', 'label': 'Review incomplete evidence'}], 'weight_label': 'Relevance weight (%) · remainder goes to condition', 'default_weight': 50, 'title': 'Listing intelligence', 'subtitle': 'Compare evidence, cost and resale potential.'}
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel, ConfigDict, Field

ROOT = Path(__file__).parent
app = FastAPI(title=CONFIG['title'])

class RunRequest(BaseModel):
    model_config = ConfigDict(extra='forbid')
    scenario: str = Field(min_length=1, max_length=60)
    weight: int = Field(default=50, ge=0, le=100)

@app.get('/')
def index():
    return FileResponse(ROOT / 'ui.html')

@app.get('/styles.css')
def styles():
    return FileResponse(ROOT / 'styles.css', media_type='text/css')

@app.get('/ui.js')
def script():
    return FileResponse(ROOT / 'ui.js', media_type='text/javascript')

@app.get('/api/health')
def health():
    return {'status': 'ok', 'mode': 'deterministic', 'synthetic': True}

@app.get('/api/config')
def config():
    return CONFIG

LISTINGS = [
    {'id': 'a', 'title': 'Northstar N14 — tested laptop', 'price_cents': 14500, 'shipping_cents': 1800, 'repair_cents': 0, 'resale_cents': 26000, 'relevance': 1.0, 'condition': 0.9, 'evidence': ['model confirmed', 'charging test recorded', 'screen test recorded'], 'missing': []},
    {'id': 'b', 'title': 'Northstar N14 — untested bargain', 'price_cents': 8500, 'shipping_cents': 2200, 'repair_cents': 6000, 'resale_cents': 26000, 'relevance': 1.0, 'condition': 0.25, 'evidence': ['model confirmed'], 'missing': ['battery health missing', 'charging function unknown', 'repair reserve is an assumption']},
    {'id': 'c', 'title': 'Meridian M2 — working laptop', 'price_cents': 13000, 'shipping_cents': 0, 'repair_cents': 0, 'resale_cents': 21000, 'relevance': 0.2, 'condition': 0.85, 'evidence': ['seller reports working'], 'missing': ['different model from the target']},
]

def calculate_cost(item):
    for key in ('price_cents', 'shipping_cents', 'repair_cents', 'resale_cents'):
        if type(item[key]) is not int or item[key] < 0:
            raise ValueError('Costs must be nonnegative integer cents')
    taxable = item['price_cents'] + item['shipping_cents']
    tax = (taxable * 7 + 50) // 100
    landed = taxable + tax + item['repair_cents']
    fee = (item['resale_cents'] * 13 + 50) // 100
    return {'landed_cents': landed, 'resale_fee_cents': fee, 'profit_cents': item['resale_cents'] - fee - landed}

def rank(weight=50, scenario='all'):
    if scenario not in ('all', 'tested_only', 'missing_evidence'):
        raise ValueError('Unknown scenario')
    rows = LISTINGS if scenario == 'all' else [i for i in LISTINGS if (not i['missing'] if scenario == 'tested_only' else bool(i['missing']))]
    results = []
    for item in rows:
        costs = calculate_cost(item)
        w = weight / 100
        score = 100 * (w * item['relevance'] + (1 - w) * item['condition'])
        results.append(dict(costs, id=item['id'], title=item['title'], score=round(score, 2), flags=item['missing'], dimensions={'relevance': item['relevance'], 'condition': item['condition']}, reason='; '.join(item['evidence']), eligible_for_review=not bool(item['missing'])))
    return {'kind': 'listing', 'mode': 'deterministic', 'items': sorted(results, key=lambda row: (-row['score'], row['id'])), 'message': 'Preset judgments, fictional listings. Costs use illustrative 7% purchase tax and 13% resale fees; verify real rates and repair costs before making a purchase.', 'weights': {'relevance': weight/100, 'condition': 1-weight/100}}

@app.post('/api/run')
def run(body: RunRequest):
    try:
        return rank(body.weight, body.scenario)
    except ValueError as exc:
        raise HTTPException(422, str(exc))
