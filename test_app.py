from fastapi.testclient import TestClient
import app

def test_health_and_ui():
    with TestClient(app.app) as client:
        assert client.get('/api/health').json()['synthetic'] is True
        assert client.get('/').status_code == 200
        assert client.get('/ui.js').status_code == 200

def test_invalid_inputs():
    with TestClient(app.app) as client:
        assert client.post('/api/run', json={'scenario': 'unknown'}).status_code == 422
        assert client.post('/api/run', json={'scenario': 'charging', 'weight': -1}).status_code == 422
        assert client.post('/api/run', json={'scenario': 'charging', 'surprise': 'x'}).status_code == 422
def test_costs_and_flags():
    result = app.calculate_cost(app.LISTINGS[0])
    assert result == {'landed_cents':17441,'resale_fee_cents':3380,'profit_cents':5179}
    items = app.rank()['items']
    assert items[0]['id'] == 'a'
    assert next(i for i in items if i['id']=='b')['eligible_for_review'] is False

def test_weight_changes_are_explainable():
    relevance = app.rank(100)['items']
    condition = app.rank(0)['items']
    assert relevance[1]['id'] == 'b'
    assert condition[1]['id'] == 'c'
    assert all(i['score'] <= 100 for i in relevance+condition)

def test_bad_cost_rejected():
    import pytest
    with pytest.raises(ValueError):
        app.calculate_cost(dict(app.LISTINGS[0],price_cents=-1))
