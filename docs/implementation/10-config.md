
# Configuration

*Complete reference for `config.json`.*

---

## Location

```
~/.outheis/human/config.json
```

Created automatically on first `outheis start` with sensible defaults.

## Full Example

```json
{
  "human": {
    "name": "Max",
    "phone": ["+49123456789"],
    "language": "de",
    "timezone": "Europe/Berlin",
    "vault": ["~/Documents/Vault", "~/Work/Notes"]
  },
  "signal": {
    "enabled": false,
    "bot_phone": "+49987654321",
    "bot_name": "Ou",
    "allowed": [
      {"name": "Partner", "phone": "+49111222333"}
    ]
  },
  "llm": {
    "providers": {
      "anthropic": {
        "api_key": "sk-ant-..."
      },
      "ollama": {
        "local": {
          "base_url": "http://localhost:11434",
          "env_vars": {"OLLAMA_MAX_LOADED_MODELS": "2"}
        },
        "cloud": {
          "api_key": "835a...",
          "base_url": "https://ollama.com/v1"
        }
      }
    },
    "models": {
      "fast": {
        "provider": "anthropic",
        "name": "claude-haiku-4-5",
        "run_mode": "on-demand"
      },
      "capable": {
        "provider": "anthropic",
        "name": "claude-sonnet-4-20250514",
        "run_mode": "on-demand"
      },
      "local": {
        "provider": "ollama.local",
        "name": "gemma4:26b",
        "run_mode": "persistent"
      },
      "cloud-gemma": {
        "provider": "ollama.cloud",
        "name": "gemma4:31b",
        "run_mode": "on-demand"
      }
    }
  },
  "agents": {
    "relay": {"name": "ou", "model": "fast", "enabled": true},
    "data": {"name": "zeno", "model": "capable", "enabled": true},
    "agenda": {"name": "cato", "model": "capable", "enabled": true},
    "action": {"name": "hiro", "model": "capable", "enabled": false},
    "pattern": {"name": "rumi", "model": "capable", "enabled": true},
    "code": {"name": "alan", "model": "capable", "enabled": false}
  },
  "schedule": {
    "pattern_infer":   {"enabled": true, "time": ["04:00"]},
    "memory_migrate":  {"enabled": false, "time": ["04:00"]},
    "index_rebuild":   {"enabled": true, "time": ["04:30"]},
    "archive_rotation":{"enabled": true, "time": ["05:00"]},
    "shadow_scan":     {"enabled": true, "time": ["03:30"]},
    "agenda_review": {
      "enabled": true,
      "time": ["04:55","05:55","06:55","07:55","08:55","09:55",
               "10:55","11:55","12:55","13:55","14:55","15:55",
               "16:55","17:55","18:55","19:55","20:55","21:55",
               "22:55","23:55"]
    },
    "agenda_midnight": {"enabled": true},
    "session_summary": {"enabled": true},
    "action_tasks":    {"enabled": true}
  },
  "updates": {
    "auto_migrate": true,
    "schedule": "04:00"
  }
}
```

## Sections

### human

User identification and vault locations.

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `name` | string | "Human" | Display name |
| `phone` | string[] | [] | Phone numbers (for Signal transport) |
| `language` | string | "en" | Preferred language code |
| `timezone` | string | "Europe/Berlin" | IANA timezone |
| `vault` | string[] | ["~/Documents/Vault"] | Vault directories (first is primary) |

**Environment overrides:**

- `OUTHEIS_HUMAN_DIR` — override human data directory (~/.outheis/human)
- `OUTHEIS_VAULT` — override primary vault path

### signal

Signal messenger transport configuration.

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `enabled` | bool | false | Enable Signal transport |
| `bot_phone` | string | null | Bot's phone number |
| `bot_name` | string | "Ou" | Bot display name |
| `allowed` | object[] | [] | Additional allowed contacts |

Allowed contact format:
```json
{"name": "Partner", "phone": "+49111222333"}
```

The user's own phone (from `human.phone`) is always allowed.

### llm

LLM providers and model aliases.

#### providers

| Field | Type | Description |
|-------|------|-------------|
| `api_key` | string | API key (or use environment variable) |
| `base_url` | string | Override base URL (for Ollama, custom endpoints) |

Provider names: `anthropic`, `openai`, `ollama.local`, `ollama.cloud`

The `ollama` provider is nested — `local` and `cloud` are sub-providers:

```json
"ollama": {
  "local": {
    "base_url": "http://localhost:11434",
    "env_vars": {"OLLAMA_MAX_LOADED_MODELS": "2"}
  },
  "cloud": {
    "api_key": "your-ollama-api-key",
    "base_url": "https://ollama.com/v1"
  }
}
```

Either sub-provider is optional. Model aliases reference them as `"provider": "ollama.local"` or `"provider": "ollama.cloud"`.

**Ollama server lifecycle:** outheis starts `ollama serve` automatically on startup if `ollama.local` is configured and Ollama is not already running. Env vars from `env_vars` are passed to the server process.

**API key resolution:**
1. Config file (`api_key` field)
2. Environment variable (`ANTHROPIC_API_KEY`, etc.)

#### local_fallback

When cloud API billing fails (credit exhausted), outheis automatically enters fallback mode:

