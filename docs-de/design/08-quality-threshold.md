# Die Qualitätsschwelle: Warum Fähigkeit nicht linear skaliert

*Über emergente Fähigkeiten, die Grenzen von Parallelismus und das minimale tragfähige Modell.*

---

## Die Intuition, die versagt

Wenn ein Modell für eine Aufgabe zu klein ist, liegt der Instinkt nahe zu kompensieren: mehr Modelle einsetzen, mehr Durchläufe, mehr Struktur. Wenn ein einzelnes 3B-Modell keinen zuverlässigen Tool-Call erzeugt — vielleicht können drei davon, die abstimmen und sich gegenseitig prüfen, die Zuverlässigkeit eines einzelnen fähigen Modells annähern.

Diese Intuition ist falsch. Sie scheitert nicht aus technischen Gründen, sondern aus Gründen, die in der Natur sprachlicher Modelle selbst liegen. Um zu verstehen warum, muss man sich ansehen, was „Fähigkeit" auf diesen Ebenen eigentlich bedeutet.

---

## Emergente Fähigkeiten und der Schwelleneffekt

Große Sprachmodelle skalieren nicht glatt. Bestimmte Fähigkeiten sind auf kleiner Skala nicht vorhanden und treten bei wachsender Größe abrupt auf — nicht als allmähliche Verbesserung, sondern als Phasenübergang.

Wei et al. (2022) haben dies über ein breites Spektrum von Aufgaben dokumentiert: arithmetisches Few-Shot-Lernen, logisches Schließen, mehrstufige Schlussfolgerungen, Instruktionsbefolgung. Auf kleiner Skala ist die Leistung nahe dem Zufallswert. An einer Schwelle — für jede Fähigkeit unterschiedlich, typischerweise im Bereich von 10–100 Milliarden Parametern — springt die Leistung diskontinuierlich. Die Modelle werden nicht schrittweise besser; sie beherrschen diese Aufgaben gar nicht, und dann plötzlich doch.

Die relevante Schwelle für outheis ist **strukturiertes Tool-Dispatch**: aus einer natürlichsprachlichen Anfrage einen gültigen JSON-Tool-Call mit korrekten Argumentnamen und -typen erzeugen. Das ist kein Muster-Matching gegen Trainingsbeispiele. Es setzt voraus:

1. Die Anfrage semantisch verstehen
2. Das passende Tool für die Absicht identifizieren
3. Die korrekten Argumente aus dem Kontext extrahieren
4. Syntaktisch valide strukturierte Ausgabe erzeugen

Modelle unterhalb der Schwelle scheitern bei Schritt 1 oder 3. Sie produzieren plausibel klingende Ausgabe — oft strukturell valides JSON — aber mit falschen Tool-Namen, halluzinierten Argumenten oder kompletten Nicht-Sequiturs. Die Fehler sind keine sanften Degradierungen; sie sind Kategorienirrtümer.

---

## Warum Parallelismus nicht hilft

Wenn eine Fähigkeit unterhalb der Schwelle fehlt, erzeugt mehr unterhalb-der-Schwelle-Modelle sie nicht. Das ist kein Ressourcenargument. Es ist ein Argument über die Natur dessen, was fehlt.

Stell dir vor, drei 3B-Modelle „stimmen" über einen Tool-Call ab. Jedes erzeugt seinen besten Vorschlag. Abstimmen erfordert, Ausgaben zu vergleichen und eine Mehrheit zu finden — aber wenn keine der Ausgaben korrekt ist, gibt die Mehrheitsentscheidung den häufigsten Fehler zurück, kein richtiges Ergebnis. Schlimmer: Die Fehler ähnlicher kleiner Modelle sind korreliert. Sie scheitern auf dieselbe Weise, weil sie dieselben Beschränkungen haben. Ensemble-Methoden profitieren von *verschiedenartigen* Fehlern, nicht von *identischen*.

Mehr Durchläufe helfen auch nicht. Ein Modell, das im ersten Durchlauf das richtige Argument nicht aus der Anfrage ableiten kann, wird es im dritten auch nicht. Die Fähigkeit liegt nicht im Durchlauf; sie müsste in den Gewichten liegen — und die Gewichte haben sie nicht.

Die technische Parallele: Man kann ein Feature nicht implementieren, indem man fehlerhaften Code schneller ausführt. Der Fehler muss behoben werden. Bei Sprachmodellen gibt es unterhalb der Schwelle kein Äquivalent zu „den Fehler beheben" ohne Neutraining. Das Modell ist, was es ist.

---

## Das strukturelle Argument

Es gibt einen tieferen Grund, warum die Schwelle nicht umgangen werden kann. Transformer-Modelle verarbeiten eine Anfrage in einem einzigen Vorwärtsdurchlauf durch alle Schichten. Jede Schicht verfeinert die Repräsentation der Anfrage und baut zunehmend abstrakte Merkmale auf. Die letzte Schicht erzeugt die Ausgabeverteilung.

