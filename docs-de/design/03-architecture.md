# Architektur

Dieses Dokument beschreibt die outheis-Architektur, abgeleitet aus den in den vorherigen Dokumenten untersuchten Betriebssystemprinzipien.

---

## Überblick

outheis ist ein Multi-Agenten-System, in dem spezialisierte Agenten über Nachrichtenaustausch kommunizieren. Ein Transport-Daemon verwaltet externe Schnittstellen, ein Dispatcher leitet Nachrichten weiter und verwaltet den Agenten-Lebenszyklus, und die Agenten verarbeiten Anfragen.

```
┌─────────────────────────────────────────────────────────────┐
│                      External World                          │
│                  (Signal, CLI, API)                          │
└─────────────────────────────┬───────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    Transport (daemon)                        │
│                     (static, no LLM)                         │
│          receives, converts, sends — no understanding        │
└─────────────────────────────┬───────────────────────────────┘
                              │
                              ▼
                       messages.jsonl
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                        Dispatcher                            │
│                     (static, no LLM)                         │
│                                                              │
│  1. Explicit: "@ou", "@zeno", "@cato", "@hiro", "@rumi"       │
│  2. Keywords + Scoring → Agent (if above threshold)          │
│  3. Fallback → Relay (LLM decides)                           │
└─────────────────────────────┬───────────────────────────────┘
                              │
    ┌──────────┬──────────┬───┴───┬──────────┬──────────┐
    ▼          ▼          ▼       ▼          ▼          ▼
 Relay      Data      Agenda   Action    Pattern
 (route,   (vault,   (user    (execute, (reflect,
 compose)  aggregate) filter)  import)   insight)
```

---

## Verzeichnisstruktur

```
~/.outheis/                      # System directory
├── agents/                      # Agent implementations
├── transport/                   # Transport daemon
├── dispatcher/                  # Dispatcher
├── web/                         # Web UI (localhost-only)
└── human/                       # ALL user-specific data
    ├── config.json              # User configuration
    ├── insights.jsonl           # Pattern agent output
    ├── rules/                   # Agenda agent rules
    ├── messages.jsonl           # Message queue (append-only)
    ├── archive/                 # Cold storage
    │   ├── messages-2025-01.jsonl
    │   └── ...
    ├── index.jsonl              # Search index (across all vaults)
    ├── tag-weights.jsonl        # Learned tag importance
    ├── cache/                   # Cached data
    │   └── agenda/              # Previous versions for diff
    ├── imports/                 # Imported external data
    │   ├── calendar/
    │   ├── email/
    │   └── ...
    └── vault/                   # Minimal starter vault

~/Documents/MyVault/             # External vault (user-managed, anywhere)
├── Agenda/
│   ├── Daily.md
│   ├── Inbox.md
│   └── Exchange.md
├── notes/
├── projects/
└── ...
```

### Datenschutzgarantie

Das Entfernen von `human/` löscht ALLE benutzerspezifischen Daten: Konfiguration, Nachrichten, Insights, Importe, Cache. Das System behält kein Wissen über den Benutzer.

---

## Komponenten

### Transport (Daemon, kein LLM)

Verwaltet externe Schnittstellen. Konvertiert zwischen Protokollen und dem internen Nachrichtenformat.

| Schnittstelle | Funktion |
|---------------|----------|
| Signal | Nachrichten empfangen/senden |
| CLI | Lokale Interaktion |
| API | Programmatischer Zugriff (zukünftig) |

Der Transport versteht Inhalte nicht. Er konvertiert und leitet nur weiter.

```
Signal message → JSON → messages.jsonl
messages.jsonl → JSON → Signal message
```

### Dispatcher (Daemon, kein LLM)

Überwacht die Nachrichtenwarteschlange (per Dateiwatcher: `inotify`/`kqueue`), leitet Nachrichten weiter, startet und benachrichtigt Agenten.

#### Routing-Logik

