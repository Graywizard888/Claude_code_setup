#!/usr/bin/env python3
"""
Claude Code Setup for Termux
----------------------------
Created by Graywizard

A small, self-contained installer / uninstaller for Claude Code on Termux.
- Installs nodejs via pkg
- Installs the *pinned* Claude Code version 2.1.112 via npm
  (later versions are known to break on Termux)
- Creates ~/.claude/settings.json and ~/.claude/CLAUDE.md
- Uninstall option removes Claude Code and every claude-related file
"""

import itertools
import json
import os
import re
import shutil
import subprocess
import sys
import threading
import time
from pathlib import Path

CLAUDE_VERSION  = "2.1.112"
CLAUDE_PKG      = f"@anthropic-ai/claude-code@{CLAUDE_VERSION}"
CLAUDE_PKG_NAME = "@anthropic-ai/claude-code"
HOME            = Path.home()
CLAUDE_DIR      = HOME / ".claude"
SETTINGS_FILE   = CLAUDE_DIR / "settings.json"
CLAUDE_MD_FILE  = CLAUDE_DIR / "CLAUDE.md"

class C:
    RESET    = "\033[0m"
    BOLD     = "\033[1m"
    DIM      = "\033[2m"
    RED      = "\033[1;31m"
    GREEN    = "\033[1;32m"
    YELLOW   = "\033[1;33m"
    BLUE     = "\033[1;34m"
    MAGENTA  = "\033[1;35m"
    CYAN     = "\033[1;36m"
    WHITE    = "\033[1;37m"
    BG_GREEN   = "\033[42m"
    BG_BLUE    = "\033[44m"
    BG_RED     = "\033[41m"
    BG_YELLOW  = "\033[43m"
    BG_MAGENTA = "\033[45m"

CHECK    = "✅"
CROSS    = "❌"
ARROW    = "➜"
STAR     = "⭐"
GEAR     = "⚙️ "
PKG_IC   = "📦"
ROCKET   = "🚀"
WARN_IC  = "⚠️ "
INFO_IC  = "ℹ️  "
WRENCH   = "🔧"
PHONE    = "📱"
CHIP     = "💻"
FOLDER   = "📁"
FILE_IC  = "📄"
SPARKLE  = "✨"
DIAMOND  = "💎"
USER_IC  = "👤"
CODE_IC  = "🧑‍💻"
SHIELD   = "🛡️ "
TRASH    = "🗑️ "
LOCK     = "🔒"
BRAIN    = "🧠"
BOOK     = "📘"
FIRE     = "🔥"
KEY_IC   = "🔑"
GPU_IC   = "🎮"
SHELL_IC = "🐚"

def clear_screen():
    os.system("clear" if os.name == "posix" else "cls")

def term_width(default=60):
    try:
        return shutil.get_terminal_size((default, 20)).columns
    except Exception:
        return default

def print_line():
    print(f"{C.CYAN}{'═' * 59}{C.RESET}")

def print_thin_line():
    print(f"{C.DIM}{C.CYAN}{'─' * 59}{C.RESET}")

def success_msg(msg):
    print(f"  {CHECK} {C.GREEN}{msg}{C.RESET}")

def error_msg(msg):
    print(f"  {CROSS} {C.RED}{msg}{C.RESET}")

def info_msg(msg):
    print(f"  {INFO_IC} {C.BLUE}{msg}{C.RESET}")

def warn_msg(msg):
    print(f"  {WARN_IC} {C.YELLOW}{msg}{C.RESET}")

class Spinner:
    """Braille-dot spinner that runs in a background thread."""
    FRAMES = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"

    def __init__(self, msg):
        self.msg   = msg
        self._stop = threading.Event()
        self._t    = threading.Thread(target=self._spin, daemon=True)

    def _spin(self):
        for frame in itertools.cycle(self.FRAMES):
            if self._stop.is_set():
                break
            sys.stdout.write(f"\r  {C.CYAN}{frame}{C.RESET} {self.msg}")
            sys.stdout.flush()
            time.sleep(0.1)
        sys.stdout.write("\r" + " " * (len(self.msg) + 10) + "\r")
        sys.stdout.flush()

    def __enter__(self):
        self._t.start()
        return self

    def __exit__(self, *_):
        self._stop.set()
        self._t.join()

