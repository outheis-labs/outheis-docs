# οὐθείς

Jede deiner KI-Interaktionen repräsentiert dich — Anfragen, Muster, Denkweisen. Mit der Zeit vervollständigt sich das Puzzle. Nicht für dich, sondern für die Plattformbetreiber.

**outheis stellt eine andere Perspektive in den Mittelpunkt: kognitive Souveränität. Es ist die digitale Repräsentation deiner Art zu denken — auf deinem Rechner, unter deiner Kontrolle.**

---

## Die Realität

Der Begriff *captured cognition* (vereinnahmte Kognition) beschreibt es gut: Deine mentale Arbeit, externalisiert durch KI-Interaktion, wird zum Rohmaterial für Systeme, die dir nicht dienen.

Diese Assistenten lernen von dir. Das Gelernte gehört jemand anderem. Das ist keine Ablehnung von KI generell — es ist eine Ablehnung des extraktiven Modells, das derzeit dominiert.

## οὐθείς

Als Polyphem fragt, wer ihn geblendet hat, antwortet Odysseus: οὐθείς — niemand. Der Zyklop ruft um Hilfe: "Niemand hat mich geblendet!" Hilfe bleibt aus. Odysseus entkommt, am Bauch des Widders festgeklammert.

Es ist ein Trick, aber auch eine Haltung: Indem er sich weigert, benannt, erfasst, festgelegt zu werden, bleibt Odysseus handlungsfähig.

outheis trägt diese Idee in die KI-Interaktion. Das System kennt dich — aber nur lokal, nur unter deiner Kontrolle, nur im Dienst deiner Arbeit.

## Das System

Ein lokal laufender Multi-Agenten-KI-Assistent. Ein zweites Gehirn — privat, menschzentriert, deins. Gebaut als Infrastruktur, nicht als Produkt. Funktioniert als persönlicher Assistent (1:1) oder Domänenexperte (n:1).

## Souveränität

- Deine Daten bleiben auf deinem Rechner. *Keine Cloud, keine Erfassung.*
- Der Assistent lernt von dir. *Das Gelernte gehört dir.*
- Append-only Logs. *Keine versteckten Zustände.*
- Markdown und JSON. *Portabel, lesbar, kein Lock-in.*

## Architektur

Unterschiedliche Agenten, jeder verantwortlich für eine definierte Aufgabe. Nach außen wie eine einzige Instanz. Bewährte Betriebssystem-Designprinzipien: Microkernel-angelehnter Dispatcher, Koordination via Messages, abgegrenzte Aufgabenkorridore, Fehlerisolation.

<div class="agents-grid">
  <div class="agent agent-ou"><div class="agent-name">ou</div><div class="agent-role">Relay Agent</div></div>
  <div class="agent agent-zeno"><div class="agent-name">zeno</div><div class="agent-role">Data Agent</div></div>
  <div class="agent agent-cato"><div class="agent-name">cato</div><div class="agent-role">Agenda Agent</div></div>
  <div class="agent agent-hiro"><div class="agent-name">hiro</div><div class="agent-role">Action Agent</div></div>
  <div class="agent agent-rumi"><div class="agent-name">rumi</div><div class="agent-role">Pattern Agent</div></div>
  <div class="agent agent-alan"><div class="agent-name">alan</div><div class="agent-role">Code Agent</div></div>
</div>

## Weiterlesen

<ul class="links-list">
  <li><a href="foundations/">Grundlagen</a></li>
  <li><a href="design/">Designprinzipien</a></li>
  <li><a href="implementation/">Implementierung</a></li>
  <li><a href="installation/">Installation</a></li>
  <li><a href="workflows/">Workflows</a></li>
</ul>

## Über das Projekt

outheis wird von Markus Schatzl entwickelt. Bei Interesse — als Nutzer, Mitarbeiter oder philantropischer Investor — gerne melden: [technology.culture@proton.me](mailto:technology.culture@proton.me)