```python
msg = read_next()

if msg.to == "transport":
    notify(transport)
elif msg.to != "dispatcher":
    # Explicit target
    agent = get_or_spawn(msg.to)
    notify(agent)
else:
    # Dispatcher decides
    target = route(msg)
    if target:
        agent = get_or_spawn(target)
        notify(agent)
    else:
        # Fallback: Relay decides
        notify(relay)
```

#### Bewertung

```python
def route(msg) -> AgentId | None:
    text = msg.payload.text.lower()

    # Explicit mention → immediate
    if "@ou" in text: return "relay"
    if "@zeno" in text: return "data"
    if "@cato" in text: return "agenda"
    if "@hiro" in text: return "action"
    if "@rumi" in text: return "pattern"

    # Scoring
    scores = {
        "data":   score(text, config.routing.data),
        "agenda": score(text, config.routing.agenda),
        "action": score(text, config.routing.action),
    }

    best = max(scores, key=scores.get)

    if scores[best] >= config.routing.threshold:
        return best

    return None  # → Relay
```

Schlüsselwörter und Schwellenwert sind konfigurierbar. Können leer sein (alles geht an Relay).

#### Lock-Manager

Der Dispatcher verwaltet den Zugriff auf die Warteschlange über einen Unix-Socket-Lock-Manager. Alle Schreiber müssen eine Sperre anfordern, bevor sie in `messages.jsonl` schreiben.

**Socket:** `~/.outheis/.dispatcher.sock`

**Prioritätsverwaltung:**

| Priorität | Anforderer | Begründung |
|-----------|------------|------------|
| HIGH (0) | transport | Benutzer wartet |
| NORMAL (1) | relay, data, agenda, action | Agenten-Arbeit |
| LOW (2) | pattern | Hintergrundverarbeitung |

Innerhalb jeder Prioritätsklasse: FIFO.

**Protokoll:**

```json
// Request lock
→ {"cmd": "request", "requester": "relay"}
← {"status": "granted"}
← {"status": "queued", "position": 2}

// Release lock
→ {"cmd": "release"}
← {"status": "released"}

// Query status
→ {"cmd": "status"}
← {"holder": "client_123", "queue_length": 2, "queue": [...]}
```

**Verhalten:**
- Sperre wird sofort gewährt, wenn die Warteschlange leer ist
- Bei Freigabe wird der Nächste in der Warteschlange benachrichtigt
- Client-Trennung → automatische Freigabe, Bereinigung
- Prioritäten sind architektonisch, nicht konfigurierbar

#### Dateisperrung

Für andere Dateien als `messages.jsonl` wird einfaches `flock` verwendet:

| Datei | Schreiber | Sperre |
|-------|-----------|--------|
| `messages.jsonl` | Transport, alle Agenten | Socket (priorisiert) |
| `session_notes.jsonl` | Alle Agenten | `flock` |
| `config.json` | CLI, Web UI | `flock` |
| Vault-Dateien | Data Agent | `flock` |

#### Write-Ahead Logging

Alle Warteschlangenschreibvorgänge verwenden Write-Ahead für Absturzsicherheit:

```
~/.outheis/human/.pending/
├── msg_abc123.json
└── msg_def456.json
```

**Schreibreihenfolge:**
1. Nachricht in `.pending/{msg_id}.json` schreiben
2. `flock` + an `messages.jsonl` anhängen
3. Aus `.pending/` löschen

**Wiederherstellung (Dispatcher-Start):**
1. `.pending/` scannen
2. Auf Duplikate prüfen (letzte 100 IDs in der Warteschlange)
3. Fehlende Nachrichten anhängen, Duplikate überspringen
4. Wiederhergestellte Pending-Dateien löschen

Wenn ein Prozess beim Warten auf die Sperre abstürzt, überlebt die Nachricht in `.pending/` und wird beim (Neu-)Start des Dispatchers wiederhergestellt.

### Web UI (nur localhost)

