
# Kalender

*Die visuelle Terminansicht im outheis WebUI.*

---

Der Kalender ist der `agenda`-Tab im WebUI. Er stellt deinen Zeitplan als interaktive Zeitleiste dar — zeitgebundene Termine als Blöcke, freischwebende Aufgaben als frei positionierbare Labels und einen kontinuierlichen farbigen Hintergrund, der das Gewicht des Geplanten widerspiegelt.

Der Kalender liest aus und schreibt in `agenda.json`:

```
~/.outheis/human/webui/pages/agenda.json
```

Diese Datei wird von cato bei jedem Stundenlauf erzeugt und kann auch direkt vom Kalender gespeichert werden. Zum Datenformat siehe [agenda.json Referenz](16-agenda-json.html).

---

## Eintragstypen

### Fixe Termine

Ein fixer Termin belegt ein definiertes Zeitfenster auf der Zeitleiste. Er wird als Block dargestellt, der genau das Start-Ende-Intervall abdeckt.

- Horizontal ziehen zum Verschieben (innerhalb desselben Tags oder tagesübergreifend)
- Größe ändern über die linken und rechten Handles an den Blockrändern
- Doppelklick öffnet das Bearbeitungspopup

**Mehrtägige Termine** (ISO-Datetime-Format) erstrecken sich über mehrere Tagesstreifen mit einem verbundenen Balken. Der erste Streifen zeigt Titel und Daten; die Folgestreifen zeigen die Fortsetzung.

### Volatile Items

Ein volatiles Item hat einen Tag, aber keine feste Uhrzeit. Es schwebt frei als Label innerhalb seines Tagesstreifens.

- In 2D ziehen: innerhalb eines Tags neu positionieren oder vertikal auf einen anderen Tag ziehen
- Doppelklick öffnet das Bearbeitungspopup
- Items mit einer **Dauer** (`#time-HH:MM`) werden als begrenztes Feld mit gestricheltem Rand dargestellt, proportional zur Dauer

Volatile Items ohne gespeicherte Drag-Position werden automatisch auf drei Y-Bänder innerhalb des Tagesstreifens verteilt, mittels deterministischem Hash aus Titel + Tag — das Layout ist so über Neuladen hinweg stabil.

### Wiederkehrende Termine

Wiederkehrende Termine werden als einzelner Anker-Eintrag in `agenda.json` gespeichert, der einen `#recurring-*`-Tag trägt. Der Kalender erzeugt Anzeige-Instanzen für alle sichtbaren Tage, die dem Wiederholungsmuster entsprechen — diese werden nie als einzelne Items zurückgeschrieben.

