---
title: Architektur
---

# Architektur

*Wie die Teile zusammenpassen.*

## Überblick

```
┌─────────────────────────────────────────┐
│              Dispatcher                  │
│            (Microkernel)                 │
│  ┌─────────┐ ┌─────────┐ ┌───────────┐  │
│  │ Watcher │ │  Lock   │ │ Scheduler │  │
│  │         │ │ Manager │ │           │  │
│  └─────────┘ └─────────┘ └───────────┘  │
└─────────────────┬───────────────────────┘
                  │
    ┌─────────────┼─────────────┬─────────────┐
    ▼             ▼             ▼             ▼
┌───────┐    ┌───────┐    ┌───────┐    ┌───────┐
│  ou   │    │ zeno  │    │ cato  │    │ rumi  │
│ relay │    │ data  │    │agenda │    │pattern│
└───┬───┘    └───┬───┘    └───┬───┘    └───┬───┘
    │            │             │             │
    ▼            ▼             ▼             ▼
┌─────────┐  ┌───────┐   ┌────────┐   ┌────────┐
│   LLM   │  │ Vault │   │ Agenda │   │ Memory │
│ (Haiku) │  │       │   │  dir   │   │        │
└─────────┘  └───────┘   └────────┘   └────────┘
```

## Dispatcher

Der dispatcher ist der Microkernel. Er:

- **überwacht** die Nachrichtenwarteschlange auf Änderungen
- **verwaltet Sperren** für gemeinsam genutzte Ressourcen
- **plant** periodische Aufgaben (Pattern-Analyse, Index-Neuerstellung)
- **stellt wieder her** ausstehende Operationen beim Start

Der dispatcher enthält keine LLM-Aufrufe. Er ist deterministisch, testbar, schnell.

## Agenten

Sechs agents, jeder mit einem Namen und einer Rolle:

| Rolle | Name | Wann verwendet | Liest | Schreibt |
|-------|------|----------------|-------|---------|
| relay | ou | Alle Nachrichten — entscheidet Routing | Memory, Context | Messages |
| data | zeno | vault-Suche (per Tool) | vault, Memory | — |
| agenda | cato | Terminabfragen (per Tool) | Agenda/ | Agenda/ |
| action | hiro | Externe Aktionen, Hintergrundjobs | Task-Registry | External |
| pattern | rumi | Geplant (04:00), autonome 7-Tool-Schleife | Messages, Memory | Memory, Rules, Skills |
| code | alan | Code-Fragen (nur Entwicklung) | Quellcode | vault/Codebase/ |

### Routing

Relay (ou) behandelt alle Benutzernachrichten. Er verwendet Haiku mit Tools:

- **search_vault** → delegiert an Data-Agent (zeno)
- **check_agenda** → delegiert an Agenda-Agent (cato)
- **refresh_agenda** → löst manuelle Agenda-Aktualisierung aus

Kein separater Klassifizierungsschritt. Relay entscheidet intelligent basierend auf der Frage und Memory.

Explizite Erwähnungen (@zeno, @cato) funktionieren weiterhin für direkte Delegation.

### Data-Agent (zeno)

Der Data-Agent behandelt vault-Abfragen. Bei einfachen Fragen antwortet er direkt — ohne LLM-Aufrufe:

| Abfragetyp | Beispiel | Antwort |
|------------|---------|---------|
| Dateiexistenz | "Habe ich X?" | `Ja, die Datei existiert: /path/to/X` |
| Statistik | "Wie viele PDFs?" | `Du hast 12 PDF-Dateien im vault.` |
| Liste | "Welche PDFs?" | Liste passender Dateien |
| Pfadsuche | "Wo ist X?" | Direkter Pfad oder Fuzzy-Treffer |

Komplexe Abfragen verwenden weiterhin LLM für intelligente Suche und Synthese.

### Agenda-Agent (cato)

cato verwaltet drei Dateien in `vault/Agenda/`:

