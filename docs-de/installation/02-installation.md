
# Installation

---

## Voraussetzungen

- macOS oder Linux
- Python 3.11+
- [signal-cli](https://github.com/AsamK/signal-cli) — erforderlich für Signal-Transport
- Ein Anthropic-API-Schlüssel — oder eine lokal laufende [Ollama](https://ollama.com)-Instanz

---

## 1. signal-cli installieren

signal-cli übernimmt Signal-Messaging. Vor outheis installieren.

**macOS**

```
brew install signal-cli
```

**Ubuntu / Debian**

```
apt install signal-cli
```

Für andere Systeme: [signal-cli Releases](https://github.com/AsamK/signal-cli/releases).

---

## 2. outheis installieren

```
pip install outheis
```

---

## 3. Einrichtungsassistent starten

```
outheis init
```

Der Assistent fragt nach:

- Vault-Verzeichnis (wo Notizen und Memory gespeichert werden)
- Bevorzugter Sprache
- Anthropic-API-Schlüssel — oder überspringen bei Ollama
- Signal-Telefonnummer

---

## 4. Starten

```
outheis start
```

Die Web-Oberfläche ist unter `http://localhost:8080` erreichbar.

---

## Aktualisieren

```
pip install --upgrade outheis
```
