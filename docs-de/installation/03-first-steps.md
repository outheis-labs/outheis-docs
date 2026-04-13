
# Erste Schritte

Nach `outheis init` und `outheis start` diese Schritte durchgehen, um sicherzustellen, dass alles funktioniert.

---

## 1. Web-Oberfläche

[http://localhost:8080](http://localhost:8080) im Browser öffnen. Die outheis Web-Oberfläche sollte erscheinen.

Eine Nachricht im Chat eingeben und senden. Der Relay-Agent (ou) antwortet. Wenn eine Antwort kommt, funktionieren Dispatcher, Relay und der API-Schlüssel korrekt.

---

## 2. Terminal-Interface

In einem zweiten Terminalfenster:

```
outheis chat
```

Nachricht eingeben und Enter drücken. Derselbe Relay, anderes Interface. Nützlich für Scripting oder wenn kein Browser verfügbar ist.

---

## 3. Erste Agenten-Läufe

Sobald der Vault Daten enthält, die Agenten über die Web-Oberfläche anstoßen: Tab **Scheduler** öffnen und neben dem gewünschten Agenten auf **Run now** klicken.

- **Agenda** — erstellt die tägliche Übersicht aus dem Vault
- **Pattern** — extrahiert Memory aus Notizen und Gesprächen

Der Pattern-Agent benötigt einige Tage Verlauf für aussagekräftige Ergebnisse. Beim ersten Lauf findet er wenig — das ist normal.

Alternativ über das Terminal:

```
outheis task run agenda
outheis task run pattern
```

---

## 4. Signal

Zuerst die Telefonnummer mit signal-cli registrieren. Das geschieht außerhalb von outheis:

```
signal-cli -a +DEINENUMMER register
signal-cli -a +DEINENUMMER verify CODE
```

Dann die Web-Oberfläche öffnen, zu **Configuration** → **Signal** wechseln und **Bot phone** mit der registrierten Nummer ausfüllen. Über den **Restart**-Button im Tab **Overview** neu starten.

Eine Signal-Nachricht an die registrierte Nummer senden. outheis antwortet über Signal genauso wie über die Web-Oberfläche.

Details zu allen Transportkanälen: [Kommunikation](05-communication.md).
