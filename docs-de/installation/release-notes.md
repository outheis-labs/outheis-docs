---
title: Versionshinweise
---

# Versionshinweise

*Private Beta — April 2026.*

---

## Was funktioniert

| Komponente | Status | Hinweise |
|------------|--------|---------|
| Dispatcher — Microkernel, Scheduler, Lock-Manager | ✓ | |
| Relay (ou) — Routing, Memory-Integration | ✓ | |
| Data (zeno) — Vault-Suche, Tag-Analyse | ✓ | |
| Agenda (cato) — Daily, Inbox, Exchange, Shadow | ✓ | |
| Pattern (rumi) — nächtliche Memory-Extraktion | ✓ | |
| Web UI — Konfig, Memory, Scheduler, Vault, Tags, Migration | ✓ | |
| Signal-Transport — empfangen, antworten, Sprachtranskription | ✓ | |
| Vault-Datei-Browser — alle Dateitypen, Bilder, Obsidian-Wikilinks | ✓ | |
| Tags — scannen, Namensraum-Gruppierung, umbenennen, löschen | ✓ | |
| Migration — Exchange.md-Genehmigungsworkflow | ✓ | |

## Was nicht funktioniert

| Komponente | Status | Hinweise |
|------------|--------|---------|
| Action (hiro) — externe Aufgaben, E-Mail, Kalender | nicht implementiert | Framework vorhanden, keine Fähigkeiten |
| Code (alan) — Codebase-Introspektion | nur Entwicklung | In Produktion deaktiviert |

**hiro ist vorhanden, aber leer.** Der Agent startet und leitet weiter, aber keine externen Integrationen existieren — keine E-Mail, kein Kalender, keine Shell-Ausführung. ihn in config.json zu aktivieren hat noch keine praktische Auswirkung.

**alan erfordert manuelle Aktivierung.** Der Code-Agent bietet Introspektion in die outheis-Codebasis — nützlich für jeden, der erkunden möchte, wie es funktioniert, oder sich den Code erklären lassen möchte. In `config.json` aktivieren unter `agents.code.enabled: true`.

## Bekannte Lücken

**Pattern-Agent benötigt Verlauf.** rumi hat bei einer frischen Installation nichts zu extrahieren. Memory baut sich über Tage auf, nicht sofort.

**Tag-Scan ist auf Anfrage.** Tags werden nicht beim Start indexiert. Über Web UI ausführen (Vault → Tags → Scan) oder im Chat `analyze tags` sagen.

**Keine mobile UI.** Web-Oberfläche ist nur localhost. Signal-Transport für mobilen Zugriff verwenden.

**Kontext nach Neustart.** Beim Neustart gibt relay die letzten 20 Nachrichten zurück, um den aktuellen Kontext wiederherzustellen. Älterer Gesprächsverlauf wird nicht zurückgespielt.
