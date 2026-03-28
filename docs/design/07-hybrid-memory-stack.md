# The Hybrid Memory Stack: Where Code Ends and LLM Begins

## The Problem with Pure Approaches

Two failure modes define the design space for adaptive AI systems.

**Pure code** can't learn. Keyword lists, regex patterns, hardcoded classifiers, icon mappings, format detectors — these encode today's understanding and simultaneously lock it in. When the user phrases something differently, writes in another language, or uses an unexpected format, the heuristic fails silently or produces wrong results. Adding more branches to handle edge cases is not learning; it is accumulating technical debt that grows faster than the system improves.

**Pure LLM** doesn't scale. Delegating every decision to a language model — including decisions that could be made deterministically — is expensive, slow, unpredictable, and opaque. It also means no stable guarantees: the same file might be classified differently on two consecutive runs.

The correct position lies between these poles, and the boundary is sharp.

---

## The Boundary

**Code handles structure** — things that are unambiguous, deterministic, and independent of content:

- Filesystem operations (read, write, rename, atomic writes via temp+rename)
- Message passing between agents (queue, dispatcher, routing)
- Scheduling (when tasks run, timestamps, deadlines)
- Persistence (memory store, search index, cache)
- Schema validation (correct JSON shape, required fields, valid types)
- Tool implementations (what `read_file` does — not what it means)

These things do not change because the user phrased something differently. Their correctness is verifiable by tests, independent of language, context, or preference.

**The LLM handles meaning** — things that depend on context, language, preference, and implicit knowledge:

- Classification (what type is this entry — user, feedback, context?)
- Pattern and contradiction detection across observations
- Deciding which action is appropriate given the current situation
- Formatting according to the user's observed preferences
- Extracting structured knowledge from free-form text (files, messages, notes)
- Judging conflicts, priorities, and relevance

No static algorithm can detect subtle patterns in natural language across sessions and languages. A language model can — and it gets better at it the more skills and memory the system has distilled.

---

## The Memory Hierarchy as a Hybrid Stack

outheis implements this principle as a three-layer stack:

```
┌──────────────────────────────────────────┐
│              SKILLS                       │  highest density
│   condensed principles that direct        │  LLM writes, LLM reads
│   attention before processing begins     │  distilled from memory
└───────────────────┬──────────────────────┘
                    │ distillation
┌───────────────────┴──────────────────────┐
│              MEMORY                       │  medium density
│   observations, facts, corrections       │  LLM writes, LLM reads
│   raw material awaiting distillation     │  stored as JSON (code)
└───────────────────┬──────────────────────┘
                    │ promotion (rare)
┌───────────────────┴──────────────────────┐
│              RULES                        │  lowest density
│   stable constraints, hard boundaries    │  LLM writes, LLM reads
│   what must never happen                 │  persisted as Markdown (code)
└──────────────────────────────────────────┘
```

Each layer is:

- **Written by the LLM** (no hardcoded extraction, no keyword matching)
- **Read by the LLM** (injected into system prompts at runtime)
- **Stored by code** (JSON files, Markdown files — deterministic I/O)
- **Governed by code** (when to load, how to validate, when to expire)

The separation is strict. Code never decides what a memory entry means. The LLM never manages file handles or transaction safety.

---

## Consequence for Agent Architecture

Every agent in outheis consists of exactly two layers:

```
┌────────────────────────────────────────┐
│            LLM  (decides)              │
│  What to do? How to format? Why?       │
│  What type? What does this mean?       │
├────────────────────────────────────────┤
│         Tools  (infrastructure)         │
│  read_file, write_file, add_memory     │
│  append_rule, read_messages, done      │
└────────────────────────────────────────┘
```

The LLM calls tools — not the other way around. Python does not orchestrate what the LLM should do. Python provides what the LLM needs to act.

The agent loop is structurally uniform across all agents:

```python
while True:
    response = call_llm(system=context, messages=history, tools=tools)
    if no tool calls: return response.text
    results = [execute_tool(t) for t in response.tool_calls]
    history += [response, results]
```

Context is provided upfront (memory, skills, rules, relevant files). Tools are pure I/O. The LLM decides sequence, strategy, and what to do with results.

This means a fixed five-step pipeline — extract, consolidate, distill, promote, validate — is a heuristic. It encodes today's assumption about which steps are needed and in which order. A tool-using agent with access to read/write primitives can decide this itself, and will make better decisions as its memory and skills grow.

---

## Concrete Boundary Cases

| Decision | Wrong: heuristic | Right: LLM |
|---|---|---|
| Which memory type is this? | Keyword match on "prefer", "always" | LLM receives content and decides |
| What does this JSON file contain? | Format detection with `isinstance()` | LLM reads file, extracts meaning |
| Are these entries duplicates? | Word-overlap ratio threshold | LLM compares semantically |
| Which icon/emoji for this type? | Hardcoded `icon_map` dict | LLM formats freely |
| How should this file look? | Hardcoded template | LLM asks once, adapts |
| What type is this migration entry? | Section-header matching | LLM classifies after reading |

---

## When Does a Heuristic Become Code?

The LLM itself identifies what remains stable across many invocations. Only once a pattern is clearly and consistently stable should it be codified — not before.

The Pattern agent observes which decisions are consistent and can formulate these as Skills (directing future attention) or flag them to the developer as candidates for implementation. This is the organic growth path:

**Code grows bottom-up from observed stability, not top-down from anticipated requirements.**

This prevents premature optimization and keeps the system flexible. An outheis deployment that has been running for a year has more code than a fresh installation — but each piece of code emerged from data, not from speculation.

---

## The Distillation Gradient

The hybrid stack creates a continuous gradient from raw observation to stable principle:

```
User interaction
     ↓
Memory (LLM extracts what's worth keeping)
     ↓
Pattern agent consolidates (LLM merges, deduplicates, resolves)
     ↓
Skills (LLM distills patterns into principles)
     ↓
Rules (LLM promotes stable constraints)
     ↓
Code (developer promotes stable behavior)
```

Each transition is a compression step. Raw observations become structured memory. Memory becomes condensed skills. Skills become hard rules. Repeated rules become code. At every level, the LLM performs the classification; code performs the persistence.

The goal is a system that requires progressively less context over time — because skills have already captured what needs to be known, and code handles what will never change.