Einfache Weboberfläche zur Konfiguration. Keine Chat-Funktionalität.

| Funktion | Beschreibung |
|----------|--------------|
| Agents | Modell, Ausführungsmodus, aktiviert |
| Models | Anbieter, Name, lokal/remote |
| Dispatcher | Schlüsselwörter, Schwellenwert |
| Human | Name, Sprache, Vault-Pfade |
| System | Log-Level |
| Status | Agentenstatus, Logs |

Zugriff: nur `http://localhost:<port>`. Keine externe Exposition.

---

## Agenten

### Rollen und Verantwortlichkeiten

| Rolle | Verantwortung | Ausführungsmodus |
|-------|---------------|-----------------|
| **Relay** | Klassifizieren, weiterleiten, zusammensetzen, Benutzer fragen | daemon |
| **Data** | Wissensmanagement, Aggregation, Synthese | on-demand |
| **Agenda** | Persönlicher Sekretär: filtern, priorisieren, Benutzer kennenlernen | on-demand |
| **Action** | Aufgabenausführung, externe Importe | on-demand |
| **Pattern** | Reflexion, Insight-Extraktion | scheduled |

### Relay Agent

Leitet unklare Anfragen weiter, verfasst Antworten, fragt bei Bedarf nach Klärung.

- Empfängt Nachrichten, die der Dispatcher nicht weiterleiten kann
- Klassifiziert die Absicht
- Leitet an den passenden Agenten weiter
- Fasst Agentenausgaben zur finalen Antwort zusammen
- Formatiert die Ausgabe für jeden Kanal (Signal, CLI, API)

### Agenda Agent (Persönlicher Modus)

Fungiert als persönlicher Sekretär. Der Name spiegelt beide Bedeutungen wider: die Agenda verwalten (Zeitplan, Prioritäten) und die Handlungsfähigkeit ermöglichen.

**Problem, das er löst**: 47 Kalendereinträge, 23 E-Mails, 14 Aufgaben — roh präsentiert erzeugt das kognitiven Mehraufwand. Der Agenda-Agent reduziert mentale Reibung durch Filtern und Priorisieren auf Basis erlernter Präferenzen.

```
Raw data (overwhelming)
  │
  ▼
Data Agent (complete, neutral)
  │
  ▼
Agenda Agent (filtered, prioritized, personal)
  │
  ▼
User (only what matters, when it matters)
```

**Was Agenda tut**:
- Erlernt Benutzerregeln ("Montag morgens: keine Meetings")
- Versteht Prioritäten ("Familie vor Arbeit, außer bei Deadlines")
- Filtert Rauschen ("diese E-Mail kann warten, jene nicht")
- Präsentiert Relevanz, nicht Vollständigkeit

**Wo Regeln gespeichert sind**: Verzeichnis `human/rules/` — nur Agenda liest sie.

Im Domain-Expert-Modus ist Agenda deaktiviert. Data liefert direkt an Relay.

### Data Agent

Zentraler Wissensmanager:

1. **Vault-Zugriff**: Lesen und Schreiben im Vault
2. **Aggregation**: Kombiniert Informationen aus mehreren Quellen
3. **Synthese**: Beantwortet komplexe Anfragen, die Schlussfolgerungen erfordern
4. **Koordination**: Fordert bei Bedarf externe Daten von Action an

```
User question: "How does X compare to current developments?"
                              │
                              ▼
                         Data Agent
                              │
              ┌───────────────┴───────────────┐
              ▼                               ▼
         vault                          Action Agent
      (internal)                     (fetches external)
              │                               │
              └───────────────┬───────────────┘
                              │
                         Data aggregates
                              │
                              ▼
                          Response
```

### Eigentumsmodell

Jeder Agent besitzt seine Domäne exklusiv. Andere fordern Zugriff über Nachrichten an.

