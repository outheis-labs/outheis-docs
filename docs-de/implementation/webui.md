---
title: Web UI
---

# Web UI

*Lokale Verwaltungsoberfläche für outheis.*

## Überblick

Die Web-Oberfläche bietet eine browserbasierte Schnittstelle zur Konfiguration und Überwachung von outheis. Sie läuft auf `localhost:8080`. Ausdrücklich **nicht** für Remote-Zugriff konzipiert — alle Benutzerdaten bleiben lokal.

```
┌─────────────────────────────────────────────────────────────┐
│ outheis                              [Overview] [Save]       │
├─────────────┬───────────────────────────────────────────────┤
│ System      │                                               │
│  Overview   │  ┌─────────┐ ┌─────────┐ ┌─────────┐         │
│  Config     │  │Dispatcher│ │ Agents │ │Messages │         │
│  Messages   │  │ Running  │ │  5/6   │ │   42    │         │
│  Scheduler  │  └─────────┘ └─────────┘ └─────────┘         │
│             │                                               │
│ Knowledge   │  Recent messages                              │
│  Memory     │  ┌─────────────────────────────────────────┐ │
│  Skills     │  │ 14:32  cato → relay  Daily updated      │ │
│  Rules      │  │ 14:30  scheduler     agenda_review      │ │
│  Patterns   │  │ 14:15  zeno → relay  Found 3 matches    │ │
│             │  └─────────────────────────────────────────┘ │
│ Vault       │                                               │
│  Agenda     │                                               │
│  Codebase   │                                               │
│  Migration  │                                               │
│  Tags       │                                               │
└─────────────┴───────────────────────────────────────────────┘
```

## Server starten

```bash
cd outheis-minimal/webui
pip install fastapi uvicorn
python server.py
```

Öffnet unter `http://localhost:8080`. Der Server überwacht `~/.outheis/human/` auf Änderungen.

## Navigation

### System

| Ansicht | Zweck |
|---------|-------|
| **Overview** | Dashboard mit Dispatcher-Status, aktiven Agenten, Nachrichtenanzahl, aktuellen Nachrichten |
| **Configuration** | Vollständiger Konfig-Editor mit Tabs: General, Providers, Models, Agents, Signal |
| **Messages** | Live-Ansicht von `messages.jsonl` mit WebSocket-Updates |
| **Scheduler** | Geplante Aufgaben verwalten (agenda_review, shadow_scan, pattern_nightly) |

### Knowledge

| Ansicht | Zweck |
|---------|-------|
| **Memory** | Dateien in `~/.outheis/human/memory/` anzeigen/bearbeiten |
| **Skills** | Dateien in `~/.outheis/human/skills/` anzeigen/bearbeiten |
| **Rules** | Dateien in `~/.outheis/human/rules/` anzeigen/bearbeiten |
| **Patterns** | Dateien in `~/.outheis/human/cache/patterns/` anzeigen (nur Lesen) |

### Vault

| Ansicht | Zweck |
|---------|-------|
| **Files** | Vollständiger Vault-Browser — alle konfigurierten Vaults, Verzeichnisbaum, bearbeiten und löschen |
| **Agenda** | Dateien in `vault/Agenda/` anzeigen/bearbeiten (Daily.md, Inbox.md, Exchange.md) |
| **Codebase** | Dateien in `vault/Codebase/` anzeigen (alans Vorschläge) |
| **Migration** | Migrationsdateien hochladen (Drop-Zone), Dateien anzeigen und bearbeiten, Migration/-Verzeichnis verwalten |
| **Tags** | Vault nach #Tags scannen, nach Namensraum-Gruppe auflisten, Tags in allen Dateien umbenennen oder löschen |

## Files-Ansicht

Vollständiger Browser für alle konfigurierten Vault-Verzeichnisse:

- **Verzeichnisbaum** links — alle Vaults als Wurzeln, Verzeichnisse standardmäßig zugeklappt, zum Aufklappen klicken
- **Datei-Viewer/-Editor** rechts — gleicher Rendered/Source-Umschalter wie andere Dateiansichten
- **Alle Dateitypen** im Baum sichtbar:
  - Textdateien (`.md`, `.txt`, `.json`, `.py`, …) — bearbeitbar, Speichern-Schaltfläche
  - Bilddateien (`.png`, `.jpg`, `.svg`, …) — inline gerendert, Download-Schaltfläche
  - Binärdateien (`.pdf`, `.docx`, …) — Download-Schaltfläche
