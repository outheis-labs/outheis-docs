# Systemüberblick: Betriebssysteme und anwendbare Konzepte

Dieses Dokument gibt einen Überblick über Betriebssysteme und Architekturmuster, die für das Design von Multi-agent-KI-Systemen relevant sind.

---

## DragonFlyBSD

**Ursprung**: Abgespalten von FreeBSD 4.x im Jahr 2003 von Matthew Dillon
**Fokus**: SMP-Skalierbarkeit durch Message-Passing

### Relevante Konzepte

#### LWKT (Light Weight Kernel Threads)

Traditionelle Unix-Kernel verwenden einen Big Kernel Lock (BKL) oder Fein-Locking. Beides hat Probleme: BKL skaliert nicht; Fein-Locking ist komplex und deadlock-anfällig.

DragonFlyBSDs Ansatz: **Per-CPU-Scheduling mit Message-Passing**.

- Jede CPU betreibt ihren eigenen Scheduler
- Keine globale Run-Queue-Lock
- Threads migrieren zwischen CPUs über explizite Nachrichten

#### IPI-Message-Queues

Inter-Processor Interrupts (IPIs) übermitteln Nachrichten zwischen CPUs:

```
CPU 0                CPU 1                CPU 2
┌─────────┐          ┌─────────┐          ┌─────────┐
│ Queue 0 │          │ Queue 1 │          │ Queue 2 │
└────▲────┘          └────▲────┘          └────▲────┘
     │                    │                    │
     └────────────────────┴────────────────────┘
              Nachrichten gehen direkt zum Ziel
```

**Keine zentrale Queue**. Jede CPU hat ihre eigene. Produzenten schreiben in die Queue des Ziels; Konsumenten lesen nur aus ihrer eigenen.

#### Ownership-Semantik

Daten „gehören" einer CPU. Nur der Eigentümer modifiziert sie. Andere senden Nachrichten und fordern Änderungen an.

Das eliminiert:
- Lock-Contention
- Cache-Line-Bouncing
- Deadlocks

### Anwendbarkeit auf agent-Systeme

| DragonFlyBSD | agent-System |
|--------------|--------------|
| CPU | Agent |
| Per-CPU-Queue | Per-agent-Posteingang |
| IPI-Nachricht | Inter-agent-Nachricht |
| Ownership | Domain-Verantwortung |
| Keine geteilten Locks | Kein geteilter veränderbarer Zustand |

---

## Erlang/OTP

**Ursprung**: Entwickelt bei Ericsson für Telecom-Switches (1986)
**Fokus**: Fehlertoleranz, Parallelität, Hot-Code-Reloading

### Relevante Konzepte

#### Actor-Modell

Prozesse (Actors) sind:
- Isoliert (kein gemeinsamer Speicher)
- Durch PID identifiziert
- Kommunizieren nur über asynchrone Nachrichten

```
┌─────────┐    Nachricht    ┌─────────┐
│ Actor A │──────────────►  │ Actor B │
└─────────┘                 └─────────┘
     │                           │
     │    (kein gemeinsamer      │
     │         Zustand)          │
     └───────────────────────────┘
```

#### Supervision-Trees

Prozesse sind hierarchisch organisiert. Eltern überwachen Kinder:

```
        ┌──────────────┐
        │  Supervisor  │
        └──────┬───────┘
               │
    ┌──────────┼──────────┐
    ▼          ▼          ▼
┌───────┐ ┌───────┐ ┌───────┐
│Worker │ │Worker │ │Worker │
└───────┘ └───────┘ └───────┘
```

Supervisor-Strategien:
- **one_for_one**: Nur das fehlgeschlagene Kind neustarten
- **one_for_all**: Alle Kinder neustarten, wenn eines scheitert
- **rest_for_one**: Fehlgeschlagenes Kind und danach gestartete neustarten

#### „Let It Crash"

Nicht defensiv programmieren. Prozesse scheitern lassen. Der Supervisor startet sie in einem bekannten guten Zustand neu.

Das ist kontraintuitiv, aber leistungsstark: Fehlerbehandlung wird von der Geschäftslogik getrennt.

### Anwendbarkeit auf agent-Systeme