def banner():
    """Print the Claude Code ASCII banner, restyled with Gemini-style border."""
    w = term_width()
    big = [
        "  ██████╗██╗      █████╗ ██╗   ██╗██████╗ ███████╗",
        " ██╔════╝██║     ██╔══██╗██║   ██║██╔══██╗██╔════╝",
        " ██║     ██║     ███████║██║   ██║██║  ██║█████╗  ",
        " ██║     ██║     ██╔══██║██║   ██║██║  ██║██╔══╝  ",
        " ╚██████╗███████╗██║  ██║╚██████╔╝██████╔╝███████╗",
        "  ╚═════╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═════╝ ╚══════╝",
        "                                                  ",
        "         ██████╗ ██████╗ ██████╗ ███████╗         ",
        "        ██╔════╝██╔═══██╗██╔══██╗██╔════╝         ",
        "        ██║     ██║   ██║██║  ██║█████╗           ",
        "        ██║     ██║   ██║██║  ██║██╔══╝           ",
        "        ╚██████╗╚██████╔╝██████╔╝███████╗         ",
        "         ╚═════╝ ╚═════╝ ╚═════╝ ╚══════╝         ",
    ]
    inner_w = len(big[0])   # 50
    palette = [
        C.CYAN, C.CYAN, C.BLUE, C.BLUE, C.MAGENTA, C.MAGENTA,
        C.WHITE,
        C.MAGENTA, C.MAGENTA, C.BLUE, C.BLUE, C.CYAN, C.CYAN,
    ]

    clear_screen()
    print()
    if w >= inner_w + 4:
        bar = "═" * (inner_w + 2)
        print(f"{C.CYAN}{C.BOLD}╔{bar}╗{C.RESET}")
        print(f"{C.CYAN}{C.BOLD}║{' ' * (inner_w + 2)}║{C.RESET}")
        for line, color in zip(big, palette):
            print(f"{C.CYAN}{C.BOLD}║ {color}{C.BOLD}{line}{C.RESET}{C.CYAN}{C.BOLD} ║{C.RESET}")
        print(f"{C.CYAN}{C.BOLD}║{' ' * (inner_w + 2)}║{C.RESET}")
        tag = f"★  TERMUX EDITION  •  v{CLAUDE_VERSION}  ★"
        sub = "~  crafted by Graywizard  ~"
        print(f"{C.CYAN}{C.BOLD}║ {C.YELLOW}{C.BOLD}{tag.center(inner_w)}{C.RESET}{C.CYAN}{C.BOLD} ║{C.RESET}")
        print(f"{C.CYAN}{C.BOLD}║ {C.MAGENTA}{C.BOLD}{sub.center(inner_w)}{C.RESET}{C.CYAN}{C.BOLD} ║{C.RESET}")
        print(f"{C.CYAN}{C.BOLD}║{' ' * (inner_w + 2)}║{C.RESET}")
        print(f"{C.CYAN}{C.BOLD}╚{bar}╝{C.RESET}\n")
    else:
        bar = "═" * max(26, w - 2)
        print(f"{C.CYAN}{C.BOLD}╔{bar}╗{C.RESET}")
        print(f"{C.MAGENTA}{C.BOLD}{'CLAUDE  CODE'.center(len(bar) + 2)}{C.RESET}")
        print(f"{C.YELLOW}{C.BOLD}{('★ v' + CLAUDE_VERSION + ' ★').center(len(bar) + 2)}{C.RESET}")
        print(f"{C.BLUE}{C.BOLD}{'TERMUX  EDITION'.center(len(bar) + 2)}{C.RESET}")
        print(f"{C.MAGENTA}{C.BOLD}{'~ by Graywizard ~'.center(len(bar) + 2)}{C.RESET}")
        print(f"{C.CYAN}{C.BOLD}╚{bar}╝{C.RESET}\n")
    print_line()


def phase_header(n: int, total: int, title: str):
    """Redraw the banner with a phase indicator beneath it."""
    banner()
    print(f"  {GEAR} {C.BOLD}{C.WHITE} PHASE {n} / {total} — {title}{C.RESET}")
    print_thin_line()
    print()


def terminated_banner():
    w = term_width()
    inner = "  ★  SCRIPT  TERMINATED  !!  ★  "
    if w >= len(inner) + 4:
        bar = "═" * (len(inner) + 2)
        print()
        print(f"{C.RED}{C.BOLD}╔{bar}╗{C.RESET}")
        print(f"{C.RED}{C.BOLD}║{' ' * (len(inner) + 2)}║{C.RESET}")
        print(f"{C.RED}{C.BOLD}║ {C.YELLOW}{C.BOLD}{inner}{C.RESET}{C.RED}{C.BOLD} ║{C.RESET}")
        print(f"{C.RED}{C.BOLD}║{' ' * (len(inner) + 2)}║{C.RESET}")
        print(f"{C.RED}{C.BOLD}╚{bar}╝{C.RESET}")
        print(f"{C.MAGENTA}{C.BOLD}{'~ Goodbye ~'.center(len(bar) + 2)}{C.RESET}\n")
    else:
        print(f"\n{C.RED}{C.BOLD}>>> SCRIPT TERMINATED !! <<<{C.RESET}")
        print(f"{C.MAGENTA}{C.BOLD}~ Goodbye ~{C.RESET}\n")

def ask(prompt, default=None):
    """Prompt with optional default. Re-asks until non-empty."""
    suffix = f" {C.DIM}[{default}]{C.RESET}" if default else ""
    while True:
        try:
            ans = input(f"  {ARROW} {C.WHITE}{prompt}{suffix}: {C.RESET}").strip()
        except EOFError:
            ans = ""
        if ans:
            return ans
        if default is not None:
            return default
        warn_msg("Value cannot be empty.")


