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

**Important:** Local models vary significantly in their ability to follow system prompts and use tools reliably. Tested models:

| Model | Size | Tool-use | Follows instructions | Verdict |
|-------|------|----------|----------------------|---------|
| qwen3:8b | 8B | ✗ None | Partial | Not suitable |
| mistral-nemo:12b | 12B | ✗ None | Partial | Not suitable |
| mistral:7b | 7B | ✗ None | Partial | Not suitable |
| gemma4:e4b | 4B | ✗ Unreliable | Weak | Not suitable |
| qwen2.5-coder:14b | 14B | Under evaluation | — | Testing |
| qwen2.5:14b | 14B | Under evaluation | — | Testing |

**Hardware requirements:** 14B models require approximately 16–20 GB RAM. 8B models run on 8–12 GB.

**Privacy note:** If data privacy is a concern, all agents that process personal vault content (relay, data, agenda) must use local models — not just the code agent. A local model that handles tool-use reliably is required for this use case.

**Recommendation:** Start with Anthropic. Switch to local models only once you have confirmed tool-use reliability on your hardware.

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
