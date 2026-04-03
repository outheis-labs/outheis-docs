# Datenformate und Konventionen

Dieses Dokument legt die Struktur und das Format der Daten in outheis fest und ermöglicht es Agenten, verlässliche Annahmen über Inhalte zu treffen.

---

## Kernprinzip: Datenlokalität

**Benutzerdaten existieren nur an zwei Orten:**

| Ort | Geschrieben von | Enthält |
|-----|----------------|---------|
| `~/.outheis/human/` | outheis-System, Benutzer über Web UI, manuelle Bearbeitung | Konfiguration, Insights, Regeln |
| `vault/` (extern) | Benutzer | Wissen, Dokumente, Assets |

Keine Benutzerdaten werden anderswo gespeichert. Das Entfernen dieser Verzeichnisse löscht alle Benutzerspuren.

---

## Verzeichnisstruktur

### Systemverzeichnis

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
    │   └── priorities.md
    ├── messages.jsonl           # Message queue (append-only)
    ├── archive/                 # Cold storage for old conversations
    │   ├── messages-2025-01.jsonl
    │   └── ...
    ├── index.jsonl              # Search index (across all vaults)
    ├── tag-weights.jsonl        # Learned tag importance
    ├── cache/                   # Cached data
    │   └── agenda/              # Previous versions for diff
    │       ├── Daily.md.prev
    │       ├── Inbox.md.prev
    │       └── Exchange.md.prev
    ├── imports/                 # Imported external data
    │   ├── calendar/
    │   │   └── 2025-03-27.jsonl
    │   ├── email/
    │   │   └── inbox.jsonl
    │   ├── tasks/
    │   └── contacts/
    └── vault/                   # Minimal starter vault
```

### Vault (Extern, vom Benutzer verwaltet)

Vaults können sich überall im Dateisystem befinden. Mehrere Vaults werden unterstützt.

```
~/Documents/MyVault/             # Example: user's primary vault
├── Agenda/                      # Special directory (required in primary vault)
│   ├── Daily.md
│   ├── Inbox.md
│   └── Exchange.md
├── notes/
│   └── project-alpha.md
├── projects/
│   └── project-alpha/
│       ├── README.md
│       └── assets/
│           └── diagram.png
└── archive/
    └── 2024/

~/Documents/Obsidian/            # Example: second vault
├── ...
```

### Konfiguration

```json
{
  "vault": [
    "~/Documents/MyVault",
    "~/Documents/Obsidian"
  ]
}
```

Der erste Vault in der Liste ist der **primäre Vault** — enthält `Agenda/`.

---

## Vault-Struktur

### Konventionen

| Regel | Beschreibung |
|-------|--------------|
| `Agenda/` | Im primären Vault erforderlich, besondere Behandlung |
| Benutzerverzeichnisse | Beliebige Struktur, beliebige Tiefe |
| Verzeichnisnamen | Können als Organisationshinweise dienen |
| Markdown-Dateien | Primäres Wissensformat, selbstbeschreibend über Tags |
| Andere Dateien | Assets, Anhänge, verlinkt oder lose |

### Philosophie

Gemäß dem Prinzip der *prospektiven Informationsarchitektur*:

- **Selbstbeschreibung**: Dateien tragen ihre Bedeutung über Tags, nicht über Position
- **Position als Hinweis**: Verzeichnisstruktur liefert Kontext, nicht Identität
- **Mehrere Zugriffspfade**: Tags ermöglichen Abruf aus beliebiger Perspektive
- **Struktur zur Abfragezeit**: Hierarchien werden berechnet, nicht gespeichert

---

## Dateitypen

### Primär: Markdown (.md)

Das primäre Wissensformat. Menschenlesbar, maschinell verarbeitbar, selbstbeschreibend.

### Häufige Assets

Dateien, die häufig neben Markdown auftauchen oder darin verlinkt sind:

| Kategorie | Erweiterungen | Behandlung |
|-----------|---------------|------------|
| Dokumente | `.docx`, `.xlsx`, `.pptx`, `.pdf` | Metadaten indexieren, Text extrahieren wo möglich |
| Archive | `.zip`, `.tgz`, `.tar.gz`, `.tar`, `.7z` | Als Container indexieren, Inhalte auflisten |
| Bilder | `.png`, `.jpg`, `.jpeg`, `.gif`, `.svg`, `.webp` | Metadaten indexieren, OCR wenn konfiguriert |
| Code | `.py`, `.js`, `.ts`, `.sh`, `.json`, `.yaml` | Als Text indexieren |
| Repositories | `.git/` (Verzeichnis) | Als Git-Repo erkennen, Metadaten indexieren |
| Daten | `.csv`, `.tsv`, `.jsonl` | Als strukturierte Daten indexieren |

### Beziehungsmuster

Dateien stehen auf verschiedene Weisen zueinander in Beziehung:

| Muster | Beschreibung |
|--------|--------------|
| **Eingebettet** | Bild/Asset in Markdown referenziert (`![](path)`) |
| **Verlinkt** | Dokument über Pfad oder Wiki-Link referenziert (`[[name]]`) |
| **Geschwister** | Verwandte Dateien im selben Verzeichnis |
| **Lose** | Dateien ohne explizite Links (über Suche auffindbar) |

---

## Markdown-Format

### Frontmatter

Optionales YAML-Frontmatter für explizite Metadaten:

```markdown
---
title: Project Alpha Notes
created: 2025-01-15
modified: 2025-03-27
tags: [project/alpha, important]
---

