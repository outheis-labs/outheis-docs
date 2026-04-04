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

Generic agents run with full system prompts: user memory, vault context, language settings, skills, and rules. This raises the bar beyond raw tool-use — the model must also route correctly between agents, synthesize results across multiple tool calls, and report "no results" without inventing data.

`llama3.1:8b` was tested under these conditions using `tools/test_agent_capability.py`, which runs 9 scenarios covering relay routing, vault search and file read, error recovery, hallucination detection, and agenda operations:

| Scenario | Result | Notes |
|----------|--------|-------|
| Relay: route to agenda | ~ | Correct tool, answer incomplete |
| Relay: route to data | ✗ | Called wrong agent |
| Relay: answer without tool | ✗ | Called tool unnecessarily |
| Data: search by tag | ✓ | |
| Data: read file | ~ | Tool correct, result not fully synthesized |
| Data: error recovery | ~ | Recovered from error, synthesis weak |
| Data: no results (hallucination check) | ~ | No hallucination, but unclear response |
| Agenda: read today | ✓ | |
| Agenda: add event | ✗ | Wrong tool, wrong date computed |

**2/9 fully correct, 4 partial, 3 fail.** Relay routing is unreliable; multi-step result synthesis is weak. Agenda reads work well. No local model has been confirmed suitable for the full generic agent stack under current hardware.

**Privacy note:** If data privacy is a concern, all agents that process personal vault content (relay, data, agenda) must use local models — not just the code agent. This currently requires a cloud provider or a hardware upgrade that enables larger models.

**Re-evaluation on M5:** Larger models (32B+) and faster inference may change this picture significantly. Use `python tools/test_agent_capability.py` to re-test after a hardware upgrade.

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
