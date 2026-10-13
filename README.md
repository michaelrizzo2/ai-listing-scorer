# Listing intelligence

Compare evidence, cost and resale potential. A portfolio starter by Michael Rizzo.

**Status: runnable local deterministic demo with synthetic data. Live API adapters and public hosting are not implemented.**

[Portfolio](https://michaelrizzo2.github.io/#projects) · [Source](https://github.com/michaelrizzo2/ai-listing-scorer)

## Implemented behavior

Compare separate relevance and condition judgments, then inspect integer-cent landed cost and potential profit. Weights change ranking without repeating judgments. Missing evidence stays visible and prevents the complete-evidence classification. Initial judgments are fixture values; no AI or marketplace calls occur. Purchase tax and selling fees are illustrative assumptions, not current platform fees.

## Run locally

Python 3.11 or newer:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/python -m pytest -q
.venv/bin/python -m uvicorn app:app --host 127.0.0.1 --port 8012
```

Open http://127.0.0.1:8012. API documentation is at `/docs`; `/api/health` reports the active mode. Production dependencies alone are in `requirements.txt`. No credentials are needed or loaded for this deterministic milestone.

## Architecture

Browser → FastAPI validation → deterministic workflow/ranking/backtest → inspectable structured response.

The application uses a small flat file layout: `app.py` contains the typed request schema and workflow; `ui.html`, `styles.css` and `ui.js` implement the interface; `test_app.py` exercises the important boundaries. This keeps the initial case study easy to clone and run.

## Verification and limitations

Run the tests above. They verify input rejection, domain calculations and the specific decision boundaries, not model accuracy. Synthetic scenarios demonstrate behavior but do not establish real-world business impact or trading performance. No private customer records or credentials belong in this repository.

## Next milestone

Add TypeSafe Score judgments for relevance/condition, and a separate evidence-completeness Noul. Add authorized eBay Browse API retrieval, dated source links, calibrated labeled evaluations and real fee configuration.

TypeSafe integration design follows the current [API](https://docs.typesafe.ai/api), [Python SDK](https://docs.typesafe.ai/sdk/python) and [composite scoring](https://docs.typesafe.ai/patterns/composite-scoring) documentation. Planned model behavior is not represented as implemented inference.