# Project Alpha Notes

Content here...
```

| Feld | Typ | Beschreibung |
|------|-----|--------------|
| `title` | string | Anzeigename |
| `created` | date | Erstellungsdatum (ISO 8601) |
| `modified` | date | Letzte Änderung (ISO 8601) |
| `tags` | array | Semantische Tags |

Wenn kein Frontmatter vorhanden ist, leiten Agenten Metadaten ab aus:
- Titel: Erste `# Überschrift` oder Dateiname
- Erstellt/Geändert: Dateisystem-Zeitstempel
- Tags: Inline-Tags im Inhalt

### Tags

Tags können aus **zwei Quellen** stammen (beide funktionieren, werden automatisch zusammengeführt):

1. **YAML-Frontmatter** (optional):
```yaml
---
tags: [project/alpha, important]
---
```

2. **Inline-#Tags** im Fließtext (bevorzugt):
```markdown
This is an #important note about #project/alpha.

Meeting scheduled for tomorrow #deadline #priority-high.
```

outheis extrahiert Tags aus beiden Quellen und dedupliziert sie.

### Tag-Formate

| Format | Beispiel | Bedeutung |
|--------|---------|-----------|
| Einfach | `#important` | Einfaches Flag |
| Schlüssel-Wert | `#priority-high` | Attribut mit Wert |
| Hierarchisch | `#project/alpha` | Verschachtelter Namensraum |
| Datum | `#date-2026-03-24` | Spezifisches Datum |
| Status | `#status-active` | Zustandsindikator |

**Das Format des Benutzers wird beibehalten.** outheis erlernt, ob `-` oder `/` als Trennzeichen verwendet wird.

### Tag-Normalisierung

Zur Indizierung und Suche werden Tags normalisiert:

```
#Important     → important
#Priority-High → priority-high
#Project/Alpha → project/alpha
```

Regeln:
- Kleinbuchstaben für die Suche
- Bindestriche und Schrägstriche beibehalten
- Führendes `#` entfernen

### Tag-Analyse

outheis verfolgt die Tag-Nutzung und kann berichten:

- **Top-Tags** — am häufigsten verwendet
- **Tag-Hierarchien** — Präfixe wie `status-*`, `project/*`
- **Einzelne Tags** — nur einmal verwendet (Bereinigungskandidaten)

Im Chat fragen: "welche tags habe ich?" oder "tag-analyse"

### Tag-Philosophie

**outheis erfindet keine Tags.** Es verwendet deine Tags, erlernt dein Format und kann:
- Bereinigung für einzelne Tags vorschlagen
- Auf inkonsistente Formate hinweisen
- Ähnliche vorhandene Tags vorschlagen, wenn neue erstellt werden

