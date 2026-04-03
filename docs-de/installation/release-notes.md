---
title: Release Notes
---

# Release Notes

*Private Beta — April 2026.*

---

## Was funktioniert

| Komponente | Status | Hinweise |
|-----------|--------|-------|
| Dispatcher — Microkernel, Scheduler, Lock Manager | ✓ | |
| relay (ou) — Routing, Memory-Integration | ✓ | |
| data (zeno) — vault-Suche, Tag-Analyse | ✓ | |
| agenda (cato) — Daily, Inbox, Exchange, Shadow | ✓ | |
| pattern (rumi) — nächtliche Memory-Extraktion | ✓ | |
| Web UI — Config, Memory, Scheduler, vault, Tags, Migration | ✓ | |
| Signal-Transport — Empfangen, Antworten, Sprachtranskription | ✓ | |
| vault-Datei-Browser — alle Dateitypen, Bilder, Obsidian-Wikilinks | ✓ | |
| Tags — Scannen, Namespace-Gruppierung, Umbenennen, Löschen | ✓ | |
| Migration — Exchange.md-Genehmigungsworkflow | ✓ | |

## Was nicht funktioniert

| Komponente | Status | Hinweise |
|-----------|--------|-------|
| action (hiro) — externe Aufgaben, E-Mail, Kalender | nicht implementiert | Framework vorhanden, keine Fähigkeiten |
| code (alan) — Codebase-Introspektion | nur Entwicklung | In Produktion deaktiviert |

**hiro ist vorhanden, aber leer.** Der agent startet und routet, aber keine externen Integrationen existieren — keine E-Mail, kein Kalender, keine Shell-Ausführung. Das Aktivieren in config.json hat derzeit keine praktische Wirkung.

**alan erfordert manuelle Aktivierung.** Der code-agent bietet Introspektion in die outheis-Codebase — nützlich für alle, die erkunden möchten, wie sie funktioniert oder den Code erklärt haben möchten. In `config.json` unter `agents.code.enabled: true` aktivieren.

## Bekannte Lücken

**pattern-agent benötigt Verlauf.** rumi hat bei einer frischen Installation nichts zu extrahieren. Memory baut sich über Tage auf, nicht sofort.

**Tag-Scan erfolgt auf Anfrage.** Tags werden beim Start nicht indiziert. Aus der Web UI ausführen (vault → Tags → Scan) oder im Chat `analyze tags` sagen.

**Keine mobile UI.** Web UI ist nur für localhost. Signal-Transport für mobilen Zugriff verwenden.

**Kontext nach Neustart.** Beim Neustart wiederholt relay die letzten 20 Nachrichten, um den kürzlichen Kontext wiederherzustellen. Älterer Gesprächsverlauf wird nicht wiedergegeben.
