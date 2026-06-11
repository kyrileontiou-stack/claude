# HANDOFF — KM3 re-apply import + email (API route)

**Goal:** Import the 707 unique "rating-6" Appointment-Setter candidates into the GoHighLevel **KM3** subaccount, tag them, and send Email 1 (re-apply invite). Follow-up sequence = GHL Workflow (UI step).

## Prereqs for this to run
- This session MUST be in an environment whose **network policy allowlists `services.leadconnectorhq.com`** (otherwise calls return `403 Host not in allowlist`). Test first with a GET to `/locations/{id}`.
- User must provide a **freshly regenerated** GHL Private Integration Token (the previous `pit-...` was exposed in chat). Token needs scopes: `contacts.write`, `contacts.readonly`, `conversations/message.write`.
- **KM3 Location ID:** `14YDrxkz7GPFcWRx67vG`

## Data sources (in repo + Drive)
- `sheet2_full_qualified.tsv` (committed) = 870 rating-6 rows: `sheetRow \t name \t email`.
- Phones: re-download the responses sheet from Drive (fileId `1YSOMPg51sLDpuurMHw6HvEh2W6o37PA1X7OfI7pPBzg`) as CSV; phone = column index 4 (WhatsApp). Map data row k (0-based) → sheetRow k+2.
- **Dedupe by lowercased email → 707 unique contacts.** Split name: first token = First Name, remainder = Last Name. Tag = `AS-Reapply-Jun2026`.

## API steps (GHL v2)
Base `https://services.leadconnectorhq.com`; headers `Authorization: Bearer <token>`, `Version: 2021-07-28`, `Content-Type: application/json`.
1. **Connectivity test:** `GET /locations/14YDrxkz7GPFcWRx67vG` → expect 200.
2. **Create/upsert each contact:** `POST /contacts/` body `{ "locationId":"14YDrxkz7GPFcWRx67vG", "firstName":..., "lastName":..., "email":..., "phone":..., "tags":["AS-Reapply-Jun2026"], "source":"Appointment Setter 2025 - rated 6" }`. (Use upsert to avoid duplicates.)
3. **Test send to 1 address**, get user confirmation on rendering, THEN batch-send Email 1 via `POST /conversations/messages` `{ "type":"Email", "contactId":..., "subject":..., "html":... }`.
4. Report progress; send in batches (~235) for deliverability.

## Email copy (CONFIRM with user before sending)
**Email 1 — Invite**
Subject: You're invited to re-apply — Kyri Media Appointment Setter
Hi {{first_name}}, Thanks for applying to the Appointment Setter role at Kyri Media. We've reopened the search with a quick new application — please re-apply so you're considered this round: https://forms.gle/nRRjWsf55rCg2s657 . It only takes a few minutes — your earlier application stood out. — Kyri Media Recruiting. *Reply STOP to opt out.*

**Email 2 — Follow-up (+3 days, via Workflow)**
Subject: Quick reminder — re-apply for the Appointment Setter role
Hi {{first_name}}, Just following up — the new application is still open and takes only a few minutes: https://forms.gle/nRRjWsf55rCg2s657 . We'd love to consider you before the window closes. — Kyri Media Recruiting. *Reply STOP to opt out.*

## Workflow (UI — user builds)
Trigger: Contact Tag = `AS-Reapply-Jun2026` → Send Email (Invite) → Wait 3 days → Send Email (Follow-up) → Stop if replied/applied.

## Guardrails
- Confirm email copy with user before ANY send.
- Test on 1 contact first.
- Keep STOP/unsubscribe line (CAN-SPAM). Verify KM3 sending domain.
