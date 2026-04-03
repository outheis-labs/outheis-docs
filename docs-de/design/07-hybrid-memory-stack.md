# Der hybride Memory-Stack: Wo Code endet und das LLM beginnt

## Das Problem mit reinen Ansätzen

Zwei Versagensmuster definieren den Designraum für adaptive KI-Systeme.

**Reiner Code** kann nicht lernen. Schlüsselwortlisten, Regex-Muster, fest kodierte Klassifikatoren, Icon-Mappings, Format-Detektoren — diese kodieren das heutige Verständnis und sperren es gleichzeitig ein. Wenn der Benutzer etwas anders formuliert, in einer anderen Sprache schreibt oder ein unerwartetes Format verwendet, schlägt die Heuristik still fehl oder liefert falsche Ergebnisse. Weitere Verzweigungen hinzuzufügen, um Randfälle zu behandeln, ist kein Lernen; es ist das Ansammeln technischer Schulden, die schneller wachsen, als das System sich verbessert.

**Reines LLM** skaliert nicht. Jede Entscheidung an ein Sprachmodell zu delegieren — einschließlich Entscheidungen, die deterministisch getroffen werden könnten — ist teuer, langsam, unvorhersehbar und undurchsichtig. Es bedeutet auch keine stabilen Garantien: Dieselbe Datei könnte bei zwei aufeinanderfolgenden Läufen unterschiedlich klassifiziert werden.

Die richtige Position liegt zwischen diesen Polen, und die Grenze ist scharf.

---

## Die Grenze

**Code behandelt Struktur** — Dinge, die eindeutig, deterministisch und inhaltsunabhängig sind:

- Dateisystemoperationen (lesen, schreiben, umbenennen, atomares Schreiben über temp+rename)
- Nachrichtenaustausch zwischen Agenten (Warteschlange, Dispatcher, Routing)
- Planung (wann Aufgaben laufen, Zeitstempel, Deadlines)
- Persistenz (Memory-Store, Suchindex, Cache)
- Schema-Validierung (korrektes JSON-Format, Pflichtfelder, gültige Typen)
- Tool-Implementierungen (was `read_file` tut — nicht was es bedeutet)

Diese Dinge ändern sich nicht, weil der Benutzer etwas anders formuliert hat. Ihre Korrektheit ist durch Tests überprüfbar, unabhängig von Sprache, Kontext oder Präferenz.

**Das LLM behandelt Bedeutung** — Dinge, die von Kontext, Sprache, Präferenz und implizitem Wissen abhängen:

- Klassifizierung (welcher Typ ist dieser Eintrag — user, feedback, context?)
- Muster- und Widerspruchserkennung über Beobachtungen hinweg
- Entscheidung, welche Aktion angesichts der aktuellen Situation angemessen ist
- Formatierung gemäß den beobachteten Präferenzen des Benutzers
- Strukturiertes Wissen aus Freitext extrahieren (Dateien, Nachrichten, Notizen)
- Konflikte, Prioritäten und Relevanz beurteilen

Kein statischer Algorithmus kann subtile Muster in natürlicher Sprache über Sitzungen und Sprachen hinweg erkennen. Ein Sprachmodell kann es — und es wird besser darin, je mehr Skills und Memory das System destilliert hat.

---

## Die Memory-Hierarchie als hybrider Stack

outheis implementiert dieses Prinzip als Drei-Schichten-Stack:

```
┌──────────────────────────────────────────┐
│              SKILLS                       │  highest density
│   condensed principles that direct        │  LLM writes, LLM reads
│   attention before processing begins     │  distilled from memory
└───────────────────┬──────────────────────┘
                    │ distillation
┌───────────────────┴──────────────────────┐
│              MEMORY                       │  medium density
│   observations, facts, corrections       │  LLM writes, LLM reads
│   raw material awaiting distillation     │  stored as JSON (code)
└───────────────────┬──────────────────────┘
                    │ promotion (rare)
┌───────────────────┴──────────────────────┐
│              RULES                        │  lowest density
│   stable constraints, hard boundaries    │  LLM writes, LLM reads
│   what must never happen                 │  persisted as Markdown (code)
└──────────────────────────────────────────┘
```

Jede Schicht wird:
- **Vom LLM geschrieben** (keine fest kodierte Extraktion, kein Schlüsselwort-Matching)
- **Vom LLM gelesen** (zur Laufzeit in System-Prompts injiziert)
- **Vom Code gespeichert** (JSON-Dateien, Markdown-Dateien — deterministisches I/O)
- **Vom Code verwaltet** (wann laden, wie validieren, wann ablaufen lassen)