Du bestimmst das Vokabular.

### Links

Wiki-Style-Links für interne Referenzen:

```markdown
See [[meeting-notes]] for details.
Related: [[projects/alpha/README]]
```

Standard-Markdown-Links für externe Referenzen:

```markdown
Based on [this paper](https://example.com/paper.pdf).
```

---

## Importierte Daten

Externe Daten (Kalender, E-Mail usw.) werden vom Action-Agenten in `~/.outheis/human/imports/` importiert. Diese Daten sind kanonisch — strukturierte Repräsentationen externer Quellen.

### Verzeichnisstruktur

```
~/.outheis/human/imports/
├── calendar/
│   ├── 2025-03-27.jsonl
│   └── recurring.jsonl
├── email/
│   ├── inbox.jsonl
│   └── sent.jsonl
├── tasks/
│   └── tasks.jsonl
└── contacts/
    └── contacts.jsonl
```

### Kalendereinträge

```json
{
  "id": "evt_abc123",
  "source": "google_calendar",
  "title": "Team Meeting",
  "start": "2025-03-27T10:00:00Z",
  "end": "2025-03-27T11:00:00Z",
  "location": "Room 3B",
  "description": "Weekly sync",
  "attendees": ["alice@example.com", "bob@example.com"],
  "recurring": false,
  "imported_at": "2025-03-27T08:00:00Z"
}
```

### E-Mail

```json
{
  "id": "msg_xyz789",
  "source": "gmail",
  "from": {"name": "Alice", "email": "alice@example.com"},
  "to": [{"name": "User", "email": "user@example.com"}],
  "cc": [],
  "subject": "Project Update",
  "body_text": "Plain text body...",
  "date": "2025-03-27T09:15:00Z",
  "thread_id": "thread_123",
  "labels": ["inbox", "important"],
  "attachments": [
    {"filename": "report.pdf", "mime_type": "application/pdf", "size": 102400}
  ],
  "imported_at": "2025-03-27T10:00:00Z"
}
```

### Aufgaben

```json
{
  "id": "task_456",
  "source": "todoist",
  "title": "Review proposal",
  "description": "Review and comment on Q2 proposal",
  "due": "2025-03-28T17:00:00Z",
  "priority": 2,
  "status": "pending",
  "project": "Work",
  "labels": ["review", "q2"],
  "imported_at": "2025-03-27T08:00:00Z"
}
```

### Kontakte

```json
{
  "id": "contact_789",
  "source": "google_contacts",
  "name": "Alice Smith",
  "email": ["alice@example.com", "alice.smith@work.com"],
  "phone": ["+1-555-123-4567"],
  "organization": "Acme Corp",
  "notes": "Met at conference 2024",
  "imported_at": "2025-03-27T08:00:00Z"
}
```

---

## Index

Der Data-Agent pflegt einen Suchindex unter `~/.outheis/human/index.jsonl`:

```json
{
  "vault": "~/Documents/MyVault",
  "path": "notes/project-alpha.md",
  "type": "markdown",
  "title": "Project Alpha Notes",
  "tags": ["project/alpha", "important"],
  "links_to": ["meeting-notes.md", "assets/diagram.png"],
  "linked_from": ["README.md"],
  "modified": "2025-03-27T10:00:00Z",
  "accessed_at": "2025-03-27T14:00:00Z",
  "access_count": 12,
  "checksum": "sha256:abc123...",
  "indexed_at": "2025-03-27T10:05:00Z"
}
```

Der Index umfasst alle konfigurierten Vaults. Jeder Eintrag enthält das `vault`-Feld.

---

## Human-Verzeichnis

### Struktur

```
~/.outheis/human/
├── config.json                  # User configuration
├── insights.jsonl               # Pattern agent output
├── rules/                       # Agenda agent rules
│   └── priorities.md
└── vault/                       # Minimal starter vault
```

### Schreibzugriff

