# Information und Semantik

*Warum Information nicht gleich Daten ist — und was das für ein persönliches KI-System bedeutet.*

---

## Die Lücke, die Shannon offenließ

Souveränität legt fest, wer das System kontrolliert. Aber es gibt eine vorgelagerte Frage: was sollte ein System mit dem tun, was es über dich lernt?

1948 veröffentlichte Claude Shannon *A Mathematical Theory of Communication* — eines der folgenreichsten Papiere in der Geschichte der Wissenschaft. Er zeigte, wie man Information als statistische Größe messen kann: je unerwarteter eine Botschaft, desto mehr Information trägt sie. Seine Entropieformel funktioniert mit perfekter Präzision für die Ingenieursprobleme, die ihn interessierten — Rauschen, Kompression, Kanalkapazität.

Shannon war explizit darin, was er nicht tat. „Die semantischen Aspekte der Kommunikation", schrieb er, „sind für das Ingenieursproblem irrelevant." Er klammerte Bedeutung bewusst aus. Seine Theorie sagt dir, wie man Daten zuverlässig überträgt. Sie sagt nichts darüber, ob irgendetwas davon wichtig ist, worauf es sich bezieht oder ob es wahr ist.

Das ist kein Fehler. Es ist eine Grenze. Der Fehler besteht darin, sie als vollständige Informationstheorie zu behandeln.

Jedes KI-System, das auf statistischem Pattern-Matching aufbaut — einschließlich großer Sprachmodelle — erbt diese Grenze. Die zugrunde liegende Mathematik ist Shannons: das nächste Token vorhersagen, Vorhersagefehler minimieren, Wahrscheinlichkeit maximieren. Bedeutung ist nicht im Modell; sie wird vom Leser projiziert. Ein System, das nur statistisch ist, kann Daten unbegrenzt anhäufen, ohne jemals etwas zu wissen.

---

## Die Frage der Bedeutung

Die Jahrzehnte nach Shannon brachten mehrere Versuche, die Informationstheorie in den semantischen Bereich zu erweitern.

**Carnap und Bar-Hillel** (1952) unternahmen den ersten formalen Versuch. Innerhalb der Logik definierten sie semantische Information als die Menge möglicher Sachverhalte, die ein Satz ausschließt — je mehr er ausschließt, desto mehr sagt er. Das war elegant, enthüllte aber sofort ein Paradox: ein Widerspruch schließt *alles* aus und sollte daher maximale Information tragen. Doch Widersprüche sind falsch, und falsche Aussagen sind schlechte Kandidaten für maximalen Informationsgehalt. Die Theorie bot keinen prinzipiellen Weg, sie auszuschließen.

**Fred Dretske** (1981) näherte sich dem Problem anders. In *Knowledge and the Flow of Information* definierte er Information in Begriffen kausaler Abhängigkeit: ein Signal trägt Information über eine Quelle, wenn es eine gesetzmäßige, zuverlässige Verbindung zwischen ihnen gibt. Rauch trägt Information über Feuer nicht aufgrund einer Konvention, sondern aufgrund der physikalischen Beziehung zwischen ihnen. Information existiert in der Welt; sie wird nicht durch Konvention zugewiesen. Und Wissen ist das, was passiert, wenn ein solches Signal eine Überzeugung verursacht: etwas zu *wissen* bedeutet, eine Überzeugung zu haben, die durch ein echtes informationstragendes Signal erzeugt wurde.

Das ist für jedes System relevant, das behauptet, Wissen zu verwalten. Die Frage ist nicht nur, ob Daten gespeichert werden, sondern ob gespeicherte Repräsentationen mit etwas Realem über die Person verbunden sind, der das System dienen soll.

**Gregory Bateson** (1972) bot vielleicht die komprimierteste Definition: Information ist „ein Unterschied, der einen Unterschied macht". Ein Unterschied in der Welt und ein Unterschied im Beobachter — beides ist erforderlich. Daten, die keine Veränderung im empfangenden System erzeugen, sind in keinem sinnvollen Sinne Information. Relevanz ist keine Eigenschaft, die Information nachträglich hinzugefügt wird; sie ist Teil dessen, was etwas überhaupt zu Information macht.

**Luciano Floridi** (2004, 2011) brachte diese Fäden in einer formalen Theorie zusammen. Seine Definition: semantische Information ist *wohlgeformte, bedeutungsvolle und wahre* Daten. Die dritte Bedingung — Wahrhaftigkeit — ist die umstrittenste und wichtigste. Floridi argumentiert, dass ein Signal, das die Welt falsch darstellt, keine Information über die Welt trägt; es trägt Rauschen, das wie Information aussieht. Er nennt das die Veridicality-These.

Die Debatte geht weiter. Scarantino und Piccinini (2010) argumentieren, dass Information keine Wahrheitsbedingung erfordert — dass kognitive Systeme und Ingenieurspraxis „Information" auf Weisen verwenden, die Falschheit erlauben. Die Meinungsverschiedenheit ist nicht rein akademisch: sie bestimmt, welche Verpflichtungen ein Wissensmanagement-System gegenüber Genauigkeit hat.

---

## Was das für outheis bedeutet

Diese Unterscheidungen sind nicht abstrakt. Jede hat direkte Konsequenzen dafür, wie ein persönliches KI-System gestaltet sein sollte.