def confirm(prompt, default_yes=False):
    suffix = "[Y/n]" if default_yes else "[y/N]"
    try:
        ans = input(f"  {ARROW} {C.WHITE}{prompt} {suffix}: {C.RESET}").strip().lower()
    except EOFError:
        ans = ""
    if not ans:
        return default_yes
    return ans in ("y", "yes")

def run(cmd, check=True, capture=False):
    """
    Run a shell command.  `cmd` may be a list or string.
    - check=True   → raise on non-zero exit
    - capture=True → return (stdout, stderr, returncode); do NOT print live
    """
    if isinstance(cmd, str):
        printable = cmd
        shell = True
    else:
        printable = " ".join(cmd)
        shell = False

    if not capture:
        print(f"  {C.DIM}$ {printable}{C.RESET}")

    if capture:
        proc = subprocess.run(
            cmd, shell=shell, text=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        )
        if check and proc.returncode != 0:
            error_msg(proc.stderr.strip() or proc.stdout.strip())
            raise subprocess.CalledProcessError(proc.returncode, cmd)
        return proc.stdout, proc.stderr, proc.returncode

    proc = subprocess.run(cmd, shell=shell)
    if check and proc.returncode != 0:
        raise subprocess.CalledProcessError(proc.returncode, cmd)
    return "", "", proc.returncode


def have(binary):
    return shutil.which(binary) is not None

def detect_abis():
    try:
        out, _, rc = run(["getprop", "ro.product.cpu.abilist"],
                         check=False, capture=True)
        if rc == 0 and out.strip():
            return out.strip()
    except Exception:
        pass
    return "arm64-v8a,armeabi-v7a,armeabi"


def detect_ram():
    try:
        with open("/proc/meminfo") as f:
            for line in f:
                if line.startswith("MemTotal:"):
                    kb = int(re.search(r"(\d+)", line).group(1))
                    return f"{kb / 1024 / 1024:.1f}G"
    except Exception:
        pass
    return "Unknown"


def detect_android():
    ver = "Unknown"
    sdk = "?"
    try:
        out, _, rc = run(["getprop", "ro.build.version.release"],
                         check=False, capture=True)
        if rc == 0 and out.strip():
            ver = out.strip()
        out, _, rc = run(["getprop", "ro.build.version.sdk"],
                         check=False, capture=True)
        if rc == 0 and out.strip():
            sdk = out.strip()
    except Exception:
        pass
    return f"{ver} (SDK {sdk})"

SETTINGS_TEMPLATE = {
    "cleanupPeriodDays": 7,
    "env": {
        "DISABLE_TELEMETRY": "1",
        "MAX_THINKING_TOKENS": "10000",
        "CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC": "1",
        "DISABLE_NON_ESSENTIAL_MODEL_CALLS": "1",
        "CLAUDE_CODE_MAX_OUTPUT_TOKENS": "8000",
        "CLAUDE_AUTOCOMPACT_PCT_OVERRIDE": "50",
        "ANTHROPIC_SMALL_FAST_MODEL": "claude-haiku-4-5-20251001",
        "CLAUDE_CODE_SUBAGENT_MODEL": "claude-haiku-4-5-20251001",
    },
    "includeCoAuthoredBy": False,
    "permissions": {
        "allow": [
            "Bash(grep:*)",
            "Bash(cat:*)",
            "Bash(ls:*)",
            "Bash(find:*)",
            "Bash(head:*)",
            "Bash(tail:*)",
            "Bash(wc:*)",
            "Bash(sort:*)",
            "Bash(git status:*)",
            "Bash(git log:*)",
            "Bash(git diff:*)",
            "Bash(git branch:*)",
            "Bash(node:*)",
            "Bash(python:*)",
            "Bash(python3:*)",
            "Read(*)",
        ],
        "deny": [
            "Bash(rm -rf /)",
            "Bash(rm -rf ~)",
            "Bash(rm -rf *)",
            "Bash(chmod 777 *)",
            "Bash(curl * | bash)",
            "Bash(wget * | bash)",
            "Read(.env)",
            "Read(.env.*)",
            "Read(secrets/**)",
            "Read(**/credentials.json)",
            "Read(**/*.pem)",
            "Read(**/*.key)",
        ],
    },
    "hooks": {
        "PostToolUse": [
            {
                "matcher": "Write|Edit",
                "hooks": [
                    {
                        "type": "command",
                        "command": "echo '[Hook] File modified: $CLAUDE_FILE_PATH'",
                    }
                ],
            }
        ]
    },
    "effortLevel": "high",
    "autoUpdates": False,
    "preferredNotifChannel": "terminal",
}