Unterstützte Wiederholungsmuster: siehe [agenda.json Referenz](16-agenda-json.html#recurring).

---

## Visuelles Modell

### Gravitationsfeld

Jeder Tagesstreifen hat einen kontinuierlichen farbigen Hintergrund, der aus einem Gravitationsfeld berechnet wird. Fixe Termine sind Segmentmassen; volatile Items sind Punktmassen. Ihre Felder überlagern und vermischen sich und erzeugen einen Farbverlauf, der das Gewicht und die Verteilung deines Zeitplans widerspiegelt.

Wo keine Termine vorhanden sind, halten gleichmäßig verteilte Geistermassen einen neutralen Farbton aufrecht. Der Übergang zwischen farbig und neutral ist fließend — keine Schwellenwerte, keine harten Kanten.

Vier Parameter steuern das Rendering (zugänglich über das **Gradients**-Panel):

| Parameter | Reglerbeschriftung | Wirkung |
|-----------|-------------------|---------|
| `peak_amp` | Intensity | Farbintensität an Terminhöhepunkten |
| `decay` | Range | Wie weit sich der Feldeinfluss seitlich ausdehnt |
| `ghost_pull` | Ghost pull | Gewicht des neutralen Hintergrundfelds |
| `overlay_alpha` | Blocks | Deckkraft der soliden Block-Füllung |

### Facetten und Farben

Facetten repräsentieren Lebensbereiche oder Agenten-Domänen. Jede Facette hat eine CI-Farbe, die in `agenda.json` definiert ist. Die Legende am oberen Rand des Kalenders wird aus dem `facets`-Array aufgebaut; Klick auf eine Facette dämpft oder aktiviert sie.

Der Kalender rendert nur im Light Mode. Kein Grau — die Palette verwendet die sechs outheis-Markenfarben.

---

## Zeitachse

Die Zeitachse ist **nichtlinear**: Jeder Tag ist in sechs 4-Stunden-Segmente unterteilt, jeweils mit einem eigenen visuellen Gewicht. Ein höheres Gewicht gibt diesem Zeitbereich mehr Bildschirmplatz — mehr Pixel pro Stunde — und macht Termine leichter lesbar.

```json
"time_axis": [
  { "from": "05:00", "to": "09:00", "weight": 0.5 },
  { "from": "09:00", "to": "13:00", "weight": 2.2 },
  { "from": "13:00", "to": "17:00", "weight": 1.8 },
  { "from": "17:00", "to": "21:00", "weight": 1.0 },
  { "from": "21:00", "to": "01:00", "weight": 0.5 },
  { "from": "01:00", "to": "05:00", "weight": 0.3 }
]
```

Fehlt `time_axis`, fällt der Kalender auf eine lineare 24-Stunden-Verteilung zurück.

Der **Tagesstart** (`day_start`) definiert die erste sichtbare Stunde. Standard: 5 (05:00). Alle Segmentgrenzen verschieben sich automatisch, wenn sich der Tagesstart ändert.

### Spread-Panel

Klicke **Spread** in der oberen Leiste, um das Zeitachsen-Konfigurationspanel zu öffnen:

- **Tag ab** — setzt `day_start` (nur ganze Stunden); alle Segmentgrenzen werden automatisch aktualisiert
- **Sechs Segment-Zeilen** — jede zeigt ihren `von–bis`-Bereich und einen Gewichts-Regler (0,1–5,0)

Änderungen gelten sofort für das sichtbare Layout und werden beim nächsten Speichern gespeichert.

---

## Interaktion

### Obere Leiste

| Steuerelement | Funktion |
|--------------|----------|
| ↻ | `agenda.json` vom Disk neu laden |
| 7 / 14 / 30 | Sichtbaren Tagesbereich einstellen |
| Add item | Erstell-Popup öffnen |
| Save | Aktuellen Stand in `agenda.json` schreiben |
| Colors | Facetten-Farbzuweisungen wechseln (CI-Palette-Permutationen) |
| Gradients | Gravitationsfeld-Parameter-Panel öffnen |
| Spread | Zeitachsen-Konfigurationspanel öffnen |

### Ziehen und Größe ändern (fixe Termine)

- **Ziehen**: Klicken und halten auf dem Block, links/rechts ziehen. Tagesübergreifende Drops werden unterstützt — der Block wechselt in den Ziel-Tagesstreifen.
- **Größe ändern**: Den linken oder rechten Handle greifen (erscheint beim Hover oder wenn der Block entsperrt ist). Der Blockrand folgt dem Cursor; das Zeitlabel wird live aktualisiert.
- **× Schaltfläche**: Termin zu volatil degradieren (erscheint beim Hover). Erfordert Bestätigung.

### Ziehen (volatile Items)

Klicken und halten auf einem volatilen Label, an eine beliebige Position im aktuellen Tagesstreifen oder in einen anderen Tagesstreifen ziehen. Die Position wird beim nächsten Speichern in `agenda.json` gespeichert.

### Volatil → fix befördern

Bearbeitungspopup öffnen (Doppelklick) und Start-/Endzeiten eintragen. Das Item wird zu einem fixen Termin befördert.

---

## Bearbeitungspopup

Doppelklick auf ein beliebiges Item öffnet das Bearbeitungspopup.

| Feld | Beschreibung |
|------|-------------|
| Title | 3-zeiliges Textarea — unterstützt mehrzeilige Titel |
| Start / End | Zeiteingaben (HH:MM) |
| Date / End date | Datumseingaben; zwei Daten erzeugen einen mehrtägigen Termin |
| × (Zeit) | Zeitfelder leeren (befördert zu volatil) |
| × (Enddatum) | Enddatum leeren |
| Facet | Aus verfügbaren Facetten auswählen |
| Size | S / M / L — visuelles Gewicht für volatile Items |
| Tags | Rohe Tag-Eingabe — strukturelle Tags werden beim Speichern neu aufgebaut |
| follows | Kommagetrennte Titel von Items, auf die dieses Item wartet |
| precedes | Kommagetrennte Titel von Items, die dieses Item blockiert |

**Schaltflächen:**

- **Save** — Änderungen übernehmen, automatisch speichern
- **Done ✓** — zeigt ein optionales Kommentarfeld; Bestätigung markiert das Item als erledigt mit dem heutigen Datum und speichert
- **Cancel** — Änderungen verwerfen
- **Delete** — Item nach Bestätigung entfernen

---

## Item hinzufügen

Klicke **Add item** in der oberen Leiste. Felder: Title, Start, End, Date, End date, Facet, Size, Tags. Das Item wird sofort hinzugefügt und gespeichert.

---

## Abhängigkeiten

Items können Reihenfolgebeziehungen zu anderen Items deklarieren.

| Feld | Richtung | Bedeutung |
|------|----------|-----------|
| `follows` | dieses Item → Vorgänger | „Ich warte darauf, dass diese Items abgeschlossen sind, bevor ich beginne" |
| `precedes` | dieses Item → Nachfolger | „Ich blockiere diese Items — sie können erst beginnen, wenn ich fertig bin" |
| `relates` | assoziativ | „Ich bin mit diesen Items verbunden" — kein Ordering |

Beide Felder `follows` und `precedes` sind eigenständige Primitive, die dieselbe Beziehung aus entgegengesetzten Perspektiven ausdrücken. Verwende dasjenige, das zur Planungsrichtung passt: gehe zum blockierten Item und trage `follows` ein, oder gehe zum blockierenden Item und trage `precedes` ein.

### effectiveDay

Wenn ein Vorgänger noch nicht erledigt ist, schiebt der Kalender das abhängige Item automatisch auf einen späteren Anzeige-Tag:

```
effectiveDay(item) = max(effectiveDay(Vorgänger) + 1, item.day)
```

Dies wird rekursiv mit Zyklenerkennung berechnet. Erledigte Vorgänger (`done`-Feld gesetzt) blockieren nicht mehr.

**Zurückgestellte Items** — über ihren geplanten Tag hinausgeschoben — zeigen einen türkisen linken Rand (fixe Termine) oder eine gepunktete Unterstreichung (volatile Items). Der in `agenda.json` gespeicherte geplante Tag wird nicht verändert; die Verschiebung wird zur Renderzeit berechnet.

Abhängigkeit setzen: Bearbeitungspopup öffnen → genauen Titel des Ziel-Items in `follows` oder `precedes` eingeben → Speichern. Mehrere Items werden durch Komma getrennt.

---

## Speichern und Synchronisierung

| Auslöser | Verhalten |
|----------|-----------|
| Save-Schaltfläche | Schreibt den aktuellen Stand sofort in `agenda.json` |
| Auto-Save | Speichert automatisch alle 60 Sekunden bei ungespeicherten Änderungen |
| Tab versteckt | Speichert, wenn der Browser-Tab den Fokus verliert |
| Server-Merge | Beim Speichern werden Server-Items, die nicht in der aktuellen Ansicht sind, erhalten |

Die Save-Schaltfläche zeigt **✓**, wenn der aktuelle Stand mit dem Disk-Stand übereinstimmt. Jede Bearbeitung setzt sie auf **Save** zurück.

Server-seitige Items (von cato oder über die CLI zwischen Seitenladevorgängen hinzugefügt) werden beim Speichern zurückgelesen und in die Ausgabe gemischt — sie werden nicht überschrieben. Wiederkehrende Items werden über ihren `#recurring-*`-Tag identifiziert und als einzelne Anker-Items erhalten.

---

## Bereich

Die Schaltflächen **7 / 14 / 30** in der oberen Leiste setzen den sichtbaren Tagesbereich. Heute ist immer die erste Zeile. Der gewählte Bereich wird in `agenda.json` gespeichert und beim nächsten Laden wiederhergestellt.