| Komponente | Kann schreiben |
|------------|----------------|
| outheis-System | config.json, insights.jsonl |
| Pattern-Agent | insights.jsonl |
| Benutzer (Web UI) | config.json, rules/ |
| Benutzer (manuell) | Jede Datei |
| Andere Agenten | **Niemals** (nur Lesen) |

### config.json

Benutzerkonfiguration:

```json
{
  "name": "Markus",
  "language": "en",
  "timezone": "Europe/Berlin",
  "vault": [
    "~/Documents/MyVault",
    "~/Documents/Obsidian"
  ]
}
```

| Feld | Typ | Beschreibung |
|------|-----|--------------|
| `name` | string | Anzeigename des Benutzers |
| `language` | string | Bevorzugte Sprache (ISO 639-1) |
| `timezone` | string | IANA-Zeitzone |
| `vault` | array | Pfade zu Vaults (erster = primär) |

### insights.jsonl

Pattern-Agent schreibt Beobachtungen:

```json
{
  "v": 1,
  "id": "ins_20251115_001",
  "type": "strategy",
  "domain": "communication",
  "insight": "When formatting for Signal, use emoji headers instead of markdown",
  "confidence": 0.8,
  "evidence_count": 5,
  "source_sessions": ["sess_001", "sess_003", "sess_007"],
  "created_at": "2025-11-15T04:12:00Z"
}
```

| Feld | Typ | Beschreibung |
|------|-----|--------------|
| `type` | string | `strategy`, `preference`, `pattern`, `capability` |
| `domain` | string | Anwendungsbereich |
| `confidence` | float | 0,0–1,0, nimmt mit Belegen zu |
| `evidence_count` | int | Anzahl unterstützender Instanzen |
| `source_sessions` | array | Rückverfolgbarkeit zu Gesprächen |

### session_notes.jsonl

Temporäre Lernnotizen, die vom Pattern-Agenten bei geplanten Läufen geprüft werden:

```json
{
  "v": 1,
  "id": "note_20251115_001",
  "session_id": "sess_007",
  "agent": "relay",
  "problem": "User asked for table formatting in Signal",
  "solution": "Replace markdown tables with emoji-separated rows",
  "context": {
    "channel": "signal",
    "user_feedback": "positive"
  },
  "created_at": "2025-11-15T10:30:00Z",
  "reviewed": false
}
```

Sitzungsnotizen werden:
- Von jedem Agenten geschrieben, wenn der Benutzer bei der Problemlösung hilft
- Vom Pattern-Agenten beim nächtlichen Lauf gelesen
- Nach der Verarbeitung als `reviewed: true` markiert
- Regelmäßig bereinigt (geprüfte Notizen älter als 30 Tage)

Der Pattern-Agent entscheidet: auf Insight verallgemeinern oder als spezifische Instanz im Archiv belassen.

### Agenda-Regeln

Markdown-Dateien in `human/rules/` definieren Benutzerpräferenzen:

```markdown
# Priorities

## Work vs Personal
- Work appointments take priority over personal, except:
  - Family events always take priority
  - Health appointments always take priority

## Time Blocks
- Monday mornings: no meetings before 10:00
- Friday afternoons: no meetings after 15:00

## Notifications
- Deadline < 3 days: always remind
- Emails from boss: always show immediately
```

---

## Textextraktion

Für Nicht-Markdown-Dateien extrahieren Agenten Text wo möglich:

| Typ | Extraktionsmethode |
|-----|-------------------|
| PDF | `pdftotext`, `pymupdf` oder ähnlich |
| DOCX/XLSX/PPTX | `python-docx`, `openpyxl`, `python-pptx` |
| Bilder | OCR (optional, konfigurierbar) |
| Archive | Inhalte auflisten, Text aus enthaltenen Dateien extrahieren |
| Code | Als Klartext behandeln |

Extrahierter Text wird im Index gespeichert, nicht als separate Dateien.

---

## Binärdateien

Binärdateien (Bilder, PDFs, Office-Dokumente) werden:

