# CLAUDE.md

Context for Claude Code sessions on this repo.

---

## Standing instruction from Kyri

**When Kyri gives you new durable information — about the business, the offer, the team, the
clients, pricing, tools, or how he wants things done — write it into this file, then commit and
push it.** Do it at the time he says it, not at the end of the session. The container is
ephemeral: anything not committed and pushed is gone when the session ends.

What counts as durable: facts that would still be true next month and that a future session would
otherwise have to rediscover. What doesn't: one-off task instructions, and anything he's actively
still deciding.

Put corrections in place rather than appending contradictions — if he corrects something below,
edit the line, don't add a second version of it.

---

## The business

**Kyri Media** (kyrimedia.us). Founder: Kyri Leontiou, based in Greece. Operating ~3 years.

Done-for-you short-form video and social media management **for US residential real estate
agents**. The agency handles strategy, ideation, scripting, recording coaching, editing, captions
and posting. The client's only job is roughly **two hours a month of recording** — this is the
central promise and the thing every prospect asks about first.

### Offer
- 2 posts per week, under 60 seconds
- Facebook, Instagram, TikTok, YouTube Shorts (long-form YouTube only after momentum)
- Organic only — no ad spend
- Listing content (coming soon / active / just sold) gets prioritised into the weekly queue
- Each client gets a 1:1 coach for onboarding and content planning

### Pricing
- **$4,500 per 3 months** ($1,500/mo), paid upfront, auto-renews unless cancelled
- Monthly billing offered case by case; **scope is never reduced** (no cheaper tier)
- No setup fees
- Client LTV around $9k — growing this via upsells and referrals is a stated priority

### Ideal client
Real estate agents doing **$6M+ annual sales volume** (below that, disqualify — a $3M agent nets
~$5k/mo and the service would be ~30% of their income). Listings-focused agents at higher price
points convert best. Common goals: more listings, moving up-market into luxury, escaping
referral-only growth, replacing Zillow/Realtor.com leads with organic.

---

## Sales motion

**Outbound.** Appointment setters dial and DM lists in GoHighLevel, book an intro call, then book
a demo — the **"Custom Marketing Plan"** call, run by Kyri himself.

- Setters: Helen, Joey, Joven, Cliff, Eddie, Jamailla (roster changes)
- Stack: GoHighLevel (GHL), Wave Dialer, Twilio, Google Sheets for KPI tracking
- Targets: 1 signed client/week; intro→demo conversion 2% → 5%; 15–20+ conversations/day per setter
- Setters must financially qualify before booking a demo
- Website video and testimonials are the strongest tools against price objections

---

## Team

| Person | Role |
|---|---|
| Krystal | Content lead — scripts, viral inspo, Kyri's own channels |
| Tinuka ("TK") | Client success / onboarding coach |
| Sherra | Ops, process enforcement, captions/scheduling |
| Saran, Sabbir | Editors |
| Shawn | Posting, deliverables tracking |
| Sanira | Automation and internal tooling (ScriptGen, KPI sheets) |

Internal comms run on **Pumble**, with a 30-minute response mandate during work hours. Video
review runs through **Frame.io**. Meetings are recorded in **Fathom** — the richest source of
client truth in the business, better than any persona doc.

---

## Known pain points in the business

- Content production stalls when clients don't submit recordings — the recurring bottleneck
- Property/listing videos have felt repetitive; a client (Brian, $5k) nearly paused over it,
  prompting a new template library (split-screen, pinch/zoom effects, client-specific branding)
- The MasterSheet (performance tracking) has gone stale before, blocking analysis of what works
- **Kyri does not record on-camera content consistently** — his own channel has pivoted to
  faceless, reusable formats because of it. Factor this into anything produced for his pages.

---

## Content work done in this repo

Branch: `claude/social-media-content-ideas-0foy44`

| File | What it is |
|---|---|
| `client_goals_struggles_content.md` / `.html` | Top 10 goals + top 10 struggles of real estate agents, ranked by frequency across 9 August 2026 discovery calls, with named evidence. Plus 10 content topics. |
| `thirty_video_ideas.md` / `.html` | 30 video ideas in 6 pillars, hooks written, 21 faceless / 9 on-camera |
| `format_playbook.md` / `.html` | The 10 formats from `VIRAL FORMATS.docx` specced (shot spec + beat structure), plus 3 scripts written word for word |
| `funnel_content_plan.md` / `.html` | The 30 re-sorted 60/30/10 by awareness stage, plus 15 new top-of-funnel ideas |

Also here: `HANDOFF_km3_import.md` (GHL KM3 subaccount re-apply import) and appointment-setter
applicant rating files.

### Key Google Drive documents
- **VIRAL FORMATS.docx** (`1TpLaOyY9OEZcO-7qfjJVyqz-fDbzKpLd`) — 10 shooting formats with one
  Instagram reference each. Note: *Double You* is undefined in the doc and has not been verified.
- **Content ideas for Kyri Media Content** (`17wtkysTjSGNKLBtu1SiakT-CGBXyvLdFCGqWpgEqw8U`) — a
  24-row content-type × 4-topic idea grid. Currently an empty template.
- `Kyri Media Content SOP`, `Content Ops SOP`, `100 content ideas for realtors`, `Viral Hacking
  Resource Sheet`

---

## Working notes for this environment

- **Push with `git push origin HEAD`.** The `-u` / `--set-upstream` form gets blocked by the
  permission classifier in this environment; plain `git push origin HEAD` works.
- Publishing Artifacts has been blocked here — deliver HTML files directly instead.
- Instagram is blocked by the network egress proxy, so reference reels can't be opened.
- Memory does not travel between surfaces. A claude.ai Project, the desktop app, or a custom bot
  cannot see this file, and this session cannot see them. This file only reaches Claude Code
  sessions on this repo.
- Client names in the content files are real and internal. **Anonymise before anything is
  published**, and get consent before showing a client's account, even blurred.
