#!/usr/bin/env python3
"""Pull KM2 opportunities from GoHighLevel and report on the "A4" source.

Usage:
    export GHL_TOKEN='pit-...'          # Private Integration Token, scope: opportunities.readonly
    export KM2_LOCATION_ID='...'        # KM2 subaccount location id
    python3 km2_a4_opportunities.py [--source a4] [--csv km2_a4_opportunities.csv]

Notes:
  * The v2 search endpoint has no server-side "source" filter, so every
    opportunity in the location is fetched and filtered locally. That is also
    what lets the script print the full source inventory, which is the fastest
    way to confirm how "A4" is actually spelled in KM2.
  * Requires a network policy that allowlists services.leadconnectorhq.com.
"""

import argparse
import collections
import csv
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

BASE = "https://services.leadconnectorhq.com"
VERSION = "2021-07-28"


def api_get(path, params, token):
    url = f"{BASE}{path}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(
        url,
        headers={
            "Authorization": f"Bearer {token}",
            "Version": VERSION,
            "Accept": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="replace")[:500]
        sys.exit(f"HTTP {e.code} on {path}: {body}")
    except urllib.error.URLError as e:
        sys.exit(
            f"Could not reach {BASE} ({e.reason}). If this is a 403 CONNECT the "
            f"environment's network policy does not allowlist the host."
        )


def fetch_pipelines(location_id, token):
    data = api_get("/opportunities/pipelines", {"locationId": location_id}, token)
    stages = {}
    pipelines = {}
    for p in data.get("pipelines", []):
        pipelines[p["id"]] = p.get("name", p["id"])
        for s in p.get("stages", []):
            stages[s["id"]] = s.get("name", s["id"])
    return pipelines, stages


def fetch_opportunities(location_id, token):
    out = []
    page = 1
    while True:
        data = api_get(
            "/opportunities/search",
            {"location_id": location_id, "limit": 100, "page": page},
            token,
        )
        batch = data.get("opportunities", [])
        if not batch:
            break
        out.extend(batch)
        print(f"  fetched page {page} ({len(out)} total)", file=sys.stderr)
        meta = data.get("meta", {})
        if not meta.get("nextPage"):
            break
        page = meta["nextPage"]
    return out


def money(v):
    try:
        return float(v or 0)
    except (TypeError, ValueError):
        return 0.0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", default="a4",
                    help="source token to match, case-insensitive (default: a4)")
    ap.add_argument("--csv", default="km2_a4_opportunities.csv",
                    help="write matched opportunities here")
    args = ap.parse_args()

    token = os.environ.get("GHL_TOKEN")
    location_id = os.environ.get("KM2_LOCATION_ID")
    if not token or not location_id:
        sys.exit("Set GHL_TOKEN and KM2_LOCATION_ID in the environment.")

    print("Fetching pipelines...", file=sys.stderr)
    pipelines, stages = fetch_pipelines(location_id, token)
    print("Fetching opportunities...", file=sys.stderr)
    opps = fetch_opportunities(location_id, token)
    print(f"{len(opps)} opportunities in KM2.\n")

    # Full source inventory — confirms how "A4" is spelled in the account.
    sources = collections.Counter((o.get("source") or "(no source)").strip() for o in opps)
    print("Source inventory (top 30):")
    for name, n in sources.most_common(30):
        print(f"  {n:>6}  {name}")
    print()

    pattern = re.compile(rf"(?<![a-z0-9]){re.escape(args.source.lower())}(?![a-z0-9])")
    matched = [o for o in opps if pattern.search((o.get("source") or "").lower())]

    print(f'=== source "{args.source}": {len(matched)} opportunities '
          f'({len(matched) / len(opps) * 100:.1f}% of KM2) ===' if opps else "no data")
    if not matched:
        print("No opportunities carry that source. Check the inventory above for the "
              "exact label and re-run with --source '<label>'.")
        return

    by_status = collections.Counter(o.get("status", "unknown") for o in matched)
    by_stage = collections.Counter(
        stages.get(o.get("pipelineStageId"), o.get("pipelineStageId") or "unknown")
        for o in matched
    )
    by_pipeline = collections.Counter(
        pipelines.get(o.get("pipelineId"), o.get("pipelineId") or "unknown")
        for o in matched
    )
    total_value = sum(money(o.get("monetaryValue")) for o in matched)
    won_value = sum(money(o.get("monetaryValue")) for o in matched if o.get("status") == "won")

    print("\nBy status:")
    for k, n in by_status.most_common():
        print(f"  {n:>6}  {k}")
    print("\nBy pipeline:")
    for k, n in by_pipeline.most_common():
        print(f"  {n:>6}  {k}")
    print("\nBy stage:")
    for k, n in by_stage.most_common():
        print(f"  {n:>6}  {k}")

    won = by_status.get("won", 0)
    lost = by_status.get("lost", 0)
    closed = won + lost
    print(f"\nPipeline value: ${total_value:,.0f}   won value: ${won_value:,.0f}")
    if closed:
        print(f"Win rate (won / closed): {won / closed * 100:.1f}%  ({won} won, {lost} lost)")

    dates = sorted(o.get("createdAt", "") for o in matched if o.get("createdAt"))
    if dates:
        print(f"Created between {dates[0][:10]} and {dates[-1][:10]}")

    with open(args.csv, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["id", "name", "source", "status", "monetaryValue", "pipeline",
                    "stage", "createdAt", "updatedAt", "contactName", "contactEmail",
                    "contactPhone"])
        for o in matched:
            c = o.get("contact") or {}
            w.writerow([
                o.get("id"), o.get("name"), o.get("source"), o.get("status"),
                o.get("monetaryValue"),
                pipelines.get(o.get("pipelineId"), o.get("pipelineId")),
                stages.get(o.get("pipelineStageId"), o.get("pipelineStageId")),
                o.get("createdAt"), o.get("updatedAt"),
                c.get("name"), c.get("email"), c.get("phone"),
            ])
    print(f"\nWrote {len(matched)} rows to {args.csv}")


if __name__ == "__main__":
    main()
