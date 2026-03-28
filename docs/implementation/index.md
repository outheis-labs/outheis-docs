# Implementation

*The current state — what's built and how to use it.*

## Documents

### [CLI Guide](guide.md)

Getting started: installation, first run, commands, usage examples.

### [Architecture](architecture.md)

Current system architecture: dispatcher, agents, knowledge stores, file layout, scheduled tasks.

### [Configuration](config.md)

Complete `config.json` reference: providers, models, agents, schedules.

### [Vault](vault.md)

How to structure your knowledge: file layout, tag systems, the faceted namespace pattern, Agenda.md template.

### [Agenda](agenda.md)

Time management through Agenda.md, Inbox.md, Exchange.md. Hourly review, manual refresh, hash-based optimization.

### [Signal](signal.md)

Signal Messenger transport: reader thread architecture, markdown stripping, authorization, voice transcription.

### [Memory & Rules](memory.md)

How outheis remembers: memory types, explicit markers, pattern extraction, rules emergence.

### [Skills](skills.md)

How agents know what to do: system skills, learned skills, the difference between skills and rules.

### [Migration](migration.md)

Bringing existing knowledge into outheis: vault/Migration workflow, approval via checkboxes.

### [Annotation Feedback Loop](annotation-feedback.md)

How `>` annotations in Agenda.md route into the memory stack — the three annotation types and the cato+rumi unified implementation.

### [Web UI](webui.md)

Local administration interface: configuration, scheduler, memory and rules editor, vault browser.

### [Hiro](hiro.md)

External action agent: task scheduling, email, calendar events. Not yet implemented.

### [Alan](alan.md)

Code intelligence agent for development environments. Disabled by default.
