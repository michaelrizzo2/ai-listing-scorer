# Validation and observed limitations

- 7 Python tests passed October 13, 2026; includes legacy regressions and enhanced evidence boundaries.
- 8 shared JavaScript tests pass in the portfolio checkout.
- 45 enhanced Python/browser combinations match ranks, scores, integer-cent costs, equity curves, drawdown, trades and gate outcomes; the previous 32 legacy combinations were verified before this upgrade.
- Edge checks covered live inference and fictional server approval locally, editable listing targets, full costs, job-profile changes, empty remote filtering and historical benchmark/gates.
- Desktop layout was visually inspected. The current Edge viewport override did not take effect, so a new 390px mobile browser check is not claimed. Responsive CSS remains in place; the previous version was checked at 390px.
- FastAPI’s current TestClient dependency emits a Starlette deprecation warning; tests still pass. No application error was observed during local functional checks. Extension-origin warnings are separate.
- Public live inference is pending owner-enabled Tailscale Funnel. Recorded model results are labeled and independently inspectable; they are not live requests.



No marketplace connection or model call; relevance and condition are explicit fictional fixture judgments. Eligibility for review is a rubric, not authorization to purchase. Real fees, tax treatment, sale prices and repair costs need independent verification.
