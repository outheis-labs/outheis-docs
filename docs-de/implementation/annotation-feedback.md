# Annotations-Feedback-Schleife

*Wie `>`-Annotationen in den Memory-Stack geroutet werden — die aktuelle Lücke und die geplante Implementierung.*

---

## Was Annotationen sind

Eine `>`-Zeile unter einem Item in Agenda.md ist eine direkte Korrektur des Nutzers. Der agent (cato) verarbeitet sie: schreibt das Item neu, entfernt die Annotationszeile und fährt fort.

Die Korrektur wurde umgesetzt. Das *Wissen*, das die Korrektur verursacht hat, wird nicht persistiert.

---

## Drei Typen, drei Schichten

Annotationen tragen nicht alle dieselbe Art von Signal. Sie fallen in drei Kategorien, die jeweils einer Schicht des [hybriden Memory-Stacks](../design/07-hybrid-memory-stack.html) entsprechen:

**Faktische Korrektur** — „das stimmt nicht — ich habe vorgestern mit ihnen gesprochen"
→ Neue Information über die Welt, in der das System operiert
→ Ziel: **Memory** (persistente Beobachtungen, als Einträge gespeichert)

**Verhaltenskorrektur** — „bezeichne einen Abstand von Tagen nicht als 'Wochen'"
→ Eine Regel darüber, wie sich das System ausdrücken oder handeln soll
→ Ziel: **Rules** (stabile Einschränkungen, in Markdown geschrieben)

**Präferenz- / Strukturkorrektur** — „der Cashflow-Abschnitt soll 3 Zeilen haben, nicht 20"
→ Verdichtetes prozedurales Wissen darüber, wie gute Ausgabe aussieht
→ Ziel: **Skills** (dichte Prinzipien, die die agent-Aufmerksamkeit lenken)

Der Inhalt der Annotation selbst bestimmt den Typ. Klassifikation ist eine Aufgabe für den agent, nicht für den Code.

---

## Die fehlende Schleife

Die aktuelle Implementierung endet nach der Verarbeitung:

```
Mensch schreibt > Korrektur
    ↓
cato schreibt Item korrekt neu         ✓
cato entfernt die > Zeile              ✓
    ↓
Faktischer Inhalt → Memory             ✗
Verhaltensregel → Rules-Schicht        ✗
Präferenz → Skills-Schicht             ✗
    ↓
rumi fördert stabile Muster → Rules    ✗
```

Jede Korrektur ist ein einmaliges Ereignis. Das System ist korrigierbar, nicht lernfähig. Derselbe Fehler kann beim nächsten Agenda-Lauf erneut auftreten, weil nichts in den Memory-Stack geschrieben wurde.

---

## Geplante Implementierung

Eine vollständige Schleife würde signifikante Annotationen als Lern-Ereignisse neben Verarbeitungs-Ereignissen behandeln:

1. **cato verarbeitet** — Item neu schreiben, `>`-Zeile entfernen (kein Unterschied zum aktuellen Verhalten)
2. **cato klassifiziert** — Annotationstyp bestimmen: faktisch, verhaltensbasiert oder Präferenz
3. **cato schreibt Vorschlag** — bei faktischem Inhalt: ein Memory-Vorschlag nach `Migration/Exchange.md`; bei Verhaltens-/Präferenzinhalt: ein `rule:agenda`- oder `skill`-Vorschlag, ebenfalls via Exchange.md
4. **rumi verarbeitet** — beim nächsten `memory_migrate`-Lauf verarbeitet rumi diese Vorschläge neben anderen Migrationsquellen
5. **Nutzer prüft** — der Vorschlag erscheint in Exchange.md mit demselben Accept/Reject-Mechanismus wie alle anderen Migrationen

Das verbindet cato und rumi zu einer einzigen kohärenten Schleife. Heute gemachte Korrekturen werden zu Regeln, die denselben Fehler morgen verhindern. Der Memory-Stack wächst aus gelebtem Gebrauch, nicht nur aus expliziten Migrationssitzungen.

### Vorschlagsformat

Vorschläge, die cato schreibt, folgen dem bestehenden Exchange.md-Item-Format, sodass rumi und die Review-Oberfläche sie ohne Änderung verarbeiten können:

```markdown
*extracted: 2026-04-07 14:32*
[faktisch] Letztes Telefonat mit Eltern vor 2 Tagen, nicht vor Wochen. [memory]
- [ ] Accept
- [ ] Reject
```

Die Typen `[rule:agenda]` und `[skill]` erweitern das bestehende Typ-Vokabular.

---

## Status

- `>`-Annotationsverarbeitung: **implementiert** (`agenda.py`)
- Klassifikation und Vorschlags-Schreiben: **noch nicht implementiert**
- Exchange.md-Routing für cato-generierte Vorschläge: **noch nicht implementiert**
