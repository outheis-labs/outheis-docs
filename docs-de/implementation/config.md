---
title: Konfiguration
---

# Konfiguration

*Vollständige Referenz für `config.json`.*

## Ort

```
~/.outheis/human/config.json
```

Wird beim ersten `outheis start` automatisch mit sinnvollen Standardwerten erstellt.

## Vollständiges Beispiel

```json
{
  "human": {
    "name": "Max",
    "phone": ["+49123456789"],
    "language": "de",
    "timezone": "Europe/Berlin",
    "vault": ["~/Documents/Vault", "~/Work/Notes"]
  },
  "signal": {
    "enabled": false,
    "bot_phone": "+49987654321",
    "bot_name": "Ou",
    "allowed": [
      {"name": "Partner", "phone": "+49111222333"}
    ]
  },
  "llm": {
    "providers": {
      "anthropic": {
        "api_key": "sk-ant-..."
      },
      "ollama": {
        "base_url": "http://localhost:11434"
      }
    },
    "models": {
      "fast": {
        "provider": "anthropic",
        "name": "claude-haiku-4-5",
        "run_mode": "on-demand"
      },
      "capable": {
        "provider": "anthropic",
        "name": "claude-sonnet-4-20250514",
        "run_mode": "on-demand"
      },
      "local": {
        "provider": "ollama",
        "name": "llama3.2:3b",
        "run_mode": "persistent"
      }
    }
  },
  "agents": {
    "relay": {"name": "ou", "model": "fast", "enabled": true},
    "data": {"name": "zeno", "model": "capable", "enabled": true},
    "agenda": {"name": "cato", "model": "capable", "enabled": true},
    "action": {"name": "hiro", "model": "capable", "enabled": false},
    "pattern": {"name": "rumi", "model": "capable", "enabled": true},
    "code": {"name": "alan", "model": "capable", "enabled": false}
  },
  "schedule": {
    "pattern_nightly": {"enabled": true, "hour": 4, "minute": 0},
    "index_rebuild": {"enabled": true, "hour": 4, "minute": 30},
    "archive_rotation": {"enabled": true, "hour": 5, "minute": 0},
    "session_summary": {"enabled": true, "minute": 0},
    "agenda_review": {
      "enabled": true,
      "hourly_at_minute": 55,
      "start_hour": 4,
      "end_hour": 23
    },
    "action_tasks": {"enabled": true}
  },
  "updates": {
    "auto_migrate": true,
    "schedule": "04:00"
  }
}
```

## Abschnitte

### human

Benutzeridentifikation und Vault-Orte.

| Feld | Typ | Standard | Beschreibung |
|------|-----|---------|--------------|
| `name` | string | "Human" | Anzeigename |
| `phone` | string[] | [] | Telefonnummern (für Signal-Transport) |
| `language` | string | "en" | Bevorzugter Sprachcode |
| `timezone` | string | "Europe/Berlin" | IANA-Zeitzone |
| `vault` | string[] | ["~/Documents/Vault"] | Vault-Verzeichnisse (erstes ist primär) |

**Umgebungsvariablen-Überschreibungen:**

- `OUTHEIS_HUMAN_DIR` — Human-Datenverzeichnis überschreiben (~/.outheis/human)
- `OUTHEIS_VAULT` — Primären Vault-Pfad überschreiben

### signal

Signal Messenger Transport-Konfiguration.

| Feld | Typ | Standard | Beschreibung |
|------|-----|---------|--------------|
| `enabled` | bool | false | Signal-Transport aktivieren |
| `bot_phone` | string | null | Telefonnummer des Bots |
| `bot_name` | string | "Ou" | Bot-Anzeigename |
| `allowed` | object[] | [] | Weitere erlaubte Kontakte |

Format erlaubter Kontakte:
```json
{"name": "Partner", "phone": "+49111222333"}
```

Die eigene Telefonnummer des Benutzers (aus `human.phone`) ist immer erlaubt.

### llm

LLM-Anbieter und Modell-Aliase.

#### providers

| Feld | Typ | Beschreibung |
|------|-----|--------------|
| `api_key` | string | API-Schlüssel (oder Umgebungsvariable verwenden) |
| `base_url` | string | Basis-URL überschreiben (für Ollama, benutzerdefinierte Endpunkte) |

Anbieternamen: `anthropic`, `ollama`, `openai`

**API-Schlüssel-Auflösung:**
1. Konfigurationsdatei (`api_key`-Feld)
2. Umgebungsvariable (`ANTHROPIC_API_KEY` usw.)

#### models

Modell-Aliase, die von Agenten verwendet werden.

| Feld | Typ | Standard | Beschreibung |
|------|-----|---------|--------------|
| `provider` | string | "anthropic" | Welcher Anbieter zu verwenden ist |
| `name` | string | — | Modell-Bezeichner |
| `run_mode` | string | "on-demand" | `on-demand` oder `persistent` |

**run_mode:**

- `on-demand` — Modell pro Anfrage starten (Cloud-APIs)
- `persistent` — Modell geladen halten (lokales Ollama)

**Standard-Aliase:**
```json
{
  "fast": {"provider": "anthropic", "name": "claude-haiku-4-5"},
  "capable": {"provider": "anthropic", "name": "claude-sonnet-4-20250514"}
}
```

