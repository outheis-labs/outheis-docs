---
title: Modellauswahl
---

# Modellauswahl

*Welches LLM für outheis — und für welchen Agenten.*

outheis unterstützt drei Modellanbieter: Anthropic (Cloud), Ollama (lokal) und OpenAI (Cloud). Jeder Agent hat einen Modell-Alias (`fast`, `capable`, `reasoning` oder ein eigener Name), der in `config.json` auf ein konkretes Modell zeigt.

---

## Anthropic

Empfohlener Einstieg. Kein zusätzliches Setup außer einem API-Schlüssel.

| Modell | ID | Geschwindigkeit | Kosten | Kontext |
|--------|----|-----------------|--------|---------|
| Claude Haiku 4.5 | `claude-haiku-4-5-20251001` | Schnell | Niedrig | 200k |
| Claude Sonnet 4.5 | `claude-sonnet-4-5` | Mittel | Mittel | 200k |
| Claude Opus 4.5 | `claude-opus-4-5` | Langsam | Hoch | 200k |

**Tool-Use-Zuverlässigkeit:** Ausgezeichnet bei allen Modellen.

**Empfehlung für outheis:**
- Alias `fast` → Haiku — für relay, data, agenda (hochfrequent, viel Tool-Use)
- Alias `capable` → Sonnet — für pattern, action (anspruchsvolle Aufgaben)
- Alias `reasoning` → Opus — optional, für komplexe mehrstufige Analysen

---

## Ollama (lokal)

Läuft vollständig auf eigener Hardware. Keine API-Kosten, keine Daten verlassen das System. Benötigt `ollama` installiert und `pip install openai`.

**GPU-Beschleunigung:** Auf Apple Silicon (M-Reihe) nutzt Ollama automatisch Metal — kein Setup erforderlich. Auf Linux/Windows ist Vulkan-Unterstützung für AMD- und Intel-GPUs über `OLLAMA_VULKAN=1` verfügbar (experimentell). Umgebungsvariablen für den Ollama-Server können in der outheis-Konfiguration unter `llm.providers.ollama.env_vars` gespeichert und in der Web UI eingesehen und bearbeitet werden.

### Code-Agent (alan)

Alans System-Prompt enthält nur Source-Root, Rolle und offene Proposals — keine User-Daten. Tool-Use-Zuverlässigkeit ist die zentrale Anforderung. Die Modelle werden über den Ollama-kompatiblen OpenAI-Endpunkt mit realistischen Tool-Schemas getestet.

| Modell | Größe | Tool-Use | Geschwindigkeit | Bewertung |
|--------|-------|----------|-----------------|-----------|
| **llama3.2:3b** | 3B | ✓ Zuverlässig | ~2s | Gut — schnell, korrekte Tool-Calls |
| **llama3.1:8b** | 8B | ✓ Zuverlässig | ~10s | Gut — solides Tool-Use |
| **mistral-nemo:12b** | 12B | ✓ Zuverlässig | ~13s | Gut — genaue Antworten |
| **devstral-small-2:24b** | 24B | ✓ Zuverlässig | ~28s | Beste Qualität, langsamer |
| qwen3:14b | 14B | ✗ Keiner | ~22s | Nicht geeignet |
| qwen2.5-coder:14b | 14B | ✗ Keiner | ~12s | Nicht geeignet — gibt JSON als Text aus |
| mistral:7b | 7B | ✗ Keiner | ~9s | Nicht geeignet |
| deepseek-coder:6.7b | 6.7B | Fehler | — | Tools-API nicht unterstützt |
| qwen3:4b | 4B | ✗ Keiner | ~7s | Nicht geeignet |
| gemma4:e4b | 4B | ✗ Unzuverlässig | — | Nicht geeignet |

**Hardware-Anforderungen:** 24B-Modelle benötigen ca. 16 GB RAM. 8B-Modelle laufen auf 8–10 GB. 3B-Modelle auf 2–4 GB.

