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

Nachrichten über die Signal-Messenger-App empfangen und senden. Der Bot läuft als separater Prozess neben dem Daemon — er hört auf eingehende Signal-Nachrichten, leitet sie an den Relay-Agenten weiter und sendet die Antworten zurück. Sprachnachrichten werden automatisch transkribiert, wenn `faster-whisper` installiert ist.

**Wann verwenden:** Der primäre Kanal, wenn du vom Handy mit outheis interagieren möchtest, ohne einen Browser oder ein Terminal zu öffnen.

### Was du brauchst

Eine dedizierte SIM-Karte mit einer Telefonnummer, die noch nicht bei Signal registriert ist. Diese Nummer wird zur Identität des Bots — es sollte nicht deine persönliche Nummer sein. Eine Prepaid-SIM reicht aus; die Nummer muss nur einmalig während der Registrierung per SMS oder Anruf erreichbar sein.

### 1. signal-cli installieren

signal-cli benötigt Java 17+. Zuerst prüfen ob vorhanden (`java -version`), ggf. installieren.

**macOS (Homebrew):**

```bash
brew install signal-cli
```

**Linux / manuell:**

Neuestes Release herunterladen von [github.com/AsamK/signal-cli/releases](https://github.com/AsamK/signal-cli/releases). Archiv entpacken und das `signal-cli`-Binary in einen Pfad legen, der in `$PATH` ist (z. B. `/usr/local/bin/signal-cli`).

Überprüfen:

```bash
signal-cli --version
```

### 2. Bot-Nummer registrieren

`+49...` überall durch die Bot-Telefonnummer im internationalen Format ersetzen.

```bash
signal-cli -a +49... register
```

Signal sendet einen Bestätigungscode per SMS an die Nummer. Falls SMS nicht verfügbar ist, alternativ einen Anruf anfordern:

```bash
signal-cli -a +49... register --voice
```

Mit dem erhaltenen Code bestätigen:

```bash
signal-cli -a +49... verify 123-456
```

Das Konto ist jetzt registriert. signal-cli speichert die Zugangsdaten unter `~/.local/share/signal-cli/`.

### 3. Eigene Nummer vertrauen

Bevor der Bot Nachrichten mit deinem persönlichen Signal-Konto austauschen kann, muss die Sicherheitsnummer einmalig bestätigt werden:

```bash
signal-cli -a +49... trust -v <sicherheitsnummer> +49DEINE_PERSÖNLICHE_NUMMER
```

Die Sicherheitsnummer ermitteln:

```bash
signal-cli -a +49... listIdentities
```

Alternativ zuerst eine Testnachricht senden — signal-cli gibt dann eine Warnung wegen nicht vertrauenswürdiger Identität aus, die die Sicherheitsnummer enthält.

### 4. outheis konfigurieren

Signal-Abschnitt in `~/.outheis/human/config.json` eintragen:

```json
"signal": {
  "enabled": true,
  "bot_name": "Ou",
  "bot_phone": "+49...",
  "allowed": []
}
```

`bot_phone` auf die registrierte Bot-Nummer setzen. `bot_name` ist der Anzeigename, den Signal-Kontakte sehen. `allowed` ist eine Whitelist erlaubter Telefonnummern — eine leere Liste bedeutet, dass nur `human.phone` (aus dem `human`-Abschnitt) Nachrichten senden kann.

`human.phone` im Config auf die eigene persönliche Nummer setzen:

```json
"human": {
  "phone": "+49DEINE_PERSÖNLICHE_NUMMER",
  ...
}
```

### 5. Optional: Sprachtranskription

Um eingehende Sprachnachrichten vor der Weiterleitung an den Relay-Agenten zu transkribieren:

```bash
pip install -e ".[signal]"
```

Installiert `faster-whisper`. Ohne diese Abhängigkeit funktioniert der Transport weiterhin; Sprachnachrichten werden stillschweigend übersprungen.

### 6. Starten

```bash
outheis signal        # Vordergrund
outheis signal -v     # verbose (zeigt Tool-Calls)
```

Signal-Transport und Haupt-Daemon laufen unabhängig voneinander. Zuerst den Daemon starten (`outheis start`), dann den Signal-Transport in einem separaten Terminal oder als Hintergrundprozess.

Details zur internen Architektur: [Signal](../implementation/signal.md).
