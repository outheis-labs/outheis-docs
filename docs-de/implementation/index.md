# Implementierung

*Der aktuelle Stand — was gebaut ist und wie man es benutzt.*

---

## Dokumente

### [Architektur](01-architecture.html)

Aktuelle Systemarchitektur: dispatcher, agents, Wissensspeicher, Datei-Layout, geplante Aufgaben.

### [Memory & Rules](02-memory.html)

Wie outheis sich erinnert: Memory-Typen, explizite Marker, Muster-Extraktion, Rules-Entstehung.

### [Agenda](03-agenda.html)

Zeitmanagement durch Agenda.md, Exchange.md. Stündliche Überprüfung, manuelle Aktualisierung, Hash-basierte Optimierung.

### [Skills](04-skills.html)

Wie agents wissen, was zu tun ist: System-Skills, gelernte Skills, der Unterschied zwischen Skills und Rules.

### [Code-Agent](05-alan.html)

Code-Intelligenz-Agent für Entwicklungsumgebungen. Standardmäßig deaktiviert.

### [Action-Agent](06-hiro.html)

Externer Aktions-Agent: Aufgabenplanung, E-Mail, Kalendereinträge. Noch nicht implementiert.

### [Signal](07-signal.html)

Signal Messenger Transport: Leser-Thread-Architektur, Markdown-Entfernung, Autorisierung, Sprachtranskription.

### [Annotations-Feedback-Schleife](08-annotation-feedback.html)

Wie `>`-Annotationen in Agenda.md in den Memory-Stack geroutet werden — die drei Annotationstypen und die cato+rumi-Implementierung.

### [Vault](09-vault.html)

Wie du dein Wissen strukturierst: Datei-Layout, Tag-Systeme, das facettierte Namensraum-Muster.

### [Konfiguration](10-config.html)

Vollständige `config.json`-Referenz: Anbieter, Modelle, agents, Zeitpläne.

### [Erste Schritte](11-guide.html)

Installation, erster Start, Befehle, Nutzungsbeispiele.

### [Migration](12-migration.html)

Bestehendes Wissen in outheis bringen: vault/Migration-Workflow, Genehmigung über Checkboxen.

### [Web UI](13-webui.html)

Lokale Administrationsoberfläche: Konfiguration, Scheduler, Memory- und Rules-Editor, Vault-Browser.
