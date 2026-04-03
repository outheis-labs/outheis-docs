---
title: Signal
---

# Signal

*Signal Messenger Transport über signal-cli JSON-RPC.*

## Überblick

Der Signal-Transport verbindet outheis mit Signal Messenger. Er läuft als eigenständiger Prozess (`outheis signal`), getrennt vom Haupt-Daemon. Er empfängt Nachrichten von Signal, leitet sie an relay weiter und sendet Antworten zurück.

Zugrundeliegender Mechanismus: signal-cli im `--json-rpc`-Modus, kommuniziert über stdin/stdout.

## Architektur

Das zentrale Design ist ein **dedizierter Leser-Thread**, der den gesamten stdout von signal-cli besitzt. Dies löst eine Race Condition, die entsteht, wenn Senden und Empfangen beide versuchen, vom selben Subprozess-stdout zu lesen.

```
signal-cli (jsonRpc)
     │
     ▼
 _read_loop() thread
     ├── receive events → Queue (for incoming messages)
     └── RPC responses → dict + Event (for send confirmations)

Main thread: read_message() ← Queue.get()
Send path:  _send_request() → stdin write → Event.wait()
```

### Klassen

- `SignalRPC` — `transport/signal_rpc.py`: verwaltet den signal-cli-Subprozess, Leser-Thread, Sende-/Empfangs-Primitiven
- `SignalTransport` — `transport/signal.py`: Nachrichten-Schleife, Autorisierung, Watcher-Thread, Markdown-Entfernung

### Nebenläufigkeitsmodell

| Komponente | Mechanismus |
|------------|-------------|
| Eingehende Nachrichten | `_receive_queue` — `Queue.get()` blockiert bis eine Nachricht eintrifft |
| RPC-Antworten (Sendebestätigungen) | `_response_map` + `threading.Event` pro Anfrage-ID |
| Stdin-Schreibvorgänge | `_stdin_lock` — verhindert verschachtelte Schreibvorgänge |

Der Leser-Thread ist der einzige Konsument von signal-cli stdout. Sonst liest nichts davon.

## Nachrichtenfluss

1. signal-cli gibt ein Empfangsereignis auf stdout aus
2. `_read_loop` parst das JSON und legt es in `_receive_queue`
3. `read_message()` gibt die geparste `SignalMessage` zurück
4. `SignalTransport._handle_message()` prüft Autorisierung, erstellt eine Benutzernachricht, hängt an `messages.jsonl` an
5. Ein Watcher-Thread (`_watch_responses`) fragt nach einer an `transport` adressierten Relay-Antwort
6. Wenn gefunden, ruft `send_message(sender_uuid, text)` über `_send_request()` auf

## Markdown-Entfernung

Vor dem Senden entfernt `_strip_markdown()` deterministisch Markdown-Syntax. Das ist ein Transport-Anliegen — das Modell gibt Inhalte unverändert zurück; die Entfernung geschieht hier.

| Eingabe | Ausgabe |
|---------|---------|
| `**bold**`, `__bold__` | Klartext |
| `*italic*`, `_italic_` | Klartext |
| `## Heading` | Überschriftentext ohne `#` |
| `` `inline code` `` | Code-Text |
| `- [ ]`, `- [x]` Checkboxen | Klartext |
| `- item`, `* item` Aufzählungen | Klartext |
| `---` horizontale Linie | `____________________` (20 Unterstriche) |

Der Ersatz für horizontale Linien erscheint in Signals UI als solide Trennlinie.

## Autorisierung

- `signal.allowed` in `config.json`: Whitelist von Telefonnummern, die Nachrichten senden dürfen
- `human.phone` ist unabhängig von der Whitelist immer erlaubt
- UUIDs werden beim ersten Kontakt gelernt und in `~/.outheis/human/signal.json` gespeichert
- Ersteinrichtung erfordert Vertrauen des Identitätsschlüssels über `signal-cli trust` (siehe Installationsanleitung)

Ein leeres `allowed`-Array bedeutet, dass nur `human.phone` mit dem Bot interagieren kann.

## Profilname

Beim Start wird der Signal-Profil-Anzeigename des Bots aus `config.signal.bot_name` über den `updateProfile`-RPC-Aufruf gesetzt. Das ist, was Signal-Kontakte als Namen des Bots sehen.

## Sprachtranskription

Wenn `faster-whisper` installiert ist, werden Sprachnachrichten vor der Weiterleitung an relay transkribiert. Das ist eine optionale Abhängigkeit — der Transport funktioniert ohne sie; Sprachnachrichten werden still übersprungen, wenn `faster-whisper` fehlt.

## Konfiguration

```json
{
  "signal": {
    "enabled": true,
    "bot_name": "Ou",
    "bot_phone": "+49...",
    "allowed": []
  }
}
```

| Schlüssel | Beschreibung |
|-----------|--------------|
| `enabled` | Signal-Transport aktivieren |
| `bot_name` | Anzeigename, der beim Start im Signal-Profil gesetzt wird |
| `bot_phone` | Die bei signal-cli registrierte Telefonnummer |
| `allowed` | Whitelist von Telefonnummern. Leer = nur human.phone |

## Ausführen

```bash
outheis signal        # foreground
outheis signal -v     # verbose (shows tool calls)
```

Signal-Transport läuft getrennt vom Haupt-Daemon. Beide können gleichzeitig laufen — der Daemon behandelt geplante Aufgaben und direkte CLI-Abfragen; der Signal-Transport behandelt eingehende Signal-Nachrichten.

## Dateiorte

```
src/outheis/transport/
├── signal.py        # SignalTransport: message loop, watcher, markdown stripping
└── signal_rpc.py    # SignalRPC: jsonRpc subprocess, reader thread, send/receive
```