| Datei | Richtung | Zweck |
|-------|----------|-------|
| Daily.md | Bidirektional | Heutiger Zeitplan, Aufgaben, Notizen |
| Inbox.md | Benutzer → System | Schnellerfassung, unverarbeitete Einträge |
| Exchange.md | System ↔ Benutzer | Asynchrone Fragen, kein Antwortzwang |

**Befehle:**

- "aktualisiere daily" / "update agenda" → löst manuelle Aktualisierung aus
- Verarbeitet Inbox-Einträge, prüft Exchange-Antworten, aktualisiert Daily

**Stündliche Überprüfung (bedingt):**

- Läuft um xx:55 (konfigurierbar)

- Prüft Datei-Hashes vor der Verarbeitung — keine Änderungen = kein LLM-Aufruf
- Unbedingt am Start (04:55) und Ende (23:55) des Tages

- Läuft nur innerhalb konfigurierter Stunden (Standard 04:55-23:55)

### Pattern-Agent (rumi)

rumi läuft nächtlich und:
1. Extrahiert Memory aus aktuellen Gesprächen
2. Konsolidiert Duplikate, löst Widersprüche auf
3. Fördert stabile Muster zu User Rules
4. Validiert eigene Extraktionsstrategien (lernt zu lernen)

**Memory-Migration** wird über Chat-Befehle ("memory migrate") durch Relay behandelt, nicht vom Pattern-Agenten. Siehe [Migration](migration.md).

### Action-Agent (hiro)

hiro führt Aufgaben und Hintergrundjobs aus. Derzeit in der Entwicklung:

| Fähigkeit | Status | Beschreibung |
|-----------|--------|--------------|
| Aufgabenplanung | Geplant | Einmalige oder wiederkehrende Aktionen planen |
| E-Mail senden | Geplant | E-Mails über konfigurierten SMTP senden |
| Kalendereinträge | Geplant | Kalendereinträge erstellen/ändern |
| Dateioperationen | Geplant | Dateien verschieben, kopieren, archivieren |
| Externe Befehle | Geplant | Zugelassene Shell-Befehle ausführen |

Action ist standardmäßig deaktiviert (`enabled: false`). Wenn aktiviert:

- Empfängt Aufgaben von anderen agents oder geplanten Jobs
- Führt Aktionen mit expliziter Bestätigung für destruktive Operationen aus
- Meldet Ergebnisse über Nachrichtenwarteschlange zurück

**Sicherheitsmodell:** hiro hat eine Whitelist erlaubter Operationen. Unbekannte Befehle erfordern explizite Benutzergenehmigung in Exchange.md.

### Code-Agent (alan)

alan bietet entwicklungszeitliche Intelligenz. Siehe [Code-Agent (alan)](alan.md) für vollständige Dokumentation.

Zusammenfassung:

- **Introspektion**: Fragen zur outheis-Implementierung beantworten

- **Vorschläge**: Verbesserungen über `vault/Codebase/Exchange.md` vorschlagen

- **Suche**: Muster und Implementierungen im Quellcode finden

- **Isolation**: Schreibzugriff auf `vault/Codebase/` beschränkt

**alan ist nur für Entwicklung.** Standardmäßig deaktiviert, wird nie in Produktion geladen.

## Wissensspeicher

### Memory

Meta-Wissen über den Benutzer:

| Typ | Zweck | Zerfall |
|-----|-------|---------|
| `user` | Persönliche Fakten | Dauerhaft |
| `feedback` | Arbeitspräferenzen | Dauerhaft |
| `context` | Aktueller Fokus | 14 Tage |

Gespeichert in `~/.outheis/human/memory/`. Siehe [Memory](memory.md) für Details.

### Rules

Externe Anweisungen an agents — was zu beachten ist:

- Benutzerdefiniert: "Auf Deutsch antworten"

- Durch Pattern gefördert: "Benutzer bevorzugt kurze Antworten"

Gespeichert in `~/.outheis/human/rules/`. Siehe [Memory](memory.md) für Details.

