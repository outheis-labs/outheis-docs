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

**Tool-Use-Zuverlässigkeit variiert erheblich je nach Modell.** Die folgende Tabelle basiert auf direkten API-Tests — die Modelle werden über den Ollama-kompatiblen OpenAI-Endpunkt mit realistischen outheis-Tool-Schemas getestet, ohne persönliche User-Daten im System-Prompt (die die Leistung kleiner Modelle beeinträchtigen).

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

**GPU-Beschleunigung:** Auf Apple Silicon (M-Reihe) nutzt Ollama automatisch Metal — kein Setup erforderlich. Auf Linux/Windows ist Vulkan-Unterstützung für AMD- und Intel-GPUs über `OLLAMA_VULKAN=1` verfügbar (experimentell). Umgebungsvariablen für den Ollama-Server können in der outheis-Konfiguration unter `llm.providers.ollama.env_vars` gespeichert und in der Web UI eingesehen und bearbeitet werden.

**Datenschutz-Hinweis:** Wenn Datenschutz ein Thema ist, müssen alle Agenten, die persönliche Vault-Inhalte verarbeiten (relay, data, agenda), lokale Modelle nutzen — nicht nur der Code-Agent. Dafür ist ein lokales Modell mit zuverlässigem Tool-Use erforderlich.

**Empfehlung:** Mit Anthropic starten. Für lokale Inferenz bietet `llama3.1:8b` das beste Verhältnis aus Geschwindigkeit und Zuverlässigkeit. `devstral-small-2:24b` liefert die beste Qualität, sofern ausreichend RAM vorhanden.

**Test-Tool:** Tool-Use auf eigener Hardware evaluieren: `python tools/test_ollama_tool_use.py` im outheis-beta-Repository.

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
