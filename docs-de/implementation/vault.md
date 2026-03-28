---
title: Vault
---

# Vault

*Wie du dein Wissen strukturierst, damit outheis damit arbeiten kann.*

## Was der Vault ist

Der Vault ist ein Verzeichnis mit Markdown-Dateien — deine Notizen, Projekte, Dokumente, Zeitpläne. outheis liest ihn, besitzt ihn aber nicht. Du bringst die Struktur; outheis lernt, darin zu navigieren.

Das einzige erforderliche Unterverzeichnis ist `Agenda/`, das outheis verwaltet:

```
vault/
├── Agenda/
│   ├── Daily.md      # Today — schedule, tasks, notes
│   ├── Inbox.md      # Quick capture, unprocessed
│   └── Exchange.md   # Async communication with outheis
└── ... your files
```

Alles andere gehört dir.

## Tags

outheis schreibt kein Tag-Schema vor. Es erlernt deines.

Wenn du outheis zum ersten Mal startest, sind deine Vault-Tags unbekannt. Der Data-Agent kann deine Tag-Taxonomie scannen und extrahieren — aber nur wenn du fragst. Keine automatische Umstrukturierung, keine erfundenen Tags.

Die eine Ausnahme: Datum-Tags. Wenn outheis eine Notiz erstellt oder kommentiert, kann es einen `#date-JJJJ-MM-TT`-Tag hinzufügen, um sie zeitlich zu verankern. Alles andere bleibt unberührt.

### Tag-Systeme variieren

Benutzer kommen mit verschiedenen Konventionen:

```
#todo #project #someday          ← flat, singular
#work/client/project             ← hierarchical with /
#action-required #status-active  ← namespaced with -
```

All das funktioniert. outheis kartiert das Gefundene und arbeitet innerhalb dieser Struktur.

### Das facettierte Namensraum-Muster

Eine besonders effektive Konvention für persönliches Wissensmanagement verwendet einen `Kategorie-Wert`-Namensraum mit Bindestrichen:

```
#action-required   #action-waiting   #action-now
#status-active     #status-completed #status-linger
#rank-urgent       #rank-high        #rank-low
#unit-work         #unit-self        #unit-family
#topic-design      #topic-admin
#size-S            #size-M           #size-L
#recurring
```

Jeder Tag trägt zwei Informationen: welche Dimension er beschreibt (`action`, `status`, `rank`) und welchen Wert er enthält (`required`, `active`, `urgent`). Das macht Dateien entlang mehrerer Achsen abfragbar ohne verschachtelte Ordner oder komplexe Metadaten.

Die zeitliche Dimension dieses Musters — wie zeitverankerte Tags mit wiederkehrender Struktur interagieren — wird in der [research-base](https://github.com/outheis-labs/research-base/tree/main/temporalization-of-order) untersucht.

### Datum-Tags

Datum-Tags (`#date-2026-03-24`) sind eine Kategorie, die outheis selbst erzeugen kann. Beim Erstellen von Notizen oder Erfassen von Informationen fügt der Data-Agent einen Datum-Tag hinzu, um den Eintrag zeitlich zu verankern. Alle anderen Tags gehören dem Benutzer.

### Interne Tags

outheis verwendet den `#outheis-`-Namensraum für seine eigene interne Zustandsverfolgung. Diese Tags werden dem Benutzer in der WebUI nie angezeigt und dienen nur Agenten-Operationen — Markierung verarbeiteter Einträge, Archivierungskandidaten, Zustandsmarker.

Beispiele: `#outheis-state-done`, `#outheis-state-pending`, `#outheis-archive`

`#outheis-*`-Tags sind immer auf Englisch. Sie werden sparsam und nur dann erstellt, wenn sie einer zukünftigen Agenten-Operation echten Mehrwert bieten.

### Tag-Analyse

outheis erlernt dein Tag-System auf Anfrage, nicht automatisch. Zum Starten:

```
analyze tags
```

Der Data-Agent scannt den Vault, extrahiert die Tag-Taxonomie und reflektiert sie zurück. Du bestätigst oder korrigierst die Interpretation. Von diesem Punkt an funktionieren Suche und Tagesplanung innerhalb deines etablierten Systems.

Wenn der Data-Agent später Inkonsistenzen oder mögliche Vereinfachungen bemerkt — eine Kategorie mit nur einem Wert, zwei Tags die immer gemeinsam auftauchen, ein Benennungsmuster das vereinheitlicht werden könnte — bringt er das direkt im Gespräch auf. Ohne deine Zustimmung werden keine Änderungen gemacht.

## Daily.md

Daily.md wird täglich frisch vom Agenda-Agenten erstellt. Die Standardstruktur:

```markdown
# [Weekday], [Date]

## Morning

## Schedule

## Tasks

## Notes

## Evening
```

Der Agenda-Agent füllt dies aus deinem Vault: geplante Termine, wiederkehrende Einträge, heute fällige Aufgaben, Einträge aus Inbox.md. Wenn dein Vault einen Terminplan, einen wiederkehrenden Zeitplan oder datum-markierte Einträge enthält, erscheinen sie hier automatisch.

Du kannst die Vorlage ändern. Gib deine bevorzugte Struktur in `rules/agenda.md` an:

```markdown
Daily.md should use these sections: [your sections here]
```

## Inbox.md

Schnellerfassung ohne Reibung. Schreibe alles — getippt, diktiert, beliebiges Format. Der Agenda-Agent verarbeitet Inbox-Einträge bei der stündlichen Überprüfung: verschiebt sie nach Daily.md, erstellt Vault-Notizen oder fragt in Exchange.md nach, wenn etwas Klärung benötigt.

Format ist frei. Eine Zeile pro Eintrag reicht.

## Exchange.md

Asynchrone Kommunikation zwischen dir und outheis. Fragen, die keine sofortige Antwort benötigen, Vorschläge die Überprüfung brauchen, Informationen die auf deine Eingabe warten.

outheis schreibt hier, wenn es etwas von dir braucht. Du antwortest, wenn du Zeit hast. Keine Benachrichtigungen, kein Druck.