| Erlang/OTP | agent-System |
|------------|--------------|
| Prozess | Agent |
| PID | Agent-ID |
| Mailbox | Message-Queue |
| Supervisor | Dispatcher |
| Neustartstrategie | agent-Wiederherstellungsrichtlinie |
| Hot-Code-Reload | agent-Update ohne Ausfallzeit |

---

## seL4

**Ursprung**: Formal verifizierter Microkernel (NICTA/Data61)
**Fokus**: Sicherheit durch minimale Trusted Computing Base

### Relevante Konzepte

#### Capabilities

Eine Capability ist ein unfälschbares Token, das spezifische Rechte für ein spezifisches Objekt gewährt.

```
┌─────────────────────────────────────┐
│ Capability                          │
│                                     │
│  Object: FileHandle_42              │
│  Rights: Read, Write                │
│  Holder: Process_7                  │
└─────────────────────────────────────┘
```

Man kann nur zugreifen, wofür man Capabilities hat. Keine Ambient Authority.

#### Minimaler Kernel

seL4s Kernel bietet nur:
- Threads
- Adressräume
- IPC
- Capability-Verwaltung

Alles andere (Dateisysteme, Treiber, Netzwerke) läuft im User Space.

### Anwendbarkeit auf agent-Systeme

| seL4 | agent-System |
|------|--------------|
| Capability | Berechtigungs-Token |
| Objekt | Ressource (Datei, API, Domain) |
| Rechte | Lesen, schreiben, ausführen, delegieren |
| Minimaler Kernel | Minimaler dispatcher |

Beispiel: Ein Pattern-agent hat Schreib-Capability für insights; andere haben nur Lese-Capability.

---

## OpenBSD

**Ursprung**: Abgespalten von NetBSD im Jahr 1995 von Theo de Raadt
**Fokus**: Sicherheit, Korrektheit, Einfachheit

### Relevante Konzepte

OpenBSD hat viele Sicherheitsinnovationen beigetragen. Für agent-Architekturen sind zwei besonders anwendbar:

#### pledge(2)

Ein Prozess erklärt vorab, welche Syscall-Klassen er benötigt. Nach dem Pledge terminiert jeder andere Syscall den Prozess.

```c
pledge("stdio rpath", NULL);  // Only stdio and read-only file access
// From here: no network, no write, no exec—enforced by kernel
```

Das ist **selbst auferlegte Einschränkung**. Der Prozess gibt Capabilities auf, die er nicht braucht.

#### unveil(2)

Ein Prozess erklärt, auf welche Dateisystempfade er zugreifen kann. Alles andere wird unsichtbar.

```c
unveil("/var/data", "r");   // Read-only access to /var/data
unveil("/tmp", "rwc");      // Read, write, create in /tmp
unveil(NULL, NULL);         // Lock it down—no more unveil calls allowed
```

Nach dem letzten `unveil(NULL, NULL)` kann der Prozess seine Sicht nicht erweitern. Das Dateisystem ist effektiv auf die deklarierten Pfade geschrumpft.

#### Privilegtrennung

OpenBSD-Daemons teilen sich in zwei Prozesse auf:

```
┌─────────────────┐
│ Parent (root)   │  ← Hält Socket, Keys, minimalen Code
└────────┬────────┘
         │ fork
         ▼
┌─────────────────┐
│ Child (nobody)  │  ← Parst Eingabe, erledigt Arbeit, unprivilegiert
└─────────────────┘
```

Der Child-Prozess verarbeitet nicht vertrauenswürdige Eingabe. Wenn er kompromittiert wird, hat er keine Privilegien. Der Elternteil führt nur minimale, auditierte Operationen im Namen des Kindes durch.

#### Historischer Kontext: Jails und Container

Prozessisolation hat sich durch mehrere Stufen entwickelt: chroot (1979), FreeBSD-Jails (1999), Solaris-Zones, Linux-Container, Docker. Diese bieten **statische Isolation** — du baust den Container, dann läufst du darin.

pledge/unveil repräsentieren einen anderen Ansatz: **dynamische Einschränkung**. Ein Prozess startet mit vollen Capabilities und gibt sie schrittweise auf, während er sich initialisiert. Das ist oft praktischer für Anwendungen, die Ressourcen beim Start, aber nicht während des Betriebs benötigen.

### Anwendbarkeit auf agent-Systeme