**Empfehlung für alan:** `llama3.1:8b` bietet das beste Verhältnis aus Geschwindigkeit und Zuverlässigkeit. `llama3.2:3b` funktioniert bei RAM-Knappheit. `devstral-small-2:24b` liefert die beste Qualität, sofern ausreichend RAM vorhanden.

**Test-Tool:** `python tools/test_ollama_tool_use.py` im outheis-beta-Repository.

### Generische Agenten (relay, data, agenda)

Generische Agenten laufen mit vollem System-Prompt: User-Memory, Vault-Kontext, Spracheinstellung, Skills und Rules. Die Anforderungen gehen über reinen Tool-Use hinaus — das Modell muss Anfragen korrekt zwischen Agenten routen, Ergebnisse über mehrere Tool-Calls hinweg synthetisieren und bei leeren Ergebnissen korrekt antworten, ohne Daten zu erfinden.

`llama3.1:8b` wurde unter diesen Bedingungen mit `tools/test_agent_capability.py` getestet — 9 Szenarien zu Relay-Routing, Vault-Suche und Datei-Lesen, Fehlerbehandlung, Halluzinationserkennung und Agenda-Operationen:

| Szenario | Ergebnis | Anmerkung |
|----------|----------|-----------|
| Relay: Weiterleitung an Agenda | ~ | Richtiges Tool, Antwort unvollständig |
| Relay: Weiterleitung an Data | ✗ | Falscher Agent aufgerufen |
| Relay: Antwort ohne Tool | ✗ | Tool unnötig aufgerufen |
| Data: Suche nach Tag | ✓ | |
| Data: Datei lesen | ~ | Tool korrekt, Ergebnis nicht vollständig synthetisiert |
| Data: Fehlerbehandlung | ~ | Fehler behoben, Synthese schwach |
| Data: Kein Ergebnis (Halluzinationstest) | ~ | Keine Halluzination, Antwort unklar |
| Agenda: Heutigen Plan lesen | ✓ | |
| Agenda: Termin hinzufügen | ✗ | Falsches Tool, falsches Datum berechnet |

**2/9 vollständig korrekt, 4 partiell, 3 fehlgeschlagen.** Relay-Routing ist unzuverlässig, mehrstufige Synthese schwach. Agenda-Reads funktionieren gut. Kein lokales Modell wurde bisher für den vollständigen generischen Agenten-Stack unter aktueller Hardware bestätigt.

**Datenschutz-Hinweis:** Wenn Datenschutz ein Thema ist, müssen alle Agenten, die persönliche Vault-Inhalte verarbeiten (relay, data, agenda), lokale Modelle nutzen — nicht nur der Code-Agent. Das erfordert derzeit einen Cloud-Anbieter oder ein Hardware-Upgrade, das größere Modelle ermöglicht.

**Neu-Evaluierung auf M5:** Größere Modelle (32B+) und schnellere Inferenz könnten dieses Bild deutlich verändern. Für Re-Tests nach einem Hardware-Upgrade: `python tools/test_agent_capability.py`.

---

## OpenAI

Als Anbieter unterstützt. Konfiguration identisch zu Anthropic — `"provider": "openai"` setzen und API-Schlüssel angeben.

| Modell | ID | Geschwindigkeit | Kosten | Kontext |
|--------|----|-----------------|--------|---------|
| GPT-4o | `gpt-4o` | Schnell | Mittel | 128k |
| GPT-4o mini | `gpt-4o-mini` | Sehr schnell | Niedrig | 128k |
| o1 | `o1` | Langsam | Hoch | 200k |

**Tool-Use-Zuverlässigkeit:** Gut (GPT-4o, GPT-4o mini). o1 hat eingeschränkten Tool-Support.

**Empfehlung:** Viable Alternative zu Anthropic. GPT-4o mini passt gut zum Alias `fast`. Nicht umfassend mit outheis getestet — Anthropic bleibt der primäre unterstützte Anbieter.
