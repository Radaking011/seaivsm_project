# SE-AI-VSM — Starter Project

First milestone: create a reproducible synthetic manufacturing event log, validate it,
and calculate baseline VSM metrics. The first domain example is CNC / precision-tool
manufacturing.

## Requirements
- Python 3.10 or newer (Python 3.11 recommended)
- Windows 11
- 16 GB RAM is sufficient; no GPU is required for this milestone.

## Setup (PowerShell)
```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python -m src.main
```

If `py -3.11` is unavailable, install Python 3.11 and reopen PowerShell.

## What this version does
1. Generates synthetic production-order event data.
2. Saves it to `data/raw/synthetic_cnc_events.csv`.
3. Checks required columns, timestamps, durations, and missing values.
4. Calculates order lead time and activity cycle-time summaries.
5. Saves reports under `outputs/`.

## Important research note
This is a **synthetic prototype dataset**, not real factory evidence. We will label it
as synthetic in experiments and later compare the pipeline against real, anonymized
manufacturing records if access becomes available. No ML accuracy claim is made at
this stage.

## Next milestone
Review the event schema with the project mentor, then add a persistent database layer
and process-mining discovery / conformance analysis.
