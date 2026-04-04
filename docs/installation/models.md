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
| devstral-small-2:24b | 24B | 5/9 | 3 | 1 | Hallucination flag on empty-results test |
| mistral-nemo:12b | 12B | 3/9 | 4 | 2 | Routing: no tool calls |
| llama3.1:8b | 8B | 2/9 | 4 | 3 | — |

**The 20B class shows a clear step up.** Routing, multi-step result synthesis, and error recovery work reliably. Consistent weakness across all models: date arithmetic in agenda operations (computing "tomorrow" from the system prompt date).

`devstral-small-2:24b` carries a hallucination flag on the empty-results scenario — the model reported a filename that appeared only in the "no results" explanation, not as an actual match.

No model scores fully correct on all scenarios. The 20B class is the current lower bound for practical use as generic agents.

**Privacy note:** If data privacy is a concern, all agents that process personal vault content (relay, data, agenda) must use local models — not just the code agent. This currently requires a cloud provider or a hardware upgrade that enables 20B+ inference at acceptable speed.

**Re-evaluation on M5:** The 20B class will run significantly faster on M5 hardware. Use `python tools/test_agent_capability.py` to re-test after a hardware upgrade — and extend to 32B+ models.

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