CLAUDE_MD_TEMPLATE = """- **Name**: {name}
- **Coding Proficiency**: {proficiency}
- **Preferred Languages**: {languages}
- **Shell**: {shell}
- **Platform**: Android / Termux (Linux userland on Android)
- **Device**: {device}
- **Processor / SoC**: {processor}
- **GPU**: {gpu}

Supported ABIs: {abis}
Total RAM : {ram}
Android Version : {android}

- When showing commands, explain what each flag and argument does.
- **ALWAYS provide FULL, COMPLETE, READY-TO-RUN code.**
- **Structure EVERY response** with clear, numbered steps.
- All code must include proper **error handling** and **input validation**.
- ask user before installing any package,tools in environment.
- Test once after code writing for proper functioning. No repeated re-runs unless it fails.
- No over-engineering. Match the simplest solution to the task where possible first suggest simple solution then complex.
- Use web search for any question involving current events, pricing, docs, versions, or APIs.
- Return a bullet summary of findings. No full article reproduction.
- Always cite the source URL inline.
- Use thinking only for architectural decisions, debugging complex logic, or multi-step planning.
- For simple tasks skip thinking entirely.
- Complex multi-file reasoning, system design switch to Opus /model.
"""

def install_nodejs():
    if have("node") and have("npm"):
        success_msg(f"Node.js already installed: {shutil.which('node')}")
        return
    info_msg("Installing Node.js via pkg ...")
    with Spinner("Installing Node.js..."):
        run(["pkg", "install", "-y", "nodejs"])
    if not (have("node") and have("npm")):
        raise RuntimeError("Node.js install failed (node/npm not on PATH).")
    success_msg("Node.js installed.")


def install_claude_code():
    info_msg(f"Installing {CLAUDE_PKG} via npm (this can take a few minutes) ...")
    print()
    run(["npm", "install", "-g", CLAUDE_PKG])
    success_msg("Claude Code installed.")


def uninstall_claude_code():
    if have("npm"):
        info_msg("Removing Claude Code via npm ...")
        with Spinner("Removing Claude Code package..."):
            run(["npm", "uninstall", "-g", CLAUDE_PKG_NAME], check=False)
        success_msg("npm package removed")
        print()
        with Spinner("Cleaning npm cache..."):
            run(["npm", "cache", "clean", "--force"], check=False)
        success_msg("npm cache cleaned")
    else:
        warn_msg("npm not found – skipping npm uninstall.")

    targets = [
        CLAUDE_DIR,
        HOME / ".claude.json",
        HOME / ".claude.json.backup",
        HOME / ".cache" / "claude-cli-nodejs",
        HOME / ".config" / "claude",
    ]
    print()
    info_msg("Removing Claude config files & directories...")
    print()
    for path in targets:
        if path.exists() or path.is_symlink():
            try:
                if path.is_dir() and not path.is_symlink():
                    shutil.rmtree(path)
                else:
                    path.unlink()
                print(f"    {C.RED}✗{C.RESET} {C.DIM}Removed {path}{C.RESET}")
            except Exception as exc:
                error_msg(f"Could not remove {path}: {exc}")
        else:
            print(f"    {C.DIM}Not present: {path}{C.RESET}")