| Agent | Besitzt |
|-------|---------|
| Relay | Routing-Entscheidungen, Antwortzusammenstellung, Kanalformatierung |
| Agenda | Benutzerpräferenzen, Regeln, Daily/Inbox/Exchange |
| Data | Vault, Wissenssynthese, Index |
| Action | Aufgabenausführung, externe Importe |
| Pattern | Insight-Generierung, Tag-Lernen |

---

## Nachrichtenprotokoll

### Nachrichtenschema

```
{
  id:              string       // Snowflake ID (contains timestamp)
  conversation_id: string       // Groups multi-turn exchanges

  from: {
    agent?:        AgentId      // If from agent
    user?: {
      channel:     string       // "signal", "cli", "api"
      identity:    string       // Phone, username, key
      name?:       string       // Display name
    }
  }

  to:              AgentId | "dispatcher" | "transport"

  type:            "request" | "response" | "event"
  intent?:         string       // e.g., "data.query", "action.execute"
  payload:         any

  reply_to?:       string       // Message ID for responses
}
```

### Beispiel eines Nachrichtenflusses

```
User sends "What's on my agenda tomorrow?" via Signal

1. Transport receives from Signal
   → writes {to: "dispatcher", ...} to queue

2. Dispatcher reads, matches keyword "agenda"
   → notifies Agenda Agent

3. Agenda queries Data, filters, prioritizes
   → writes {to: "relay", ...} to queue

4. Dispatcher notifies Relay
   → Relay composes human-readable response
   → writes {to: "transport", ...} to queue

5. Transport sends via Signal
```

---

## Warteschlange

### Implementierung

Die Nachrichtenwarteschlange ist eine append-only-JSONL-Datei:

```
~/.outheis/human/messages.jsonl
```

- **Append-only**: Nachrichten werden nie verändert oder gelöscht
- **Einzelne Datei**: Einfachheit vor Leistung
- **Dateisperrung**: Einfaches `fcntl`-Locking für gleichzeitigen Zugriff

```python
import fcntl
import json

def append_message(path: str, msg: dict) -> None:
    with open(path, 'a') as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        f.write(json.dumps(msg) + '\n')
        fcntl.flock(f, fcntl.LOCK_UN)
```

### Vorteile (Event Sourcing)

- **Prüfprotokoll**: Vollständige Geschichte aller Interaktionen
- **Replay**: Beliebigen vergangenen Zustand rekonstruieren
- **Debugging**: Genau nachvollziehen, was passiert ist
- **Wiederherstellung**: Beim letzten verarbeiteten Eintrag fortsetzen

---

## Deployment-Spektrum

Das System skaliert von minimal (Cloud, kostenbewusst) bis maximal (lokal, alles als Daemon):

### Minimal (Cloud, selten)

```json
{
  "dispatcher": {
    "routing": {
      "threshold": 0.3,
      "data":   ["vault", "search", "find"],
      "agenda": ["appointment", "calendar", "tomorrow"],
      "action": ["send", "email", "open"]
    }
  },
  "agents": {
    "instances": {
      "relay":   { "model": "fast",      "run_mode": "daemon" },
      "data":    { "model": "capable",   "run_mode": "on-demand" },
      "agenda":  { "model": "capable",   "run_mode": "on-demand" },
      "action":  { "model": "capable",   "run_mode": "on-demand" },
      "pattern": { "model": "strategic", "run_mode": "scheduled" }
    },
    "models": {
      "fast":      { "provider": "anthropic", "name": "..." },
      "capable":   { "provider": "anthropic", "name": "..." },
      "strategic": { "provider": "anthropic", "name": "..." }
    }
  }
}
```

Strategie: Strenge Schlüsselwörter, hoher Schwellenwert → LLM-Aufrufe minimieren.

### Maximal (Lokal, alles als Daemon)