- **Obsidian-Wikilinks** — `![[image.jpg]]` und `![[image.jpg|WxH]]` werden aufgelöst und als Inline-Bilder gerendert
- **Löschen** — Bestätigungsdialog, entfernt Datei aus Vault

## Tags-Ansicht

Die Tags-Ansicht scannt den Vault nach allen `#Tags` und zeigt sie nach Namensraum-Präfix gruppiert:

- **Scan-Schaltfläche** — stellt eine `tag_scan`-Dispatcher-Aufgabe in die Warteschlange (gleiche asynchrone UX wie Scheduler)
- Ergebnisse werden gecacht; Scan-Schaltfläche führt bei Bedarf erneut aus
- Tags werden nach Namensraum-Präfix gruppiert (`#action-*`, `#date-*`, `#rank-*` usw.), standardmäßig alle zugeklappt
- Jede Gruppe zeigt Tag-Anzahl und Gesamtaufkommen im Vault
- Pro Tag: Aufkommensanzahl, Dateianzahl, Umbenennen-Eingabefeld, Löschen-Schaltfläche

- `#outheis-*`-Tags sind ausgeblendet (nur interne Systemnutzung)

## Konfigurationseditor

Die Konfigurationsansicht bietet einen vollständigen Editor für `~/.outheis/human/config.json`:

### General-Tab

- **Benutzerprofil**: Name, E-Mail, Telefon, Sprache, Zeitzone

- **Vaults**: Liste der Vault-Verzeichnisse (primär + sekundär)

### Providers-Tab

Drei Anbieter-Karten (Anthropic, OpenAI, Ollama):

- API-Schlüssel (Passwortfeld, nicht als Klartext in der UI gespeichert)
- Basis-URL (für benutzerdefinierte Endpunkte oder Proxys)
- Status-Indikator (grüner Punkt wenn konfiguriert)

### Models-Tab

Modell-Alias-Zuordnung:
```
fast      → claude-haiku-4-5
capable   → claude-sonnet-4-20250514
reasoning → claude-opus-4-5
```

Aliase mit Anbieterauswahl hinzufügen/entfernen.

### Agents-Tab

Agenten-Konfiguration pro Agent:

| Agent | Name | Modell | Aktiviert |
|-------|------|--------|-----------|
| relay | ou | capable | ✓ |
| data | zeno | capable | ✓ |
| agenda | cato | capable | ✓ |
| action | hiro | capable | ☐ |
| pattern | rumi | capable | ✓ |
| code | alan | capable | ☐ |

Jeder Agent kann einen anderen Modell-Alias verwenden (fast/capable/reasoning).

### Signal-Tab

Signal-Transport-Konfiguration:

- Aktiviert-Umschalter
- Telefonnummer (bei signal-cli registriert)
- CLI-Pfad (Standard: `/usr/local/bin/signal-cli`)

- Whitelist (Telefonnummern zur Interaktion erlaubt)

## Scheduler

Geplante Aufgaben verwalten:

```
┌─ Task Type ─────────┬─ Times ──────────────┬─ Enabled ─┐
│ agenda_review       │ 06:00 12:00 18:00 +  │    ✓      │
│ shadow_scan         │ 03:30              +  │    ✓      │
│ pattern_nightly     │ 04:00              +  │    ✓      │
└─────────────────────┴──────────────────────┴───────────┘
```

- **+-Schaltfläche**: Weitere Zeit hinzufügen (erhöht automatisch um 1 Stunde)

- **×-Schaltfläche**: Zeit entfernen (mindestens eine verbleibt)

- **Checkbox**: Aufgabe aktivieren/deaktivieren

- **History-Tab**: Vergangene Scheduler-Ereignisse aus messages.jsonl anzeigen

## Datei-Browser

Memory-, Skills-, Rules-, Patterns-, Agenda- und Codebase-Ansichten teilen sich einen Datei-Browser:

```
┌─ Files ───────┬─ Content ──────────────────────────────┐
│ common.md  ✓  │  [Rendered] [Source]                   │
│ relay.md      │                                        │
│ data.md       │  # Common Skills                       │
│               │                                        │
│               │  ## Dates                              │
│               │  Always use ISO format (YYYY-MM-DD)    │
│               │                                        │
└───────────────┴────────────────────────────────────────┘
```