def collect_user_info():
    """Prompt user + auto-detect → dict for CLAUDE.md.  [Logic unchanged]"""
    print(f"  {SPARKLE} {C.WHITE}Let's personalise your Claude Code experience.{C.RESET}")
    print(f"  {LOCK} {C.DIM}This data stays LOCAL on your device — zero data collection.{C.RESET}")
    print()
    print_thin_line()
    print()

    print(f"  {USER_IC} {C.BOLD}{C.CYAN}Your Name{C.RESET}")
    name = ask("Enter your name / alias", default="Unknown")
    success_msg(f"Name: {C.WHITE}{name}{C.RESET}")
    print()

    print(f"  {CODE_IC} {C.BOLD}{C.CYAN}Coding Proficiency{C.RESET}")
    print()
    print(f"       {C.BG_GREEN}{C.WHITE}{C.BOLD} 1 {C.RESET}  {C.GREEN}Beginner{C.RESET}")
    print(f"          {C.DIM}New to programming. Needs detailed explanations,{C.RESET}")
    print(f"          {C.DIM}comments on every line, and beginner-friendly language.{C.RESET}")
    print()
    print(f"       {C.BG_BLUE}{C.WHITE}{C.BOLD} 2 {C.RESET}  {C.BLUE}Intermediate{C.RESET}")
    print(f"          {C.DIM}Comfortable with basics. Knows data structures,{C.RESET}")
    print(f"          {C.DIM}OOP concepts, and can debug with some guidance.{C.RESET}")
    print()
    print(f"       {C.BG_MAGENTA}{C.WHITE}{C.BOLD} 3 {C.RESET}  {C.MAGENTA}Advanced{C.RESET}")
    print(f"          {C.DIM}Deep understanding of systems, architecture, and{C.RESET}")
    print(f"          {C.DIM}design patterns. Writes production-grade code.{C.RESET}")
    print()
    print(f"       {C.BG_RED}{C.WHITE}{C.BOLD} 4 {C.RESET}  {C.RED}Expert / Professional{C.RESET}")
    print(f"          {C.DIM}Industry-level. Understands low-level systems,{C.RESET}")
    print(f"          {C.DIM}compilers, security, and advanced optimisation.{C.RESET}")
    print()
    PROF_MAP = {
        "1": ("Beginner",            C.GREEN),
        "2": ("Intermediate",        C.BLUE),
        "3": ("Advanced",            C.MAGENTA),
        "4": ("Expert",              C.RED),
    }
    while True:
        choice = ask("Select proficiency [1/2/3/4]", default="1")
        if choice in PROF_MAP:
            proficiency, prof_color = PROF_MAP[choice]
            break
        warn_msg("Please enter 1, 2, 3, or 4.")
    success_msg(f"Proficiency: {prof_color}{C.BOLD}{proficiency}{C.RESET}")
    print()

    print(f"  {BOOK} {C.BOLD}{C.CYAN}Preferred Programming Languages{C.RESET}")
    languages = ask(
        "Enter your languages (comma-separated)",
        default="bash",
    )
    success_msg(f"Languages: {C.WHITE}{languages}{C.RESET}")
    print()

    print(f"  {SHELL_IC} {C.BOLD}{C.CYAN}Shell{C.RESET}")
    shell_name = ask(
        "Shell",
        default=os.environ.get("SHELL", "zsh").split("/")[-1],
    )
    success_msg(f"Shell: {C.WHITE}{shell_name}{C.RESET}")
    print()

    print(f"  {PHONE} {C.BOLD}{C.CYAN}Device Name{C.RESET}")
    device = ask(
        "Enter your device name (e.g., Samsung Galaxy S24, Pixel 9 Pro)",
        default="Unknown",
    )
    success_msg(f"Device: {C.WHITE}{device}{C.RESET}")
    print()

    print(f"  {CHIP} {C.BOLD}{C.CYAN}Processor / SoC{C.RESET}")
    processor = ask(
        "Enter your processor (e.g., Snapdragon 8 Gen 3, Dimensity 9300)",
        default="Unknown",
    )
    success_msg(f"Processor: {C.WHITE}{processor}{C.RESET}")
    print()

    print(f"  {GPU_IC} {C.BOLD}{C.CYAN}GPU{C.RESET}")
    gpu = ask("Enter your GPU (e.g., Adreno 750, Mali-G720)", default="Unknown")
    success_msg(f"GPU: {C.WHITE}{gpu}{C.RESET}")
    print()

    print_thin_line()
    print()
    info_msg("Auto-detecting device properties...")
    print()
    with Spinner("Detecting ABIs / RAM / Android version..."):
        abis    = detect_abis()
        ram     = detect_ram()
        android = detect_android()

    w = 30
    print(f"  {C.DIM}{C.WHITE}┌{'─' * (w + 14)}┐{C.RESET}")
    print(f"  {C.DIM}{C.WHITE}│{C.RESET}  {C.WHITE}ABIs    : {C.CYAN}{abis[:w]:<{w}}{C.RESET}{C.DIM}{C.WHITE} │{C.RESET}")
    print(f"  {C.DIM}{C.WHITE}│{C.RESET}  {C.WHITE}RAM     : {C.CYAN}{ram:<{w}}{C.RESET}{C.DIM}{C.WHITE} │{C.RESET}")
    print(f"  {C.DIM}{C.WHITE}│{C.RESET}  {C.WHITE}Android : {C.CYAN}{android:<{w}}{C.RESET}{C.DIM}{C.WHITE} │{C.RESET}")
    print(f"  {C.DIM}{C.WHITE}└{'─' * (w + 14)}┘{C.RESET}")
    print()
    success_msg("Device info collected")

    return {
        "name": name, "proficiency": proficiency, "languages": languages,
        "shell": shell_name, "device": device, "processor": processor,
        "gpu": gpu, "abis": abis, "ram": ram, "android": android,
    }


def write_config_files(user_info):
    """Write settings.json + CLAUDE.md.  [Logic unchanged]"""
    CLAUDE_DIR.mkdir(parents=True, exist_ok=True)
    success_msg(f"Directory ready: {C.WHITE}{CLAUDE_DIR}{C.RESET}")

    if SETTINGS_FILE.exists():
        warn_msg(f"{SETTINGS_FILE} already exists.")
        if not confirm("Overwrite?", default_yes=False):
            info_msg("Keeping existing settings.json.")
        else:
            SETTINGS_FILE.write_text(json.dumps(SETTINGS_TEMPLATE, indent=2))
            success_msg(f"Written: {SETTINGS_FILE}")
    else:
        SETTINGS_FILE.write_text(json.dumps(SETTINGS_TEMPLATE, indent=2))
        success_msg(f"Written: {SETTINGS_FILE}")

    md_content = CLAUDE_MD_TEMPLATE.format(**user_info)
    if CLAUDE_MD_FILE.exists():
        warn_msg(f"{CLAUDE_MD_FILE} already exists.")
        if not confirm("Overwrite?", default_yes=False):
            info_msg("Keeping existing CLAUDE.md.")
            return
    CLAUDE_MD_FILE.write_text(md_content)
    success_msg(f"Written: {CLAUDE_MD_FILE}")

