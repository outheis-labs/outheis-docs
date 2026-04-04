---
title: Model Selection
---

# Model Selection

*Which LLM to use with outheis — and for which agent.*

outheis supports three model providers: Anthropic (cloud), Ollama (local), and OpenAI (cloud). Each agent has a model alias (`fast`, `capable`, `reasoning`, or a custom name) that maps to a concrete model in `config.json`.

---

## Anthropic

Recommended starting point. No additional setup beyond an API key.

| Model | ID | Speed | Cost | Context |
|-------|----|-------|------|---------|
| Claude Haiku 4.5 | `claude-haiku-4-5-20251001` | Fast | Low | 200k |
| Claude Sonnet 4.5 | `claude-sonnet-4-5` | Medium | Medium | 200k |
| Claude Opus 4.5 | `claude-opus-4-5` | Slow | High | 200k |

**Tool-use reliability:** Excellent across all models.

**Recommendation for outheis:**
- `fast` alias → Haiku — for relay, data, agenda (high-frequency, tool-heavy)
- `capable` alias → Sonnet — for pattern, action (reasoning-heavy tasks)
- `reasoning` alias → Opus — optional, for complex multi-step analysis

---

## Ollama (local)

Runs entirely on your hardware. No API costs, no data leaves the system. Requires `ollama` installed and `pip install openai`.

> **Test environment:** All benchmarks were measured on Apple M4, 24 GB unified memory. Results are a good basis for estimating performance on comparable hardware.

**GPU acceleration:** On Apple Silicon (M-series), Ollama uses Metal automatically — no configuration needed. On Linux/Windows, Vulkan support is available for AMD and Intel GPUs via `OLLAMA_VULKAN=1` (experimental). Environment variables for the Ollama server can be stored in outheis config under `llm.providers.ollama.env_vars` and are shown in the Web UI as a reference.

### Code Agent (alan)

Alan's system prompt contains only source root, role, and open proposals — no user memory. Tool-use reliability is the main requirement. Models are tested via the Ollama OpenAI-compatible endpoint with realistic tool schemas.

| Model | Size | Tool-use | Speed | Verdict |
|-------|------|----------|-------|---------|
| **llama3.2:3b** | 3B | ✓ Reliable | ~2s | Good — fast, correct tool calls |
| **llama3.1:8b** | 8B | ✓ Reliable | ~10s | Good — solid tool-use |
| **mistral-nemo:12b** | 12B | ✓ Reliable | ~13s | Good — accurate answers |
| **devstral-small-2:24b** | 24B | ✓ Reliable | ~28s | Best quality, slowest |
| qwen3:14b | 14B | ✗ None | ~22s | Not suitable |
| qwen2.5-coder:14b | 14B | ✗ None | ~12s | Not suitable — outputs JSON as text |
| mistral:7b | 7B | ✗ None | ~9s | Not suitable |
| deepseek-coder:6.7b | 6.7B | Error | — | Tools API not supported |
| qwen3:4b | 4B | ✗ None | ~7s | Not suitable |
| gemma4:e4b | 4B | ✗ Unreliable | — | Not suitable |

**Hardware requirements:** 24B models require approximately 16 GB RAM. 8B models run on 8–10 GB. 3B models run on 2–4 GB.

**Recommendation for alan:** `llama3.1:8b` is the best balance of speed and reliability. `llama3.2:3b` works if RAM is limited. `devstral-small-2:24b` gives the best quality if you have the RAM.

**Test tool:** `python tools/test_ollama_tool_use.py` from the outheis-beta repository.

### Generic Agents (relay, data, agenda)

Generic agents run with full system prompts: user memory, vault context, language settings, skills, and rules. The bar is higher than raw tool-use — the model must route correctly between agents, synthesize results across multiple tool calls, and report "no results" without inventing data.

Models tested using `tools/test_agent_capability.py` (9 scenarios: relay routing, vault search, file read, error recovery, hallucination detection, agenda read and add):

| Model | Size | OK | Partial | Fail | Notes |
|-------|------|----|---------|------|-------|
| **voytas26/openclaw-oss-20b-deterministic** | 20B | 6/9 | 2 | 1 | Best routing and error recovery |
| **gpt-oss:20b** | 20B | 6/9 | 2 | 1 | Strong error recovery |
| **glm-4.7-flash-32k** | 17B | 6/9 | 1 | 2 | Slowest (~180s total for all scenarios) |
| **gemma4:e4b** | MoE/4B active | 6/9 | 1 | 2 | Hallucination flag; empty-response failure; ~133s total |
| devstral-small-2:24b | 24B | 5/9 | 3 | 1 | Hallucination flag on empty-results test |
| mistral-nemo:12b | 12B | 3/9 | 4 | 2 | Routing: no tool calls |
| llama3.1:8b | 8B | 2/9 | 4 | 3 | — |

