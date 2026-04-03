# Attention as Architecture

## The Structural Analogy

The transformer architecture's central insight — that learned attention mechanisms can replace complex sequential processing — applies directly to how outheis is structured. This isn't metaphor. It's the same principle operating at a different level of abstraction.

| LLM Concept | outheis Equivalent |
|---|---|
| Trained weights | Skills (distilled principles) |
| Context window | Memory (current observations) |
| Query | User message |
| Attention scores | Relevance — what context gets loaded |
| Training loop | Pattern Agent (nightly) |

In a transformer:
- **Weights** are learned patterns that direct attention to relevant parts of input
- **Context** is the current input being processed
- **Training** refines weights so less context is needed for good outputs

In outheis:
- **Skills** are learned principles that direct agent attention to what matters
- **Memory** is accumulated observations awaiting distillation
- **Pattern Agent** refines skills so agents need less in their context

The goal in both cases: require progressively less explicit input to produce good output, because learned representations already capture what matters.

---

## The Learning Loop

```
User interacts with agents
        ↓
Corrections, preferences observed
        ↓
Stored in Memory (feedback type)
        ↓
Pattern Agent runs (nightly)
        ↓
Recognizes patterns (3+ similar observations)
        ↓
Distills into Skill (condensed principle)
        ↓
Deletes redundant Memory entries
        ↓
Next agent invocation: Skill directs attention
        ↓
Agent behaves differently (learned)
```

This is gradient descent at the system level. Each correction adjusts the "weights" (skills). Over time, the system needs less explicit context because the skills direct attention efficiently.

---

## Why Not More Code?

The anti-pattern is solving learning with code:

```python
# Wrong: hardcoded preference checks
def format_date(date):
    if user_prefers_iso:
        return date.isoformat()
    elif user_prefers_german:
        return date.strftime("%d.%m.%Y")
    # ... more branches for each preference
```

```
# Right: distilled skill
Skill: "Dates: Always ISO format (YYYY-MM-DD)"
```

The LLM reads the skill and applies it. No code changes when preferences change. The system learns by refining skills, not by adding branches.

This is why the boundary between code and LLM is a design constraint, not just a preference. Code that encodes learned behavior makes the system rigid. Skills that encode learned behavior make it adaptive.

---

## Compression as the Core Mechanism

As context grows, naive approaches fail:

```
Wrong: add more tools to fetch more data
read_file_1(), read_file_2(), ... read_file_n()

Right: better compression through skills
One skill replaces 10 memory entries.
One principle replaces 10 examples.
```

A trained model doesn't store all training examples — it learns patterns. Similarly, outheis doesn't keep all observations; it distills principles. The measure of a maturing system is not how much it stores, but how little it needs.

---

## The Hierarchy as Attention Layers

```
Skills (highest density)
   │  "Use ISO dates" — applies everywhere
   │  Compressed knowledge, maximum leverage
   │
Memory (medium density)
   │  "User corrected date format 3x"
   │  Raw observations, awaiting compression
   │
Rules (lowest density)
      "Never delete without confirmation"
      Hard constraints, override everything
```

| Layer | Density | Volatility | Function |
|---|---|---|---|
| Skills | High | Changes via distillation | Direct attention |
| Memory | Medium | Changes constantly | Store observations |
| Rules | Low | Rarely changes | Set boundaries |

---

## Pattern Agent as Optimizer

The Pattern Agent plays the role of the optimizer in this system:

1. **Observes gradients** — user corrections signal error
2. **Accumulates updates** — memory stores observations
3. **Applies batch update** — nightly distillation
4. **Prunes redundancy** — deletes obsolete memory entries

Like a training loop, it runs continuously in the background, gradually improving the system's "weights" (skills) based on observed "loss" (corrections and feedback).

---

## Practical Implications

- Don't hardcode preferences — let skills emerge from observation
- Don't add tools to fetch more data — compress data into context via skills
- Trust the distillation — corrections today become skills tomorrow
- Measure by context size: better skills = smaller context needed

The goal: a system that gets better not by adding code, but by refining attention. The longer it runs, the less it needs in context, because skills already direct focus to what matters.
