# Listing intelligence

[Portfolio](https://michaelrizzo2.github.io/#projects) · [Try the case study](https://michaelrizzo2.github.io/#demo-listings)

Compare fictional listings using separate **target match, evidence completeness and risk**. A wrong target no longer counts as missing evidence. The enhanced `/api/evidence` endpoint accepts target and cost assumptions; `evidence.py` independently computes the browser’s results. Original preset `/api/run` remains as a legacy fixture demonstration.

Projected margin includes purchase, inbound shipping, illustrative 7% purchase tax, repair reserve, illustrative 13% selling fee, outbound shipping, labor, returns reserve and overhead. Edit the last four assumptions in the UI. Costs use integer cents; resale values and rates are illustrative, not current marketplace pricing or guaranteed profit. Missing evidence remains visible regardless of ranking.

## Limits

No marketplace connection or model call; relevance and condition are explicit fictional fixture judgments. Eligibility for review is a rubric, not authorization to purchase. Real fees, tax treatment, sale prices and repair costs need independent verification.

## Run and verify

Python 3.11+:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/python -m pytest -q
.venv/bin/python -m uvicorn app:app --host 127.0.0.1 --port 8012
```

Open http://127.0.0.1:8012. The shared browser workspace uses published evidence assets; enhanced Python APIs expose independent reproducible calculations. All four browser modes are included to make comparison easy; each repository’s own Python implementation is its named project. Repair live mode additionally needs the separately configured backend on 8021. No credentials are bundled in browser files.

7 Python tests pass for this project. Portfolio tests and 45 enhanced Python/browser parity combinations validate the shared outputs. See `VALIDATION.md`.
