# Attention als Architektur

## Die strukturelle Analogie

Die zentrale Erkenntnis der Transformer-Architektur — dass erlernte Attention-Mechanismen komplexe sequentielle Verarbeitung ersetzen können — gilt direkt für die Struktur von outheis. Das ist keine Metapher. Es ist dasselbe Prinzip auf einer anderen Abstraktionsebene.

| LLM-Konzept | outheis-Äquivalent |
|---|---|
| Trainierte Gewichte | Skills (destillierte Prinzipien) |
| Kontextfenster | Memory (aktuelle Beobachtungen) |
| Query | Nutzernachricht |
| Attention-Scores | Relevanz — welcher Kontext geladen wird |
| Trainingsschleife | Pattern-agent (nächtlich) |

In einem Transformer:
- **Gewichte** sind erlernte Muster, die die Aufmerksamkeit auf relevante Teile der Eingabe lenken
- **Kontext** ist die aktuell verarbeitete Eingabe
- **Training** verfeinert Gewichte, sodass weniger Kontext für gute Ausgaben benötigt wird

In outheis:
- **Skills** sind erlernte Prinzipien, die die agent-Aufmerksamkeit auf das Wesentliche lenken
- **Memory** sind angesammelte Beobachtungen, die auf Destillation warten
- **Pattern-agent** verfeinert Skills, sodass agents weniger in ihrem Kontext benötigen

Das Ziel in beiden Fällen: progressiv weniger explizite Eingabe für gute Ausgaben benötigen, weil erlernte Repräsentationen bereits das Wesentliche erfassen.

---

## Die Lernschleife

```
Nutzer interagiert mit agents
        ↓
Korrekturen, Präferenzen beobachtet
        ↓
In Memory gespeichert (feedback-Typ)
        ↓
Pattern-agent läuft (nächtlich)
        ↓
Erkennt Muster (3+ ähnliche Beobachtungen)
        ↓
Destilliert zu Skill (verdichtetes Prinzip)
        ↓
Löscht redundante Memory-Einträge
        ↓
Nächste agent-Invokation: Skill lenkt Aufmerksamkeit
        ↓
Agent verhält sich anders (gelernt)
```

Das ist Gradient-Descent auf Systemebene. Jede Korrektur passt die „Gewichte" (Skills) an. Mit der Zeit benötigt das System weniger expliziten Kontext, weil die Skills die Aufmerksamkeit effizient lenken.

---

## Warum nicht mehr Code?

Das Anti-Pattern ist, Lernen mit Code zu lösen:

```python
# Falsch: fest codierte Präferenzprüfungen
def format_date(date):
    if user_prefers_iso:
        return date.isoformat()
    elif user_prefers_german:
        return date.strftime("%d.%m.%Y")
    # ... weitere Zweige für jede Präferenz
```

```
# Richtig: destillierter Skill
Skill: "Dates: Always ISO format (YYYY-MM-DD)"
```

Das LLM liest den Skill und wendet ihn an. Kein Code ändert sich, wenn sich Präferenzen ändern. Das System lernt durch Verfeinern von Skills, nicht durch Hinzufügen von Zweigen.

Deshalb ist die Grenze zwischen Code und LLM eine Designeinschränkung, nicht nur eine Präferenz. Code, der gelerntes Verhalten codiert, macht das System starr. Skills, die gelerntes Verhalten codieren, machen es adaptiv.

---

## Kompression als Kernmechanismus

Wenn Kontext wächst, scheitern naive Ansätze:

```
Falsch: mehr Tools hinzufügen, um mehr Daten zu holen
read_file_1(), read_file_2(), ... read_file_n()

Richtig: bessere Kompression durch Skills
Ein Skill ersetzt 10 Memory-Einträge.
Ein Prinzip ersetzt 10 Beispiele.
```

Ein trainiertes Modell speichert nicht alle Trainingsbeispiele — es lernt Muster. Ebenso behält outheis nicht alle Beobachtungen; es destilliert Prinzipien. Das Maß eines reifenden Systems ist nicht, wie viel es speichert, sondern wie wenig es braucht.

---

## Die Hierarchie als Attention-Ebenen

```
Skills (höchste Dichte)
   │  "Use ISO dates" — gilt überall
   │  Verdichtetes Wissen, maximale Hebelwirkung
   │
Memory (mittlere Dichte)
   │  "User corrected date format 3x"
   │  Rohe Beobachtungen, auf Kompression wartend
   │
Rules (niedrigste Dichte)
      "Never delete without confirmation"
      Harte Einschränkungen, überschreiben alles
```

| Ebene | Dichte | Flüchtigkeit | Funktion |
|---|---|---|---|
| Skills | Hoch | Ändert sich durch Destillation | Aufmerksamkeit lenken |
| Memory | Mittel | Ändert sich ständig | Beobachtungen speichern |
| Rules | Niedrig | Ändert sich selten | Grenzen setzen |

---

## Pattern-agent als Optimierer

Der Pattern-agent spielt die Rolle des Optimierers in diesem System:

1. **Beobachtet Gradienten** — Nutzerkorrekturen signalisieren Fehler
2. **Sammelt Updates** — Memory speichert Beobachtungen
3. **Wendet Batch-Update an** — nächtliche Destillation
4. **Beschneidet Redundanz** — löscht veraltete Memory-Einträge

Wie eine Trainingsschleife läuft er kontinuierlich im Hintergrund und verbessert schrittweise die „Gewichte" (Skills) des Systems basierend auf beobachtetem „Loss" (Korrekturen und Feedback).

---

## Praktische Implikationen

- Präferenzen nicht fest codieren — Skills aus Beobachtung entstehen lassen
- Keine Tools hinzufügen, um mehr Daten zu holen — Daten durch Skills in Kontext komprimieren
- Der Destillation vertrauen — Korrekturen von heute werden morgen zu Skills
- An der Kontextgröße messen: bessere Skills = kleinerer benötigter Kontext

Das Ziel: ein System, das besser wird nicht durch Hinzufügen von Code, sondern durch Verfeinern der Aufmerksamkeit. Je länger es läuft, desto weniger benötigt es im Kontext, weil Skills bereits die Aufmerksamkeit auf das Wesentliche lenken.
