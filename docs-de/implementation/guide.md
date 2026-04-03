---
title: Anleitung
---

# Anleitung

*Einstieg in outheis.*

## Voraussetzungen

- Python 3.11+
- Ein Anthropic-API-Schlüssel
- Ein Vault-Verzeichnis — ein Ordner mit Markdown-Dateien (Obsidian funktioniert direkt)

Optional — nur erforderlich, wenn du ein lokales Modell über Ollama konfigurierst:

- [Ollama](https://ollama.com) installiert und aktiv
- `pip install openai` (outheis nutzt die OpenAI-kompatible Ollama-API)

Optional für Messaging über Signal:

- Ein registriertes Signal-Konto für die Bot-Telefonnummer
- `signal-cli` installiert und konfiguriert

## Schnellstart

Der schnellste Weg zu einem funktionierenden Setup ist ein Anthropic-API-Schlüssel. Keine zusätzlichen Abhängigkeiten — outheis läuft damit sofort mit Claude als einzigem Modellanbieter.

Lokale Modelle über Ollama sind optional und erfordern zusätzliche Einrichtung (siehe unten).

## Installation

Modernes pip erzwingt virtuelle Umgebungen. Erstelle zuerst eine:

```bash
git clone https://github.com/outheis-labs/outheis-minimal.git
cd outheis-minimal
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e .
```

Der `outheis`-Befehl ist nur verfügbar, solange die venv aktiv ist. Füge `source /path/to/outheis-minimal/.venv/bin/activate` zu deinem Shell-Profil hinzu, wenn du ihn immer verfügbar haben möchtest.

Für Sprachtranskription über Signal:

```bash
pip install -e ".[signal]"
```

## Einrichtung

```bash
outheis init
```

Das erstellt `~/.outheis/human/config.json` mit Standardwerten. Bearbeite sie:

```bash
$EDITOR ~/.outheis/human/config.json
```

Minimale erforderliche Konfiguration:

```json
{
  "human": {
    "name": "Your Name",
    "language": "en",
    "timezone": "Europe/Berlin",
    "vault": ["~/Documents/Vault"]
  },
  "llm": {
    "providers": {
      "anthropic": {
        "api_key": "sk-ant-..."
      }
    },
    "models": {
      "fast":    {"provider": "anthropic", "name": "claude-haiku-4-5"},
      "capable": {"provider": "anthropic", "name": "claude-sonnet-4-5"}
    }
  }
}
```

Das `vault`-Array akzeptiert mehrere Pfade. outheis überwacht alle davon.

## Dispatcher starten

```bash
outheis start        # Background daemon
outheis start -f     # Foreground (useful for first run / debugging)
outheis status       # Check PID, uptime, agent status
outheis stop         # Stop daemon
```

## Web UI

Sobald der Dispatcher läuft, ist die Web-Oberfläche verfügbar unter:

```
http://127.0.0.1:8080
```

Sie bietet:

- Live-Nachrichtenfeed (Gespräche mit Agenten)
- Memory-, Rules- und Skills-Viewer und -Editor
- Scheduler-Status und manuelle Aufgaben-Auslöser
- Vault-Datei-Browser

Der Web-UI-Port und -Host sind in `config.json` unter `"webui": {"host": "127.0.0.1", "port": 8080}` konfigurierbar.

### Remote-Zugriff über SSH

Die Web-Oberfläche bindet nur an localhost. Um von einem anderen Rechner darauf zuzugreifen, verwende SSH-Port-Weiterleitung:

```bash
ssh -L 8080:localhost:8080 user@your-server
```

Dann öffne `http://localhost:8080` in deinem lokalen Browser. Der Tunnel bleibt aktiv, solange die SSH-Verbindung besteht.

## Vault-Einrichtung

Dein Vault ist dein primärer Wissensspeicher. outheis liest daraus, schreibt darin (über cato und die Web-Oberfläche) und lernt im Laufe der Zeit daraus. Die Struktur ist flexibel — beliebige Markdown-Dateien funktionieren. Das empfohlene Agenda-Layout:

```
vault/
└── Agenda/
    ├── Daily.md      # Today's schedule — written by cato
    ├── Inbox.md      # Your quick capture — processed hourly
    └── Exchange.md   # Async back-and-forth with cato
```

Erstelle das `Agenda/`-Verzeichnis und leere Dateien. cato generiert `Daily.md` beim ersten Lauf.

## Signal-Einrichtung (optional)

Um Nachrichten über Signal zu empfangen und zu senden:

1. Eine dedizierte Telefonnummer bei Signal registrieren
2. `signal-cli` für diese Nummer installieren und konfigurieren
3. Zu `config.json` hinzufügen:

```json
{
  "signal": {
    "enabled": true,
    "bot_name": "ou",
    "bot_phone": "+49...",
    "allowed": []
  }
}
```

Setze `allowed` auf ein leeres Array, um alle Kontakte zu erlauben, oder liste spezifische Nummern auf: `["+49..."]`.

## CLI-Befehle

### Daemon-Steuerung

```bash
outheis start       # Start dispatcher (background)
outheis start -f    # Start in foreground
outheis start -fv   # Foreground + verbose (shows tool calls)
outheis stop        # Stop dispatcher
outheis status      # Show status, PID, uptime
```

### Messaging

```bash
outheis send "Hello"              # Single message
outheis send "@zeno find notes"   # Direct to Data agent
outheis chat                      # Interactive mode (with history)
```

### Memory

```bash
outheis memory              # Show all memories
outheis memory --type user  # Show only user facts
```

### Rules

```bash
outheis rules         # Show all rules (system + user)
outheis rules relay   # Show relay agent rules
```

## Mit outheis sprechen

Einfach natürlich sprechen. Relay entscheidet, wann Tools zu verwenden sind:

| Du sagst | Was passiert |
|----------|-------------|
| "hi" | Direkte Antwort |
| "was steht heute an?" | Verwendet check_agenda-Tool → Agenda-Agent |
| "wo wohne ich?" | Verwendet search_vault-Tool → Data-Agent |
| "! ich bin 54" | Speichert in Memory (expliziter Marker) |

### Explizite Agenten-Erwähnungen

Verwende `@name` für direkte Delegation:

| Erwähnung | Agent | Verwenden für |
|-----------|-------|---------------|
| @zeno | Data | Vault explizit durchsuchen |
| @cato | Agenda | Terminabfragen |
| @hiro | Action | Externe Aktionen (zukünftig) |

## Vault

Dein Vault ist ein Verzeichnis mit Markdown-Dateien:

```markdown
---
title: Project Alpha
tags: [active, client-work]
created: 2025-01-15
---
# Project Alpha

Status update...
```

### Empfohlene Struktur

```
vault/
├── Agenda/
│   ├── Daily.md      # Today's schedule
│   ├── Inbox.md      # Unprocessed items
│   └── Exchange.md   # External sync
├── projects/
├── notes/
└── references/
```

## Fehlerbehebung

### "Dispatcher not running"

```bash
outheis status   # Check if running
outheis start    # Start it
```

### Veraltete PID-Datei

```bash
rm ~/.outheis/.dispatcher.pid
outheis start
```

### Kein API-Schlüssel

```bash
export ANTHROPIC_API_KEY="sk-ant-..."
# Or add to ~/.bashrc / ~/.zshrc
```

### "openai package not installed" (Ollama-Modelle)

Wenn du ein Modell mit `"provider": "ollama"` konfigurierst, verwendet outheis die OpenAI-kompatible Ollama-API und benötigt das `openai`-Python-Paket:

```bash
pip install openai
```

Außerdem muss Ollama selbst laufen (`ollama serve`) und das Modell heruntergeladen sein (`ollama pull <modell>`).

### macOS: Daemon startet nicht im Hintergrund

Verwende den Vordergrundmodus:

```bash
outheis start -f &
```