### Skills

Interne Fähigkeiten — wie agents handeln:

- System-Skills: Basisfähigkeiten (im Paket)

- Gelernte Skills: Durch Nutzung und Korrektur verfeinert

Gespeichert in `src/outheis/agents/skills/` (System) und `~/.outheis/human/skills/` (gelernt). Siehe [Skills](skills.md) für Details.

### Vault

Der vault ist ein Verzeichnis mit Markdown-Dateien und YAML-Frontmatter:

```
vault/
├── Agenda/
│   ├── Daily.md      # Today's schedule
│   ├── Inbox.md      # Unprocessed items
│   └── Exchange.md   # Async communication
├── projects/
│   └── *.md
└── notes/
    └── *.md
```

Der Data-Agent pflegt einen Suchindex in `~/.outheis/human/cache/index/`.

## Nachrichtenwarteschlange

Die gesamte Kommunikation fließt durch `messages.jsonl`:

```json
{"v":1,"id":"msg_abc","conversation_id":"conv_xyz","to":"dispatcher",...}
{"v":1,"id":"msg_def","conversation_id":"conv_xyz","to":"transport",...}
```

Append-only. Versioniert. Wiederherstellbar.

## Datei-Layout

```
~/.outheis/
├── .dispatcher.pid       # PID file
├── .dispatcher.sock      # Lock manager socket
└── human/
    ├── config.json       # Configuration (includes schedule)
    ├── messages.jsonl    # Message queue
    ├── memory/           # Persistent memory
    │   ├── user.json
    │   ├── feedback.json
    │   ├── context.json
    │   └── pattern/      # Pattern agent's learning
    │       └── strategies.md
    ├── cache/            # Regenerable working data
    │   ├── index/        # Search indices
    │   │   └── Vault.jsonl
    │   ├── agenda/       # Agenda file state
    │   │   ├── hashes.json       # Quick change detection
    │   │   ├── Daily.md.prev     # For diff
    │   │   ├── Inbox.md.prev
    │   │   └── Exchange.md.prev
    │   └── sessions/     # Session replay logs
    ├── rules/            # User-defined rules (external)
    │   ├── common.md
    │   ├── relay.md
    │   ├── agenda.md
    │   └── data.md
    ├── skills/           # Learned skills (internal)
    │   ├── common.md
    │   ├── relay.md
    │   ├── agenda.md
    │   └── data.md
    ├── vault/            # Primary vault (default)
    │   └── Migration/    # Temporary migration dir (user creates)
    │       ├── data.md           # Files to import
    │       └── Migration.md      # outheis creates
    └── archive/          # Archived messages
```

### Cache vs. Memory vs. Vault vs. Rules vs. Skills

| Verzeichnis | Was | Wer schreibt | Löschbar? |
|-------------|-----|--------------|-----------|
| `memory/` | Fakten über Benutzer | Pattern-Agent | Lernfortschritte gehen verloren |
| `rules/` | Anweisungen an agents | Benutzer, Pattern | Präferenzen gehen verloren |
| `skills/` | Agenten-Fähigkeiten | Agent, Pattern | Verfeinerungen gehen verloren |
| `cache/` | Arbeitszustand | System | Sicher — wird neu erstellt |
| `vault/` | Inhalte des Benutzers | Benutzer | Liegt beim Benutzer |

Das Cache-Verzeichnis ist explizit neu erstellbar. Jederzeit löschen — outheis baut nach Bedarf neu auf.

## Geplante Aufgaben

Der dispatcher führt periodische Aufgaben über den integrierten Scheduler aus. Alle Zeiten in `config.json` konfigurierbar:

| Aufgabe | Standardzeit | Zweck |
|---------|-------------|-------|
| `pattern_nightly` | 04:00 | Memory extrahieren, konsolidieren, Rules fördern |
| `index_rebuild` | 04:30 | vault-Suchindizes neu erstellen |
| `archive_rotation` | 05:00 | Alte Nachrichten archivieren |
| `shadow_scan` | 03:30 | vault nach chronologischen Einträgen scannen → Shadow.md |
| `agenda_review` | xx:55 (04-23) | Agenda-Dateien parsen (bedingt bei Änderungen) |
| `action_tasks` | alle 15 Min. | Fällige geplante Aufgaben ausführen |
| `session_summary` | alle 6 Stunden | Sitzungs-Insights extrahieren |
| `tag_scan` | auf Anfrage | vault nach #Tags scannen, Cache aktualisieren — aus WebUI ausgelöst |

**Ressourceneffizienz:** Agenda-Überprüfung prüft Datei-Hashes vor der Verarbeitung. Wenn nichts geändert wurde, wird kein LLM-Aufruf gemacht. Morgen- (04:55) und Abendläufe (23:55) sind unbedingt, um Tagesgrenzen korrekt zu behandeln.

### Zeitplan-Konfiguration

In `config.json`:

```json
{
  "schedule": {
    "pattern_nightly": {"enabled": true, "times": ["04:00"]},
    "index_rebuild":   {"enabled": true, "times": ["04:30"]},
    "archive_rotation":{"enabled": true, "times": ["05:00"]},
    "shadow_scan":     {"enabled": true, "times": ["03:30"]},
    "agenda_review": {
      "enabled": true,
      "times": ["04:55","05:55","06:55","07:55","08:55","09:55",
                "10:55","11:55","12:55","13:55","14:55","15:55",
                "16:55","17:55","18:55","19:55","20:55","21:55",
                "22:55","23:55"]
    }
  }
}
```

Jede Aufgabe kann unabhängig deaktiviert werden. Aufgaben laufen in Daemon-Threads — eine laufende Aufgabe blockiert einen zweiten Start derselben Aufgabe, aber nicht andere.

## Das Skalierungsproblem

Wenn ein vault wächst, können agents nicht alles im Kontext halten. Das wird durch Abstraktion adressiert — nicht durch mehr Lese-Tools.

**Falsch:** Mehr Tools
```
read_file_1(), read_file_2(), ... read_file_n()
```

**Richtig:** Bessere Abstraktionen — ein Index, den der agent abfragen kann, mit Details auf Abruf.

Vier Strategien in Nutzung oder geplant:

**1. Index mit Aktualitätsgewichtung** — Der Data-Agent pflegt einen Suchindex. Agents sehen einen kompakten Index, nicht rohe Dateien. Der Index enthält Zugriffshäufigkeit und Aktualitätssignale.

**2. Shadow.md als chronologischer Vorfilter** — Der Data-Agent führt einen nächtlichen vault-Scan durch und schreibt alle zeitrelevanten Einträge in eine einzelne strukturierte Datei (`Agenda/Shadow.md`). cato lädt diese statt bei jeder stündlichen Überprüfung den gesamten vault zu scannen.

**3. Progressives Laden** — Überblick zuerst, Details auf Anfrage. Der `load_skill(topic)`-Mechanismus funktioniert wie kontrolliertes Demand Paging: Der agent hat eine Zusammenfassung im Kontext und fordert Details nur bei Bedarf an.

**4. Skill-basierte Kompression** — Skills ersetzen ausführliche Anweisungen. "ISO-Datumsformat verwenden" statt zehn Beispiele. Bessere Skills bedeuten kleinere Prompts und mehr Platz für Benutzerinhalte.

---

## Weiterführende Lektüre

- [Memory](memory.md) — Wie dauerhaftes Memory funktioniert
- [Agenda](agenda.md) — Zeitmanagement mit Daily, Inbox, Exchange
- [Migration](migration.md) — Memory aus externen Quellen einpflegen
- [Code-Agent (alan)](alan.md) — Code-Intelligenz zur Entwicklungszeit
- [Web UI](webui.md) — Browser-basierte Verwaltungsoberfläche
- [Grundlagen](../foundations/) — Warum diese Architektur
