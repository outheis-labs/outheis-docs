# Semantic Foundations

*Why information is not data — and what follows from that for a personal AI system.*

---

## The Gap Shannon Left Open

Sovereignty establishes who controls the system. But there is a prior question: what should a system do with what it learns about you?

In 1948, Claude Shannon published *A Mathematical Theory of Communication* — one of the most consequential papers in the history of science. He showed how to measure information as a statistical quantity: the more unexpected a message, the more information it carries. His entropy formula works with perfect precision for the engineering problems he cared about — noise, compression, channel capacity.

Shannon was explicit about what he was not doing. "The semantic aspects of communication," he wrote, "are irrelevant to the engineering problem." He bracketed meaning deliberately. His theory tells you how to transmit data reliably. It says nothing about whether any of it matters, what it refers to, or whether it is true.

This is not a flaw. It is a boundary. The flaw is treating it as a complete theory of information.

Every AI system built on statistical pattern matching — including large language models — inherits this boundary. The underlying mathematics is Shannon's: predict the next token, minimize prediction error, maximize likelihood. Meaning is not in the model; it is projected by the reader. A system that is only statistical can accumulate data indefinitely without ever knowing anything.

---

## The Question of Meaning

The decades following Shannon produced several attempts to extend information theory into the semantic domain.

**Carnap and Bar-Hillel** (1952) made the first formal attempt. Working within logic, they defined semantic information as the set of possible states of affairs a sentence rules out — the more it excludes, the more it says. This was elegant, but it exposed an immediate paradox: a contradiction rules out *everything*, and should therefore carry maximum information. Yet contradictions are false, and false statements are poor candidates for maximum information content. The theory gave no principled way to exclude them.

**Fred Dretske** (1981) approached the problem differently. In *Knowledge and the Flow of Information*, he defined information in terms of causal dependency: a signal carries information about a source when there is a lawful, reliable connection between them. Smoke carries information about fire not because of any convention, but because of the physical relationship between them. Information exists in the world; it is not assigned by convention. And knowledge is what happens when such a signal causes a belief: to *know* something is to hold a belief produced by a genuine information-carrying signal.

This matters for any system that claims to manage knowledge. The question is not just whether data is stored, but whether stored representations are connected to anything real about the person the system is supposed to serve.

**Gregory Bateson** (1972) offered what may be the most compressed definition: information is "a difference that makes a difference." A difference in the world, and a difference in the observer — both are required. Data that produces no change in the system receiving it is not information in any meaningful sense. Relevance is not a property added to information after the fact; it is part of what makes something information at all.

**Luciano Floridi** (2004, 2011) brought these threads together in a formal theory. His definition: semantic information is *well-formed, meaningful, and truthful* data. The third condition — truthfulness — is the most contested and the most important. Floridi argues that a signal which misrepresents the world is not carrying information about the world; it is carrying noise that happens to look like information. He calls this the veridicality thesis.

The debate continues. Scarantino and Piccinini (2010) argue that information requires no truth condition — that cognitive systems and engineering practice both use "information" in ways that permit falsehood. The disagreement is not merely academic: it determines what obligations a knowledge management system has toward accuracy.

---

## What This Means for outheis

These distinctions are not abstract. Each one has direct consequences for how a personal AI system should be designed.

**The data/information gap** is the difference between a system that logs everything and one that understands what is worth keeping. A conversation that occurred is a fact — a datum. That you consistently prefer morning appointments is *information* in Dretske's sense: a reliable pattern causally connected to your actual behavior. A system that only logs cannot distinguish them. outheis makes this distinction explicit: messages are logged, patterns are distilled, and the distillation process is not automatic but evaluative.

**Bateson's relevance criterion** is the design principle behind distillation. The question is not "what should we store?" but "what produces a difference in future behavior?" Skills replace long explanations not because they are shorter, but because they direct attention differently — they change what the agent does. An instruction that is never activated is not information; it is stored text. Distillation is not compression; it is a judgment about what makes a difference.

**Floridi's veridicality principle** explains why the pattern agent discards rather than accumulates. A memory system that tolerates false or outdated entries does not degrade gracefully — it becomes unreliable in proportion to the noise it contains. The question "is this still true?" is not a housekeeping nicety; it is constitutive of whether the entry is information at all. Forgetting, in outheis, is a form of epistemic hygiene.

**The DIKW distinction** (Ackoff, 1989) — data, information, knowledge, wisdom — explains why outheis separates memory, skills, and rules into distinct tiers. These are not technical categories invented for implementation convenience. Memory holds what is particular to you: events, preferences, patterns observed. Skills hold what generalizes: how to structure a day, how to interpret a request. Rules hold what is invariant: constraints that should not be violated regardless of context. The three tiers correspond to epistemically distinct kinds of things. Collapsing them into a single store would not be simpler; it would be confused.

---

## A Second Frame: Operating Systems

Alongside information theory, a different discipline developed complementary solutions to related problems — not philosophically, but through engineering under constraint.

Operating systems manage resources under scarcity: limited memory, limited processor time, multiple processes competing for both. The abstractions they developed over decades — demand paging, process isolation, virtual memory, scheduling — are answers to the question of how a system can behave coherently when it cannot hold everything at once.

The parallel is direct. A language model's context window is a working memory with hard limits. The question of what to load, when, and in what form is exactly the question operating systems answer for processes. Skills loaded on demand when a topic arises correspond to pages swapped in from storage. The nightly pattern review corresponds to a low-priority background process running when the foreground is idle. The three memory tiers correspond to the storage hierarchy every operating system manages: fast and volatile at the top, slow and persistent at the bottom.

This is not metaphor deployed for elegance. It is a set of tested abstractions for resource-constrained cognition, developed under constraints far more severe than a modern context window imposes. The solutions are worth borrowing because the problems are structurally similar.

---

## Further Reading

**On semantic information theory:**

- Floridi, L. *The Philosophy of Information*. Oxford University Press, 2011. — The most comprehensive treatment; Chapters 4–7 cover the veridicality thesis and the logical theory of semantic information.
- Dretske, F. *Knowledge and the Flow of Information*. MIT Press, 1981. — The causal-nomological account; essential for understanding what it means for a system to genuinely *know* something.
- Shannon, C. E. & Weaver, W. *The Mathematical Theory of Communication*. University of Illinois Press, 1949. — Read Weaver's introductory essay for the explicit three-level framing and the acknowledgment of what the theory leaves open.
- Bateson, G. "Form, Substance and Difference." In *Steps to an Ecology of Mind*. Chandler, 1972. — The "difference that makes a difference" essay; short, direct, and foundational.

**On knowledge architecture:**

- Ackoff, R. L. "From Data to Wisdom." *Journal of Applied Systems Analysis*, 16, 1989. — Four pages. The DIKW hierarchy in its original form, immediately readable.
- Polanyi, M. *The Tacit Dimension*. Doubleday, 1966. — The limit case: what no information system can fully capture, and why that matters.
