---
title: Mit outheis kommunizieren
---

# Mit outheis kommunizieren

outheis ist über drei Kanäle erreichbar. Alle Kanäle verbinden sich mit demselben Dispatcher und denselben Agenten — der Unterschied liegt darin, wo du tippst und wie du Antworten erhältst.

---

## Web UI

Eine browserbasierte Oberfläche, die vom Dispatcher lokal bereitgestellt wird.

**Zugriff:** `http://127.0.0.1:8080` (während der Dispatcher läuft)

**Was sie bietet:**
- Live-Nachrichtenfeed — Gespräche mit Agenten in Echtzeit
- Eingabefeld — Nachrichten direkt aus dem Browser senden
- Konfigurationseditor — Modelle, Agenten, Scheduler
- Memory-, Rules- und Skills-Viewer und -Editor
- Vault-Dateibrowser
- Scheduler-Status und manuelle Aufgaben-Auslöser

**Einrichtung:** Standardmäßig aktiviert. Port und Host sind in `config.json` konfigurierbar:

```json
"webui": { "host": "127.0.0.1", "port": 8080 }
```

**Remote-Zugriff via SSH-Port-Weiterleitung:**

```bash
ssh -L 8080:localhost:8080 user@dein-server
```

---

## CLI

Kommandozeilen-Interface zum Senden von Nachrichten und Verwalten des Daemons.

**Einrichtung:** Verfügbar nach `pip install -e .` mit aktiver venv.

**Nachrichten senden:**

```bash
outheis send "Was steht heute an?"
outheis send "@zeno suche Notizen zu Projekt Alpha"
outheis chat                                         # interaktiver Modus
```

**Daemon-Steuerung:**

```bash
outheis start         # im Hintergrund starten
outheis start -f      # im Vordergrund starten
outheis start -fv     # Vordergrund + verbose (zeigt Tool-Calls)
outheis stop          # Daemon stoppen
outheis status        # PID, Uptime, Agenten-Status anzeigen
```

---

## Signal

Nachrichten über die Signal-Messenger-App empfangen und senden. Erfordert eine dedizierte Telefonnummer für den Bot.

**Einrichtung:** Siehe [Signal](../implementation/signal.md) in der Implementierungsdokumentation.

**Funktionsweise:** Der Bot hört auf eingehende Signal-Nachrichten und leitet sie an den Dispatcher weiter. Antworten werden als Signal-Nachrichten zurückgesendet. Sprachnachrichten werden automatisch transkribiert, wenn `faster-whisper` installiert ist.

**Wann verwenden:** Primärer Kanal, wenn du vom Handy mit outheis interagieren möchtest, ohne einen Browser oder ein Terminal zu öffnen.
