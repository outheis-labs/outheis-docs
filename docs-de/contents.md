# Contents

## Grundlagen {#foundations}

<ul class="toc-list">
<li><a href="foundations/index.html"><div class="title">Warum outheis</div><div class="description">Über Souveränität, Kognition und warum das Extraktionsmodell scheitert.</div></a></li>
<li><a href="foundations/01-design-principles.html"><div class="title">Design-Prinzipien</div><div class="description">Über Werkzeuge, die das Leben unterstützen, statt es zu vereinnahmen.</div></a></li>
<li><a href="foundations/02-semantic-foundations.html"><div class="title">Information und Semantik</div><div class="description">Warum Information nicht gleich Daten ist — und was das für ein persönliches KI-System bedeutet.</div></a></li>
<li><a href="foundations/03-attention-as-architecture.html"><div class="title">Aufmerksamkeit als Architekturprinzip</div><div class="description">Die zentrale Erkenntnis der Transformer-Architektur — dass erlernte Attention-Mechanismen...</div></a></li>
<li><a href="foundations/04-annotation-as-ground-truth.html"><div class="title">Annotation als Ground Truth</div><div class="description">Über die strukturelle Parallele zwischen überwachtem Lernen und menschlicher Korrektur — und was...</div></a></li>
<li><a href="foundations/05-tags-as-scaffolding.html"><div class="title">Tags als Gerüst: Ein Ablösungspfad</div><div class="description">Ein persönliches KI-System, das den Nutzer wirklich versteht, würde im Idealfall alles aus dem...</div></a></li>
</ul>

## Design {#design}

<ul class="toc-list">
<li><a href="design/01-why-os-principles.html"><div class="title">Warum Betriebssystemprinzipien auf agent-Architekturen zutreffen</div><div class="description">Multi-agent-KI-Systeme stehen vor Herausforderungen, die Betriebssysteme vor Jahrzehnten gelöst...</div></a></li>
<li><a href="design/02-systems-survey.html"><div class="title">Systemüberblick: Betriebssysteme und anwendbare Konzepte</div><div class="description">Betriebssysteme haben Probleme gelöst, die agent-Architekturen gerade erst entdecken. Dieser...</div></a></li>
<li><a href="design/03-architecture.html"><div class="title">Architektur</div><div class="description">Die outheis-Architektur ist kein Zufallsprodukt — sie ist aus Betriebssystemprinzipien abgeleitet.</div></a></li>
<li><a href="design/04-data-formats.html"><div class="title">Datenformate und Konventionen</div><div class="description">Klare Formate ermöglichen verlässliche Annahmen. Agents wissen, was sie vorfinden — ohne raten...</div></a></li>
<li><a href="design/05-related-work.html"><div class="title">Verwandte Arbeiten</div><div class="description">Die Anwendung von Betriebssystemkonzepten auf KI-agent-Systeme ist jung — aber wächst schnell....</div></a></li>
<li><a href="design/06-agent-prompts.html"><div class="title">Agenten-Prompts und Kommunikationsregeln</div><div class="description">Alle Prompts sind aus Gründen der Transparenz veröffentlicht. Was hier steht, ist was die agents...</div></a></li>
<li><a href="design/07-hybrid-memory-stack.html"><div class="title">Der hybride Memory-Stack: Wo Code endet und das LLM beginnt</div><div class="description">Zwei Versagensmuster definieren den Designraum.</div></a></li>
<li><a href="design/08-quality-threshold.html"><div class="title">Die Qualitätsschwelle: Warum Fähigkeit nicht linear skaliert</div><div class="description">Über emergente Fähigkeiten, die Grenzen von Parallelismus und das minimale tragfähige Modell.</div></a></li>
</ul>

## Implementierung {#implementation}

<ul class="toc-list">
<li><a href="implementation/01-architecture.html"><div class="title">Architektur</div><div class="description">Wie die Teile zusammenpassen.</div></a></li>
<li><a href="implementation/02-memory.html"><div class="title">Memory</div><div class="description">Was outheis über dich erinnert — und wie.</div></a></li>
<li><a href="implementation/03-agenda.html"><div class="title">Agenda</div><div class="description">Zeitmanagement durch drei einfache Dateien.</div></a></li>
<li><a href="implementation/04-skills.html"><div class="title">Skills</div><div class="description">Was Agenten darüber wissen, wie sie handeln sollen.</div></a></li>
<li><a href="implementation/05-alan.html"><div class="title">Alan</div><div class="description">Code-Intelligenz für Entwicklungsumgebungen.</div></a></li>
<li><a href="implementation/06-hiro.html"><div class="title">Hiro</div><div class="description">Action-Agent — noch nicht implementiert.</div></a></li>
<li><a href="implementation/07-signal.html"><div class="title">Signal</div><div class="description">Signal Messenger Transport über signal-cli JSON-RPC.</div></a></li>
<li><a href="implementation/08-annotation-feedback.html"><div class="title">Annotations-Feedback-Schleife</div><div class="description">Wie `>`-Annotationen in den Memory-Stack geroutet werden — die aktuelle Lücke und die geplante...</div></a></li>
<li><a href="implementation/09-vault.html"><div class="title">Vault</div><div class="description">Wie du dein Wissen strukturierst, damit outheis damit arbeiten kann.</div></a></li>
<li><a href="implementation/10-config.html"><div class="title">Konfiguration</div><div class="description">Vollständige Referenz für `config.json`.</div></a></li>
<li><a href="implementation/11-guide.html"><div class="title">Anleitung</div><div class="description">Einstieg in outheis.</div></a></li>
<li><a href="implementation/12-migration.html"><div class="title">Migration</div><div class="description">Wie du bestehendes Wissen in outheis bringst.</div></a></li>
<li><a href="implementation/13-webui.html"><div class="title">Web UI</div><div class="description">Lokale Verwaltungsoberfläche für outheis.</div></a></li>
<li><a href="implementation/14-data-safety.html"><div class="title">Datensicherheit</div><div class="description">Wie outheis sich gegen Prompt-Injection und unvertrauenswürdige Inhalte schützt.</div></a></li>
<li><a href="implementation/15-models.html"><div class="title">Modell-Evaluation</div><div class="description">Fähigkeits-Benchmarks für lokale und Cloud-Modelle.</div></a></li>
</ul>

## Installation {#installation}

<ul class="toc-list">
<li><a href="installation/01-release-notes.html"><div class="title">Versionshinweise</div><div class="description">Public Beta — April 2026.</div></a></li>
<li><a href="installation/02-installation.html"><div class="title">Installation</div><div class="description"></div></a></li>
<li><a href="installation/03-first-steps.html"><div class="title">Erste Schritte</div><div class="description">Nach `outheis init` und `outheis start` diese Schritte durchgehen, um sicherzustellen, dass...</div></a></li>
<li><a href="installation/04-models.html"><div class="title">Modellauswahl</div><div class="description">Welches LLM für outheis — und für welchen Agenten.</div></a></li>
<li><a href="installation/05-communication.html"><div class="title">Mit outheis kommunizieren</div><div class="description">outheis ist über drei Kanäle erreichbar. Alle Kanäle verbinden sich mit demselben Dispatcher und...</div></a></li>
</ul>

## Workflows {#workflows}

<ul class="toc-list">
<li><a href="workflows/index.html"><div class="title">Workflows</div><div class="description">Praktische Anleitungen — wie man outheis im Alltag nutzt.</div></a></li>
</ul>
