# Annotation Feedback Loop

*How `>` annotations route into the memory stack — the current gap and the planned implementation.*

---

## What Annotations Are

A `>` line written beneath an item in Agenda.md is a direct correction from the user. The agent (cato) processes it: rewrites the item, removes the annotation line, and moves on.

The correction is acted on. The *knowledge* that caused the correction is not persisted.

---

## Three Types, Three Layers

Annotations are not all the same kind of signal. They fall into three categories, each corresponding to a layer of the [hybrid memory stack](../design/07-hybrid-memory-stack.html):

**Factual correction** — "that's wrong — I called them two days ago"
→ New information about the world the system operates in
→ Target: **Memory** (persistent observations, stored as entries)

**Behavioral correction** — "don't describe a gap of days as 'weeks'"
→ A rule about how the system should express itself or act
→ Target: **Rules** (stable constraints, written in Markdown)

**Preference / structural correction** — "the cashflow section should be 3 lines, not 20"
→ Condensed procedural knowledge about what good output looks like
→ Target: **Skills** (dense principles directing agent attention)

The content of the annotation itself determines the type. Classification is a task for the agent, not the code.

---

## The Missing Loop

The current implementation stops after processing:

```
Human writes > correction
    ↓
cato rewrites the item correctly       ✓
cato removes the > line                ✓
    ↓
Factual content → Memory               ✗
Behavioral rule → Rules layer          ✗
Preference → Skills layer              ✗
    ↓
rumi promotes stable patterns → Rules  ✗
```

Every correction is a one-shot event. The system is correctable, not learnable. The same error can recur on the next Agenda run because nothing was written to the memory stack.

---

## Planned Implementation

A complete loop would treat significant annotations as learning events alongside processing events:

1. **cato processes** — rewrite item, remove `>` line (no change from current behavior)
2. **cato classifies** — identify annotation type: factual, behavioral, or preference
3. **cato writes proposal** — for factual content: a Memory proposal to `Migration/Exchange.md`; for behavioral/preference: a `rule:agenda` or `skill` proposal, also via Exchange.md
4. **rumi picks up** — on the next `memory_migrate` run, rumi processes these proposals alongside other migration sources
5. **user reviews** — the proposal appears in Exchange.md with the same Accept/Reject mechanism as all other migrations

This connects cato and rumi into a single coherent loop. Corrections made today become rules that prevent the same error tomorrow. The memory stack grows from lived use, not only from explicit migration sessions.

### Proposal format

Proposals written by cato follow the existing Exchange.md item format, so rumi and the review UI handle them without modification:

```markdown
*extracted: 2026-04-07 14:32*
[factual] Last call with parents was 2 days ago, not weeks. [memory]
- [ ] Accept
- [ ] Reject
```

The `[rule:agenda]` and `[skill]` types extend the existing type vocabulary.

---

## Implementation

Implemented in `agenda.py` on branch `annotation-loop` (2026-04-08).

### propose_memory tool

cato has a new tool `propose_memory(content, type)` that appends a proposal to
`Migration/Exchange.md` in the same `---` separated, checkbox format that
rumi's Phase A parser already reads:

```markdown
---
*from annotation: 2026-04-08 09:15*
Email an Justizministerium gesendet, Antwort erwartet bis Freitag. [user]
- [ ] Accept
- [ ] Reject
---
```

The `[type]` tag uses the existing vocabulary: `user`, `rule:agenda`, `skill`.

### When cato proposes

| Annotation type | Trigger | Memory type |
|---|---|---|
| Correction / clarification | Always | `user` |
| Behavioral instruction (`immer`, `grundsätzlich`, `nie`, `ab jetzt`, `always`, `never`) | Always | `rule:agenda` |
| Completion with meaningful context | When outcome contains a fact | `user` |
| Trivial completion (`erledigt`, `done`) | Never | — |
| Postpone | Never | — |

### Data flow

```
User annotates Agenda.md with > line
    ↓
cato processes annotation (rewrite / remove / update Shadow.md)
    ↓
cato calls propose_memory if annotation reveals something worth keeping
    ↓
Proposal written to Migration/Exchange.md (same format as all migration proposals)
    ↓
Next memory_migrate run — rumi Phase A reads and processes
    ↓
User accepts or rejects in Exchange.md
    ↓
Accepted → stored in memory / rules / skills
```

### rumi — no changes needed

rumi's Phase A already processes `Migration/Exchange.md` in this format.
cato-generated proposals flow through the same review pipeline as explicit
migration sessions.

## Status

- `>` annotation processing: **implemented** (`agenda.py`)
- `propose_memory` tool + system prompt: **implemented** (`annotation-loop` branch)
- rumi Phase A pickup: **works without changes** — format is identical
