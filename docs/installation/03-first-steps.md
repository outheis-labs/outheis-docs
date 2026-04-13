
# First Steps

After `outheis init` and `outheis start`, run through these steps to verify everything works.

---

## 1. Web interface

Open [http://localhost:8080](http://localhost:8080) in your browser. You should see the outheis Web UI.

Type a message in the chat field and send it. The relay agent (ou) responds. If you get a response, the dispatcher, relay, and your API key are working.

---

## 2. Terminal interface

In a second terminal window:

```
outheis chat
```

Type a message and press Enter. Same relay, different interface. Useful for scripting or when a browser isn't available.

---

## 3. First agent runs

Once your vault contains data, trigger the agents from the Web UI: open the **Scheduler** tab and click **Run now** next to the agent you want to run.

- **Agenda** — generates today's daily view from your vault
- **Pattern** — extracts memory from your notes and conversations

The pattern agent needs a few days of history to produce meaningful results. On first run it will find little — this is expected.

Alternatively, from the terminal:

```
outheis task run agenda
outheis task run pattern
```

---

## 4. Signal

First, register your phone number with signal-cli. This happens outside of outheis:

```
signal-cli -a +YOURNUMBER register
signal-cli -a +YOURNUMBER verify CODE
```

Then open the Web UI, go to **Configuration** → **Signal**, and fill in **Bot phone** with the registered number. Restart via the **Restart** button in the **Overview** tab.

Send a Signal message to the registered number. outheis responds via Signal the same way it responds in the Web UI.

See [Communication](05-communication.md) for details on all transport channels.
