---
title: Alan
---

# Alan

*Code-Intelligenz für Entwicklungsumgebungen.*

## Was alan tut

alan ist outheis' Code-Agent. Er liest lokal verfügbaren Quellcode, beantwortet Fragen zur Implementierung und schlägt Verbesserungen über einen strukturierten Review-Workflow vor.

**alan ist ein reiner Entwicklungs-Agent. Er ist in Produktionsumgebungen niemals aktiv.**

## Der Codebase-Workflow

alan stellt alle Vorschläge in `vault/Codebase/` bereit, in Anlehnung an das von catos `vault/Agenda/` etablierte Muster:

```
vault/Codebase/
├── Exchange.md          # proposals for review
└── <staged files>       # modified files or diffs for context
```

### Exchange.md

Jeder Vorschlag von alan ist ein Eintrag in `vault/Codebase/Exchange.md`:

```markdown
## 2026-04-01 — Beschreibung des Vorschlags

**Type:** refactor | bugfix | improvement | answer
**Files:** src/outheis/agents/data.py
**Status:** proposed | approved | rejected | discussing

### Summary
Was wird vorgeschlagen und warum.

### Proposed Change
Verweis auf staged file oder inline diff.

### Discussion
(Deine Antworten und Rückfragen kommen hier hin)
```

Du antwortest unter "Discussion", genehmigst oder lehnst mit einem Schlüsselwort ab (`approved`, `rejected`), und alan nimmt die Entscheidung beim nächsten Lauf auf.

### Bereitgestellte Dateien

Für nicht-triviale Änderungen schreibt alan die geänderte Datei in `vault/Codebase/<dateiname>` neben den Exchange.md-Eintrag. Überprüfe den Diff und antworte dann in Exchange.md.

## Verantwortlichkeiten

### Code-Introspektion

Fragen zur Implementierung von outheis beantworten. Beispiele:

- "Wie funktioniert der Dispatcher?"
- "Wo wird memory.json geschrieben?"
- "Was passiert wenn ich `@zeno` verwende?"

alan liest Quelldateien, verfolgt Aufrufpfade und erklärt die Logik — ohne Änderungen vorzunehmen.

### Verbesserungsvorschläge

Auf Anfragen reagieren oder proaktiv identifizieren:

- Refactoring-Möglichkeiten
- Bug-Fixes
- Inkonsistenzen zwischen Dokumentation und Implementierung

Alle Vorschläge gehen durch Exchange.md. alan modifiziert `src/` nie direkt.

### Code-Suche

Implementierungen, Muster und Referenzen im lokalen Codebase finden:

- "Zeig mir alle Stellen wo Vault-Dateien gelesen werden"
- "Welcher Agent ist für Scheduling zuständig?"
- "Wie ist das Tool `append_file` implementiert?"

## Tools

| Tool | Zweck |
|------|-------|
| `read_file(path)` | Beliebige lokale Quelldatei lesen |
| `search_code(query, path)` | Nach Mustern, Funktionsnamen, Bezeichnern suchen |
| `list_files(path)` | Verzeichnisstruktur erkunden |
| `write_vault(path, content)` | Nur in `vault/Codebase/` schreiben |
| `append_vault(path, content)` | An Exchange.md anhängen |
| `load_skill(topic)` | alan-spezifische Skills bei Bedarf laden |

alan hat **Lesezugriff** auf jeden lokalen Pfad. **Schreibzugriff ist auf `vault/Codebase/` beschränkt.**

## Kontext beim Start

alan erhält beim Aufruf:

- Einen Code-Index des Ziel-Repositories (Dateibaum + kurze Beschreibungen)
- Aktuellen Inhalt von `vault/Codebase/Exchange.md`
- Skills aus `agents/skills/code.md`

Bei großen Repositories werden vollständige Dateiinhalte auf Anfrage über `read_file` abgerufen — der Index dient zur Orientierung.

## alan ansprechen

Direkt aufrufen:

```
@alan wie ist der Dispatcher implementiert?
@alan schlage eine Verbesserung für die Vault-Suche vor
```

Oder natürlich im Chat — ou erkennt code-bezogene Fragen und delegiert automatisch an alan.

## Verfügbarkeit

alan wird im Dispatcher nur registriert, wenn `config.json` enthält:

```json
{
  "agents": {
    "code": {
      "name": "alan",
      "model": "capable",
      "enabled": true
    }
  }
}
```

Hinweis: Der Konfig-Schlüssel ist `code` (Funktionsname), der Anzeigename ist `alan` (Persona).

Produktions-Deployments lassen diesen Eintrag weg. alan wird nie standardmäßig geladen.

## Konfiguration

| Einstellung | Standard | Beschreibung |
|-------------|---------|--------------|
| `enabled` | false | Muss explizit aktiviert werden |
| `model` | capable | Leistungsfähiges Modell verwenden — Code-Verständnis profitiert davon |

## Speicherung

```
vault/Codebase/
├── Exchange.md           # Open proposals and decisions
└── <staged files>        # Proposed changes awaiting review
```

## Integration mit anderen Agenten

**Relay (ou)** erkennt Code-Fragen und delegiert an alan. Leitet das `@alan`-Präfix direkt weiter.

**Data-Agent (zeno)** behandelt Vault und persönliche Daten. alan behandelt Quellcode. Die Domänen überschneiden sich nicht.

**Pattern-Agent (rumi)** kann alans Vorschlagshistorie beobachten und Muster extrahieren — z. B. können wiederkehrende Refactoring-Vorschläge auf ein tieferes strukturelles Problem hinweisen, das erwähnenswert ist.

## Design-Anmerkungen

- Das `vault/Codebase/Exchange.md`-Muster ist bewusst parallel zu `vault/Agenda/Exchange.md`. Das Interaktionsmodell ist dasselbe: outheis schlägt vor, du entscheidest.

- Schreibzugriff auf `vault/Codebase/` wird auf Tool-Ebene erzwungen, nicht nur durch Prompt-Anweisung.
- alan ist absichtlich aus der Produktion ausgeschlossen. Code-Introspektion und Vorschlags-Workflows sind Entwicklungsbelange.
