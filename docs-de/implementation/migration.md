---
title: Migration
---

# Migration

*Wie du bestehendes Wissen in outheis bringst.*

## Überblick

outheis lernt durch:
1. **Direkte Interaktion** — Gespräche mit dir
2. **Muster-Extraktion** — Pattern-Agent beobachtet und fördert Rules
3. **Manuelle Migration** — Bestehendes Wissen über den Vault importieren

Diese Anleitung behandelt Option 3: Daten von Claude.ai oder anderen Quellen migrieren.

## Das Migrationsverzeichnis

Platziere zu migrierende Dateien in deinem Vault:

```
vault/Migration/
├── claude-export.json    # Your data
├── preferences.md        # Your rules/preferences
└── data.md               # Rules for Data agent
```

Dieses Verzeichnis ist **temporär** — erstelle es, wenn du etwas zu migrieren hast, lösche es wenn fertig.

## Chat-Befehle

Alle Migration geschieht durch natürliches Gespräch:

| Du sagst | Was passiert |
|----------|-------------|
| "memory migrate" | Migration/-Dateien parsen, Kandidaten in Exchange.md schreiben |
| "migriere memory" | Dasselbe, auf Deutsch |
| "memory traits" | Aktuellen Memory und Rules anzeigen |
| "zeige traits" | Dasselbe, auf Deutsch |
| "was weißt du über mich" | Dasselbe, umgangssprachlich |
| "schreibe regel: ..." | Rule direkt hinzufügen, Pattern-Agent umgehen |

Keine CLI-Befehle nötig. Einfach mit outheis sprechen.

## Dateiformate

### JSON-Dateien

```json
{
  "entries": [
    {
      "content": "User arbeitet bei senswork",
      "type": "user"
    },
    {
      "content": "Antworte knapp und direkt",
      "type": "feedback"
    },
    {
      "content": "Arbeitet gerade an outheis",
      "type": "context"
    }
  ]
}
```

**Typen:**
- `user` — Fakten über dich (dauerhaft)
- `feedback` — Wie du möchtest, dass outheis sich verhält (dauerhaft)
- `context` — Aktueller Fokus (zerfällt nach 14 Tagen)

Wenn `type` fehlt, erschließt outheis ihn aus dem Inhalt.

### Markdown-Dateien

```markdown
# Preferences

## user
- Lebt in München
- Arbeitet als Software-Entwickler

## feedback
- Antworte immer auf Deutsch
- Bevorzuge kurze Antworten

## rule:agenda
- MAX 10 Items in Daily.md
- Keine Meetings vor 10 Uhr

## rule:data
- Durchsuche auch PDF-Dateien
```

Abschnitte entsprechen Memory-Typen oder Rules:
- `## user`, `## feedback`, `## context` → Memory
- `## rule:agenda`, `## rule:data`, `## rule:relay` → Rules-Dateien

Jede Markdown- oder JSON-Struktur ist akzeptabel — outheis verwendet LLM-Parsing und erfordert kein bestimmtes Schema.

## Workflow

### 1. Migrationsverzeichnis erstellen

```bash
mkdir ~/Documents/Vault/Migration
```

### 2. Deine Dateien hinzufügen

Kopiere deine Daten:
- Export von Claude.ai → `claude-export.json`
- Deine Präferenzen → `preferences.md`
- Agenten-spezifische Rules → `agenda.md`, `data.md`

### 3. "memory migrate" sagen

outheis parst alle Dateien in `vault/Migration/`, dedupliziert Kandidaten gegen bestehendes Memory via LLM und schreibt konsolidierte Einträge als Block in `vault/Agenda/Exchange.md`:

```
<!-- outheis:migration:start -->
## Migration-Vorschläge

*2026-04-03 14:30 — Bitte prüfen und markieren:*
*`[x]` übernehmen · `[-]` ablehnen · `[ ]` offen lassen*
*Anschließend: `memory migrate` erneut ausführen.*

- [ ] Works as Director Innovation Lab [user]
- [ ] Prefers short, direct answers [feedback]
- [ ] Respond in German [rule:relay]

<!-- outheis:migration:end -->
```

Duplikate sind immer zu erwarten — der LLM-Deduplizierungsschritt behandelt sie. Nur neue oder eigenständige Einträge erscheinen im Block.

