# Tags als Gerüst: Ein Ablösungspfad

## Das Problem mit vollständigem Textverständnis — heute

Ein persönliches KI-System, das den Nutzer wirklich versteht, würde im Idealfall alles aus dem Freitext ableiten. Es würde eine Notiz lesen, deren Dringlichkeit einschätzen, sie kategorisieren, ihre Beziehung zu laufenden Projekten erkennen — ohne jede explizite Markierung. Der Nutzer schreibt natürlich; das System versteht.

Das ist die richtige langfristige Richtung. Sie ist heute jedoch noch nicht zuverlässig erreichbar.

Aktuelle Sprachmodelle haben begrenzte Kontextfenster. Wenn eine Sitzung genug Geschichte ansammelt, fallen frühere Beobachtungen aus dem Blickfeld. Ein Modell, das vor drei Wochen etwas verstanden hat, hat dieses Verständnis jetzt möglicherweise nicht mehr zur Verfügung. Grundlegender noch: vollständige Textverständnis — das zuverlässige Extrahieren von Struktur aus mehrdeutiger natürlicher Sprache über Sitzungen, Sprachen und Formulierungsvarianten hinweg — scheitert noch oft genug, um in einem täglich laufenden System zu zählen.

Tags sind die Antwort auf diese Einschränkung — aber nur vorübergehend.

---

## Was Tags eigentlich sind

Ein Tag wie `#action-required` oder `#money` ist ein diskretisiertes Signal. Er verdichtet ein Urteil — "das erfordert Handlung", "das ist finanziell relevant" — in eine Form, die ohne vollständiges Textverstehen verarbeitet werden kann.

Zwei Items können strukturell identisch aussehen:

```
- 📋 **—** Neuen Lieferanten registrieren `#action-required`
- 📋 **—** Materialkosten kalkulieren `#action-required`
```

Ohne Tags erfordert die Unterscheidung ihrer Dringlichkeit ein Verständnis der aktuellen Projekte, Fristen und Prioritäten des Nutzers. Mit Tags steht ein minimales Signal zur Verfügung, selbst wenn der Kontext fehlt.

Tags überbrücken die Lücke zwischen **Code** (der Struktur deterministisch verarbeitet) und **Bedeutung** (die sprachliches Verstehen erfordert). Sie sind eine strukturierte Zwischenschicht — lesbar für Algorithmen, kompatibel mit LLM-Reasoning, unabhängig von der Kontextfenstergröße.

---

## Das Kontinuitätsprinzip

Tags sind Gerüst. Gerüst ist nicht dazu gedacht, dauerhaft zu bleiben.

Während memory wächst — durch Annotationen, die zur ground truth werden, durch Muster, die zu Skills werden, durch Korrekturen, die zu Regeln werden — entsteht ein dichteres Bild des Nutzers. Items, die früher einen Tag erforderten um verstanden zu werden, können schließlich allein aus ihrem Text verstanden werden, weil das System genug Kontext gelernt hat.

Das Kontinuitätsprinzip lautet: **Jeder Tag hat einen Ablösungspfad.**

Ein Tag wird redundant, wenn das System zuverlässig aus memory allein ableiten kann, was er signalisiert. An diesem Punkt liefert der Tag keine Information mehr — er dupliziert sie. Das System sollte an diesem Kriterium gemessen werden, und Tags, die es erfüllen, sollten stillgelegt werden.

Das ist keine Ablehnung von Struktur. Es ist die Erkenntnis, dass Struktur durch das verdient werden sollte, was das Modell noch nicht kann — nicht dauerhaft als Kompensation für Einschränkungen auferlegt, die aktiv reduziert werden.

---

## Praktische Konsequenzen

**Tags nicht proliferieren lassen.** Jeder neue Tag ist technische Schuld mit einem Ablösungszeitplan. Vor dem Hinzufügen eines Tags sollte geprüft werden, ob memory dasselbe Signal tragen könnte. Wenn ja — oder bald — ist der Tag verfrüht.

**In memory investieren, nicht in Taxonomien.** Ein reiches memory des Nutzerkontexts ist dauerhafter als eine verfeinerte Tag-Hierarchie. Tag-Hierarchien kodieren das heutige Verständnis und fixieren es. Memory kodiert Beobachtungen, die neu interpretiert werden können, wenn das System reift.

**Tags als Testfälle für memory-Qualität nutzen.** Wenn das System ein Item korrekt priorisiert, ohne seinen Tag zu sehen — Dringlichkeit allein aus dem memory-Kontext ableitend — ist dieser Tag bereit für die Stilllegung. Der Backlog-Generator ist ein natürlicher Test dafür: wie gut sortiert er Items, wenn er sich primär auf memory statt auf Tag-Signale stützt?

**Auf Tag-Freiheit hin gestalten.** Die langfristige Nutzererfahrung sollte nicht erfordern, dass der Nutzer irgendetwas taggt. Annotationen — freitext, natürlich, mit geringer Reibung — sollten ausreichen. Tags können vom Nutzer geschrieben werden, wenn es praktisch ist, aber das System sollte nicht von ihnen abhängen.

---

## Die Richtung

Die Entwicklungslinie ist klar:

1. **Jetzt** — Tags sind primäre Signale; memory ergänzt sie
2. **Nahe Zukunft** — memory wird dicht genug, dass Tags bestätigend wirken, nicht notwendig sind
3. **Langfristig** — reine Textverständnis; Tags sind optionale Annehmlichkeiten, die natürlich verschwinden

Jeder Schritt setzt den vorherigen voraus. Ground truth durch Annotation (siehe: *Annotation als Ground Truth*) macht memory zuverlässig. Zuverlässiges memory macht Tags redundant. Das System entwickelt sich nicht dadurch, dass ein Mechanismus durch einen anderen ersetzt wird, sondern dadurch, dass der frühere Mechanismus durch die Reifung des nächsten überflüssig wird.

Tags werden nicht gelöscht. Sie werden schlicht aufhören, gebraucht zu werden.