| OpenBSD | agent-System |
|---------|--------------|
| pledge | agent erklärt Capabilities beim Start |
| unveil | agent sieht nur relevante Pfade |
| privsep | dispatcher privilegiert, agents eingeschränkt |
| Sicher per Standard | Keine impliziten Berechtigungen |

Beispiel: Ein Daten-agent pledged `["vault:read", "vault:write"]` und unveiled nur `vault/`. Er kann nicht auf `human/` zugreifen, keine Netzwerkanrufe machen, keinen Code ausführen.

---

## macOS / Darwin

**Ursprung**: Apples XNU-Kernel, kombiniert Mach-Microkernel mit BSD
**Fokus**: Verbraucherfreundlichkeit mit Unix-Unterbau

### Relevante Konzepte

#### Grand Central Dispatch (GCD)

Ein systemweites Framework für parallele Ausführung. Statt Threads direkt zu verwalten, wird Arbeit in Dispatch-Queues eingereicht:

```
┌─────────────────────────────────────────┐
│           Dispatch Queues               │
├─────────────────────────────────────────┤
│  Main Queue      │ Seriell, UI-Thread   │
├──────────────────┼──────────────────────┤
│  Global Queues   │ Parallel, nach       │
│  (QoS-Stufen)    │ Priorität:           │
│                  │  - User Interactive  │
│                  │  - User Initiated    │
│                  │  - Utility           │
│                  │  - Background        │
├──────────────────┼──────────────────────┤
│  Custom Queues   │ Seriell oder parallel│
└──────────────────┴──────────────────────┘
```

Das System verwaltet Thread-Pools. Du sagst einfach „mach diese Arbeit" und „wie wichtig ist sie".

#### Quality of Service (QoS)

Arbeit wird mit ihrer Prioritätsstufe markiert. Das System kann:
- Hintergrundarbeit drosseln, wenn der Nutzer aktiv ist
- Priorität erhöhen, wenn Ergebnisse sofort benötigt werden
- Energieverbrauch auf Laptops/Phones ausbalancieren

### Anwendbarkeit auf agent-Systeme

| GCD | agent-System |
|-----|--------------|
| Dispatch-Queue | agent-Message-Queue |
| QoS-Stufen | agent-Priorität |
| Main Queue | Nutzerseitiger relay-agent |
| Background Queue | Pattern-recognition-agent |
| Serielle Queue | Sequentielle Operationen (Schreibvorgänge) |
| Parallele Queue | Parallele Operationen (Lesevorgänge) |

Beispiel: Ein relay-agent, der Nutzereingaben verarbeitet, läuft mit hoher Priorität. Ein Pattern-agent, der Geschichte analysiert, läuft im Hintergrund. Der dispatcher verwaltet Queue-Prioritäten basierend auf Systemlast und Nutzeraktivität.

---

## Plan 9

**Ursprung**: Bell Labs (1980er–2000er), Nachfolger von Unix
**Fokus**: Verteilte Systeme, einheitliche Schnittstellen

### Relevante Konzepte

#### Alles ist eine Datei

Nicht nur Dateien und Geräte — Prozesse, Netzwerkverbindungen, Fenster, sogar andere Maschinen erscheinen als Dateien.

```
/proc/42/mem      # Prozess-Speicher
/net/tcp/clone    # Neue TCP-Verbindung
/mnt/remote/      # Dateisystem einer Remote-Maschine
```

#### 9P-Protokoll

Ein einfaches Protokoll für den Dateizugriff über ein Netzwerk. Jede Ressource, die 9P implementiert, kann eingehängt und einheitlich zugegriffen werden.

#### Per-Prozess-Namespaces

Jeder Prozess kann seine eigene Sicht auf das Dateisystem haben. Das Einhängen von Ressourcen ist lokal zum Prozess.

### Anwendbarkeit auf agent-Systeme

| Plan 9 | agent-System |
|--------|--------------|
| Datei | Ressource |
| 9P | Ressourcenzugriffsprotokoll |
| Mount | Wissensdatenbank einbinden |
| Namespace | agent-Sicht auf verfügbare Ressourcen |

Beispiel: Ein vault wird in den Namespace eines agents eingehängt. Der agent interagiert damit durch eine einheitliche dateiähnliche Schnittstelle.

---

## Event Sourcing

