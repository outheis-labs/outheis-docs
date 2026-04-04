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

**Wichtig:** Lokale Modelle unterscheiden sich erheblich in der Fähigkeit, System-Prompts zu befolgen und Tools zuverlässig zu nutzen. Getestete Modelle:

| Modell | Größe | Tool-Use | Instruktionen | Bewertung |
|--------|-------|----------|---------------|-----------|
| qwen3:8b | 8B | ✗ Keiner | Teilweise | Nicht geeignet |
| mistral-nemo:12b | 12B | ✗ Keiner | Teilweise | Nicht geeignet |
| mistral:7b | 7B | ✗ Keiner | Teilweise | Nicht geeignet |
| gemma4:e4b | 4B | ✗ Unzuverlässig | Schwach | Nicht geeignet |
| qwen2.5-coder:14b | 14B | ✗ Keiner | Teilweise | Nicht geeignet |

**Hardware-Anforderungen:** 14B-Modelle benötigen ca. 24 GB RAM. 8B-Modelle laufen auf 8–12 GB.

**Datenschutz-Hinweis:** Wenn Datenschutz ein Thema ist, müssen alle Agenten, die persönliche Vault-Inhalte verarbeiten (relay, data, agenda), lokale Modelle nutzen — nicht nur der Code-Agent. Dafür ist ein lokales Modell mit zuverlässigem Tool-Use erforderlich.

**Empfehlung:** Mit Anthropic starten. Auf lokale Modelle umsteigen erst, wenn Tool-Use-Zuverlässigkeit auf der eigenen Hardware bestätigt ist.

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