- All agents switch to the model alias specified by `local_fallback`
- The user is notified on all channels
- A periodic probe checks when cloud credits are restored and exits fallback automatically

```json
{
  "llm": {
    "local_fallback": "local"
  }
}
```

If `local_fallback` is not configured, outheis notifies the user but cannot process requests until credits are restored.

#### models

Model aliases used by agents.

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `provider` | string | "anthropic" | `anthropic`, `openai`, `ollama.local`, `ollama.cloud` |
| `name` | string | — | Model identifier |
| `run_mode` | string | "on-demand" | `on-demand` or `persistent` |

**run_mode:**

- `on-demand` — Start model per request (cloud APIs)
- `persistent` — Keep model loaded (local Ollama)

**Default aliases:**
```json
{
  "fast": {"provider": "anthropic", "name": "claude-haiku-4-5"},
  "capable": {"provider": "anthropic", "name": "claude-sonnet-4-20250514"}
}
```

### agents

Agent configuration. Each agent has:

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `name` | string | (varies) | Display name (ou, zeno, cato, hiro, rumi, alan) |
| `model` | string | "capable" | Model alias to use |
| `enabled` | bool | true | Whether agent is active |

**Agent roles:**

| Role | Default Name | Default Model | Purpose |
|------|--------------|---------------|---------|
| relay | ou | fast | Message routing, conversation |
| data | zeno | capable | Vault search |
| agenda | cato | capable | Schedule management |
| action | hiro | capable | External actions (disabled by default) |
| pattern | rumi | capable | Memory extraction, rules |
| code | alan | capable | Code intelligence (dev only, disabled) |

Disabled agents are not instantiated and their scheduled tasks don't run.

### schedule

Scheduled task configuration.

All scheduled tasks use the `"time"` field (list of `"HH:MM"` strings) for time-based scheduling. Interval-based tasks only support `"enabled"`.

#### Fixed-time tasks

| Task | Default | Description |
|------|---------|-------------|
| `pattern_infer` | 04:00 | Memory extraction, consolidation, rule promotion |
| `memory_migrate` | 04:00 (disabled) | Process seed files from vault/Migration/ |
| `vault_scan` | 03:30 | Scan vault for chronological entries → agenda.json |
| `index_rebuild` | 04:30 | Rebuild vault search indices |
| `archive_rotation` | 05:00 | Archive old messages |

Fields:
```json
{
  "enabled": true,
  "time": ["04:00"]
}
```

Multiple times are supported: `"time": ["04:00", "16:00"]`

#### Time-list tasks

| Task | Default | Description |
|------|---------|-------------|
| `agenda_review` | xx:55 (04-23) | Process agenda files (conditional on changes) |

Fields:
```json
{
  "enabled": true,
  "time": ["04:55","05:55","06:55","07:55","08:55","09:55",
           "10:55","11:55","12:55","13:55","14:55","15:55",
           "16:55","17:55","18:55","19:55","20:55","21:55",
           "22:55","23:55"]
}
```

**Conditional execution:** Agenda review checks file hashes before running. If nothing changed, no LLM call is made. Morning (04:55) and evening (23:55) runs are unconditional.

#### Interval tasks

| Task | Interval | Description |
|------|----------|-------------|
| `agenda_midnight` | 00:00 daily | Regenerate Agenda.md for the new day |
| `session_summary` | 6 hours | Extract session insights from recent conversations |
| `action_tasks` | 15 minutes | Run due action tasks |

Fields:
```json
{
  "enabled": true
}
```

Interval is hardcoded; only `enabled` is configurable.

### updates

Memory migration and housekeeping.

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `auto_migrate` | bool | true | Automatically process seed files |
| `schedule` | string | "04:00" | Time for update tasks |

## Minimal Config

The smallest working config:

```json
{
  "llm": {
    "providers": {
      "anthropic": {
        "api_key": "sk-ant-..."
      }
    }
  }
}
```

Everything else uses defaults.

## Environment Variables

| Variable | Purpose |
|----------|---------|
| `ANTHROPIC_API_KEY` | Anthropic API key (fallback) |
| `OPENAI_API_KEY` | OpenAI API key (fallback) |
| `OUTHEIS_HUMAN_DIR` | Override human directory |
| `OUTHEIS_VAULT` | Override primary vault |

Environment variables take precedence over config file values.

## CLI Commands

```bash
# Show current config
outheis config show

# Edit config (opens in $EDITOR)
outheis config edit

# Set a value
outheis config set human.language de

# Validate config
outheis config validate
```

## Validation

Config is validated on load. Invalid config prevents daemon startup:

- Required fields must be present
- Types must match (string, int, bool, array)
- Referenced model aliases must exist
- Provider names must be valid

## Hot Reload

Some settings can be reloaded without restarting:

- Agent `enabled` status
- Schedule times
- Model aliases

Others require restart:

- Provider configuration
- Vault paths
- Signal configuration

```bash
# Reload config
outheis reload

# Or restart
outheis stop && outheis start
```

## See Also

- [Architecture](architecture.md) — How components fit together
- [Memory](memory.md) — Memory system details
- [Agenda](agenda.md) — Agenda agent configuration