Die Fähigkeit, einer komplexen Instruktion zu folgen, hängt davon ab, genügend Schichten, Köpfe und Parameter zu haben, um die notwendigen intermediären Abstraktionen zu repräsentieren. Ein kleines Modell hat keine degradierte Version dieser Fähigkeit; es hat eine andere Architektur, die eine niedrigere Decke erreicht. Man kann es öfter laufen lassen, aber die Decke bewegt sich nicht.

Größere Modelle haben auch mehr Kapazität, um zu repräsentieren, was nicht gesagt wird — Schlussfolgerungen aus Kontext, Disambiguierung, Erkennung unstated Absicht. Genau das ist es, was Tool-Dispatch erfordert: „prüf meine Agenda" muss zu einem `agenda_query`-Call aufgelöst werden, nicht zu einem `file_read` oder `memory_lookup`. Die Auflösung erfordert kontextuelle Schlussfolgerung, die ein kleines Modell nicht zuverlässig leisten kann.

---

## Die praktische Schwelle für outheis

Empirisch hält die 7B-Grenze für Instruktionsbefolgung in outheis' Kontext zuverlässig. Darunter:

- Tool-Call-Syntax ist korrekt; Tool-Auswahl ist falsch
- Argumente klingen plausibel, entsprechen aber nicht den tatsächlichen Parametern
- Mehrstufiges Reasoning (welches Tool, dann welche Argumente) bricht zusammen

Bei 7B mit Instruction-Tuning ist die Schwelle für Routing-Klassen-Aufgaben (relay) überschritten. Bei 12–14B hält sie für Tool-Use-Agenten (zeno, cato), wenn überprüft. Unter 7B erzeugt kein Maß an Prompt-Engineering, Wiederholung oder strukturellem Scaffolding zuverlässige Ergebnisse — weil die Fähigkeit, die das Scaffolding voraussetzt, nicht vorhanden ist.

Das bedeutet: Die relevante Frage bei der Modellauswahl ist nicht „wie klein kann ich gehen?", sondern „hat dieses Modell die Schwelle für die Aufgabe überschritten?". Es ist eine binäre Entscheidung, kein Gradient. Tests bestätigen das: `test_ollama_tool_use.py` liefert ✓ oder ✗, kein Score. Ein ✗-Modell kann nicht mit mehr Sorgfalt provisorisch verwendet werden.

---

## Was das für das outheis-Design bedeutet

**Ein fähiger Agent schlägt viele schwache.** outheis ist um eine kleine Anzahl spezialisierter Agenten aufgebaut, jeder mit einem fokussierten Tool-Set und einem Modell, das die relevante Fähigkeitsschwelle überschritten hat. Das ist kein Zugeständnis an praktische Grenzen; es ist eine strukturelle Eigenschaft dieser Systeme.

**Die Grenze ist eine Qualitätsschwelle, keine Ressourcenschwelle.** Die Entscheidung, eine Mindestmodellgröße zu fordern, betrifft nicht laufende Kosten oder Latenz. Es geht darum, ob die von der Aufgabe geforderte Fähigkeit im Modell überhaupt vorhanden ist. Ein Modell, das den Tool-Use-Test nicht besteht, ist nicht eine langsamere oder günstigere Version eines Modells das ihn besteht; es ist eine andere Kategorie von Werkzeug.

**Verifikation ist vor dem Einsatz obligatorisch.** Weil Fähigkeit schwellenbasiert ist und nicht allein aus der Parameterzahl ableitbar (verschiedene Architekturen, verschiedene Trainingsregimes, verschiedenes Fine-tuning), ist empirisches Testen erforderlich. Die Parameterzahl ist eine Heuristik für den Startpunkt; das Testergebnis ist die Grundwahrheit.

**Deaktivieren statt degradieren.** Wenn kein Modell jenseits der Schwelle für eine Agentenrolle verfügbar ist, ist die richtige Reaktion, die geplanten Aufgaben dieses Agenten zu deaktivieren — nicht sie mit einem Modell unterhalb der Schwelle auszuführen. Ein nächtlicher Pattern-Inference-Lauf, der halluzinierte Erinnerungen erzeugt, ist schlimmer als kein Lauf: Er injiziert falsche Daten in die Wissensbasis. Ein fehlgeschlagener Lauf lässt das System unverändert. Ein degradierter Lauf korrumpiert es.

---

## Weiterführende Literatur

- Wei, J. et al. „Emergent Abilities of Large Language Models." *Transactions on Machine Learning Research*, 2022.
- Kaplan, J. et al. „Scaling Laws for Neural Language Models." *arXiv*, 2020.
- Schaeffer, R. et al. „Are Emergent Abilities of Large Language Models a Mirage?" *NeurIPS*, 2023.
- Srivastava, A. et al. „Beyond the Imitation Game." *Transactions on Machine Learning Research*, 2023.
