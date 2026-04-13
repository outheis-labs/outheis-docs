# Tags as Scaffolding: A Deprecation Path

*Full free text analysis is not yet feasible due to general limitations of current models, but will be the long-term path to AI interaction.*

---

## The Problem with Full Text Comprehension — Today

A personal AI system that understands the user deeply would ideally derive everything from free text. It would read a note, infer its urgency, its category, its relationship to ongoing projects — without any explicit markup. The user writes naturally; the system understands.

This is the right long-term direction. It is not, however, reliably achievable today.

Current language models have finite context windows. When a session accumulates enough history, earlier observations fall out of scope. A model that understood something three weeks ago may not have access to that understanding now. More fundamentally, full text comprehension — extracting reliable structure from ambiguous natural language across sessions, languages, and phrasing variations — still fails often enough to matter in a system that runs daily.

Tags are the answer to this limitation, but only temporarily.

---

## What Tags Actually Are

A tag like `#action-required` or `#money` is a discretized signal. It compresses a judgment — "this requires action", "this is financially relevant" — into a form that can be processed without full comprehension of the surrounding text.

Two items may look identical structurally:

```
- 📋 **—** Gewerbeanmeldung durchführen `#action-required`
- 📋 **—** Nussbaum-Material kalkulieren `#action-required`
```

Without tags, distinguishing their urgency requires understanding the user's current projects, deadlines, and priorities. With tags, a minimal signal is available even when context is absent.

Tags bridge the gap between **code** (which handles structure deterministically) and **meaning** (which requires language understanding). They are a structured intermediate layer — legible to algorithms, compatible with LLM reasoning, and independent of context window size.

---

## The Continuity Principle

Tags are scaffolding. Scaffolding is not meant to be permanent.

As memory accumulates — through annotations that become ground truth, through patterns that become skills, through corrections that become rules — the system builds a denser picture of the user. Items that once required a tag to be understood can eventually be understood from their text alone, because the system has learned enough context.

The continuity principle is this: **every tag has a deprecation path**.

A tag becomes redundant when the system can reliably infer what it signals from memory alone. At that point, the tag is no longer providing information — it is duplicating it. The system should be tested against this criterion, and tags that fail it should be retired.

This is not a rejection of structure. It is a recognition that structure should be earned by what the model cannot yet do, not imposed permanently as compensation for limitations that are being actively reduced.

---

## Practical Implications

**Do not proliferate tags.** Each new tag is technical debt with a deprecation timeline. Before adding a tag, ask whether memory could carry the same signal. If it could — or soon will — the tag is premature.

**Invest in memory over taxonomy.** A rich memory of the user's context is more durable than a refined tag hierarchy. Tag hierarchies encode today's understanding and lock it in. Memory encodes observations that can be re-interpreted as the system matures.

**Use tags as test cases for memory quality.** If the system correctly prioritizes an item without seeing its tag — inferring urgency from memory context alone — that tag is ready to be retired. The backlog generator is a natural test for this: how well does it sort items when relying primarily on memory rather than tag signals?

**Design for eventual tag-freedom.** The long-term user experience should not require the user to tag anything. Annotations — freeform, natural, low-friction — should be sufficient. Tags may be written by the user when convenient, but the system should not depend on them.

---

## The Direction

The trajectory is clear:

1. **Now** — tags are primary signals; memory supplements them
2. **Near term** — memory becomes dense enough that tags are confirmatory, not required
3. **Long term** — pure text comprehension; tags are optional conveniences that retire naturally

Each step depends on the previous one. Ground truth through annotation (see: *Annotation as Ground Truth*) is what makes memory reliable. Reliable memory is what makes tags redundant. The system evolves not by replacing one mechanism with another, but by the earlier mechanism becoming unnecessary through the maturation of the next.

Tags will not be deleted. They will simply stop being needed.