```json
{
  "dispatcher": {
    "routing": {
      "threshold": 0.0,
      "data":   [],
      "agenda": [],
      "action": []
    }
  },
  "agents": {
    "instances": {
      "relay":   { "model": "local", "run_mode": "daemon" },
      "data":    { "model": "local", "run_mode": "daemon" },
      "agenda":  { "model": "local", "run_mode": "daemon" },
      "action":  { "model": "local", "run_mode": "daemon" },
      "pattern": { "model": "local", "run_mode": "daemon" }
    },
    "models": {
      "local": { "provider": "ollama", "name": "..." }
    }
  }
}
```

Strategie: Leere Schlüsselwörter, Schwellenwert null → Relay leitet alles weiter (lokal kostenlos).

### Hybrid

Mischung aus lokalen und entfernten Modellen. Schnelle/günstige Modelle lokal, leistungsfähige Modelle remote.

---

## Zugangskontrolle

### Dynamische Einschränkung (OpenBSD-inspiriert)

Agenten deklarieren Fähigkeiten beim Start und schränken sich progressiv ein:

```python
class DataAgent:
    def __init__(self):
        self.pledge(["vault:read", "vault:write"])
        self.unveil(["vault/"])
        # From here: cannot access human/, cannot make network calls
```

### Fähigkeitsmatrix

| Agent | vault | human/insights | human/rules | network | execute |
|-------|-------|----------------|-------------|---------|---------|
| Relay | - | - | - | - | - |
| Agenda | read | read | read | - | - |
| Data | read, write | read | - | - | - |
| Action | write (import) | read | - | ✓ | ✓ |
| Pattern | read | read, write | - | - | - |

Hinweis: Agenten fordern Dienste von anderen Agenten über Nachrichten an. Data kann Action bitten, externe Daten abzurufen; Agenda fragt Data nach aggregierten Informationen.

---

## Fehlerbehandlung

Wenn ein Agent ausfällt:

```
1. Log error (always)
2. Inform user via Relay
3. Retry with clarification if applicable
4. If persistent failure: escalate to user
```

### Fehler-Nachrichtenfluss

```
Agent fails
    │
    ▼
Dispatcher catches
    │
    ├──► Log error message to messages.jsonl
    │
    └──► Write {to: "relay", type: "error", ...} to queue
            │
            ▼
        Relay informs user:
        "I couldn't complete that. Can you clarify...?"
```

### Wiederholungslogik

| Fehlertyp | Aktion |
|-----------|--------|
| Vorübergehend (Timeout, Rate Limit) | Automatischer Wiederholungsversuch (max. 3) |
| Mehrdeutige Eingabe | Benutzer um Klärung bitten |
| Dauerhafter Fehler | Benutzer informieren, protokollieren, abbrechen |

---

## Gesprächslebenszyklus

Gespräche enden nicht explizit. Sie laufen aus.

### Rotation

Wenn `messages.jsonl` einen Schwellenwert überschreitet (konfigurierbar, Standard 10 MB):

```
messages.jsonl          → messages.jsonl (current)
                        → archive/messages-2025-03.jsonl (cold)
```

### Kaltspeicherung

Alte Gespräche werden nach `human/archive/` verschoben:

```
~/.outheis/human/
├── messages.jsonl           # Hot: current, fast access
└── archive/
    ├── messages-2025-01.jsonl
    ├── messages-2025-02.jsonl
    └── ...                  # Cold: slower access
```

### Zugriffsmuster

| Speicher | Zugriffszeit | Anwendungsfall |
|----------|--------------|----------------|
| Hot | Sofort | Aktuelle Gespräche |
| Cold | Langsamer (bei Bedarf laden) | "Was haben wir im Januar besprochen?" |

Kaltspeicherzugriff:
1. Benutzer fragt nach altem Gespräch
2. Data-Agent lädt relevante Archivdatei
3. Sucht, gibt Ergebnisse zurück
4. Entlädt (Speicherverwaltung)

---

## Pattern-Agent-Planung

Der Pattern-Agent läuft:

1. **Geplant**: Standardmäßig 04:00 Ortszeit (konfigurierbar über Web UI)
2. **Auf Anfrage**: Wenn der Benutzer explizit Reflexion anfordert