def _get_tool_version(binary, flag="--version"):
    try:
        out, _, rc = run([binary, flag], check=False, capture=True)
        if rc == 0 and out.strip():
            return out.strip().splitlines()[0]
    except Exception:
        pass
    return shutil.which(binary) or "N/A"


def _print_install_summary(user_info, node_ver, npm_ver):
    clear_screen()
    print()
    print_line()
    print()
    print(f"  {C.GREEN}{C.BOLD}{CHECK} CLAUDE CODE SETUP FINISHED SUCCESSFULLY {CHECK}{C.RESET}")
    print()
    print_line()
    print()

    print(f"  {SPARKLE} {C.BOLD}{C.WHITE}Setup Summary{C.RESET}")
    print()

    col = 32
    W   = col + 22
    print(f"  {C.DIM}{C.WHITE}┌{'─' * W}┐{C.RESET}")

    def row(icon, label, value, color=C.CYAN):
        v = str(value)[:col]
        print(f"  {C.DIM}{C.WHITE}│{C.RESET}  {icon} {C.WHITE}{label:<13}: {color}{v:<{col}}{C.RESET}{C.DIM}{C.WHITE}│{C.RESET}")

    row(USER_IC,  "User",       user_info["name"])
    row(CODE_IC,  "Proficiency",user_info["proficiency"])
    row(BOOK,     "Languages",  user_info["languages"])
    row(SHELL_IC, "Shell",      user_info["shell"])
    row(ROCKET,   "Version",    f"v{CLAUDE_VERSION}")
    row(CHIP,     "Node.js",    node_ver)
    row(PKG_IC,   "npm",        npm_ver)
    row(PHONE,    "Device",     user_info["device"])
    row(CHIP,     "Processor",  user_info["processor"])
    row(GPU_IC,   "GPU",        user_info["gpu"])
    row(FOLDER,   "Config",     "~/.claude/")
    row(SHIELD,   "Telemetry",  "ALL DISABLED",  C.RED)
    row(LOCK,     "Privacy",    "FULLY HARDENED", C.GREEN)
    print(f"  {C.DIM}{C.WHITE}└{'─' * W}┘{C.RESET}")
    print()

    print(f"  {FIRE} {C.BOLD}{C.WHITE}What's been configured:{C.RESET}")
    print()
    print(f"    {CHECK} {C.GREEN}Pinned to v{CLAUDE_VERSION} — tested & stable on Termux{C.RESET}")
    print(f"    {CHECK} {C.GREEN}Complete code responses — no snippets, no placeholders{C.RESET}")
    print(f"    {CHECK} {C.GREEN}Step-by-step detailed explanations on every response{C.RESET}")
    print(f"    {CHECK} {C.GREEN}Proficiency-matched tuning ({user_info['proficiency']}){C.RESET}")
    print(f"    {CHECK} {C.GREEN}All telemetry & non-essential traffic KILLED{C.RESET}")
    print(f"    {CHECK} {C.GREEN}Privacy-first configuration enforced{C.RESET}")
    print(f"    {CHECK} {C.GREEN}Termux-aware context with full device specs{C.RESET}")
    print(f"    {CHECK} {C.GREEN}Bash permissions hardened and increased token efficiency{C.RESET}")
    print()

    print(f"  {ROCKET} {C.BOLD}{C.WHITE}Quick Start:{C.RESET}")
    print()
    print(f"     {C.CYAN}{C.BOLD}claude{C.RESET}                      {C.DIM}# Launch Claude Code{C.RESET}")
    print(f"     {C.CYAN}{C.BOLD}claude --version{C.RESET}            {C.DIM}# Check installed version{C.RESET}")
    print(f"     {C.CYAN}{C.BOLD}claude -p \"Hello\"{C.RESET}           {C.DIM}# One-shot prompt{C.RESET}")
    print(f"     {C.CYAN}{C.BOLD}cat ~/.claude/CLAUDE.md{C.RESET}     {C.DIM}# View your context file{C.RESET}")
    print(f"     {C.CYAN}{C.BOLD}cat ~/.claude/settings.json{C.RESET} {C.DIM}# View settings{C.RESET}")
    print()

    print_thin_line()
    print()
    print(f"  {C.DIM}{C.WHITE}Run {C.CYAN}claude{C.WHITE} to start. First launch will ask for your Anthropic API key.{C.RESET}")
    print(f"  {LOCK} {C.DIM}{C.WHITE}All config stays LOCAL. Nothing is shared. Ever.{C.RESET}")
    print()
    print_line()
    print()
    print(f"       {C.YELLOW}{C.BOLD}✦ Created by {C.MAGENTA}Graywizard {C.YELLOW}✦{C.RESET}")
    print()
    print_line()
    print()


