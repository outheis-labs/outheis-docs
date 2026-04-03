# Verwandte Arbeiten

Dieses Dokument gibt einen Überblick über bestehende Forschungsarbeiten zur Anwendung von Betriebssystemprinzipien auf KI-Agenten-Architekturen.

---

## Das entstehende Forschungsfeld

Die Anwendung von Betriebssystemkonzepten auf KI-Agenten-Systeme ist ein junges, aber wachsendes Forschungsgebiet. Neuere Arbeiten erkennen, dass Agenten-Architekturen mit Herausforderungen konfrontiert sind, die Betriebssysteme vor Jahrzehnten gelöst haben.

Wie eine aktuelle Arbeit beobachtet: "Heutige Agenten-Architekturen ähneln der Vor-Betriebssystem-Ära des Rechnens — einem Chaos duplizierter Lösungen, dem grundlegende Abstraktionen für Ressourcenverwaltung, Isolation und Koordination fehlen."

---

## Wichtige Publikationen

### AIOS: LLM Agent Operating System

**Quelle**: arXiv 2403.16971, COLM 2025

Die direkteste verwandte Arbeit. AIOS schlägt einen OS-Kernel für LLM-basierte Agenten vor mit:

- Scheduler für die Verteilung von Agenten-Anfragen
- Kontextmanager mit Snapshot/Wiederherstellung (analog zum Prozess-Kontextwechsel)
- Memory-Manager für Laufzeitoperationen
- Storage-Manager für Persistenz
- Zugangskontrolle für Agenten-Berechtigungen

Kernidee: LLMs werden als Kerne behandelt, analog zu CPU-Kernen, mit einer einheitlichen Schnittstelle für verschiedene LLM-Endpunkte.

**Unterschied zu outheis**: AIOS fokussiert auf mandantenfähiges Agenten-Serving mit Performance-Optimierung. outheis fokussiert auf persönlichen Assistenten mit Datenschutzgarantien und Klartext-Datenarchitektur.

### Agent Operating Systems (Agent-OS)

**Quelle**: Preprints.org, 2025

Schlägt eine geschichtete Architektur vor:

1. Kernel-Ebene
2. Ressourcen- & Dienste-Ebene
3. Agenten-Laufzeit-Ebene
4. Orchestrierungs- & Workflow-Ebene
5. Benutzer- & Anwendungsebene

Betont Echtzeitgarantien und Sicherheitsprimitive für autonome Systeme.

**Unterschied zu outheis**: Agent-OS zielt auf Enterprise/SmartTech-Szenarien mit formaler Verifikation. outheis zielt auf persönlichen Einsatz mit Einfachheit und Transparenz.

### Multi-Agent Memory from a Computer Architecture Perspective

**Quelle**: arXiv 2603.10062, 2026

Rahmt Multi-Agenten-Memory als Computerarchitektur-Problem:

- Unterscheidet gemeinsame und verteilte Memory-Paradigmen
- Schlägt eine Drei-Schichten-Hierarchie vor: I/O, Cache, Memory
- Identifiziert Cache-Sharing und Memory-Konsistenz als kritische Lücken

Kernidee: "Agent-Performance ist ein End-to-End-Datenbewegungsproblem."

**Relevanz für outheis**: Validiert unsere indexbasierte Zugriffsstrategie und die Unterscheidung zwischen heißem (messages.jsonl) und kaltem (archive/) Speicher.

### Integrating AI into Operating Systems: A Survey

**Quelle**: arXiv 2407.14567, 2025

Umfassende Übersicht, die zwei Richtungen abdeckt:

1. **KI für BS**: ML/LLM-Techniken zur Verbesserung von BS (Scheduling, Memory, Sicherheit)
2. **BS für KI**: Betriebssystem-Architektur-Innovationen zur Unterstützung von KI-Workloads

Identifiziert drei Paradigmen:
- KI-Integration auf Kernel-Ebene
- Agenten-vermittelte Workflows
- LLM-als-OS-Abstraktion

**Relevanz für outheis**: Bestätigt die Gültigkeit der Anwendung von BS-Prinzipien auf Agenten-Design; liefert Vokabular und Rahmen.

### Modeling an Operating System Based on Agents

**Quelle**: Springer HAIS 2012

Frühe Arbeit, die BS-Modellierung mit Multi-Agenten-Paradigmen vorschlägt, unter Berücksichtigung interaktionsbasierter Berechnung und Cloud Computing.

**Relevanz für outheis**: Zeigt, dass dies keine völlig neue Idee ist, aber vor der LLM-Ära entstand.

### The Orchestration of Multi-Agent Systems

**Quelle**: arXiv 2601.13671, 2026

Technischer Entwurf für Enterprise-Multi-Agenten-Systeme:

- Model Context Protocol (MCP) für Tool-Zugriff
- Agent-to-Agent (A2A)-Protokoll für Peer-Koordination
- Governance-Frameworks und Observability

**Unterschied zu outheis**: Fokussiert auf Enterprise-Orchestrierung mit komplexen Protokollen. outheis verwendet einfaches Message Passing mit append-only-Warteschlange.

---

## Konzeptionelle Parallelen

