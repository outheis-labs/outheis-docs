# Semantic Foundations

*Why information is not data — and why that matters for a personal AI system.*

---

## The Gap Shannon Left Open

In 1948, Claude Shannon published *A Mathematical Theory of Communication* — one of the most consequential papers in the history of science. He showed how to measure information as a statistical quantity: the more unexpected a message, the more information it carries. His entropy formula works with perfect precision for the engineering problems he cared about — noise, compression, channel capacity.

Shannon was explicit about what he was not doing. "The semantic aspects of communication," he wrote, "are irrelevant to the engineering problem." He bracketed meaning deliberately. His theory tells you how to transmit data reliably. It says nothing about whether any of it matters, what it refers to, or whether it is true.

This is not a flaw. It is a boundary. The flaw is treating it as a complete theory of information.

Every AI system built on statistical pattern matching — including large language models — inherits this boundary. The underlying mathematics is Shannon's: predict the next token, minimize prediction error, maximize likelihood. Meaning is not in the model; it is projected by the reader.

---

## The Question of Meaning

The decades following Shannon produced several attempts to extend information theory into the semantic domain.

**Carnap and Bar-Hillel** (1952) made the first formal attempt. Working within logic, they defined semantic information as the set of possible states of affairs a sentence rules out — the more it excludes, the more it says. This was elegant, but it exposed an immediate paradox: a contradiction rules out *everything*, and should therefore carry maximum information. Yet contradictions are false, and false statements seem like poor candidates for maximum information content. Their theory gave no principled way to exclude them.

**Fred Dretske** (1981) approached the problem differently. In *Knowledge and the Flow of Information*, he defined information in terms of causal dependency: a signal carries information about a source when there is a lawful, reliable connection between them. Smoke carries information about fire not because of any convention but because of the physical relationship between them. On this account, information exists in the world — it is not assigned by convention. And knowledge is what happens when such a signal causes a belief: to *know* that something is the case is to hold a belief that was produced by a genuine information-carrying signal.

This matters for any system that claims to manage knowledge. The question is not just whether data is stored, but whether stored representations are causally connected to anything real.

**Gregory Bateson** (1972) offered what may be the most compressed definition: information is "a difference that makes a difference." Two things are compressed into one phrase: a difference in the world, and a difference in the observer. Data that produces no change in the system receiving it is not information in any meaningful sense. Relevance is not a property added to information after the fact — it is part of what makes something information at all.

**Luciano Floridi** (2004, 2011) brought these threads together in a formal theory. His definition: semantic information is *well-formed, meaningful, and truthful* data. The third condition — truthfulness — is the most contested and the most important. Floridi argues that false information is a contradiction in terms: a signal that misrepresents the world is not carrying information about the world; it is carrying noise that happens to look like information. He calls this the veridicality thesis.

The debate continues. Scarantino and Piccinini (2010) argue that information can be false — that the concept requires no truth condition. The disagreement is not merely academic: it determines what obligations a knowledge management system has toward accuracy.

---

## What This Means in Practice

These distinctions are not abstract. They show up directly in how a personal knowledge system should behave.

**The data/information gap** is the difference between a system that logs everything and one that understands what is worth keeping. A conversation that occurred is a fact — a datum. That you consistently prefer morning appointments is *information* in Dretske's sense: it is a reliable pattern causally connected to your actual behavior. A system that only logs cannot distinguish them.

**Bateson's relevance criterion** is the design principle behind distillation. The question is not "what should we store?" but "what produces a difference in future behavior?" Skills replace long explanations not because they are shorter, but because they make a difference — they change how the agent acts. An instruction that is never activated is not information; it is stored text.

**Floridi's veridicality principle** explains why the pattern agent discards rather than accumulates. A memory system that tolerates false or outdated entries does not degrade gracefully — it becomes unreliable in proportion to the noise it contains. The question "is this still true?" is not a nicety; it is constitutive of whether the entry is information at all.

**The DIKW distinction** — data, information, knowledge, wisdom (Ackoff, 1989) — explains the three-tier architecture. Rules are behavioral dispositions: know-that. Skills are procedural: know-how. Memory is contextual: know-when. These are not technical categories invented for implementation convenience. They correspond to epistemically distinct kinds of things a system can hold.

---

## A Second Frame: Operating System Concepts

Alongside information theory, a different field developed complementary solutions to related problems — not philosophically, but engineeringly.

Operating systems manage resources under scarcity: limited memory, limited processor time, multiple competing processes. The solutions they developed — demand paging, process isolation, scheduling, virtual memory — are answers to the question of how to make a system behave coherently when it cannot hold everything at once.

The parallel to a personal AI system is direct. An agent with a context window is a process with a working memory. Skills loaded on demand are pages swapped in from disk. The scheduler that runs the pattern agent at 04:00 is an OS scheduler. The three-tier memory architecture — rules, skills, episodic memory — maps onto registers, RAM, and storage.

This is not metaphor for its own sake. It is a set of tested abstractions for resource-constrained cognition. The operating system solved these problems under much stricter constraints than an LLM context window imposes. The solutions are worth borrowing.

---

## Further Reading

**On semantic information theory:**

- Floridi, L. *The Philosophy of Information*. Oxford University Press, 2011. — The most comprehensive treatment; Chapters 4–7 cover the veridicality thesis and semantic theory directly.
- Dretske, F. *Knowledge and the Flow of Information*. MIT Press, 1981. — The causal-nomological account; essential for understanding what it means to *know* something.
- Shannon, C. E. & Weaver, W. *The Mathematical Theory of Communication*. University of Illinois Press, 1949. — Read Weaver's introduction for the explicit acknowledgment of what the theory leaves open.
- Bateson, G. "Form, Substance and Difference." In *Steps to an Ecology of Mind*. Chandler, 1972. — The "difference that makes a difference" essay; short and direct.

**On knowledge architecture:**

- Ackoff, R. L. "From Data to Wisdom." *Journal of Applied Systems Analysis*, 16, 1989. — The foundational DIKW paper; four pages, immediately readable.
- Polanyi, M. *The Tacit Dimension*. Doubleday, 1966. — The limit case: what no information system can fully capture.
