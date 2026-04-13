
# Installation

---

## Requirements

- macOS or Linux
- Python 3.11+
- [signal-cli](https://github.com/AsamK/signal-cli) — required for Signal transport
- An Anthropic API key — or a locally running [Ollama](https://ollama.com) instance

---

## 1. Install signal-cli

signal-cli handles Signal messaging. Install it before outheis.

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

## 2. Install outheis

```
pip install outheis
```

---

## 3. Run the setup wizard

```
outheis init
```

The wizard will ask for:

- Your vault directory (where notes and memory are stored)
- Your preferred language
- Your Anthropic API key — or skip if using Ollama locally
- Your Signal phone number

---

## 4. Start

```
outheis start
```

The Web UI is available at `http://localhost:8080`.

---

## Updating

```
pip install --upgrade outheis
```
