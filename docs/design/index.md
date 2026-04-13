# Design

*Technical foundations — the conceptual architecture before code.*

---

## Documents

These documents capture the design rationale, not the implementation. They explain *why* outheis works the way it does, drawing from operating system research and distributed systems theory.

### [Why OS Principles](01-why-os-principles.html)

The core insight: multi-agent AI systems face the same challenges that operating systems solved decades ago. Message passing, ownership semantics, fault isolation — these aren't arbitrary choices but proven solutions.

### [Systems Survey](02-systems-survey.html)

A technical survey of operating systems and their applicable concepts:

- **DragonFlyBSD** — LWKT, per-CPU queues, ownership semantics
- **Erlang/OTP** — Actor model, supervision trees, "let it crash"
- **seL4** — Capability-based access control
- **Plan 9** — Everything as filesystem
- **OpenBSD** — Privilege separation, pledge/unveil

### [Architecture](03-architecture.html)

The complete architecture specification: system structure, agent roles, ownership model, message protocol, dispatcher design, vault structure, configuration format.

### [Data Formats](04-data-formats.html)

Detailed specification of all data formats: message schema, configuration structure, memory storage, vault conventions, logging format.

### [Related Work](05-related-work.html)

Survey of existing multi-agent frameworks and how outheis differs.

### [Agent Prompts](06-agent-prompts.html)

System prompt specifications for each agent: common principles, role-specific instructions, capability boundaries.

### [The Hybrid Memory Stack](07-hybrid-memory-stack.html)

Where code ends and LLM begins — the sharp boundary between deterministic structure and learned meaning. Why neither pure code nor pure LLM is sufficient, and how outheis divides responsibility between the two.

### [The Quality Threshold](08-quality-threshold.html)

Why model capability is not a gradient but a threshold — and why twenty small models cannot substitute for one capable one. Emergent abilities, the failure modes of below-threshold models, and what this means for outheis's architecture.