def do_install():
    node_ver = npm_ver = "N/A"
    try:
        phase_header(1, 4, "Installing Dependencies")
        info_msg("Checking / installing Node.js...")
        print()
        install_nodejs()

        node_ver = _get_tool_version("node")
        npm_ver  = _get_tool_version("npm")

        print()
        info_msg(f"Node.js version : {C.WHITE}{node_ver}{C.RESET}")
        info_msg(f"npm version     : {C.WHITE}{npm_ver}{C.RESET}")
        print()
        success_msg("Dependencies ready!")
        print()
        time.sleep(0.5)

        phase_header(2, 4, f"Installing Claude Code v{CLAUDE_VERSION}")
        install_claude_code()
        print()
        time.sleep(0.5)

        phase_header(3, 4, "User Profile & Preferences")
        user_info = collect_user_info()
        print()
        time.sleep(0.5)

        phase_header(4, 4, "Creating Configuration Files")
        info_msg(f"Setting up {C.CYAN}~/.claude/{C.RESET} ...")
        print()
        write_config_files(user_info)
        print()

        print_thin_line()
        print()
        info_msg(f"Files written to {C.CYAN}~/.claude/{C.RESET}:")
        print(f"  {FILE_IC} {C.WHITE}~/.claude/settings.json{C.RESET}  {C.DIM}(telemetry & non-essential traffic OFF){C.RESET}")
        print(f"  {FILE_IC} {C.WHITE}~/.claude/CLAUDE.md{C.RESET}      {C.DIM}(personalised context & behaviour rules){C.RESET}")
        print()
        print(f"  {SHIELD} {C.BOLD}{C.WHITE}Privacy Hardening Applied:{C.RESET}")
        print(f"    {LOCK} {C.RED}Telemetry                   → {C.BOLD}DISABLED{C.RESET}")
        print(f"    {LOCK} {C.RED}Non-essential traffic       → {C.BOLD}DISABLED{C.RESET}")
        print(f"    {LOCK} {C.RED}Auto-updates                → {C.BOLD}DISABLED{C.RESET}")
        print(f"    {LOCK} {C.RED}Co-authored-by tag          → {C.BOLD}DISABLED{C.RESET}")
        print(f"    {LOCK} {C.RED}Non-essential model calls   → {C.BOLD}DISABLED{C.RESET}")
        print()
        time.sleep(0.5)

        _print_install_summary(user_info, node_ver, npm_ver)

    except subprocess.CalledProcessError as exc:
        error_msg(f"A command failed (exit {exc.returncode}). Aborting.")
    except Exception as exc:
        error_msg(f"Install failed: {exc}")

    input(f"\n  {C.DIM}Press Enter to return to the menu...{C.RESET}")

