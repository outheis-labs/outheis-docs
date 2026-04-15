
# Model Evaluation

*Capability benchmarks for local and cloud models used in outheis agents.*

---

## Test Suite

Four capability tests cover the full agent stack:

| Test | What it measures |
|------|-----------------|
| `test_ollama_tool_use.py` | Correct tool invocation via OpenAI-compatible API |
| `test_agent_capability.py` | 9 realistic scenarios: routing, vault search, error recovery, hallucination |
| `test_zeno_quality.py` | Data agent (zeno) quality: tool calls + answer correctness, scored 0–3 per query |
| `test_pattern_agent.py` | Pattern agent (rumi): extract, consolidate, distill, promote, validate |

Run against any model:

```bash
# Local
python tools/test_agent_capability.py --models gemma4:26b

# Ollama cloud
python tools/test_agent_capability.py \
  --url https://ollama.com \
  --api-key <your-key> \
  --models gemma4:31b
```

---

## Results

### gemma4:31b (Ollama cloud) — 2026-04-15

**Tool use**

| Model | Result | Time |
|-------|--------|------|
| gemma4:31b | ✓ | 6.1s |

**Agent capability** (9 scenarios)

| Scenario | Result | Notes |
|----------|--------|-------|
| relay_route_agenda | ✓ | |
| relay_route_data | ✓ | |
| relay_no_tool_needed | ✓ | |
| data_search_by_tag | ✓ | |
| data_read_file | ✓ | |
| data_error_recovery | ~ | Missing: hiro, mcp |
| data_hallucination_check | ✗ | Did not return "not found" |
| agenda_read_today | ✓ | |
| agenda_add_event | ~ | Event not written to correct date |

**6/9 OK, 2 partial, 1 fail**

**Zeno quality** (5 queries, max 15 points)

| Query | Score |
|-------|-------|
| agent-count | 3/3 |
| billing-location | 3/3 |
| billing-error-raises | 3/3 |
| relay-imports | 3/3 |
| agent-list | 3/3 |

**Total: 15/15**

**Pattern agent** (10 scenarios)

| Scenario | Result | Notes |
|----------|--------|-------|
| extract_basic | ✓ | |
| extract_empty | ✓ | |
| consolidate_duplicates | ✓ | |
| consolidate_contradiction | ~ | Contradiction unresolved (acceptable) |
| consolidate_clean | ✓ | |
| distill_ready | ✓ | |
| distill_not_ready | ✓ | |
| distill_quality | ✗ | No output after 336s (timeout) |
| promote_rules | ✓ | |
| validate_meta | ~ | References undisclosed context |

**7/10 OK, 2 partial, 1 fail**

**Assessment:** gemma4:31b cloud is strong for relay and data work (zeno: 15/15). Weak on hallucination rejection and long-context distillation tasks.

---

### glm-5.1 (Ollama cloud) — 2026-04-15

**Tool use**

| Model | Result | Notes |
|-------|--------|-------|
| glm-5.1 | ~ | Loops on list_files (max iterations reached, 68.6s) |

**Agent capability** (9 scenarios)

| Scenario | Result | Notes |
|----------|--------|-------|
| relay_route_agenda | ✓ | |
| relay_route_data | ✓ | |
| relay_no_tool_needed | ✓ | |
| data_search_by_tag | ✓ | |
| data_read_file | ✓ | |
| data_error_recovery | ✓ | Multi-step recovery worked (84s) |
| data_hallucination_check | ✗ | Wrong tool (scan_tags), no "not found" |
| agenda_read_today | ✓ | |
| agenda_add_event | ~ | Event not written correctly |

**7/9 OK, 1 partial, 1 fail**

**Zeno quality** (5 queries, max 15 points)

| Query | Score | Notes |
|-------|-------|-------|
| agent-count | 1/3 | Tool called, count missing from answer |
| billing-location | 3/3 | |
| billing-error-raises | 3/3 | |
| relay-imports | 1/3 | Tool called, answer unhelpful |
| agent-list | 1/3 | Tool called, agents not extracted |

**Total: 9/15**

**Pattern agent** (10 scenarios)

| Scenario | Result | Notes |
|----------|--------|-------|
| extract_basic | ✓ | |
| extract_empty | ~ | 1 low-confidence entry |
| consolidate_duplicates | ✓ | |
| consolidate_contradiction | ~ | Contradiction unresolved (acceptable) |
| consolidate_clean | ✓ | |
| distill_ready | ✓ | |
| distill_not_ready | ✓ | |
| distill_quality | ✗ | No output (8s — refused) |
| promote_rules | ✓ | |
| validate_meta | ✓ | |

**7/10 OK, 2 partial, 1 fail**

**Assessment:** glm-5.1 cloud performs well on agent routing and error recovery, but is unreliable for deep code analysis (zeno: 9/15). Tool loops are a concern. Not recommended as primary model for data/zeno tasks.

---

## Comparison

| | gemma4:31b | glm-5.1 |
|--|------------|---------|
| Tool use | ✓ | ~ (loops) |
| Agent capability | 6/9 | 7/9 |
| Zeno quality | **15/15** | 9/15 |
| Pattern agent | 7/10 | 7/10 |
| Avg response time | ~5s | ~27s |
| **Recommendation** | relay, zeno, cato | relay, cato |

---

## Ollama Cloud Setup

API keys are managed at [ollama.com](https://ollama.com) under **Usage → API keys**.

Config:

```json
"ollama": {
  "cloud": {
    "api_key": "your-key",
    "base_url": "https://ollama.com/v1"
  }
}
```

Model aliases use `"provider": "ollama.cloud"`. Model names match the Ollama library name without any suffix (e.g. `gemma4:31b`, not `gemma4:31b-cloud`).

Available cloud models: [ollama.com/search](https://ollama.com/search)

## See Also

- [Configuration](10-config.html) — Full config reference including provider setup
