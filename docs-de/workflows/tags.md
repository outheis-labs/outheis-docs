# Mit Tags arbeiten

*Wie outheis dein Tag-System lernt und damit arbeitet.*

## Das Prinzip

outheis bringt kein Tag-Schema mit. Es lernt deins.

Wenn du outheis zum ersten Mal startest, sind deine vault-Tags ihm unbekannt. Der data-agent kann deine Tag-Taxonomie scannen und extrahieren — aber nur wenn du ihn darum bittest. Keine automatische Umstrukturierung, keine erfundenen Tags.

Die eine Ausnahme: Datums-Tags. Wenn outheis eine Notiz erstellt oder annotiert, kann es einen `#date-YYYY-MM-DD`-Tag hinzufügen, um sie zeitlich zu verankern. Alles andere bleibt unberührt.

## Die Analyse starten

Sobald dein vault verbunden ist, ausführen:

```
analyze tags
```

Der data-agent scannt alle Markdown-Dateien, extrahiert jeden gefundenen Tag und spiegelt die Struktur zurück. Zum Beispiel:

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

Du bestätigst oder korrigierst. Ab diesem Punkt sucht, plant und denkt outheis innerhalb deines Systems.

## Was outheis mit Tags macht

**Tagesplanung** — der agenda-agent verwendet `#action-required`, `#action-now`, `#focus-today` und Datums-Tags beim Erstellen deiner Tagesansicht. Für heute markierte Einträge erscheinen automatisch.

**Suche** — du kannst direkt nach Tags abfragen:

```
show everything tagged #unit-work and #action-waiting
what's tagged #recurring this week?
```

**Shadow.md** — der nächtliche vault-Scan nutzt deine Tags, um zeitrelevante Einträge zu identifizieren. Einträge mit `#recurring`, `#date-*` oder Aktions-Tags erscheinen im chronologischen Index, den der agenda-agent jeden Morgen liest.

## Tag-Systeme variieren

outheis arbeitet mit jeder Konvention, die du verwendest:

```
#todo #project #someday           ← flach
#work/client/project              ← hierarchisch mit /
#action-required #status-active   ← Namespace mit -
```

Der data-agent kartiert die gefundene Struktur. Er schreibt deine Tags nicht um, um einem bevorzugten Format zu entsprechen.

## Das facettierte Namespace-Muster

Eine besonders effektive Konvention verwendet einen `Kategorie-Wert`-Namespace mit Bindestrichen. Jeder Tag trägt zwei Informationen: welche Dimension er beschreibt und welchen Wert er enthält.

```
#action-required    was geschehen muss
#status-active      aktueller Zustand
#rank-high          Priorität
#unit-work          Kontext
#topic-design       Thema
#size-M             geschätzter Aufwand
#recurring          wiederholt sich
```

Das macht jede Datei entlang mehrerer Achsen abfragbar — ohne verschachtelte Ordner oder formale Metadaten. Eine Datei mit den Tags `#action-required #rank-urgent #unit-work` sagt dir sofort, was sie ist, wie dringend sie ist und wohin sie gehört.

Die zeitliche Dimension dieses Musters — wie zeitverankerte Tags mit wiederkehrender Struktur interagieren — wird in der [research-base](https://github.com/outheis-labs/research-base/tree/main/temporalization-of-order) untersucht.

## Verbesserungen und Vorschläge

Im Laufe der Zeit kann der data-agent Dinge bemerken: eine Kategorie mit nur einem Wert, zwei Tags die immer zusammen auftreten, eine Inkonsistenz, die eine kleine Konventionsänderung lösen würde. Wenn das passiert, spricht er das direkt im Gespräch an — nicht still, nicht automatisch.

Du entscheidest, ob du den Vorschlag annimmst. Wenn ja, hilft outheis dir, ihn umzusetzen. Das Tag-System bleibt deins.
