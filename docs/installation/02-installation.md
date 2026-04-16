
# Installation

---

## Requirements

- macOS or Linux
- Python 3.11+
- An Anthropic API key — or a locally running [Ollama](https://ollama.com) instance
- [signal-cli](https://github.com/AsamK/signal-cli) — optional, for Signal Messenger integration

---

## 1. Install outheis

```
pipx install outheis
```

> **Note:** If pipx warns that `~/.local/bin` is not on your PATH, run `pipx ensurepath` and restart your shell.

---

## 2. Install signal-cli (optional)

signal-cli enables Signal Messenger as a communication channel. Skip this step if you plan to use the Web UI or CLI only.

**macOS**

```
brew install signal-cli
```

**Ubuntu / Debian**

```
apt install signal-cli
```

For other systems, see the [signal-cli releases](https://github.com/AsamK/signal-cli/releases).

---

## 3. Run the setup wizard

```
outheis init
```

The wizard will ask for:

- Your vault directory (where notes and memory are stored)
- Your preferred language
- Your Anthropic API key — or skip if using Ollama locally
- Your Signal phone number (optional)

---

## 4. Start

```
outheis start
```

The Web UI is available at `http://localhost:8080`.

---

## Updating

```
pipx upgrade outheis
```

---

## Multiple accounts on the same machine

Each user's data is isolated under `~/.outheis/`. The only shared resource is the WebUI port (default: 8080). If more than one user runs outheis on the same host, each must use a different port.

Set `webui.port` in `~/.outheis/human/config.json`:

```json
{
  "webui": {
    "port": 8081
  }
}
```