Die Trennung ist strikt. Code entscheidet nie, was ein Memory-Eintrag bedeutet. Das LLM verwaltet nie Datei-Handles oder Transaktionssicherheit.

---

## Konsequenz für die Agenten-Architektur

Jeder Agent in outheis besteht aus genau zwei Schichten:

```
┌────────────────────────────────────────┐
│            LLM  (decides)              │
│  What to do? How to format? Why?       │
│  What type? What does this mean?       │
├────────────────────────────────────────┤
│         Tools  (infrastructure)         │
│  read_file, write_file, add_memory     │
│  append_rule, read_messages, done      │
└────────────────────────────────────────┘
```

Das LLM ruft Tools auf — nicht umgekehrt. Python orchestriert nicht, was das LLM tun soll. Python stellt bereit, was das LLM zum Handeln braucht.

Die Agentenschleife ist strukturell einheitlich über alle Agenten:

```python
while True:
    response = call_llm(system=context, messages=history, tools=tools)
    if no tool calls: return response.text
    results = [execute_tool(t) for t in response.tool_calls]
    history += [response, results]
```

Kontext wird vorab bereitgestellt (Memory, Skills, Rules, relevante Dateien). Tools sind reines I/O. Das LLM entscheidet Reihenfolge, Strategie und was mit Ergebnissen zu tun ist.

Das bedeutet: Eine feste Fünf-Schritte-Pipeline — extrahieren, konsolidieren, destillieren, promoten, validieren — ist eine Heuristik. Sie kodiert die heutige Annahme darüber, welche Schritte in welcher Reihenfolge benötigt werden. Ein tool-nutzendes Agenten mit Zugang zu Lese-/Schreib-Primitiven kann dies selbst entscheiden und wird mit wachsendem Memory und Skills bessere Entscheidungen treffen.

---

## Konkrete Grenzfälle

| Entscheidung | Falsch: Heuristik | Richtig: LLM |
|---|---|---|
| Welcher Memory-Typ ist das? | Schlüsselwort-Match auf "prefer", "always" | LLM erhält Inhalt und entscheidet |
| Was enthält diese JSON-Datei? | Format-Erkennung mit `isinstance()` | LLM liest Datei, extrahiert Bedeutung |
| Sind diese Einträge Duplikate? | Wortüberlappungs-Verhältnis-Schwellenwert | LLM vergleicht semantisch |
| Welches Icon/Emoji für diesen Typ? | Fest kodiertes `icon_map`-Dict | LLM formatiert frei |
| Wie soll diese Datei aussehen? | Fest kodierte Vorlage | LLM fragt einmal, passt sich an |
| Welcher Typ ist dieser Migrationseintrag? | Abschnittsüberschriften-Matching | LLM klassifiziert nach dem Lesen |

---

## Wann wird eine Heuristik zu Code?

Das LLM selbst erkennt, was über viele Aufrufe hinweg stabil bleibt. Erst wenn ein Muster klar und konsistent stabil ist, sollte es kodiert werden — nicht vorher.

Der Pattern-Agent beobachtet, welche Entscheidungen konsistent sind, und kann diese als Skills formulieren (die zukünftige Aufmerksamkeit lenken) oder sie dem Entwickler als Implementierungskandidaten melden. Das ist der organische Wachstumspfad:

**Code wächst von unten nach oben aus beobachteter Stabilität, nicht von oben nach unten aus antizipierten Anforderungen.**

Das verhindert vorzeitige Optimierung und hält das System flexibel. Eine outheis-Instanz, die ein Jahr lang läuft, hat mehr Code als eine frische Installation — aber jedes Code-Stück entstand aus Daten, nicht aus Spekulation.

---

## Der Destillationsgradient

Der hybride Stack erzeugt einen kontinuierlichen Gradienten von der rohen Beobachtung zum stabilen Prinzip:

```
User interaction
     ↓
Memory (LLM extracts what's worth keeping)
     ↓
Pattern agent consolidates (LLM merges, deduplicates, resolves)
     ↓
Skills (LLM distills patterns into principles)
     ↓
Rules (LLM promotes stable constraints)
     ↓
Code (developer promotes stable behavior)
```

Jeder Übergang ist ein Kompressionsschritt. Rohe Beobachtungen werden zu strukturiertem Memory. Memory wird zu kondensierten Skills. Skills werden zu harten Rules. Wiederholte Rules werden zu Code. Auf jeder Ebene führt das LLM die Klassifizierung durch; Code übernimmt die Persistenz.

Das Ziel ist ein System, das mit der Zeit progressiv weniger Kontext benötigt — weil Skills bereits erfasst haben, was gewusst werden muss, und Code das behandelt, was sich nie ändern wird.