**Die Daten/Information-Lücke** ist der Unterschied zwischen einem System, das alles protokolliert, und einem, das versteht, was es wert ist, behalten zu werden. Ein Gespräch, das stattgefunden hat, ist eine Tatsache — ein Datum. Dass du konsequent morgendliche Termine bevorzugst, ist *Information* im Sinne von Dretske: ein zuverlässiges Muster, das kausal mit deinem tatsächlichen Verhalten verbunden ist. Ein System, das nur protokolliert, kann sie nicht unterscheiden. outheis macht diese Unterscheidung explizit: Nachrichten werden protokolliert, Muster werden destilliert, und der Destillationsprozess ist nicht automatisch, sondern evaluativ.

**Batesons Relevanzkriterium** ist das Gestaltungsprinzip hinter der Destillation. Die Frage ist nicht „was sollen wir speichern?", sondern „was erzeugt einen Unterschied im zukünftigen Verhalten?" Skills ersetzen lange Erklärungen nicht weil sie kürzer sind, sondern weil sie die Aufmerksamkeit anders lenken — sie verändern, was der agent tut. Eine Anweisung, die nie aktiviert wird, ist keine Information; sie ist gespeicherter Text. Destillation ist keine Kompression; sie ist ein Urteil darüber, was einen Unterschied macht.

**Floridis Veridicality-Prinzip** erklärt, warum der Pattern-agent eher verwirft als anhäuft. Ein Gedächtnissystem, das falsche oder veraltete Einträge toleriert, degradiert nicht graceful — es wird in dem Maß unzuverlässig, wie das enthaltene Rauschen zunimmt. Die Frage „ist das noch wahr?" ist keine Ordnungsfreundlichkeit; sie ist konstitutiv dafür, ob der Eintrag überhaupt Information ist. Vergessen ist in outheis eine Form epistemischer Hygiene.

**Die DIKW-Unterscheidung** (Ackoff, 1989) — Daten, Information, Wissen, Weisheit — erklärt, warum outheis Gedächtnis, Skills und Regeln in separate Ebenen aufteilt. Das sind keine technischen Kategorien, die aus Implementierungsbequemlichkeit erfunden wurden. Das Gedächtnis hält, was dir eigen ist: Ereignisse, Präferenzen, beobachtete Muster. Skills halten, was verallgemeinert: wie man einen Tag strukturiert, wie man eine Anfrage interpretiert. Regeln halten, was invariant ist: Einschränkungen, die unabhängig vom Kontext nicht verletzt werden sollten. Die drei Ebenen entsprechen epistemisch unterschiedlichen Arten von Dingen. Sie in einen einzigen Speicher zu kollabieren wäre nicht einfacher; es wäre konfus.

---

## Ein zweiter Rahmen: Betriebssysteme

Neben der Informationstheorie entwickelte eine andere Disziplin komplementäre Lösungen für verwandte Probleme — nicht philosophisch, sondern durch Ingenieurswesen unter Einschränkungen.

Betriebssysteme verwalten Ressourcen unter Knappheit: begrenzter Speicher, begrenzte Prozessorzeit, mehrere Prozesse, die um beides konkurrieren. Die Abstraktionen, die sie über Jahrzehnte entwickelten — Demand-Paging, Prozessisolation, virtueller Speicher, Scheduling — sind Antworten auf die Frage, wie ein System kohärent agieren kann, wenn es nicht alles auf einmal halten kann.

Die Parallele ist direkt. Das Kontextfenster eines Sprachmodells ist ein Arbeitsgedächtnis mit harten Grenzen. Die Frage, was wann und in welcher Form geladen werden soll, ist genau die Frage, die Betriebssysteme für Prozesse beantworten. Skills, die bei Auftreten eines Themas bei Bedarf geladen werden, entsprechen Pages, die aus dem Speicher eingelagert werden. Die nächtliche Musterüberprüfung entspricht einem Hintergrundprozess mit niedriger Priorität, der läuft, wenn der Vordergrund inaktiv ist. Die drei Speicherebenen entsprechen der Speicherhierarchie, die jedes Betriebssystem verwaltet: schnell und flüchtig oben, langsam und persistent unten.

Das ist keine Metapher, die aus Eleganzgründen eingesetzt wird. Es ist eine Reihe getesteter Abstraktionen für ressourcenbeschränkte Kognition, entwickelt unter Einschränkungen, die weit schwerwiegender sind als das, was ein modernes Kontextfenster auferlegt. Die Lösungen lohnen es, entliehen zu werden, weil die Probleme strukturell ähnlich sind.

---

## Weiterführende Literatur

**Zur semantischen Informationstheorie:**

- Floridi, L. *The Philosophy of Information*. Oxford University Press, 2011. — Die umfassendste Behandlung; Kapitel 4–7 behandeln die Veridicality-These und die logische Theorie semantischer Information.
- Dretske, F. *Knowledge and the Flow of Information*. MIT Press, 1981. — Der kausal-nomologische Ansatz; wesentlich für das Verständnis, was es bedeutet, dass ein System etwas wirklich *weiß*.
- Shannon, C. E. & Weaver, W. *The Mathematical Theory of Communication*. University of Illinois Press, 1949. — Weavers Einleitungsessay für die explizite Drei-Ebenen-Rahmung und die Anerkennung dessen, was die Theorie offenlässt.
- Bateson, G. „Form, Substance and Difference." In *Steps to an Ecology of Mind*. Chandler, 1972. — Der „Unterschied, der einen Unterschied macht"-Essay; kurz, direkt und grundlegend.

**Zur Wissensarchitektur:**

- Ackoff, R. L. „From Data to Wisdom." *Journal of Applied Systems Analysis*, 16, 1989. — Vier Seiten. Die DIKW-Hierarchie in ihrer Originalform, sofort lesbar.
- Polanyi, M. *The Tacit Dimension*. Doubleday, 1966. — Der Grenzfall: was kein Informationssystem vollständig erfassen kann, und warum das wichtig ist.