**The 20B class shows a clear step up.** Routing, multi-step result synthesis, and error recovery work reliably. Consistent weakness across all models: date arithmetic in agenda operations (computing "tomorrow" from the system prompt date).

`gemma4:e4b` is a Mixture-of-Experts model: 9.6 GB on disk, ~4B active parameters per token. It scores 6/9 — matching the 20B class — but carries two flags: a hallucination on the empty-results scenario (invented file names), and an empty response on a no-tool-needed query (model produced no text when no tool call was appropriate). At ~15s per scenario on M4/24 GB it is the most efficient model tested at this score level. The larger gemma4 variants are worth evaluating on M5 hardware.

`devstral-small-2:24b` carries a hallucination flag on the empty-results scenario — the model reported a filename that appeared only in the "no results" explanation, not as an actual match.

No model scores fully correct on all scenarios. The 20B class (and gemma4:e4b) is the current lower bound for practical use as generic agents.

**Privacy note:** If data privacy is a concern, all agents that process personal vault content (relay, data, agenda) must use local models — not just the code agent. This currently requires a cloud provider or a hardware upgrade that enables 20B+ inference at acceptable speed.

**Re-evaluation on M5:** The 20B class will run significantly faster on M5 hardware. Use `python tools/test_agent_capability.py` to re-test after a hardware upgrade — and extend to 32B+ models, and larger gemma4 variants.

### Pattern Agent (rumi)

rumi runs nightly with no user waiting — latency is irrelevant. The bar is quality: extract memory entries without hallucination, consolidate duplicates and contradictions, distill skills from mature memory, promote stable patterns to rules, and reflect on meta-learning.

Tested with `tools/test_pattern_agent.py` — 10 scenarios across all 5 phases of `run_scheduled()`:

| Model | Size | OK | Partial | Fail | Notes |
|-------|------|----|---------|------|-------|
| gemma4:26b | 26B | 6/10 | 2 | 2 | Hallucination flag (extract_empty); distill_quality failure; ~270s total |

`gemma4:26b` is a dense 26B model (all parameters active per token). It scores 6/10 with two flags: a hallucination on the empty-extraction scenario (invented a memory entry from casual chat where none should be extracted), and a failure to distill when the memory was clearly ready. The consolidate phase finds 0 of 2 duplicates (partial). At ~270s total for all 10 scenarios on M4/24 GB, nightly runtime is acceptable — but the hallucination flag means rumi would occasionally create false memory entries. Not yet suitable for production use as a local rumi.

**Test tool:** `python tools/test_pattern_agent.py` from the outheis-beta repository.

---

## OpenAI

Supported as a provider. Configuration is identical to Anthropic — set `"provider": "openai"` and provide an API key.

| Model | ID | Speed | Cost | Context |
|-------|----|-------|------|---------|
| GPT-4o | `gpt-4o` | Fast | Medium | 128k |
| GPT-4o mini | `gpt-4o-mini` | Very fast | Low | 128k |
| o1 | `o1` | Slow | High | 200k |

**Tool-use reliability:** Good (GPT-4o, GPT-4o mini). o1 has limited tool support.

**Recommendation:** Viable alternative to Anthropic. GPT-4o mini maps well to the `fast` alias. Not tested extensively with outheis — Anthropic remains the primary supported provider.

---

## Local Fallback

outheis can automatically switch to a local Ollama model when a cloud provider becomes unavailable due to exhausted credits or an invalid API key.

**How it works:**

1. At startup, outheis probes the configured cloud provider with a minimal call. If billing fails, fallback mode activates immediately.
2. During operation, any `BillingError` (HTTP 402/401, or error messages matching credit/quota patterns) triggers the same switch mid-conversation.
3. On activation: relay, data, agenda, pattern, and code agents are switched to the fallback model. The user is notified in the current chat and via Signal (if configured). The Web UI status dot turns yellow and the overview shows the active fallback model and reason.

**Configuration:**

```json
"llm": {
  "local_fallback": "llama3.1:8b",
  "providers": { ... },
  "models": { ... }
}
```

`local_fallback` is a model alias — it must be defined in `llm.models` and point to an Ollama model. The recommended convention is to name both the alias and the model entry `local-fallback`, which makes the intent self-documenting:

```json
"llm": {
  "local_fallback": "local-fallback",
  "models": {
    "local-fallback": { "provider": "ollama", "name": "llama3.1:8b" },
    ...
  }
}
```

Changing the target model later only requires updating the `name` field inside `local-fallback` — the alias reference stays stable.

If `local_fallback` is not set, outheis logs the billing error but does not switch — requests will continue to fail until credits are restored.

**Limitations:** Fallback mode is not automatically cleared when credits are restored. Restart the daemon to return to cloud models.