- **Rendered**: Markdown als HTML gerendert (via marked.js)

- **Source**: Rohtext, bearbeitbar (contenteditable)

- **Save**: Schreibt Änderungen zurück auf Disk

## Live-Updates

Die Messages-Ansicht verwendet WebSocket für Echtzeit-Updates:

1. Server überwacht `messages.jsonl` auf Änderungen
2. Neue Zeilen werden geparst und an verbundene Clients gesendet
3. Nachrichten erscheinen sofort in der UI

Verbindungsstatus in der Statusleiste:

- `Connected` — WebSocket aktiv
- `Disconnected` — Verbinde in 3 Sekunden erneut
- `Error` — Verbindung fehlgeschlagen

## API-Endpunkte

Der Server stellt REST-Endpunkte bereit:

### Config
- `GET /api/config` — config.json lesen
- `POST /api/config` — config.json schreiben

### Status
- `GET /api/status` — Dispatcher läuft, PID, Agenten-Anzahl, Nachrichten heute

### Messages
- `GET /api/messages?limit=50` — Aktuelle Nachrichten aus messages.jsonl

### Files
- `GET /api/{type}` — Dateien auflisten (type: memory, skills, rules, patterns, agenda, codebase)

- `GET /api/{type}/{filename}` — Dateiinhalt lesen
- `PUT /api/{type}/{filename}` — Dateiinhalt schreiben

### Tags
- `GET /api/tags` — Tag-Scan-Ergebnisse (gecacht, gefiltert, lexikalisch sortiert)
- `POST /api/tags/scan` — tag_scan-Dispatcher-Aufgabe einreihen, gibt conversation_id zurück
- `POST /api/tags/rename` — Tag in allen Vault-Dateien umbenennen
- `POST /api/tags/delete` — Tag aus allen Vault-Dateien entfernen

### Vault Files
- `GET /api/vault/tree` — Rekursiver Baum aller konfigurierten Vaults
- `GET /api/vault/file?path=` — Datei lesen (Text-/Bild-/Binärerkennung, Wikilinks für .md aufgelöst)
- `PUT /api/vault/file` — Dateiinhalt schreiben
- `DELETE /api/vault/file?path=` — Datei löschen
- `GET /api/vault/raw?path=` — Rohdatei bereitstellen (für Inline-Bilder und Downloads)

### Migration
- `GET /api/migration` — Dateien in vault/Migration/ auflisten
- `GET /api/migration/{filename}` — Dateiinhalt lesen
- `PUT /api/migration/{filename}` — Dateiinhalt schreiben
- `POST /api/migration/create` — vault/Migration-Verzeichnis erstellen
- `POST /api/migration/upload` — Datei per Multipart-Formular hochladen

### WebSocket
- `WS /ws` — Live-Nachrichten-Stream

## Dateiorte

```
outheis-minimal/
└── webui/
    ├── server.py      # FastAPI backend
    ├── index.html     # HTML structure
    ├── style.css      # Lexend Deca, light/dark mode
    ├── app.js         # View routing, WebSocket, forms
    └── assets/
        ├── logo.svg   # outheis labs logo
        └── logo.png   # Fallback
```

## Designentscheidungen

### Typografie

Einzelne Schriftfamilie (Lexend Deca) in zwei Stärken:

- **400** — Fließtext, Labels, Eingaben
- **500** — Titel, Hervorhebungen, Agentennamen

### Farbmodi

CSS-Variablen unterstützen automatischen Hell-/Dunkel-Modus über `prefers-color-scheme`. Das Logo kehrt im Dunkelmodus die Farben um.

### Keine Authentifizierung

Die UI ist aus Design-Gründen nur auf localhost. Kein Login, keine Sitzungen. Wenn du Port 8080 erreichen kannst, hast du vollen Zugriff.

### Kein Chat

Das ist eine Verwaltungsoberfläche, keine Chat-UI. Für Chat verwende die CLI (`nous chat`) oder den Signal-Transport.

## Abhängigkeiten

Server-seitig:

- `fastapi` — Web-Framework
- `uvicorn` — ASGI-Server

Client-seitig:

- `marked.js` — Markdown-Rendering (CDN)
- Lexend Deca — Typografie (Google Fonts)

Kein Build-Schritt. Kein Bundler. Einfache Dateien direkt ausgeliefert.