### Konfiguration

```json
{
  "agents": {
    "instances": {
      "pattern": {
        "model": "strategic",
        "run_mode": "scheduled",
        "schedule": {
          "times": ["04:00"],
          "timezone": "local"
        }
      }
    }
  }
}
```

Mehrere Zeiten möglich: `["04:00", "16:00"]`

### Manueller Auslöser

Benutzer kann anfordern: "@rumi reflect on this week" → Dispatcher leitet an Pattern weiter.

---

## Prioritätsverwaltung (GCD-inspiriert)

Agenten haben implizite Prioritätsstufen:

| Priorität | Agent | Begründung |
|-----------|-------|------------|
| Hoch | Relay | Benutzerseitig, latenzempfindlich |
| Standard | Action, Data, Agenda | Normalbetrieb |
| Hintergrund | Pattern | Reflexion kann warten |

Der Dispatcher kann Hintergrundarbeit zurückstellen, wenn Nachrichten mit hoher Priorität ausstehen.

---

## Kanalspezifische Formatierung

Der Relay-Agent formatiert die Ausgabe für jeden Kanal:

### Signal

Keine Markdown-Unterstützung, aber gute Emoji-Unterstützung:

```
📅 TODAY

• 09:00 Standup
• 14:00 Workshop

⚠️ CONFLICT
   10:00 Team meeting
   10:00 Dentist
   → Which takes priority?

✅ Proposal reviewed
☐ Finish report

💬 1 open question → see Exchange
```

| Element | Formatierung |
|---------|--------------|
| Überschriften | GROSSBUCHSTABEN + Emoji |
| Listen | • Aufzählungspunkte |
| Offene Aufgaben | ☐ |
| Erledigte Aufgaben | ✅ |
| Konflikte | ⚠️ hervorgehoben |
| Deadlines | 🔴 oder ⏰ |
| Fragen | 💬 |
| Links/Referenzen | → Klartext |

### CLI

ANSI-Farben und Formatierung:

```
TODAY
─────
  09:00  Standup
  14:00  Workshop

⚠ CONFLICT
  10:00  Team meeting
  10:00  Dentist

Tasks
  [ ] Finish report
  [x] Proposal reviewed
```

### API

Strukturiertes JSON für programmatischen Zugriff.

### Benutzerverhalten

| Datei | Benutzeraufmerksamkeit |
|-------|------------------------|
| `Daily.md` | Primär — regelmäßig geprüft |
| `Inbox.md` | Aus Benutzersicht nur Schreiben |
| `Exchange.md` | Gelegentlich — wenn Daily darauf verweist |

Konflikte und dringende Punkte müssen in `Daily.md` auftauchen, nicht versteckt in Exchange.

---

## Betriebsmodi

### Persönlicher Assistent (Standard)

- `human/`-Verzeichnis aktiv
- Agenda-Agent aktiviert
- Pattern-Agent reflektiert über Benutzerverhalten
- Einzelner Benutzer über Transport

### Domain-Experte (Zukünftig)

- `human/`-Verzeichnis repräsentiert Administrator, nicht Endbenutzer
- Agenda-Agent deaktiviert
- Pattern-Agent reflektiert über Domänenwissen
- Mehrere Endbenutzer über Transport
- Administrator konfiguriert System über Web UI

---

## Bedeutung von Aufmerksamkeit

Die zentrale Erkenntnis der Transformer-Architektur aus "Attention Is All You Need" (Vaswani et al., 2017) — dass Aufmerksamkeitsmechanismen die Verarbeitung auf das Wesentliche lenken — gilt direkt für outheis. Das ist keine Metapher; es ist dasselbe Prinzip auf einer anderen Ebene.

### Die Lernarchitektur

