# Mit Tags arbeiten

*Wie outheis dein Tag-System erlernt und darin arbeitet.*

## Das Prinzip

outheis kommt ohne Tag-Schema. Es erlernt deines.

Wenn du outheis zum ersten Mal startest, sind deine Vault-Tags unbekannt. Der Data-Agent kann deine Tag-Taxonomie scannen und extrahieren — aber nur wenn du fragst. Keine automatische Umstrukturierung, keine erfundenen Tags.

Die eine Ausnahme: Datum-Tags. Wenn outheis eine Notiz erstellt oder kommentiert, kann es einen `#date-JJJJ-MM-TT`-Tag hinzufügen, um sie zeitlich zu verankern. Alles andere bleibt unberührt.

## Analyse starten

Sobald dein Vault verbunden ist, führe aus:

```
analyze tags
```

Der Data-Agent scannt alle Markdown-Dateien, extrahiert jeden gefundenen Tag und reflektiert die Struktur zurück. Zum Beispiel:

```
Found 847 tags across 134 files.

Tag categories detected:
  action-*   (required, waiting, idle, now, call, send)
  status-*   (active, linger, completed, init)
  rank-*     (urgent, high, medium, low)
  unit-*     (work, self, family, ...)
  topic-*    (12 values)
  size-*     (S, M, L)
  recurring

No fixed schema assumed. Does this match how you use these tags?
```

Du bestätigst oder korrigierst. Von diesem Punkt an sucht, plant und denkt outheis innerhalb deines Systems.

## Was outheis mit Tags macht

**Tagesplanung** — der Agenda-Agent verwendet `#action-required`, `#action-now`, `#focus-today` und Datum-Tags beim Erstellen deiner Tagesansicht. Für heute markierte Einträge erscheinen automatisch.

**Suche** — du kannst direkt nach Tags abfragen:

```
show everything tagged #unit-work and #action-waiting
what's tagged #recurring this week?
```

**Shadow.md** — der nächtliche Vault-Scan verwendet deine Tags, um zeitrelevante Einträge zu identifizieren. Einträge mit `#recurring`, `#date-*` oder Aktions-Tags erscheinen im chronologischen Index, den der Agenda-Agent jeden Morgen liest.

## Tag-Systeme variieren

outheis arbeitet mit der Konvention, die du verwendest:

```
#todo #project #someday           ← flat
#work/client/project              ← hierarchical with /
#action-required #status-active   ← namespaced with -
```

Der Data-Agent kartiert die gefundene Struktur. Er schreibt deine Tags nicht um, um einem bevorzugten Format zu entsprechen.

## Das facettierte Namensraum-Muster

Eine besonders effektive Konvention verwendet einen `Kategorie-Wert`-Namensraum getrennt durch Bindestriche. Jeder Tag trägt zwei Informationen: welche Dimension er beschreibt und welchen Wert er enthält.

```
#action-required    what needs to happen
#status-active      current state
#rank-high          priority
#unit-work          context
#topic-design       subject matter
#size-M             estimated effort
#recurring          repeats
```

Das macht jede Datei entlang mehrerer Achsen abfragbar — ohne verschachtelte Ordner oder formale Metadaten. Eine Datei mit den Tags `#action-required #rank-urgent #unit-work` sagt dir sofort, was sie ist, wie dringend sie ist und wohin sie gehört.

Die zeitliche Dimension dieses Musters — wie zeitverankerte Tags mit wiederkehrender Struktur interagieren — wird in der [research-base](https://github.com/outheis-labs/research-base/tree/main/temporalization-of-order) untersucht.

## Verbesserungen und Vorschläge

Mit der Zeit kann der Data-Agent Dinge bemerken: eine Kategorie mit nur einem Wert, zwei Tags die immer gemeinsam auftrauchen, eine Inkonsistenz die eine kleine Konventionsänderung lösen würde. Wenn das passiert, bringt er es direkt im Gespräch auf — nicht still, nicht automatisch.

Du entscheidest, ob du den Vorschlag übernimmst. Wenn ja, hilft outheis dir, ihn umzusetzen. Das Tag-System bleibt deins.