### agents

Agenten-Konfiguration. Jeder Agent hat:

| Feld | Typ | Standard | Beschreibung |
|------|-----|---------|--------------|
| `name` | string | (variiert) | Anzeigename (ou, zeno, cato, hiro, rumi, alan) |
| `model` | string | "capable" | Zu verwendender Modell-Alias |
| `enabled` | bool | true | Ob Agent aktiv ist |

**Agenten-Rollen:**

| Rolle | Standard-Name | Standard-Modell | Zweck |
|-------|--------------|-----------------|-------|
| relay | ou | fast | Nachrichtenrouting, Gespräch |
| data | zeno | capable | Vault-Suche |
| agenda | cato | capable | Terminverwaltung |
| action | hiro | capable | Externe Aktionen (standardmäßig deaktiviert) |
| pattern | rumi | capable | Memory-Extraktion, Rules |
| code | alan | capable | Code-Intelligenz (nur Entwicklung, deaktiviert) |

Deaktivierte Agenten werden nicht instanziiert und ihre geplanten Aufgaben laufen nicht.

### schedule

Konfiguration geplanter Aufgaben.

#### Aufgaben zu festen Zeiten

| Aufgabe | Standard | Beschreibung |
|---------|---------|--------------|
| `pattern_nightly` | 04:00 | Memory-Extraktion, Konsolidierung |
| `index_rebuild` | 04:30 | Vault-Suchindizes neu erstellen |
| `archive_rotation` | 05:00 | Alte Nachrichten archivieren |

Felder:
```json
{
  "enabled": true,
  "hour": 4,
  "minute": 0
}
```

#### Stündliche Aufgaben

| Aufgabe | Standard | Beschreibung |
|---------|---------|--------------|
| `agenda_review` | xx:55 (04-23) | Agenda-Dateien verarbeiten |

Felder:
```json
{
  "enabled": true,
  "hourly_at_minute": 55,
  "start_hour": 4,
  "end_hour": 23
}
```

- `hourly_at_minute` — In dieser Minute jeder Stunde ausführen
- `start_hour` — Erste Stunde des Tages zum Ausführen (einschließlich)
- `end_hour` — Letzte Stunde des Tages zum Ausführen (einschließlich)

**Bedingte Ausführung:** Agenda-Überprüfung prüft Datei-Hashes vor dem Laufen. Wenn nichts geändert wurde, wird kein LLM-Aufruf gemacht. Morgen- (start_hour) und Abendläufe (end_hour) sind unbedingt.

#### Intervall-Aufgaben

| Aufgabe | Intervall | Beschreibung |
|---------|-----------|--------------|
| `session_summary` | 6 Stunden | Sitzungs-Insights extrahieren |
| `action_tasks` | 15 Minuten | Fällige Action-Aufgaben ausführen |

Felder:
```json
{
  "enabled": true
}
```

Intervall ist fest kodiert; nur `enabled` ist konfigurierbar.

### updates

Memory-Migration und Housekeeping.

| Feld | Typ | Standard | Beschreibung |
|------|-----|---------|--------------|
| `auto_migrate` | bool | true | Seed-Dateien automatisch verarbeiten |
| `schedule` | string | "04:00" | Zeit für Update-Aufgaben |

## Minimale Konfiguration

Die kleinste funktionierende Konfiguration:

```json
{
  "llm": {
    "providers": {
      "anthropic": {
        "api_key": "sk-ant-..."
      }
    }
  }
}
```

Alles andere verwendet Standardwerte.

## Umgebungsvariablen

| Variable | Zweck |
|----------|-------|
| `ANTHROPIC_API_KEY` | Anthropic-API-Schlüssel (Fallback) |
| `OPENAI_API_KEY` | OpenAI-API-Schlüssel (Fallback) |
| `OUTHEIS_HUMAN_DIR` | Human-Verzeichnis überschreiben |
| `OUTHEIS_VAULT` | Primären Vault überschreiben |

Umgebungsvariablen haben Vorrang vor Konfigurationsdatei-Werten.

## CLI-Befehle

```bash
# Show current config
outheis config show

# Edit config (opens in $EDITOR)
outheis config edit

# Set a value
outheis config set human.language de

# Validate config
outheis config validate
```

## Validierung

Die Konfiguration wird beim Laden validiert. Ungültige Konfiguration verhindert den Daemon-Start:

- Pflichtfelder müssen vorhanden sein
- Typen müssen übereinstimmen (string, int, bool, array)
- Referenzierte Modell-Aliase müssen existieren
- Anbieternamen müssen gültig sein

## Hot Reload

Einige Einstellungen können ohne Neustart neu geladen werden:

- Agenten-`enabled`-Status
- Zeitplan-Zeiten
- Modell-Aliase

Andere erfordern einen Neustart:

- Anbieter-Konfiguration
- Vault-Pfade
- Signal-Konfiguration

```bash
# Reload config
outheis reload

# Or restart
outheis stop && outheis start
```

## Siehe auch

- [Architektur](architecture.md) — Wie Komponenten zusammenpassen
- [Memory](memory.md) — Details zum Memory-System
- [Agenda](agenda.md) — Agenda-Agent-Konfiguration
