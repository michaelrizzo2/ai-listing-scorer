import pytest
from evidence import evaluate

def test_target_is_separate_from_missing_evidence():
 rows={r['id']:r for r in evaluate()['items']}
 assert not rows['c']['matches_target'] and not rows['c']['evidence_complete']
 assert rows['a']['evidence_complete'] and rows['a']['matches_target']
 other={r['id']:r for r in evaluate(target='Meridian M2')['items']}
 assert other['a']['evidence_complete'] and not other['a']['matches_target'] and not other['a']['eligible_for_review']

def test_all_costs_and_sensitivity():
 a=evaluate()['items'][0];assert a['profit_cents']==a['resale_cents']-sum(l['cents'] for l in a['cost_lines'])
 b=evaluate(assumptions={'outbound_cents':3000})['items'][0]
 assert b['profit_cents']==a['profit_cents']-1000
 with pytest.raises(ValueError):evaluate(assumptions={'labor_cents':-1})