**Ursprung**: Domain-Driven-Design-Community
**Fokus**: Zustand als abgeleitet aus unveränderlichen Ereignissen

### Relevante Konzepte

#### Append-Only-Log

Zustand wird nicht direkt gespeichert. Stattdessen werden Ereignisse an ein unveränderliches Log angehängt:

```
┌─────────────────────────────────────────────┐
│ Event Log                                   │
│                                             │
│ 1. UserCreated {id: 1, name: "..."}         │
│ 2. UserEmailChanged {id: 1, email: "..."}   │
│ 3. UserDeleted {id: 1}                      │
└─────────────────────────────────────────────┘
```

Aktueller Zustand = Fold über alle Ereignisse.

#### Vorteile

- **Audit-Trail**: Vollständige Geschichte
- **Replay**: Jeden vergangenen Zustand rekonstruieren
- **Debugging**: Genau sehen, was passiert ist
- **Temporale Abfragen**: „Was war der Zustand zu Zeit T?"

### Anwendbarkeit auf agent-Systeme

| Event Sourcing | agent-System |
|----------------|--------------|
| Ereignis | Nachricht |
| Ereignislog | Message-Queue (append-only) |
| Projektion | Aktueller Gesprächszustand |
| Replay | Debuggen, wiederholen, wiederherstellen |

---

## Unikernels

**Ursprung**: Akademische Forschung (MirageOS, IncludeOS, Nanos)
**Fokus**: Einzelzweck, minimale Angriffsfläche

### Relevante Konzepte

#### Library Operating System

Die Anwendung verlinkt direkt gegen OS-Bibliotheken. Kein separater Kernel. Das Ergebnis ist ein einzelnes bootfähiges Image.

```
Traditionell:
┌─────────────┐
│ Anwendung   │
├─────────────┤
│   Kernel    │
└─────────────┘

Unikernel:
┌─────────────────────┐
│ Anwendung + LibOS   │
└─────────────────────┘
```

#### Spezialisierung

Jeder Unikernel macht eine Sache. Keine Shell, keine Benutzer, keine unnötigen Treiber.

### Anwendbarkeit auf agent-Systeme

| Unikernel | agent-System |
|-----------|--------------|
| Einzelzweck-Image | Einzelzweck-agent |
| Keine Shell | Keine allgemeinen Capabilities |
| Minimale Oberfläche | Minimaler Prompt, fokussierte Rolle |

Beispiel: Ein action-agent ist spezialisiert — er führt Aufgaben aus. Er analysiert keine Muster oder verfasst keine Nachrichten.

---

## Vergleichsmatrix

| System | Primärer Beitrag | Schlüsselmechanismus |
|--------|-----------------|---------------------|
| DragonFlyBSD | Skalierbare Parallelität | Per-CPU-Queues, Ownership |
| Erlang/OTP | Fehlertoleranz | Supervision, let it crash |
| seL4 | Formale Sicherheit | Capabilities |
| OpenBSD | Praktische Sicherheit | pledge, unveil, privsep |
| macOS/GCD | Prioritäts-Scheduling | QoS-markierte Dispatch-Queues |
| Plan 9 | Einheitlicher Zugang | Alles ist eine Datei |
| Event Sourcing | Auditierbarkeit | Append-only-Log |
| Unikernels | Minimalismus | Einzelzweck-Images |

---

## Synthese für agent-Architekturen

Ein gut entworfenes Multi-agent-System kann kombinieren:

1. **DragonFlyBSDs Message-Passing** für agent-Kommunikation
2. **Erlangs Supervision** für Fehlertoleranz
3. **seL4s Capabilities** für formale Zugangskontrolle
4. **OpenBSDs pledge/unveil** für praktische, selbst auferlegte Einschränkungen
5. **GCDs Prioritäts-Queues** für Workload-Management
6. **Plan 9s einheitliche Schnittstelle** für Ressourcenzugang
7. **Event-Sourcings append-only-Log** für Auditierbarkeit
8. **Unikernels Spezialisierung** für fokussierte agent-Rollen

Das sind keine konkurrierenden Ansätze — sie addressieren orthogonale Belange und kombinieren sich natürlich.

---

Weiter: [03-architecture.md](03-architecture.md) — Die outheis-Architektur, abgeleitet aus diesen Prinzipien.