### 4. Exchange.md prüfen

Öffne `vault/Agenda/Exchange.md` — dieselbe Datei, die du bereits für asynchrone Kommunikation mit outheis nutzt. Der Migrationsblock erscheint oben oder eingebettet, klar abgegrenzt.

Markiere jeden Eintrag:

```
- [x] Works as Director Innovation Lab [user]
- [x] Prefers short, direct answers [feedback]
- [-] Respond in German [rule:relay]
- [ ] Lebt in München [user]
```

- `[x]` — auf Memory/Rules anwenden
- `[-]` — verwerfen
- `[ ]` — für nächste Runde offen lassen

Cato (Agenda-Agent) ignoriert den Migrationsblock bei der Verarbeitung von Exchange.md.

### 5. Erneut "memory migrate" sagen

```
Du: memory migrate
Ou: Migration verarbeitet:
    - 2 übernommen
    - 1 abgelehnt
    - 1 noch offen
```

- `[x]`-Einträge werden in Memory und Rules geschrieben
- `[-]`-Einträge werden verworfen
- `[ ]`-Einträge verbleiben im Block für die nächste Runde
- Der Block wird aus Exchange.md entfernt, sobald alle Einträge aufgelöst sind (oder auf deine Anfrage)

### 6. Verarbeitete Quelldateien

Nach dem Parsen erhalten Quelldateien in `vault/Migration/` ein `x-`-Präfix:

```
vault/Migration/
├── x-claude-export.json    # Processed
├── x-preferences.md        # Processed
```

Das verhindert erneutes Verarbeiten. Lösche die `x-`-Dateien selbst, wenn bereit, oder nutze die WebUI-Migrationsansicht.

## WebUI-Migrationsansicht

Die Migrationsansicht in der Web-Oberfläche bietet:
- Vollständige Liste der Dateien in `vault/Migration/`
- Jede Datei direkt ansehen und bearbeiten
- Drop-Zone zum Hochladen neuer Migrationsdateien

Verwende sie, um Dateien hinzuzufügen ohne den Browser zu verlassen, oder um zu prüfen, was bereits verarbeitet wurde.

## Direkte Rule-Eingabe

Um eine Rule sofort ohne den Migrations-Workflow hinzuzufügen:

```
Du: schreibe regel: antworte immer auf Deutsch
Ou: ✓ Regel hinzugefügt zu relay: antworte immer auf Deutsch
```

Oder den Agenten angeben:

```
Du: schreibe regel für agenda: keine Meetings vor 10 Uhr
Ou: ✓ Regel hinzugefügt zu agenda: keine Meetings vor 10 Uhr
```

Das umgeht Pattern-Agent und schreibt direkt in `~/.outheis/human/rules/{agent}.md`.

## Aktuellen Zustand ansehen

Um zu sehen, was outheis weiß:

```
Du: memory traits

Ou: Erkannte Eigenschaften:

    ## Identität
      • User arbeitet bei senswork
      • User lebt in München

    ## Präferenzen
      • Antworte knapp und direkt
      • Bevorzuge deutsche Sprache

    ## Etablierte Regeln
      • agenda: 2 Regeln
      • relay: 1 Regel
```

Oder umgangssprachlicher:

```
Du: was weißt du über mich?
```

## Memory vs. Rules

| Aspekt | Memory | Rules |
|--------|--------|-------|
| Ort | `~/.outheis/human/memory/` | `~/.outheis/human/rules/` |
| Format | JSON | Markdown |
| Flüchtigkeit | Kann sich ändern, Kontext zerfällt | Stabil einmal gesetzt |
| Beispiel | "User ist 35" | "Antworte auf Deutsch" |

Memory = "was ich über dich weiß"
Rules = "wie ich mich verhalten soll"

Beide werden durch Migration oder laufende Gespräche befüllt.

## Datenschutz

Alle Daten bleiben lokal:
- Migrationsdateien sind in deinem Vault
- Memory ist in `~/.outheis/human/memory/`
- Rules sind in `~/.outheis/human/rules/`
- Nichts wird extern übertragen

Lösche jede Datei jederzeit — outheis passt sich dem an, was verbleibt.
