# HANDOFF — KM2 "A4" source opportunity check

**Goal:** Report on every opportunity in the GoHighLevel **KM2** subaccount whose
**source** is `A4`.

## Status: blocked on environment access, tooling ready

Attempted 2026-08-20 from a Claude Code web session. `services.leadconnectorhq.com`
is rejected at the egress proxy with `403 CONNECT` (gateway logged it as a policy
denial), and no GHL token is present in the session environment. This is the same
blocker recorded in `HANDOFF_km3_import.md`.

## To run it

1. Use an environment whose **network policy allowlists `services.leadconnectorhq.com`**.
2. Provide a Private Integration Token with scope `opportunities.readonly`, plus the
   KM2 location id:

   ```
   export GHL_TOKEN='pit-...'
   export KM2_LOCATION_ID='...'
   python3 km2_a4_opportunities.py
   ```

3. Optional: `--source '<label>'` if A4 is spelled differently in the account,
   `--csv <path>` to change the output file.

## What the script does

* `GET /opportunities/pipelines?locationId=...` — resolves pipeline and stage ids to names.
* `GET /opportunities/search?location_id=...&limit=100&page=N` — pages through every
  opportunity in KM2. The v2 search endpoint has no server-side source filter, so
  filtering happens locally.
* Prints a **full source inventory** first. That is the quickest confirmation of how
  `A4` is actually labelled in KM2 — if the exact string differs, re-run with `--source`.
* Matches the source token on word boundaries, so `a4` and `A4 - realtor.com` match
  but `a41` does not.
* Reports: match count and share of KM2, breakdown by status / pipeline / stage,
  total and won pipeline value, win rate over closed opportunities, and the created-at
  date range.
* Writes matched opportunities to CSV (id, name, source, status, value, pipeline,
  stage, timestamps, contact name/email/phone).

## Alternative if the allowlist can't be changed

Export KM2 opportunities from the GHL UI to CSV, put the file in Drive, and the same
breakdown can be produced from the export — no API access needed.
