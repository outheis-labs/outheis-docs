# Design

*Technische Grundlagen — die konzeptionelle Architektur vor dem Code.*

Diese Dokumente erfassen die Design-Rationale, nicht die Implementierung. Sie erklären *warum* outheis so funktioniert, wie es das tut, und beziehen sich dabei auf Betriebssystemforschung und Theorie verteilter Systeme.

## Dokumente

### [Warum OS-Prinzipien](01-why-os-principles.md)

Die zentrale Erkenntnis: Multi-agent-KI-Systeme stehen vor denselben Herausforderungen, die Betriebssysteme vor Jahrzehnten gelöst haben. Message-Passing, Ownership-Semantik, Fehler-Isolation — das sind keine willkürlichen Entscheidungen, sondern bewährte Lösungen.

### [Systemüberblick](02-systems-survey.md)

Eine technische Übersicht über Betriebssysteme und ihre anwendbaren Konzepte:

- **DragonFlyBSD** — LWKT, per-CPU-Queues, Ownership-Semantik
- **Erlang/OTP** — Actor-Modell, Supervision-Trees, „let it crash"
- **seL4** — Capability-basierte Zugangskontrolle
- **Plan 9** — Alles als Dateisystem
- **OpenBSD** — Privilegtrennung, pledge/unveil

### [Architektur](03-architecture.md)

Die vollständige Architekturspezifikation: Systemstruktur, agent-Rollen, Ownership-Modell, Nachrichtenprotokoll, dispatcher-Design, vault-Struktur, Konfigurationsformat.

### [Datenformate](04-data-formats.md)

Detaillierte Spezifikation aller Datenformate: Nachrichtenschema, Konfigurationsstruktur, Memory-Speicherung, vault-Konventionen, Logging-Format.

### [Verwandte Arbeiten](05-related-work.md)

Überblick über bestehende Multi-agent-Frameworks und wie outheis sich davon unterscheidet.

### [Agent-Prompts](06-agent-prompts.md)

System-Prompt-Spezifikationen für jeden agent: gemeinsame Prinzipien, rollenspezifische Anweisungen, Fähigkeitsgrenzen.

### [Der Hybrid-Memory-Stack](07-hybrid-memory-stack.md)

Wo Code endet und LLM beginnt — die scharfe Grenze zwischen deterministischer Struktur und erlernter Bedeutung. Warum weder reiner Code noch reines LLM ausreicht und wie outheis die Verantwortung zwischen beiden aufteilt.