```
Skills (highest density)
   │  condensed principles
   │  "Dates: Always ISO format"
   │  direct attention BEFORE processing
   │
Memory (medium density)
   │  facts, observations
   │  "User corrected date format 3x"
   │  raw material for distillation
   │
Rules (lowest density)
      hard constraints
      "Never delete without confirmation"
      override everything, rarely change
```

### Die Entsprechung

| LLM-Konzept | outheis-Äquivalent |
|-------------|-------------------|
| Trainierte Gewichte | Skills (destillierte Prinzipien) |
| Kontextfenster | Memory (aktuelle Beobachtungen) |
| Anfrage | Benutzernachricht |
| Trainingsschleife | Pattern Agent (nächtlich) |

### Wie Lernen funktioniert

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

Das ist Gradientenabstieg auf Systemebene. Jede Korrektur passt die "Gewichte" (Skills) an. Mit der Zeit benötigt das System weniger expliziten Kontext, weil Skills die Aufmerksamkeit effizient lenken.

### Warum nicht mehr Code?

Das Anti-Muster besteht darin, Lernen mit fest kodierter Logik zu lösen:

**Falsch:**
```python
def format_date(date):
    if user_prefers_iso:
        return date.isoformat()
    elif user_prefers_german:
        return date.strftime("%d.%m.%Y")
```

**Richtig:**
```
Skill: "Dates: Always ISO format (YYYY-MM-DD)"
```

Das LLM liest den Skill und wendet ihn an. Kein Code muss geändert werden, wenn sich Präferenzen ändern. Das System lernt durch Verfeinern von Skills, nicht durch Hinzufügen von Verzweigungen.

### Skalierung durch semantische Kompression

Mit wachsendem Kontext scheitern naive Ansätze:

**Falsch:** Mehr Tools hinzufügen, um mehr Daten abzurufen

**Richtig:** Semantische Kompression — der Pattern Agent destilliert viele spezifische Beobachtungen zu wenigen allgemeinen Prinzipien

```
3x "User corrected date format"  →  "Dates: Always ISO format"
5x "User prefers short answers"  →  "Brevity: be concise"
```

Die Bedeutung bleibt erhalten, die Redundanz verschwindet. Ein Skill ersetzt zehn Memory-Einträge und lenkt die Aufmerksamkeit auf das Wesentliche.

### Pattern Agent als Optimierer

Der Pattern Agent ist der Optimierer dieses Systems:

1. **Beobachtet Gradienten** — Benutzerkorrekturen zeigen Fehler an
2. **Akkumuliert Aktualisierungen** — Memory speichert Beobachtungen
3. **Führt Batch-Update durch** — nächtliche Destillation
4. **Bereinigt Redundanz** — löscht veraltete Memory-Einträge

Ziel: Ein System, das sich verbessert, nicht durch das Hinzufügen von Code, sondern durch das Verfeinern von Aufmerksamkeit. Je länger es läuft, desto weniger Kontext benötigt es.

---

## Zusammenfassung der Designprinzipien

| Prinzip | Implementierung |
|---------|----------------|
| Message Passing | Append-only-Warteschlange, kein gemeinsamer Zustand |
| Ownership | Jeder Agent besitzt seine Domäne |
| Supervision | Dispatcher überwacht und startet neu |
| Dynamic Restriction | Agenten pledge/unveil beim Start |
| Priority Scheduling | Benutzerseitige Arbeit zuerst |
| Append-Only Log | Warteschlange als Quelle der Wahrheit |
| Specialization | Ein Agent, eine Rolle |
| Secure by Default | Keine impliziten Fähigkeiten |

---

## Implementierungs-Stack

| Komponente | Technologie |
|------------|-------------|
| Transport | Python (daemon) |
| Dispatcher | Python (daemon) |
| Agents | Python |
| Queue | JSONL file |
| Configuration | JSON |
| Web UI | localhost-only, config only |
| Vault | Markdown files + arbitrary assets |

---

Nächste Schritte: Implementierung der Kernkomponenten gemäß dieser Architektur.