1. **Indiziert** nach Metadaten (Größe, Typ, Änderungsdatum)
2. **Textextrahiert** wo möglich
3. **Verlinkt** über Referenzen in Markdown
4. **Nicht verändert** von outheis (aus Agentenperspektive nur Lesen)

---

## Git-Repositories

Wenn ein Verzeichnis `.git/` enthält:

1. **Erkannt** als Git-Repository
2. **Indiziert** nach Metadaten (Remotes, Branches, aktuelle Commits)
3. **Nicht verändert** von outheis-Agenten
4. **Action-Agent** kann Git-Befehle ausführen, wenn angewiesen

---

## Zeitstempel

Alle Zeitstempel verwenden ISO 8601-Format in UTC:

```
2025-03-27T10:00:00Z
```

Agenten konvertieren zur Anzeige in die lokale Zeitzone basierend auf der Zeitzoneneinstellung in `human/config.json`.

---

## Dateinamen

### Konventionen

| Typ | Konvention | Beispiel |
|-----|------------|---------|
| Notizen | Kleinbuchstaben, Bindestriche | `project-alpha-notes.md` |
| Importe | Datum- oder Typpräfix | `2025-03-27.jsonl` |
| System | Beschreibend | `index.jsonl` |

### Verbotene Zeichen

Dateinamen dürfen nicht enthalten:
- `/` `\` `:` `*` `?` `"` `<` `>` `|`
- Führende/abschließende Leerzeichen
- Führenden `.` in Benutzerdateien (für System reserviert)

---

## Kodierung

Alle Textdateien verwenden UTF-8-Kodierung ohne BOM.

---

## Zusammenfassung

| Datentyp | Ort | Format | Geschrieben von |
|----------|-----|--------|----------------|
| Benutzernotizen | `vault/` | Markdown | Benutzer |
| Benutzer-Assets | `vault/` | Verschiedene | Benutzer |
| Suchindex | `~/.outheis/human/index.jsonl` | JSONL | Data-Agent |
| Tag-Gewichte | `~/.outheis/human/tag-weights.jsonl` | JSONL | Pattern-Agent |
| Importierte Daten | `~/.outheis/human/imports/` | JSONL | Action-Agent |
| Nachrichtenwarteschlange | `~/.outheis/human/messages.jsonl` | JSONL | Alle Agenten |
| Archiv | `~/.outheis/human/archive/` | JSONL | Dispatcher |
| Benutzerkonfiguration | `~/.outheis/human/config.json` | JSON | System, Benutzer |
| Insights | `~/.outheis/human/insights.jsonl` | JSONL | Pattern-Agent |
| Agenda-Regeln | `~/.outheis/human/rules/` | Markdown | Benutzer |

---

## Schema-Versionierung

### Das Problem

Datenstrukturen entwickeln sich weiter. Nachrichten, Insights und andere Formate werden sich im Laufe der Zeit ändern. Ohne Versionierung:

- Alte Daten werden nach Upgrades unlesbar
- Gemischte Versionen in derselben Datei verursachen Parsing-Fehler
- Kein Migrationspfad für vorhandene Daten

### Versionsfeld

Jeder Datensatz in outheis-verwalteten JSONL-Dateien trägt eine Version:

```json
{"v": 1, "id": "msg_001", "from": {"agent": "zeno"}, ...}
{"v": 1, "id": "msg_002", "from": {"agent": "cato"}, ...}
{"v": 2, "id": "msg_003", "from": {"agent": "zeno"}, "priority": "high", ...}
```

| Feld | Typ | Bedeutung |
|------|-----|-----------|
| `v` | integer | Schema-Version dieses Datensatzes |

Kurzer Feldname (`v` statt `version`), weil JSONL kompakt sein sollte.

### Versionsautorität

Die Schema-Version ist in `core/schema.py` definiert:

```python
# core/schema.py — single source of truth

MESSAGES_VERSION = 2
INSIGHTS_VERSION = 1
CONFIG_VERSION = 1

def write_message(msg):
    msg["v"] = MESSAGES_VERSION
    return json.dumps(msg)
```

Alle Agenten importieren dieses Modul. Kein Agent schreibt JSON direkt.

