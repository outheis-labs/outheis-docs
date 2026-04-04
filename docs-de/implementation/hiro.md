---
title: Hiro
---

# Hiro

*Action-Agent — noch nicht implementiert.*

## Was hiro tut

hiro ist der Action-Agent von outheis. Während zeno den Vault durchsucht und cato die Zeit verwaltet, handelt hiro in der Außenwelt: E-Mails versenden, Kalender aktualisieren, externe Dienste auslösen.

**hiro ist in der aktuellen Version vorhanden, hat aber keine Fähigkeiten.** Der Agent startet, routet Nachrichten und antwortet — aber es existiert noch keine externe Integration. Das Aktivieren in `config.json` hat derzeit keine praktische Wirkung.

## Geplante Architektur

hiro wird als **MCP-Client** gebaut. Statt Integrationen direkt in outheis zu implementieren, verbindet sich hiro mit externen MCP-Servern — einen pro Dienst — und stellt deren Tools über die Standard-Agenten-Schnittstelle bereit.

### Warum MCP

Das Model Context Protocol bietet eine standardisierte Schnittstelle zwischen LLMs und externen Tools. Das MCP-Ökosystem deckt viele gängige Integrationen bereits ab (E-Mail, Kalender, Browser, Shell). hiro als MCP-Client zu bauen bedeutet:

- Kein Integrationscode lebt in outheis selbst
- Neue Fähigkeiten werden durch das Konfigurieren eines Servers hinzugefügt, nicht durch das Schreiben von Code
- Jeder Server läuft als isolierter Prozess mit eigenen Berechtigungen

### Server-Lifecycle

MCP-Server laufen als Subprozesse, die vom Dispatcher verwaltet werden. hiro verwaltet den Server-Lifecycle nicht selbst — der Dispatcher startet konfigurierte Server beim Launch, überwacht sie und startet sie bei Bedarf neu. hiro verbindet sich mit bereits laufenden Servern.

Zwei Modi sind geplant:

| Modus | Verhalten |
|-------|-----------|
| Persistent | Server läuft kontinuierlich neben dem Dispatcher |
| On-demand | Server wird gestartet, wenn hiro ihn benötigt, und nach einem konfigurierbaren Idle-Timeout gestoppt |

### Kuratierte Server-Liste

hiro akzeptiert keine beliebigen MCP-Server-Konfigurationen. Unterstützte Server werden in einer kuratierten Liste geführt, die festhält, welcher Server getestet wurde, gegen welche Version und wann. Ein Server erscheint auf der Liste erst, nachdem er verifiziert wurde.

Das ist eine bewusste Einschränkung. Das MCP-Ökosystem ist groß und uneinheitlich — die Qualität variiert erheblich. Ein Whitelist-Ansatz bedeutet, dass bekannt ist, was hiro kann, und dass es funktioniert.

Die Liste wird im outheis-Repository gepflegt und aktualisiert, wenn Server getestet werden.

### Konfiguration

Wenn implementiert, werden hiros Server in `config.json` konfiguriert:

```json
{
  "agents": {
    "action": {
      "enabled": true,
      "servers": [
        {"name": "gmail",  "command": "npx", "args": ["-y", "@modelcontextprotocol/server-gmail"]},
        {"name": "gcal",   "command": "npx", "args": ["-y", "@modelcontextprotocol/server-gcal"]}
      ]
    }
  }
}
```

Nur Server auf der kuratierten Liste werden akzeptiert. Unbekannte Server werden beim Start ignoriert und mit einer Warnung protokolliert.

## Aktueller Stand

| Komponente | Status |
|------------|--------|
| Agent-Shell (Routing, Dispatch) | ✓ vorhanden |
| MCP-Client | nicht implementiert |
| Server-Lifecycle-Verwaltung | nicht implementiert |
| Kuratierte Server-Liste | nicht begonnen |
| Externe Integrationen | nicht implementiert |