| BS-Konzept | AIOS | Agent-OS | outheis |
|------------|------|----------|---------|
| Kernel | LLM-Kernel mit Modulen | Geschichtete Ebenen | Dispatcher (kein LLM) |
| Scheduling | FIFO, Round Robin | Echtzeitgarantien | Priorität + Schlüsselwörter |
| Memory | K-LRU-Verdrängung | Drei-Schichten-Hierarchie | Index + Lazy Load |
| IPC | System-Aufrufe | Protokolle (MCP, A2A) | Nachrichtenwarteschlange (JSONL) |
| Zugangskontrolle | Privileggruppen | Sicherheitsprimitive | Fähigkeiten (pledge/unveil) |
| Kontextwechsel | Logit-basierter Snapshot | Nicht spezifiziert | Gesprächsarchivierung |

---

## Was outheis unterscheidet

### 1. Privacy-First-Architektur

Die meisten verwandten Arbeiten setzen mandantenfähiges Cloud-Deployment voraus. outheis zielt auf zwei Modi: Persönlicher Assistent (Einzelbenutzer, local-first) und Domain-Expert-Assistent (spezialisierter Wissensdienst). Beide priorisieren Datenschutz:

- Benutzerdaten nur in `human/` und `vault/`
- Entfernen von `human/` löscht alle Benutzerspuren
- Keine Telemetrie, keine Cloud-Abhängigkeit (optional)

### 2. Klartext-Datenphilosophie

Verwandte Arbeiten verwenden typischerweise Datenbanken oder spezialisierte Speicherung. outheis verwendet:

- Markdown-Dateien mit Tags (prospektive Informationsarchitektur)
- JSONL für strukturierte Daten (Nachrichten, Index, Importe)
- Menschenlesbare, werkzeugunabhängige Formate

Dies lehnt sich an die Unix-Philosophie an, nicht an die Datenbanktradition.

### 3. Einfachheit vor Leistung

AIOS optimiert für Durchsatz (2,1× schnellere Ausführung). outheis optimiert für:

- Verständlichkeit (statischer Dispatcher, kein LLM im Routing)
- Nachvollziehbarkeit (append-only-Log)
- Deployment-Flexibilität (von Cloud-minimal bis lokal-maximal)

### 4. Persönliche Handlungsfähigkeit

Das Agenda-Agenten-Konzept — Benutzerhandlungsfähigkeit durch intelligentes Filtern ermöglichen — findet sich nicht in enterprise-fokussierten verwandten Arbeiten.

---

## Theoretische Grundlagen

Die verwandten Arbeiten stützen sich hauptsächlich auf:

- **Verteilte Systeme**: Message Passing, Konsens, Fehlertoleranz
- **Betriebssysteme**: Scheduling, Memory-Hierarchie, Zugangskontrolle
- **Software-Architektur**: Microservices, Event Sourcing

outheis zieht zusätzlich aus:

- **Informationswissenschaft**: Prospektive vs. retrospektive Architektur
- **Unix-Philosophie**: Klartext, kleine Werkzeuge, Kombinierbarkeit
- **Erlang/OTP**: Actor-Modell, Supervision, Let-it-crash

---

## Offene Forschungsfragen

Die Literatur identifiziert mehrere offene Probleme, die für outheis relevant sind:

1. **Memory-Konsistenz** in Multi-Agenten-Systemen
2. **Cache-Sharing**-Protokolle zwischen Agenten
3. **Kontextmanagement** für lang laufende Gespräche
4. **Tag-Harmonisierung** über LLM (in unserer theoretischen Arbeit behandelt)

---

## Referenzen

1. Mei, K., Li, Z., et al. (2024). AIOS: LLM Agent Operating System. arXiv:2403.16971. COLM 2025.

2. Agent Operating Systems (Agent-OS): A Foundational Specification. Preprints.org, 2025.

3. Multi-Agent Memory from a Computer Architecture Perspective. arXiv:2603.10062, 2026.

4. Integrating Artificial Intelligence into Operating Systems: A Survey. arXiv:2407.14567, 2025.

5. Cámara, J.P., et al. (2012). Modeling an Operating System Based on Agents. HAIS 2012, Springer.

6. The Orchestration of Multi-Agent Systems: Architectures, Protocols, and Enterprise Adoption. arXiv:2601.13671, 2026.

7. Ge, Y., et al. (2023). LLM as OS, Agents as Apps: Envisioning AIOS, Agents and the AIOS-Agent Ecosystem.

---

## Fazit

Die Anwendung von Betriebssystemprinzipien auf KI-Agenten-Architekturen ist ein aktives Forschungsgebiet. Bestehende Arbeiten konzentrieren sich primär auf Performance-Optimierung für Enterprise-Multi-Agenten-Systeme. outheis trägt eine komplementäre Perspektive bei: Privacy-First-Architektur für persönliche Assistenten mit Klartext-Datenphilosophie und Betonung von Benutzerhandlungsfähigkeit.

Die theoretische Grundlage, die prospektive Informationsarchitektur mit Agenten-Design verknüpft (siehe: [Temporalization of Order](https://github.com/outheis-labs/research-base/blob/main/temporalization-of-order/temporalization-of-order.md)), scheint neuartig und wird in der aktuellen Literatur nicht behandelt.
