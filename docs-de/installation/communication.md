---
title: Mit outheis kommunizieren
---

# Mit outheis kommunizieren

outheis ist über drei Kanäle erreichbar. Alle Kanäle verbinden sich mit demselben Dispatcher und denselben Agenten — der Unterschied liegt darin, wo du tippst und wie du Antworten erhältst.

---

## Web UI

Eine browserbasierte Oberfläche, die vom Dispatcher lokal bereitgestellt wird. Kein separater Server notwendig — die Web UI ist im Daemon integriert und startet automatisch mit ihm.

**Zugriff:** `http://127.0.0.1:8080` (während der Dispatcher läuft)

**Was sie bietet:**
- Live-Nachrichtenfeed — alle Agenten-Gespräche in Echtzeit
- Eingabefeld — Nachrichten direkt aus dem Browser an den Relay-Agenten senden
- Konfigurationseditor (Modelle, Agenten, Anbieter, Scheduler)
- Memory-, Rules- und Skills-Viewer und -Editor
- Vault-Dateibrowser — Dateien in allen konfigurierten Vaults ansehen, bearbeiten und löschen
- Tags-Ansicht — `#Tags` scannen, umbenennen oder im gesamten Vault entfernen
- Scheduler — wiederkehrende Aufgaben verwalten, Verlauf anzeigen

**Konfiguration:** Standardmäßig aktiviert. Port und Host können in `config.json` geändert werden:

```json
"webui": { "host": "127.0.0.1", "port": 8080 }
```

**Remote-Zugriff:** Die UI bindet nur an localhost. Um von einem anderen Rechner darauf zuzugreifen, SSH-Port-Weiterleitung verwenden:

```bash
ssh -L 8080:localhost:8080 user@dein-server
```

Dann `http://localhost:8080` im lokalen Browser öffnen. Der Tunnel bleibt aktiv, solange die SSH-Verbindung besteht.

Eine vollständige Beschreibung aller Ansichten und API-Endpunkte findet sich unter [Web UI](../implementation/webui.md).

---

## CLI

Kommandozeilen-Interface zum Senden von Nachrichten und Verwalten des Daemons. Nach der Installation als `outheis` verfügbar.

**Einrichtung:** Verfügbar nach `pip install -e .` mit aktiver venv.

**Nachrichten senden:**

```bash
outheis send "Was steht heute an?"
outheis send "@zeno suche Notizen zu Projekt Alpha"
outheis chat                                         # interaktiver Modus mit Verlauf
```

Der Relay-Agent verarbeitet alle Nachrichten und leitet sie automatisch an den richtigen Agenten weiter. Mit `@name` kann ein Agent direkt angesprochen werden (`@zeno`, `@cato`, `@alan`, …).

**Daemon-Steuerung:**

```bash
outheis start         # im Hintergrund starten
outheis start -f      # im Vordergrund starten
outheis start -fv     # Vordergrund + verbose (zeigt Tool-Calls)
outheis stop          # Daemon stoppen
outheis status        # PID, Uptime, Agenten-Status anzeigen
```

**Memory und Rules einsehen:**

```bash
outheis memory              # alle gespeicherten Erinnerungen anzeigen
outheis memory --type user  # nur Benutzer-Facts anzeigen
outheis rules               # alle Regeln anzeigen (System + Benutzer)
outheis rules relay         # Regeln eines bestimmten Agenten anzeigen
```

---

## Signal

Nachrichten über die Signal-Messenger-App empfangen und senden. Erfordert eine dedizierte Telefonnummer für den Bot und installiertes sowie registriertes `signal-cli`.

**Funktionsweise:** Der Signal-Transport läuft als separater Prozess neben dem Daemon. Er hört auf eingehende Signal-Nachrichten von autorisierten Nummern, leitet sie an den Relay-Agenten weiter und sendet die Antworten als Signal-Nachrichten zurück. Sprachnachrichten werden automatisch transkribiert, wenn `faster-whisper` installiert ist.

**Voraussetzungen:**
- Eine bei `signal-cli` registrierte Telefonnummer für den Bot
- `signal-cli` installiert und konfiguriert
- `pip install -e ".[signal]"` für Sprachtranskription (optional)

**Konfiguration:**

```json
"signal": {
  "enabled": true,
  "bot_name": "Ou",
  "bot_phone": "+49...",
  "allowed": []
}
```

`allowed` ist eine Whitelist von Telefonnummern, die mit dem Bot interagieren dürfen. Eine leere Liste bedeutet, dass nur `human.phone` Nachrichten senden kann.

**Starten:**

```bash
outheis signal        # Vordergrund
outheis signal -v     # verbose
```

Signal-Transport und Haupt-Daemon laufen unabhängig voneinander und können gleichzeitig aktiv sein.

**Wann verwenden:** Der primäre Kanal, wenn du vom Handy mit outheis interagieren möchtest, ohne einen Browser oder ein Terminal zu öffnen.

Vollständige Einrichtungsanleitung: [Signal](../implementation/signal.md).
