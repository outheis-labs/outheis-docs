# Annotation as Ground Truth

*On the structural parallel between supervised learning and human correction — and what it implies for personal AI systems.*

---

## The Familiar Picture

In machine learning, annotation is an act of external observation. A human labeler examines a data point — an image, a sentence, a decision — and assigns a label. The label is ground truth not because the labeler created the phenomenon, but because they are positioned outside it and can judge it from there.

The model learns from this signal. Over many examples, the distribution of labels shapes the model's internal representation of the world. The labeler and the subject are separate.

---

## An Inverted Structure

When a user writes a `>` line beneath an item in their agenda, something structurally different is happening.

```
**Call parents** — no contact in weeks
> That's not right — I spoke with them two days ago.
```

This is not a labeler judging the system's output from the outside. The user is the subject of the system. They are correcting a statement *about themselves*. The ground truth here is not observation — it is **self-disclosure**.

The parallel with annotation holds at the structural level:

| ML annotation | `>` annotation |
|---|---|
| Labeler judges model output | Human judges agent output |
| External observation | Self-disclosure |
| Shapes model weights | Should shape memory, rules, skills |
| Ground truth by convention | Ground truth by authority |

But the relationship between annotator and subject has inverted. In classical annotation, the labeler stands outside the phenomenon. Here, there is no outside. The human is the only possible authority on what is true about their own life, intentions, and preferences.

---

## The Consequence

This inversion is not a detail. It is the defining property of a personal AI assistant, and it has a clear implication: the system must treat the human's corrections as authoritative — not as suggestions to be weighed against prior beliefs, not as feedback to be averaged against past behavior, but as corrections that override whatever the system previously held.

The asymmetry is structural. The system can hold beliefs about the human; the human can overwrite any of them with a single `>` line. This is the correct asymmetry for a system that is supposed to serve one person. The labeler and the subject are the same person, and that person's authority over the representation of their own life is absolute.

A system that resists correction — that hedges, qualifies, or gradually updates rather than immediately revising — has implicitly claimed that its model of the person is as valid as the person's model of themselves. That claim is indefensible. The system has no access to the person's inner life; the person has nothing but.

---

## A Note on Truth

There is an apparent complication: the human may be wrong about facts external to themselves. If a user corrects an agent's claim about a date or a price, and the user's correction is factually mistaken, should the system still adopt it?

The answer is yes — with one distinction. What is in question here is not external fact but self-representation: how the person understands their own situation, their own preferences, their own experience. The agent's claim about when the person last called their parents was not a claim about an independently verifiable fact; it was a claim about the person's own life and history. The person's correction is the only authoritative source for that.

Where a genuine external factual conflict exists, the system can note it. But the default posture must be deference. A system that routinely second-guesses its user's self-understanding has inverted the relationship it was designed to serve.

---

→ [Annotation Feedback Loop](../implementation/annotation-feedback.html) — how this principle is implemented in outheis