### Lesen mit Versionsüberprüfung

```python
def read_message(line):
    msg = json.loads(line)
    version = msg.get("v", 0)  # v0 = pre-versioning

    if version == MESSAGES_VERSION:
        return msg  # Hot path, no overhead

    if version > MESSAGES_VERSION:
        raise UnsupportedVersion(
            f"Message v{version} requires newer outheis"
        )

    # Only old messages go through migration
    return migrate_message(msg, from_version=version)
```

**Performance:** 99 % der Nachrichten entsprechen der aktuellen Version → einzelner Integer-Vergleich, kein Overhead.

### Migrationslogik

Migration erfolgt schrittweise (v0 → v1 → v2), in `core/schema.py`:

```python
def migrate_message(msg, from_version):
    """Stepwise migration: v0 → v1 → v2 → ..."""

    if from_version < 1:
        # v0 → v1: "from" was string, now object
        if isinstance(msg.get("from"), str):
            msg["from"] = {"agent": msg["from"]}
        msg["v"] = 1
        from_version = 1

    if from_version < 2:
        # v1 → v2: New field "priority" with default
        msg.setdefault("priority", "normal")
        msg["v"] = 2
        from_version = 2

    return msg
```

| Prinzip | Grund |
|---------|-------|
| Schrittweise (v0→v1→v2) | Jeder Schritt isoliert, testbar |
| Verlustfrei | Alte Daten bleiben vollständig lesbar |
| Migration zur Lesezeit | Originaldatei unverändert |
| Schreiben immer aktuell | Niemals alte Versionen erstellen |

### Migrations-CLI

```bash
# Scan for outdated records
outheis migrate --scan

> Found 47 messages at v1 (current: v2)
> Found 12 insights at v0 (current: v1)
>
> Run 'outheis migrate --apply' to convert

# Apply migration
outheis migrate --apply

> Migrating messages.jsonl: 47 entries v1 → v2
> Migrating archive/messages-2025-01.jsonl: 128 entries v1 → v2
> Migrating insights.jsonl: 12 entries v0 → v1
> Done. Backup in human/.migrate-backup/2025-11-15T10:00:00/

# Quiet mode for automation
outheis migrate --apply --quiet
```

### Automatische Migration

Optional: Migration im nächtlichen Batch mit Pattern-Agent ausführen.

```json
{
  "system": {
    "auto_migrate": true,
    "migrate_schedule": "04:00"
  }
}
```

### Versionshistorie

| Datei | Aktuell | Änderungen |
|-------|---------|------------|
| messages.jsonl | v1 | Initial |
| insights.jsonl | v1 | Initial |
| config.json | v1 | Initial |
| tag-weights.jsonl | v1 | Initial |
| index.jsonl | v1 | Initial |

*Wird mit jeder Schema-Änderung aktualisiert.*

---

## Theoretischer Hintergrund

Die Vault-Architektur implementiert Prinzipien der *prospektiven Informationsarchitektur*:

- **Selbstbeschreibende Objekte**: Dateien tragen Bedeutung über Tags, nicht Position
- **Multiple Relationierung**: Tags und Links ermöglichen mehrere Zugriffspfade
- **Struktur zur Abfragezeit**: Hierarchien werden berechnet, nicht gespeichert
- **Klartext als Fundament**: Universelle Lesbarkeit, langfristige Stabilität

