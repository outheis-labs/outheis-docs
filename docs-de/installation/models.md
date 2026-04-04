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

> **Testumgebung:** Alle Benchmarks wurden auf einem Apple M4 mit 24 GB Unified Memory gemessen. Die Ergebnisse sind eine gute Grundlage zur Abschätzung der Leistung auf vergleichbarer Hardware.

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

Getestet mit `tools/test_agent_capability.py` — 9 Szenarien zu Relay-Routing, Vault-Suche, Datei-Lesen, Fehlerbehandlung, Halluzinationserkennung und Agenda-Operationen:

| Modell | Größe | OK | Partiell | Fail | Anmerkung |
|--------|-------|----|----------|------|-----------|
| **voytas26/openclaw-oss-20b-deterministic** | 20B | 6/9 | 2 | 1 | Bestes Routing und Fehlerbehandlung |
| **gpt-oss:20b** | 20B | 6/9 | 2 | 1 | Starke Fehlerbehandlung |
| **glm-4.7-flash-32k** | 17B | 6/9 | 1 | 2 | Langsamster (~180s gesamt) |
| **gemma4:e4b** | MoE/4B aktiv | 6/9 | 1 | 2 | halluziniert bei leerem Input; leere Antwort bei Tool-freier Anfrage; ~133s gesamt |
| devstral-small-2:24b | 24B | 5/9 | 3 | 1 | halluziniert beim Leer-Ergebnis-Test |
| mistral-nemo:12b | 12B | 3/9 | 4 | 2 | Routing: keine Tool-Calls |
| llama3.1:8b | 8B | 2/9 | 4 | 3 | — |

**Die 20B-Klasse zeigt einen deutlichen Sprung.** Routing, mehrstufige Synthese und Fehlerbehandlung funktionieren zuverlässig. Konsistente Schwäche quer durch alle Modelle: Datumsberechnung bei Agenda-Operationen (Berechnung von "morgen" aus dem System-Prompt-Datum).

`gemma4:e4b` ist ein Mixture-of-Experts-Modell: 9,6 GB auf Disk, ~4B aktive Parameter pro Token. Es erreicht 6/9 — gleichauf mit der 20B-Klasse — hat aber zwei Fehler: Halluzination beim Leer-Ergebnis-Szenario (erfindet Dateinamen) und eine leere Antwort bei einer Anfrage ohne nötigen Tool-Call. Mit ~15s pro Szenario auf M4/24 GB ist es das effizienteste Modell auf diesem Score-Niveau. Größere gemma4-Varianten sind für M5-Hardware interessant.

`devstral-small-2:24b` halluziniert beim Leer-Ergebnis-Szenario — das Modell meldete einen Dateinamen, der nur in der "Keine Ergebnisse"-Erklärung des Tools vorkam, nicht als tatsächlichen Treffer.

Kein Modell schneidet in allen Szenarien vollständig korrekt ab. Die 20B-Klasse (und gemma4:e4b) ist die aktuelle untere Grenze für den praktischen Einsatz als generische Agenten.

**Datenschutz-Hinweis:** Wenn Datenschutz ein Thema ist, müssen alle Agenten, die persönliche Vault-Inhalte verarbeiten (relay, data, agenda), lokale Modelle nutzen — nicht nur der Code-Agent. Das erfordert derzeit einen Cloud-Anbieter oder ein Hardware-Upgrade, das 20B+-Inferenz in akzeptabler Geschwindigkeit ermöglicht.

**Neu-Evaluierung auf M5:** Die 20B-Klasse wird auf M5-Hardware deutlich schneller laufen. Für Re-Tests nach dem Hardware-Upgrade: `python tools/test_agent_capability.py` — und Erweiterung auf 32B+-Modelle sowie größere gemma4-Varianten.

### Pattern-Agent (rumi)

rumi läuft nächtlich, kein User wartet — Latenz ist irrelevant. Entscheidend ist Qualität: Memory-Einträge ohne Halluzination extrahieren, Duplikate und Widersprüche bereinigen, Skills aus reifen Einträgen destillieren, stabile Muster zu Regeln promoten und Meta-Learning reflektieren.

Getestet mit `tools/test_pattern_agent.py` — 10 Szenarien über alle 5 Phasen von `run_scheduled()`:

| Modell | Größe | OK | Partiell | Fail | Anmerkung |
|--------|-------|----|----------|------|-----------|
| gemma4:26b | 26B | 6/10 | 2 | 2 | halluziniert bei extract_empty; distill_quality-Fehler; ~270s gesamt |

`gemma4:26b` ist ein dichtes 26B-Modell (alle Parameter pro Token aktiv). Es erreicht 6/10 mit zwei Fehlern: Halluzination im Leer-Extraktions-Szenario (erfindet Memory-Einträge aus Smalltalk, wo keine entstehen sollten) und fehlende Destillation trotz reifer Memory-Einträge. Die Konsolidierungsphase findet 0 von 2 Duplikaten (partiell). Mit ~270s Gesamtlaufzeit für alle 10 Szenarien auf M4/24 GB ist der nächtliche Betrieb zeitlich akzeptabel — das Halluzinations-Problem bedeutet aber, dass rumi gelegentlich falsche Memory-Einträge erzeugen würde. Für den produktiven Einsatz als lokaler rumi noch nicht geeignet.

**Test-Tool:** `python tools/test_pattern_agent.py` im outheis-beta-Repository.

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

---

## Lokaler Fallback

outheis kann automatisch auf ein lokales Ollama-Modell umschalten, wenn ein Cloud-Anbieter wegen aufgebrauchtem Guthaben oder ungültigem API-Schlüssel nicht mehr verfügbar ist.

**Funktionsweise:**

1. Beim Start überprüft outheis den konfigurierten Cloud-Anbieter mit einem minimalen Aufruf. Schlägt dieser wegen Billing fehl, wird der Fallback-Modus sofort aktiviert.
2. Im laufenden Betrieb löst jeder `BillingError` (HTTP 402/401 oder Fehlermeldungen mit Credit-/Quota-Inhalten) denselben Wechsel aus — mitten in einer Konversation.
3. Bei Aktivierung: relay, data, agenda, pattern und code werden auf das Fallback-Modell umgestellt. Der User wird im laufenden Chat und über Signal (falls konfiguriert) benachrichtigt. Der Status-Punkt der Web-UI wird gelb, die Übersicht zeigt das aktive Fallback-Modell und den Grund an.

**Konfiguration:**

```json
"llm": {
  "local_fallback": "llama3.1:8b",
  "providers": { ... },
  "models": { ... }
}
```

`local_fallback` ist ein Modell-Alias — er muss in `llm.models` definiert sein und auf ein Ollama-Modell zeigen. Die empfohlene Konvention ist, sowohl den Alias als auch den Modelleintrag `local-fallback` zu nennen, was die Absicht selbst dokumentiert:

```json
"llm": {
  "local_fallback": "local-fallback",
  "models": {
    "local-fallback": { "provider": "ollama", "name": "llama3.1:8b" },
    ...
  }
}
```

Das Zielmodell lässt sich später durch Änderung des `name`-Felds innerhalb von `local-fallback` anpassen — der Alias-Verweis bleibt stabil.

Ist `local_fallback` nicht gesetzt, protokolliert outheis den Billing-Fehler, schaltet aber nicht um — Anfragen schlagen weiterhin fehl, bis das Guthaben aufgefüllt wird.

**Einschränkung:** Der Fallback-Modus wird nicht automatisch aufgehoben, wenn das Guthaben wieder vorhanden ist. Ein Neustart des Daemons stellt den Cloud-Betrieb wieder her.
