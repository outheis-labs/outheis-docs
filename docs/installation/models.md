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

**Tool-use reliability varies significantly by model.** The table below reflects direct API tests — models are tested via the Ollama OpenAI-compatible endpoint with realistic outheis tool schemas, without personal user context in the system prompt (which degrades small model performance).

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

**GPU acceleration:** On Apple Silicon (M-series), Ollama uses Metal automatically — no configuration needed. On Linux/Windows, Vulkan support is available for AMD and Intel GPUs via `OLLAMA_VULKAN=1` (experimental). See the [Ollama documentation](https://ollama.com/docs) for platform-specific setup. Environment variables for the Ollama server can be stored in outheis config under `llm.providers.ollama.env_vars` and are shown in the Web UI as a reference.

**Privacy note:** If data privacy is a concern, all agents that process personal vault content (relay, data, agenda) must use local models — not just the code agent. A local model with reliable tool-use is required for this use case.

**Recommendation:** Start with Anthropic. For local inference, `llama3.1:8b` is the best balance of speed and reliability. `devstral-small-2:24b` gives the best quality if you have the RAM.

**Test tool:** To evaluate tool-use on your own hardware, run `python tools/test_ollama_tool_use.py` from the outheis-beta repository.

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
