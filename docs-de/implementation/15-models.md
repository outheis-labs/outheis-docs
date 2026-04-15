
# Modell-Evaluation

*Fähigkeits-Benchmarks für lokale und Cloud-Modelle in outheis-Agenten.*

---

## Test-Suite

Vier Tests decken den gesamten Agenten-Stack ab:

| Test | Was gemessen wird |
|------|------------------|
| `test_ollama_tool_use.py` | Korrekte Tool-Aufrufe via OpenAI-kompatible API |
| `test_agent_capability.py` | 9 realistische Szenarien: Routing, Vault-Suche, Fehlerbehandlung, Halluzination |
| `test_zeno_quality.py` | Data-Agent (zeno): Tool-Calls + Antwortqualität, 0–3 Punkte pro Query |
| `test_pattern_agent.py` | Pattern-Agent (rumi): extract, consolidate, distill, promote, validate |

Aufruf gegen beliebiges Modell:

```bash
# Lokal
python tools/test_agent_capability.py --models gemma4:26b

# Ollama Cloud
python tools/test_agent_capability.py \
  --url https://ollama.com \
  --api-key <key> \
  --models gemma4:31b
```

---

## Ergebnisse

### gemma4:31b (Ollama Cloud) — 2026-04-15

**Tool Use**

| Modell | Ergebnis | Zeit |
|--------|----------|------|
| gemma4:31b | ✓ | 6.1s |

**Agent Capability** (9 Szenarien)

| Szenario | Ergebnis | Anmerkung |
|----------|----------|-----------|
| relay_route_agenda | ✓ | |
| relay_route_data | ✓ | |
| relay_no_tool_needed | ✓ | |
| data_search_by_tag | ✓ | |
| data_read_file | ✓ | |
| data_error_recovery | ~ | Fehlend: hiro, mcp |
| data_hallucination_check | ✗ | Kein "not found" zurückgegeben |
| agenda_read_today | ✓ | |
| agenda_add_event | ~ | Termin nicht auf korrektes Datum geschrieben |

**6/9 OK, 2 teilweise, 1 Fehler**

**Zeno Quality** (5 Queries, max. 15 Punkte)

| Query | Punkte |
|-------|--------|
| agent-count | 3/3 |
| billing-location | 3/3 |
| billing-error-raises | 3/3 |
| relay-imports | 3/3 |
| agent-list | 3/3 |

**Gesamt: 15/15**

**Pattern Agent** (10 Szenarien)

| Szenario | Ergebnis | Anmerkung |
|----------|----------|-----------|
| extract_basic | ✓ | |
| extract_empty | ✓ | |
| consolidate_duplicates | ✓ | |
| consolidate_contradiction | ~ | Widerspruch ungelöst (tolerierbar) |
| consolidate_clean | ✓ | |
| distill_ready | ✓ | |
| distill_not_ready | ✓ | |
| distill_quality | ✗ | Kein Output nach 336s (Timeout) |
| promote_rules | ✓ | |
| validate_meta | ~ | Referenziert nicht offengelegten Kontext |

**7/10 OK, 2 teilweise, 1 Fehler**

**Einschätzung:** gemma4:31b cloud ist stark für Relay- und Datenarbeit (zeno: 15/15). Schwächen bei Halluzinations-Erkennung und langen Distillations-Aufgaben.

---

### glm-5.1 (Ollama Cloud) — 2026-04-15

**Tool Use**

| Modell | Ergebnis | Anmerkung |
|--------|----------|-----------|
| glm-5.1 | ~ | Schleife bei list_files (max. Iterationen erreicht, 68.6s) |

**Agent Capability** (9 Szenarien)

| Szenario | Ergebnis | Anmerkung |
|----------|----------|-----------|
| relay_route_agenda | ✓ | |
| relay_route_data | ✓ | |
| relay_no_tool_needed | ✓ | |
| data_search_by_tag | ✓ | |
| data_read_file | ✓ | |
| data_error_recovery | ✓ | Mehrstufige Wiederherstellung funktioniert (84s) |
| data_hallucination_check | ✗ | Falsches Tool (scan_tags), kein „not found" |
| agenda_read_today | ✓ | |
| agenda_add_event | ~ | Termin nicht korrekt geschrieben |

**7/9 OK, 1 teilweise, 1 Fehler**

**Zeno Quality** (5 Queries, max. 15 Punkte)

| Query | Punkte | Anmerkung |
|-------|--------|-----------|
| agent-count | 1/3 | Tool aufgerufen, Zahl fehlt in Antwort |
| billing-location | 3/3 | |
| billing-error-raises | 3/3 | |
| relay-imports | 1/3 | Tool aufgerufen, Antwort nicht hilfreich |
| agent-list | 1/3 | Tool aufgerufen, Agenten nicht extrahiert |

**Gesamt: 9/15**

**Pattern Agent** (10 Szenarien)

| Szenario | Ergebnis | Anmerkung |
|----------|----------|-----------|
| extract_basic | ✓ | |
| extract_empty | ~ | 1 Eintrag mit geringer Konfidenz |
| consolidate_duplicates | ✓ | |
| consolidate_contradiction | ~ | Widerspruch ungelöst (tolerierbar) |
| consolidate_clean | ✓ | |
| distill_ready | ✓ | |
| distill_not_ready | ✓ | |
| distill_quality | ✗ | Kein Output (8s — abgelehnt) |
| promote_rules | ✓ | |
| validate_meta | ✓ | |

**7/10 OK, 2 teilweise, 1 Fehler**

**Einschätzung:** glm-5.1 cloud performt gut bei Agent-Routing und Fehlerbehandlung, aber unzuverlässig bei tiefer Code-Analyse (zeno: 9/15). Tool-Schleifen sind ein Problem. Nicht empfohlen als primäres Modell für Data/Zeno-Aufgaben.

---

## Vergleich

| | gemma4:31b | glm-5.1 |
|--|------------|---------|
| Tool Use | ✓ | ~ (Schleifen) |
| Agent Capability | 6/9 | 7/9 |
| Zeno Quality | **15/15** | 9/15 |
| Pattern Agent | 7/10 | 7/10 |
| Ø Antwortzeit | ~5s | ~27s |
| **Empfehlung** | relay, zeno, cato | relay, cato |

---

## Ollama Cloud Einrichtung

API-Keys werden unter [ollama.com](https://ollama.com) verwaltet (**Usage → API keys**).

Konfiguration:

```json
"ollama": {
  "cloud": {
    "api_key": "dein-key",
    "base_url": "https://ollama.com/v1"
  }
}
```

Modell-Aliase verwenden `"provider": "ollama.cloud"`. Modellnamen entsprechen dem Ollama-Library-Namen ohne Suffix (z.B. `gemma4:31b`, nicht `gemma4:31b-cloud`).

Verfügbare Cloud-Modelle: [ollama.com/search](https://ollama.com/search)

## Siehe auch

- [Konfiguration](10-config.html) — Vollständige Konfigurationsreferenz
