---
title: Release Notes
---

# Release Notes

*Private beta — April 2026.*

---

## What Works

| Component | Status | Notes |
|-----------|--------|-------|
| Dispatcher — microkernel, scheduler, lock manager | ✓ | |
| Relay (ou) — routing, memory integration | ✓ | |
| Data (zeno) — vault search, tag analysis | ✓ | |
| Agenda (cato) — Daily, Inbox, Exchange, Shadow | ✓ | |
| Pattern (rumi) — nightly memory extraction | ✓ | |
| Web UI — config, memory, scheduler, vault, tags, migration | ✓ | |
| Signal transport — receive, respond, voice transcription | ✓ | |
| Vault file browser — all file types, images, Obsidian wikilinks | ✓ | |
| Tags — scan, namespace grouping, rename, delete | ✓ | |
| Migration — Exchange.md approval workflow | ✓ | |

## What Doesn't

| Component | Status | Notes |
|-----------|--------|-------|
| Action (hiro) — external tasks, email, calendar | not implemented | Framework present, no capabilities |
| Code (alan) — codebase introspection | dev only | Disabled in production |

**hiro is present but empty.** The agent starts and routes, but no external integrations exist — no email, no calendar, no shell execution. Enabling it in config.json has no practical effect yet.

**alan is for development use only.** It provides introspection into the outheis codebase itself. Not relevant for users.

## Known Gaps

**Pattern agent requires history.** rumi has nothing to extract on a fresh install. Memory builds over days, not immediately.

**Tag scan is on demand.** Tags are not indexed at startup. Run from Web UI (Vault → Tags → Scan) or say `analyze tags` in chat.

**No mobile UI.** Web UI is localhost-only. Use Signal transport for mobile access.

**Session continuity is limited.** Relay replays the last 20 messages on restart. Longer conversation context is lost between sessions.