Siehe: [Temporalization of Order](https://github.com/outheis-labs/research-base/blob/main/temporalization-of-order/temporalization-of-order.md) für theoretische Grundlagen.

---

## Randfälle

### Symlinks

| Typ | Behandlung |
|-----|------------|
| Symlink innerhalb des Vault | Folgen, Ziel indexieren |
| Symlink außerhalb des Vault | **Nicht folgen**, als Fehler protokollieren |

Begründung: Symlinks außerhalb des Vault könnten Daten leaken oder die Zugriffskontrolle umgehen.

### Versteckte Dateien

Dateien und Verzeichnisse, die mit `.` beginnen, werden ignoriert, außer:

| Pfad | Behandlung |
|------|------------|
| `.git/` | Als Repository-Metadaten erkannt |
| Alle anderen `.*` | Ignoriert (nicht indexiert, nicht verarbeitet) |

Dies umfasst `.obsidian/`, `.DS_Store`, `.gitignore` usw.

### Große Dateien

| Größe | Behandlung |
|-------|------------|
| < 50 MB | Vollständige Textextraktion |
| 50 MB - 200 MB | Erste/letzte Seiten extrahieren, nur Metadaten |
| > 200 MB | Nur Metadaten, Warnung protokollieren |

Schwellenwerte sind konfigurierbar.

### Kodierungsprobleme

Wenn eine Datei kein gültiges UTF-8 ist:

1. Erkennung versuchen (ISO-8859-1, Windows-1252 usw.)
2. Wenn Konvertierung erfolgreich: konvertierten Text indexieren
3. Wenn Konvertierung fehlschlägt: nur Metadaten indexieren, **Benutzer benachrichtigen**

Benachrichtigungspfad: Data-Agent → Dispatcher → Agenda-Agent (Persönlicher Modus) oder Relay (Domain-Expert-Modus) → Benutzer

---

## Domain-Expert-Modus: Administratorrolle

Im Domain-Expert-Modus dient das `human/`-Verzeichnis einem anderen Zweck:

| Aspekt | Persönlicher Modus | Domain-Expert-Modus |
|--------|-------------------|---------------------|
| `human/` repräsentiert | Einzelner Benutzer | Systemadministrator |
| Agenda-Agent | Aktiv (persönlicher Sekretär) | Deaktiviert |
| Pattern-Agent | Reflektiert über Benutzerverhalten | Reflektiert über Domänenwissen |
| Konfigurationszugriff | Benutzer über Web UI | Admin über Web UI |
| Regeln | Benutzerpräferenzen | Systemrichtlinien |

Die Administratorrolle im Domain-Expert-Modus:

- Konfiguriert Agenten, Modelle, Routing
- Definiert domänenspezifische Regeln
- Überwacht Systemzustand
- Empfängt **kein** persönliches Filtern (kein Agenda)

Mehrere Endbenutzer interagieren über Transport, aber nur der Administrator konfiguriert `human/`.

---

## Agenda-Verzeichnis

Der primäre Vault enthält ein spezielles `Agenda/`-Verzeichnis, das als strukturierte Schnittstelle zwischen Benutzer und System dient.

### Struktur

```
vault/Agenda/
├── Daily.md
├── Inbox.md
└── Exchange.md
```

Drei Dateien, keine Unterverzeichnisse.

### Zweck

| Datei | Richtung | Zweck |
|-------|----------|-------|
| `Daily.md` | Bidirektional | Heute: Termine, Aufgaben, Notizen |
| `Inbox.md` | Benutzer → System | Schnelleingabe, unstrukturierte Gedanken |
| `Exchange.md` | System ↔ Benutzer | Fragen, Klärungen, Lernen |

### Daily.md

Der aktuelle Tag. Agenda-Agent pflegt die Struktur, Benutzer fügt Inhalte hinzu.

```markdown
# 2025-03-27

## Appointments
- 09:00 Standup
- 14:00 Workshop

## Focus
- [ ] Finish report #deadline
- [ ] Review proposal

## Notes

```

### Inbox.md

Schnellerfassung. Benutzer schreibt, System verarbeitet.

```markdown
meeting with X next week, important

remember to call Y about the contract

#idea redesign the onboarding flow
```

Agenda-Agent liest, klassifiziert und leitet an passende Agenten weiter.

### Exchange.md

Asynchroner Dialog. System fragt, Benutzer antwortet wenn es passt. Kein Druck.

```markdown
# Open

## Scheduling conflict
> Friday 28.03 you have:
> - 10:00 Team meeting
> - 10:00 Dentist
>
> Which takes priority?

Your answer:


---

# Resolved

## Tag meaning
> You use #wip and #in-progress. Synonyms?

Your answer: Yes, merge to #wip

Learned: #in-progress → #wip
```

### Besondere Behandlung

Das `Agenda/`-Verzeichnis erhält besondere Behandlung:

| Aspekt | Behandlung |
|--------|------------|
| Änderungserkennung | Prüfsumme + Diff (vorherige Version gecacht) |
| Eigentümerschaft | Agenda-Agent |
| Indizierung | Höhere Priorität, immer aktuell |
| Diff-Analyse | Kommentare, Hinzufügungen, Löschungen werden verfolgt |

Dies ermöglicht dem Agenda-Agenten zu verstehen, *was* sich geändert hat, nicht nur *dass* sich etwas geändert hat.

### Cache-Ort

```
~/.outheis/human/cache/agenda/
├── Daily.md.prev
├── Inbox.md.prev
└── Exchange.md.prev
```

Vorherige Versionen werden im Systemverzeichnis gecacht, um Diffs zu berechnen.

---

## Zugriffsstrategien

Ohne Datenbank erfordert schneller Zugriff clevere Strategien auf Basis von Klartext.

### Index als primärer Nachschlageort

Der Index (`~/.outheis/human/index.jsonl`) dient als erster Zugangspunkt. Dateiinhalte werden nur bei Bedarf geladen.

```
Query
  │
  ▼
Index (fast, in-memory)
  │
  ├── Filter by tags, type, date
  ├── Rank candidates
  │
  ▼
Top-N file access (lazy load)
```

### Ranking-Heuristiken

Kandidaten aus dem Index werden nach mehreren Signalen gerankt:

| Signal | Gewicht | Begründung |
|--------|---------|------------|
| **Aktualität** | Hoch | Kürzlich geändert = wahrscheinlich relevant |
| **Zugriffshäufigkeit** | Mittel | Oft zugegriffen = wichtig |
| **Link-Dichte** | Mittel | Viele Backlinks = zentraler Knoten |
| **Tag-Übereinstimmung** | Hoch | Direkte Tag-Übereinstimmung = starkes Signal |
| **Tag-Gewicht** | Mittel | Gelernte Tag-Bedeutung |

### Tag-Lernen

Pattern-Agent analysiert Tag-Nutzung und erlernt Gewichte:

```json
{
  "tag": "project/alpha",
  "weight": 0.85,
  "access_count": 47,
  "co_occurs_with": ["deadline", "important"],
  "last_accessed": "2025-03-27T10:00:00Z"
}
```

Gespeichert in `~/.outheis/human/tag-weights.jsonl`.

Gewichte werden aktualisiert basierend auf:
- Zugriffshäufigkeit (Tag erscheint in aufgerufenen Dateien)
- Gemeinsames Auftreten mit erfolgreichen Suchen
- Implizitem Feedback (wurde Ergebnis verwendet?)

### Volltextsuche

Für Inhalte, die nicht im Index erfasst sind:

| Ansatz | Anwendungsfall |
|--------|----------------|
| Grep + Cache | Einfache Teilstring-Suche |
| Invertierter Index | Häufige Volltextabfragen |
| Embedding-Suche | Semantische Ähnlichkeit (optional, lokal) |

Implementierungswahl hängt von Vault-Größe und Hardware ab.

### Index-Aktualisierungen

| Auslöser | Aktion |
|----------|--------|
| Dateiwatcher auf Vault | Änderungen erkennen |
| Prüfsummen-Mismatch | Datei neu indexieren |
| Periodischer Scan | Verpasste Änderungen erfassen |

Dateiwatcher verwendet `inotify` (Linux) oder `kqueue` (macOS/BSD) — ereignisgesteuert, kein Polling.

### Kaltspeicherzugriff

Für archivierte Gespräche (`~/.outheis/human/archive/messages-*.jsonl`):

```
Query about old conversation
  │
  ▼
Data agent identifies relevant archive
  │
  ▼
Load archive file (slower)
  │
  ▼
Search within archive
  │
  ▼
Return results, unload archive
```

Kein dauerhafter Speichereinfluss. Bei Bedarf laden, nach Verwendung freigeben.
