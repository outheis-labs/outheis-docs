---
title: Signal
---

# Signal

*Signal Messenger transport via signal-cli JSON-RPC.*

## Overview

The Signal transport connects outheis to Signal Messenger. It runs as a standalone process (`outheis signal`), separate from the main daemon. It receives messages from Signal, forwards them to relay, and sends responses back.

Underlying mechanism: signal-cli in `--json-rpc` mode, communicating over stdin/stdout.

## Architecture

The central design is a **dedicated reader thread** that owns all stdout from signal-cli. This solves a race condition that arises when send and receive both try to read from the same subprocess stdout.

```
signal-cli (jsonRpc)
     │
     ▼
 _read_loop() thread
     ├── receive events → Queue (for incoming messages)
     └── RPC responses → dict + Event (for send confirmations)

Main thread: read_message() ← Queue.get()
Send path:  _send_request() → stdin write → Event.wait()
```

### Classes

- `SignalRPC` — `transport/signal_rpc.py`: manages the signal-cli subprocess, reader thread, send/receive primitives
- `SignalTransport` — `transport/signal.py`: message loop, authorization, watcher thread, markdown stripping

### Concurrency model

| Component | Mechanism |
|-----------|-----------|
| Incoming messages | `_receive_queue` — `Queue.get()` blocks until a message arrives |
| RPC responses (send confirmations) | `_response_map` + `threading.Event` per request ID |
| Stdin writes | `_stdin_lock` — prevents interleaved writes |

The reader thread is the only consumer of signal-cli stdout. Nothing else reads from it.

## Message Flow

1. signal-cli emits a receive event on stdout
2. `_read_loop` parses the JSON and puts it in `_receive_queue`
3. `read_message()` returns the parsed `SignalMessage`
4. `SignalTransport._handle_message()` checks authorization, creates a user message, appends to `messages.jsonl`
5. A watcher thread (`_watch_responses`) polls for a relay reply addressed to `transport`
6. When found, calls `send_message(sender_uuid, text)` via `_send_request()`

## Markdown Stripping

Before sending, `_strip_markdown()` removes markdown syntax deterministically. This is a transport concern — the model returns content as-is; stripping happens here.

| Input | Output |
|-------|--------|
| `**bold**`, `__bold__` | plain text |
| `*italic*`, `_italic_` | plain text |
| `## Heading` | heading text without `#` |
| `` `inline code` `` | code text |
| `- [ ]`, `- [x]` checkboxes | plain text |
| `- item`, `* item` bullets | plain text |
| `---` horizontal rule | `____________________` (20 underscores) |

The horizontal rule replacement renders as a solid dividing line in Signal's UI.

## Authorization

- `signal.allowed` in `config.json`: whitelist of phone numbers permitted to send messages
- `human.phone` is always allowed regardless of the whitelist
- UUIDs are learned on first contact and saved to `~/.outheis/human/signal.json`
- First-time setup requires trusting the identity key via `signal-cli trust` (see installation guide)

An empty `allowed` array means only `human.phone` can interact with the bot.

## Profile Name

On startup, the bot's Signal profile display name is set from `config.signal.bot_name` via the `updateProfile` RPC call. This is what Signal contacts see as the bot's name.

## Voice Transcription

If `faster-whisper` is installed, voice messages are transcribed before being forwarded to relay. This is an optional dependency — the transport works without it; voice messages are silently skipped if `faster-whisper` is absent.

## Configuration

```json
{
  "signal": {
    "enabled": true,
    "bot_name": "Ou",
    "bot_phone": "+49...",
    "allowed": []
  }
}
```

| Key | Description |
|-----|-------------|
| `enabled` | Enable Signal transport |
| `bot_name` | Display name set on the Signal profile at startup |
| `bot_phone` | The phone number registered with signal-cli |
| `allowed` | Whitelist of phone numbers. Empty = human.phone only |

## Running

```bash
outheis signal        # foreground
outheis signal -v     # verbose (shows tool calls)
```

Signal transport runs separately from the main daemon. Both can run simultaneously — the daemon handles scheduled tasks and direct CLI queries; the Signal transport handles incoming Signal messages.

## File Locations

```
src/outheis/transport/
├── signal.py        # SignalTransport: message loop, watcher, markdown stripping
└── signal_rpc.py    # SignalRPC: jsonRpc subprocess, reader thread, send/receive
```
