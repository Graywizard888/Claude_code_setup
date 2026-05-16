# Claude_code_setup

<div align="center">
    <img src="https://raw.githubusercontent.com/Graywizard888/Claude_code_setup/main/.icons/claude.jpg" width="350px">
</div>

### ★ TERMUX EDITION · v2.1.112 ★
#### ~ crafted by Graywizard ~

---

![Platform](https://img.shields.io/badge/Platform-Android%20%2F%20Termux-brightgreen?style=for-the-badge&logo=android)
![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python)
![Version](https://img.shields.io/badge/Claude%20Code-v2.1.112%20-purple?style=for-the-badge)
![Privacy](https://img.shields.io/badge/Telemetry-DISABLED-red?style=for-the-badge&logo=shield)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

**A self-contained, one-command installer for Claude Code on Android Termux.**  
Pinned to a stable version. Privacy-hardened out of the box. Fully personalised.

</div>

---


## 🧠 What is this?

`claude_code_setup.py` is a **beautiful, interactive Python script** that automates the complete setup of [Claude Code](https://docs.anthropic.com/claude/docs/claude-code) inside **Termux** (Android Linux userland).

It handles everything in 4 guided phases:

| Phase | Task |
|-------|------|
| 1 | Install Node.js via `pkg` |
| 2 | Install Claude Code `v2.1.112` via `npm` |
| 3 | Collect your user profile, preferences & Claude plan type interactively |
| 4 | Write hardened `settings.json` + personalised `CLAUDE.md` |

---

## 📌 Why pinned to v2.1.112?

> Later versions of `@anthropic-ai/claude-code` are known to **break on Termux** due to filesystem changes and claude code moved to x86 native architecture only. Also disabled Auto updates to prevent auto updates.
> This script deliberately pins to **v2.1.112** — tested, confirmed stable, and production-ready on Termux.

---

## ✨ Features

- 🎨 **Beautiful TUI** — colourful ASCII banner, braille spinner, phase headers
- 📦 **Auto-installs Node.js** if not present via `pkg`
- 📌 **Pinned version** — no surprise breakage from upstream updates
- 👤 **Interactive user profiling** — name, coding level, languages, device specs
- 🔍 **Auto-detects** ABIs, RAM, Android version from device
- 🛡️ **Privacy-first** — all telemetry and non-essential traffic disabled by default
- 🔒 **Hardened permissions** — safe bash allowlist + dangerous command blocklist
- 📊 **Token Status Bar** — live context %, 5-hour & 7-day rate-limit bars inside Claude Code
- 🗑️ **Clean uninstaller** — double-confirm safety, removes every Claude-related file
- ✅ **Post-install verification** — confirms everything is correctly set up

---

## 📱 Requirements

| Requirement | Details |
|-------------|---------|
| **Device** | Any Android device running Termux |
| **Android** | 7.0+ recommended (tested on Android 16) |
| **Termux** | Latest from [F-Droid](https://f-droid.org/packages/com.termux/) (not Play Store) |
| **Python** | 3.x (pre-installed in Termux) — **do not uninstall**, required by statusline |
| **Internet** | Required for `pkg` and `npm` downloads |
| **Storage** | ~200 MB free space |

> **Note:** Install Termux from **F-Droid only**. The Play Store version is Experimental and will cause issues.

---

## 📥 Installation

**1. Open Termux and update packages:**
```bash
pkg update && pkg upgrade -y
```

**2. Clone this repo or download the script:**
```bash
# Clone
git clone https://github.com/Graywizard888/Claude_code_setup.git
cd Claude_code_setup
```

```
# OR download directly
curl -O https://raw.githubusercontent.com/Graywizard888/Claude_code_setup/main/claude_code_setup.py
```

**3. Run the setup script:**
```bash
python claude_code_setup.py
```

That's it. The interactive menu takes it from here.

---

## 🚀 Usage

```
╔═══════════════════════════════════════════════╗
║                                               ║
║   1   Install Claude Code                     ║
║       ┃ Full install + personalised config    ║
║       ┃ Pinned to v2.1.112 (stable)           ║
║                                               ║
║   2   Uninstall Claude Code                   ║
║       ┃ Complete removal                      ║
║       ┃ Two-step confirmation                 ║
║                                               ║
║   3   Add Settings Only                       ║
║       ┃ Write recommended settings.json       ║
║       ┃ Safe to run on existing install       ║
║                                               ║
║   4   Enable Token Status Bar                 ║
║       ┃ Install statusline.py                 ║
║       ┃ Shows ctx%, 5-hour & 7-day limits     ║
║                                               ║
║   5   Exit                                    ║
╚═══════════════════════════════════════════════╝
```

### Option 1 — Install

Walks you through 4 phases:

1. **Dependencies** — Checks for Node.js, installs if missing
2. **Claude Code** — Installs pinned `v2.1.112` globally via npm
3. **User Profile** — Asks for your name, skill level, languages, device info, and Claude plan type
4. **Config Files** — Writes `~/.claude/settings.json` and `~/.claude/CLAUDE.md`

At the end, you are offered to also enable the Token Status Bar immediately.

### Option 2 — Uninstall

Performs a clean, complete removal with **two separate confirmation prompts** (`YES` → `UNINSTALL`) to prevent accidents.

### Option 3 — Add Settings Only

Writes (or overwrites) `~/.claude/settings.json` with the latest recommended config without doing a full install. Safe to run on an existing Claude Code setup.

### Option 4 — Enable Token Status Bar

Installs `~/.claude/statusline.py` and wires the `statusLine` key into `settings.json`. Prompts you to select your Claude plan (Pro / Max5 / Max20) so the bars show the correct token limits.

---

## ⚙️ What gets installed & configured

### Files written

| File | Purpose |
|------|---------|
| `~/.claude/settings.json` | Token limits, telemetry, permissions, statusLine hook |
| `~/.claude/CLAUDE.md` | Your personalised Claude context & behaviour rules (includes token-check instructions) |
| `~/.claude/statusline.py` | Token status bar script (installed by Option 1 or Option 4) |
| `~/.claude/statusline_cache.json` | Live token-usage cache written by statusline on each render |

### `settings.json` highlights

```json
{
  "env": {
    "DISABLE_TELEMETRY": "1",
    "DISABLE_ERROR_REPORTING": "1",
    "CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC": "1",
    "DISABLE_NON_ESSENTIAL_MODEL_CALLS": "1",
    "MAX_THINKING_TOKENS": "10000",
    "CLAUDE_CODE_MAX_OUTPUT_TOKENS": "8000",
    "CLAUDE_CODE_AUTOCOMPACT_PCT_OVERRIDE": "50",
    "CLAUDE_CODE_MAX_TOOL_USE_CONCURRENCY": "3",
    "CLAUDE_CODE_TMPDIR": "/data/data/com.termux/files/usr/tmp",
    "ANTHROPIC_SMALL_FAST_MODEL": "claude-haiku-4-5-20251001",
    "CLAUDE_CODE_SUBAGENT_MODEL": "claude-haiku-4-5-20251001",
    "TMPDIR": "/data/data/com.termux/files/usr/tmp",
    "EDITOR": "nano",
    "USE_BUILTIN_RIPGREP": "1"
  },
  "autoUpdates": false,
  "includeCoAuthoredBy": false,
  "effortLevel": "high",
  "showThinkingSummaries": true,
  "autoMemoryEnabled": true
}
```

### `CLAUDE.md` personalisation

Dynamically generated from your answers + auto-detected device info. Also includes token-check rules so Claude warns you before starting heavy tasks when limits are near:

```markdown
- Name: YourName
- Coding Proficiency: Beginner / Intermediate / Advanced / Expert
- Preferred Languages: python, bash, kotlin ...
- Device: OnePlus 12R IN
- Processor: Snapdragon 8 Gen 2
- ABIs: arm64-v8a, armeabi-v7a
- RAM: 7.0G
- Android: 16 (SDK 36)

- Check token usage in .claude/statusline_cache.json ...
- Warn and ask "can we continue?" if ctx/rl5/rl7 is at 75%+ ...
```

### Token Status Bar

When enabled, a live status bar appears at the bottom of Claude Code showing:

```
  🤖 Current Model    claude-sonnet-4-6
  🧠 Chat Context     ████████░░░░░░░░░░░░░░░░   35.0%
  ⏱  5-hour limit     ██░░░░░░░░░░░░░░░░░░░░░░   10.5%
  📅 7-day limit      █░░░░░░░░░░░░░░░░░░░░░░░    4.0%
```

Supports three plan tiers:

| Plan | 5-hour token limit |
|------|--------------------|
| `pro` | 44,000 |
| `max5` | 88,000 |
| `max20` | 220,000 |

> ⚠️ **Do NOT uninstall Python from Termux** — `statusline.py` requires Python to run.

---

## 🛡️ Privacy Hardening

Every install applies these protections automatically:

| Setting | Status |
|---------|--------|
| Telemetry | ❌ DISABLED |
| Error reporting | ❌ DISABLED |
| Non-essential network traffic | ❌ DISABLED |
| Auto-updates | ❌ DISABLED |
| Co-authored-by git tag | ❌ DISABLED |
| Non-essential model calls | ❌ DISABLED |

### Permission allowlist (safe read-only commands)

```
grep, cat, ls, find, head, tail, wc, sort
git status, git log, git diff, git branch
node, python, python3, Read(*)
```

### Permission ask-list (prompts before running)

```
Write(*), Edit(*)
rm -rf, bash, chmod, curl, wget
WebFetch(*), WebSearch(*)
```

### Permission blocklist (always denied)

```
Read(.env), Read(.env.*)
Read(secrets/**), Read(**/credentials.json)
Read(**/*.pem), Read(**/*.key)
```

---

## 📁 File Structure

```
~/ (Termux home)
├── claude_code_setup.py          ← this script
└── .claude/
    ├── settings.json              ← hardened Claude Code settings
    ├── CLAUDE.md                  ← your personalised context file
    ├── statusline.py              ← token status bar (optional, Option 4)
    └── statusline_cache.json      ← live token-usage cache (auto-written)
```

---

## 🗑️ Uninstalling

The uninstaller removes **everything**:

```
● @anthropic-ai/claude-code     (global npm package)
● ~/.claude/                    (config, CLAUDE.md, statusline, history)
● ~/.claude.json                (auth / account file)
● ~/.cache/claude-cli-nodejs    (npm CLI cache)
● ~/.config/claude              (system config)
```

Requires typing `YES` followed by `UNINSTALL` — no accidental removals.

---

## ⚡ Quick Start after setup

```bash
# Launch Claude Code
claude

# Check installed version
claude --version

# One-shot prompt (no interactive session)
claude -p "Write a Python hello world"

# View your context file
cat ~/.claude/CLAUDE.md

# View settings
cat ~/.claude/settings.json

# View live token usage
cat ~/.claude/statusline_cache.json
```

> First launch will ask for your **Anthropic API key**.  
> Get one at [console.anthropic.com](https://console.anthropic.com)

> Or login via your google Claude subscription account in claude

---

## 🔑 Getting an Anthropic API Key

1. Go to [console.anthropic.com](https://console.anthropic.com)
2. Sign up / log in
3. Navigate to **API Keys** → **Create Key**
4. Paste it when `claude` asks on first launch

---

## 📊 Tested On

| Device | Android | Termux | Status |
|--------|---------|--------|--------|
| OnePlus 12R IN | Android 16 (SDK 36) | Latest | ✅ Working |
| Snapdragon 8 Gen 2 | — | — | ✅ Working |

---

## 🤝 Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you'd like to change.

1. Fork the repo
2. Create your branch: `git checkout -b feature/your-feature`
3. Commit: `git commit -m "Add your feature"`
4. Push: `git push origin feature/your-feature`
5. Open a Pull Request

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

<div align="center">

```
✦ Created by Graywizard ✦
```

*Running AI on Android, one Termux session at a time.*

[![GitHub](https://img.shields.io/badge/GitHub-Graywizard-black?style=flat-square&logo=github)](https://github.com/Graywizard888)

</div>
