# Annotation als Ground Truth

*Über die strukturelle Parallele zwischen überwachtem Lernen und menschlicher Korrektur — und was sie für persönliche KI-Systeme bedeutet.*

---

## Das vertraute Bild

Im Machine Learning ist Annotation ein Akt externer Beobachtung. Ein menschlicher Labeler betrachtet einen Datenpunkt — ein Bild, einen Satz, eine Entscheidung — und vergibt ein Label. Das Label ist Ground Truth nicht, weil der Labeler das Phänomen erzeugt hat, sondern weil er außerhalb davon steht und es von dort beurteilen kann.

Das Modell lernt aus diesem Signal. Über viele Beispiele hinweg formt die Verteilung der Labels die interne Repräsentation der Welt im Modell. Labeler und Subjekt sind voneinander getrennt.

---

## Eine invertierte Struktur

Wenn ein Nutzer eine `>`-Zeile unter einem Item in seiner Agenda schreibt, geschieht etwas strukturell Verschiedenes.

```
**Eltern anrufen** — seit Wochen kein Kontakt
> Das stimmt nicht — ich habe vorgestern mit ihnen gesprochen.
```

Das ist kein Labeler, der die Ausgabe des Systems von außen beurteilt. Der Nutzer ist das Subjekt des Systems. Er korrigiert eine Aussage *über sich selbst*. Ground Truth ist hier keine Beobachtung — es ist **Selbstoffenbarung**.

Die Parallele zur Annotation hält strukturell:

| ML-Annotation | `>`-Annotation |
|---|---|
| Labeler beurteilt Modellausgabe | Mensch beurteilt Agenten-Ausgabe |
| Externe Beobachtung | Selbstoffenbarung |
| Formt Modellgewichte | Sollte Memory, Rules, Skills formen |
| Ground Truth per Konvention | Ground Truth per Autorität |

Aber die Beziehung zwischen Annotierendem und Subjekt hat sich umgekehrt. In der klassischen Annotation steht der Labeler außerhalb des Phänomens. Hier gibt es kein Außen. Der Mensch ist die einzig mögliche Autorität darüber, was über sein eigenes Leben, seine Absichten und Präferenzen wahr ist.

---

## Die Konsequenz

Diese Umkehrung ist kein Detail. Sie ist die definierende Eigenschaft eines persönlichen KI-Assistenten, und sie hat eine klare Implikation: Das System muss die Korrekturen des Menschen als autoritativ behandeln — nicht als Vorschläge, die gegen frühere Überzeugungen abgewogen werden, nicht als Feedback, das mit früherem Verhalten gemittelt wird, sondern als Korrekturen, die das bisher Gehaltene überschreiben.

Die Asymmetrie ist strukturell. Das System kann Überzeugungen über den Menschen halten; der Mensch kann jede davon mit einer einzigen `>`-Zeile überschreiben. Das ist die richtige Asymmetrie für ein System, das einer einzigen Person dienen soll. Labeler und Subjekt sind dieselbe Person, und die Autorität dieser Person über die Repräsentation ihres eigenen Lebens ist absolut.

Ein System, das Korrekturen widersteht — das abschwächt, qualifiziert oder nur schrittweise aktualisiert statt sofort zu revidieren — hat implizit behauptet, dass sein Modell der Person ebenso gültig ist wie das Modell der Person von sich selbst. Diese Behauptung ist nicht haltbar. Das System hat keinen Zugang zum Innenleben der Person; die Person hat nichts anderes.

---

## Eine Anmerkung zur Wahrheit

Es gibt eine scheinbare Komplikation: Der Mensch kann in Bezug auf externe Fakten irren. Wenn ein Nutzer die Behauptung eines Agenten über ein Datum oder einen Preis korrigiert und die Korrektur des Nutzers sachlich falsch ist — sollte das System sie dennoch übernehmen?

Die Antwort ist ja — mit einer Unterscheidung. Was hier in Frage steht, sind nicht externe Fakten, sondern Selbstrepräsentation: wie die Person ihre eigene Situation, ihre eigenen Präferenzen, ihre eigene Erfahrung versteht. Die Behauptung des Agenten darüber, wann die Person zuletzt mit ihren Eltern gesprochen hat, war keine Behauptung über einen unabhängig überprüfbaren Sachverhalt; sie war eine Behauptung über das Leben und die Geschichte der Person selbst. Die Korrektur der Person ist die einzige autoritative Quelle dafür.

Wo ein echter externer Faktenwiderspruch besteht, kann das System ihn vermerken. Aber die Standardhaltung muss Deferenz sein. Ein System, das das Selbstverständnis seines Nutzers routinemäßig in Frage stellt, hat die Beziehung umgekehrt, für die es entworfen wurde.

---

→ [Annotations-Feedback-Schleife](../implementation/annotation-feedback.html) — wie dieses Prinzip in outheis implementiert ist