def do_uninstall():
    banner()
    print(f"  {TRASH} {C.BOLD}{C.RED} Claude Code Uninstaller{C.RESET}")
    print_thin_line()
    print()

    warn_msg("This will completely remove Claude Code from your device.")
    print()
    print(f"  {C.DIM}{C.WHITE}The following will be removed:{C.RESET}")
    print()
    print(f"  {C.RED}●{C.RESET} {C.WHITE}@anthropic-ai/claude-code{C.RESET}  {C.DIM}(global npm package){C.RESET}")
    print(f"  {C.RED}●{C.RESET} {C.WHITE}~/.claude/{C.RESET}                {C.DIM}(config, CLAUDE.md, history){C.RESET}")
    print(f"  {C.RED}●{C.RESET} {C.WHITE}~/.claude.json{C.RESET}             {C.DIM}(auth / account file){C.RESET}")
    print(f"  {C.RED}●{C.RESET} {C.WHITE}~/.cache/claude-cli-nodejs{C.RESET} {C.DIM}(npm cache){C.RESET}")
    print(f"  {C.RED}●{C.RESET} {C.WHITE}~/.config/claude{C.RESET}           {C.DIM}(system config){C.RESET}")
    print()
    print_thin_line()
    print()

    if have("claude"):
        cv = _get_tool_version("claude")
        info_msg(f"Detected Claude Code: {C.WHITE}{cv}{C.RESET}")
    elif CLAUDE_DIR.exists():
        warn_msg("claude binary not found, but ~/.claude config exists.")
    else:
        error_msg("Claude Code is not installed on this device.")
        print()
        print(f"  {ARROW} {C.DIM}Nothing to uninstall. Returning to menu...{C.RESET}")
        input(f"\n  {C.DIM}Press Enter to return to the menu...{C.RESET}")
        return

    print()

    print(f"  {WARN_IC} {C.BOLD}{C.RED}Are you sure you want to uninstall Claude Code?{C.RESET}")
    try:
        c1 = input(f"  {ARROW} {C.WHITE}Type {C.RED}{C.BOLD}YES{C.RESET}{C.WHITE} to confirm: {C.RESET}").strip()
    except EOFError:
        c1 = ""

    if c1 != "YES":
        print()
        info_msg("Uninstallation cancelled. Returning to menu...")
        input(f"\n  {C.DIM}Press Enter to return to the menu...{C.RESET}")
        return

    print()
    print(f"  {LOCK} {C.BOLD}{C.YELLOW}Final confirmation — this action is IRREVERSIBLE.{C.RESET}")
    try:
        c2 = input(f"  {ARROW} {C.WHITE}Type {C.RED}{C.BOLD}UNINSTALL{C.RESET}{C.WHITE} to proceed: {C.RESET}").strip()
    except EOFError:
        c2 = ""

    if c2 != "UNINSTALL":
        print()
        info_msg("Uninstallation cancelled. Returning to menu...")
        input(f"\n  {C.DIM}Press Enter to return to the menu...{C.RESET}")
        return

    print()
    print_thin_line()
    print()

    try:
        uninstall_claude_code()
        print()
        success_msg("All targets processed.")
    except Exception as exc:
        error_msg(f"Uninstall error: {exc}")

    print()
    print_thin_line()
    print()
    info_msg("Verifying uninstallation...")
    print()

    all_clean = True

    if have("claude"):
        error_msg("claude command still found in PATH")
        all_clean = False
    else:
        print(f"    {CHECK} {C.GREEN}claude command removed from PATH{C.RESET}")

    if CLAUDE_DIR.exists():
        error_msg("~/.claude directory still exists")
        all_clean = False
    else:
        print(f"    {CHECK} {C.GREEN}~/.claude directory removed{C.RESET}")

    print()

    if all_clean:
        print()
        print_line()
        print()
        print(f"  {C.GREEN}{C.BOLD}{CHECK} CLAUDE CODE UNINSTALLED SUCCESSFULLY {CHECK}{C.RESET}")
        print()
        print(f"  {C.DIM}{C.WHITE}All Claude Code components have been purged from your device.{C.RESET}")
        print(f"  {C.DIM}{C.WHITE}You can reinstall anytime by running this setup script again.{C.RESET}")
    else:
        print()
        warn_msg("Uninstallation completed with some warnings.")
        warn_msg("Restart Termux to fully clear the environment.")

    print()
    print_line()
    print()
    print(f"       {C.YELLOW}{C.BOLD}✦ Created by {C.MAGENTA}Graywizard {C.YELLOW}✦{C.RESET}")
    print()
    print_line()
    print()

    input(f"\n  {C.DIM}Press Enter to return to the menu...{C.RESET}")

def menu():
    while True:
        banner()
        print()
        print(f"  {DIAMOND} {C.BOLD}{C.WHITE}Welcome to Claude Code Setup{C.RESET}")
        print(f"  {C.DIM}{C.WHITE}One-stop setup & management for Claude Code on Termux{C.RESET}")
        print()
        print_thin_line()
        print()

        print(f"  {C.BG_GREEN}{C.WHITE}{C.BOLD}  1  {C.RESET}  {C.GREEN}{C.BOLD}Install Claude Code{C.RESET}")
        print(f"       {C.DIM}{C.WHITE}┃{C.RESET} {C.DIM}Full installation with dependencies & personalised config{C.RESET}")
        print(f"       {C.DIM}{C.WHITE}┃{C.RESET} {C.DIM}Pinned to v{CLAUDE_VERSION} — tested & stable on Termux{C.RESET}")
        print()

        print(f"  {C.BG_RED}{C.WHITE}{C.BOLD}  2  {C.RESET}  {C.RED}{C.BOLD}Uninstall Claude Code{C.RESET}")
        print(f"       {C.DIM}{C.WHITE}┃{C.RESET} {C.DIM}Completely removes Claude Code, configs, and all data{C.RESET}")
        print(f"       {C.DIM}{C.WHITE}┃{C.RESET} {C.DIM}Clean removal with two-step confirmation{C.RESET}")
        print()

        print(f"  {C.BG_YELLOW}{C.WHITE}{C.BOLD}  3  {C.RESET}  {C.YELLOW}{C.BOLD}Exit{C.RESET}")
        print(f"       {C.DIM}{C.WHITE}┃{C.RESET} {C.DIM}Quit Claude Code Setup{C.RESET}")
        print()

        print_thin_line()
        print()

        try:
            choice = input(f"  {ARROW} {C.BOLD}{C.WHITE}Select option [1/2/3]: {C.RESET}").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            choice = "3"

        if choice == "1":
            do_install()
        elif choice == "2":
            do_uninstall()
        elif choice == "3":
            clear_screen()
            print()
            terminated_banner()
            sys.exit(0)
        else:
            warn_msg("Invalid choice. Please enter 1, 2, or 3.")
            input(f"  {C.DIM}Press Enter to retry...{C.RESET}")


if __name__ == "__main__":
    try:
        menu()
    except KeyboardInterrupt:
        clear_screen()
        terminated_banner()
        sys.exit(130)
