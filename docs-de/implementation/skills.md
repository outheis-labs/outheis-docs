---
title: Skills
---

# Skills

*Was Agenten darüber wissen, wie sie handeln sollen.*

## Überblick

Skills sind die internen Fähigkeiten eines Agenten — Strategien, Methoden, Heuristiken zur Erledigung von Aufgaben. Anders als Rules (externe Anweisungen) repräsentieren Skills das eigene Wissen des Agenten darüber, *wie* Dinge zu tun sind.

## Die drei Speicher

| Speicher | Was er enthält | Wer schreibt | Beispiel |
|----------|---------------|--------------|---------|
| **memory** | Fakten, Beobachtungen, Zustand | Pattern-Agent | "User lives in Munich" |
| **rules** | Anweisungen, Beschränkungen | Benutzer, Pattern-Agent | "Respond in German" |
| **skills** | Fähigkeiten, Strategien | Agent selbst, Pattern-Agent | "Date formats I recognize: ..." |

## Wie sie zusammenwirken

Wenn ein Agent eine Anfrage verarbeitet:

```
Agent receives message
    ↓
Skills: "How do I approach this?"
    ↓
Rules: "What constraints apply?"
    ↓
Memory: "What do I know about this user/context?"
    ↓
Action
```

## Verzeichnisstruktur

```
# System skills (in package, read-only)
src/outheis/agents/skills/
├── common.md       # Shared by all agents
├── relay.md        # Relay-specific
├── agenda.md       # Agenda-specific
├── data.md         # Data-specific
└── pattern.md      # Pattern-specific

# User skills (learned, mutable)
~/.outheis/human/skills/
├── common.md       # Learned strategies (all agents)
├── relay.md        # Relay refinements
├── agenda.md       # Agenda refinements
└── data.md         # Data refinements
```

## System Skills

Vom Entwickler definierte Basisfähigkeiten. Beispiele:

**Agenda-Agent:**

- Datumsformate erkennen
- Daily.md-Struktur
- Inbox-Verarbeitungsstrategie
- Exchange.md-Nutzung

**Data-Agent:**

- Datei-Suchstrategien
- Tag-Interpretation
- JSON-Struktur-Parsing
- Ergebnis-Ranking

**Relay-Agent:**

- Anfragen-Routing
- Tool-Auswahl
- Migrations-Behandlung
- Korrektur-Verarbeitung

**Pattern-Agent:**

- Memory-Extraktion
- Rule-Förderung
- Konflikt-Erkennung
- Selbstbewertung

## User Skills (gelernt)

Durch Nutzung und Korrektur verfeinerte Skills. Geschrieben von:

1. **Agent selbst** — wenn eine Strategie konsistent funktioniert
2. **Pattern-Agent** — beim Beobachten stabiler Muster

Beispiel-Evolution:

```markdown
# ~/.outheis/human/skills/agenda.md

## Date Formats

- User writes dates as DD.MM.YYYY, not MM/DD/YYYY
- "nächste Woche" means Monday, not 7 days from now

## Daily Structure

- User prefers 🧘/🔴/🟠 emoji sections
- No "Evening" section needed — user doesn't use it
```

## Skill vs. Rule

| Aspekt | Skill | Rule |
|--------|-------|------|
| Perspektive | "Wie ich das angehe" | "Was ich beachten soll" |
| Herkunft | Vom Agenten gelernt | Vom Benutzer/Pattern gegeben |
| Bereich | Interne Fähigkeit | Externe Beschränkung |
| Beispiel | "I recognize dates like..." | "Always respond in German" |

Rules beschränken Verhalten von außen.
Skills ermöglichen Verhalten von innen.

## Ladereihenfolge

Im System-Prompt:

1. **Skills** (common + agentenspezifisch)
2. **Rules** (common + agentenspezifisch)
3. **Memory-Kontext** (user + feedback + context)

System-Versionen zuerst, Benutzer-Versionen ergänzen/überschreiben.

## Skills schreiben

Skills sollten sein:

- **Konkret**: Spezifische Muster, keine vagen Prinzipien

- **Handlungsorientiert**: Dem Agenten sagen, was zu tun ist

- **Lernbar**: Kann durch Feedback verfeinert werden

Guter Skill:
```markdown
## Date Recognition
- "morgen" → tomorrow's date
- "nächsten Montag" → next Monday (not today if today is Monday)
- "24.03.2026" → parse as YYYY-MM-DD internally
```

Schwacher Skill:
```markdown
## Dates
- Understand dates properly
- Be smart about date parsing
```

## Skill-Verfeinerung

Wenn ein Benutzer einen Agenten korrigiert:

1. Agent speichert Korrektur in Memory (feedback)
2. Pattern-Agent beobachtet wiederholte Korrekturen
3. Wenn stabil: wird zu User-Skill gefördert
4. Skill beeinflusst jetzt alle zukünftigen Aktionen

Das erzeugt eine Lernschleife, bei der Korrekturen zu dauerhaften Verbesserungen werden.

### Destillations-Auslöser

Der Pattern-Agent verwendet Urteilsvermögen, keine festen Schwellenwerte. Aber diese Bedingungen zeigen an, dass ein Muster bereit ist:

- **3+ ähnliche Beobachtungen** → Muster erkennbar
- **Wiederholte Korrekturen** → Prinzip extrahierbar
- **Stabile Präferenz** → Bereit für Skill

Eine einmal klar geäußerte starke Präferenz kann ein Skill werden. Etwas oft beiläufig Erwähntes vielleicht nicht. Explizite Korrekturen haben immer mehr Gewicht als erschlossene Muster.

### Qualitätskriterien

Ein guter Skill:

- **Lenkt Aufmerksamkeit** — sagt dem Agenten, was zu beachten ist, nicht was zu tun ist
- **Verallgemeinert** — gilt über die spezifische Instanz hinaus, die ihn ausgelöst hat
- **Ersetzt** — macht einen oder mehrere Memory-Einträge unnötig

Wenn ein Skill nichts ersetzt, könnte er zu spezifisch sein. Wenn er keine Aufmerksamkeit lenkt, könnte er eine verkleidete Rule sein.
