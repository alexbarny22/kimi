from __future__ import annotations

import os
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BRANCH = os.getenv("BOT_BRANCH", "main")
INTERVAL = int(os.getenv("UPDATE_INTERVAL", "30"))


def log(msg: str) -> None:
    print(f"[autoupdate] {msg}", flush=True)


def venv_python() -> str:
    win = ROOT / ".venv" / "Scripts" / "python.exe"
    posix = ROOT / ".venv" / "bin" / "python"
    if win.exists():
        return str(win)
    if posix.exists():
        return str(posix)
    return sys.executable


def git(*args: str) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    output = (result.stdout or "").strip()
    if result.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} failed: {output}")
    return output


def rev(ref: str) -> str:
    return git("rev-parse", ref)


def install_deps(py: str) -> None:
    req = ROOT / "requirements.txt"
    if req.exists():
        log("installing dependencies")
        subprocess.run([py, "-m", "pip", "install", "-r", "requirements.txt"], cwd=ROOT, check=False)


def start_bot(py: str) -> subprocess.Popen:
    log("starting bot")
    return subprocess.Popen([py, "-m", "src.bot"], cwd=ROOT)


def stop_bot(proc: subprocess.Popen | None) -> None:
    if proc and proc.poll() is None:
        log("stopping bot")
        proc.terminate()
        try:
            proc.wait(timeout=10)
        except subprocess.TimeoutExpired:
            proc.kill()


def main() -> None:
    py = venv_python()
    bot: subprocess.Popen | None = None
    try:
        install_deps(py)
        bot = start_bot(py)
        while True:
            time.sleep(INTERVAL)

            if bot.poll() is not None:
                log(f"bot exited with code {bot.returncode}, restarting")
                bot = start_bot(py)

            try:
                git("fetch", "origin", BRANCH)
                local = rev("HEAD")
                remote = rev(f"origin/{BRANCH}")
            except Exception as exc:  # noqa: BLE001
                log(f"update check failed: {exc}")
                continue

            if local != remote:
                log(f"new commit detected: {local[:7]} -> {remote[:7]}")
                stop_bot(bot)
                try:
                    git("pull", "--ff-only", "origin", BRANCH)
                    install_deps(py)
                except Exception as exc:  # noqa: BLE001
                    log(f"pull failed: {exc}")
                bot = start_bot(py)
    except KeyboardInterrupt:
        log("stopped by user")
    finally:
        stop_bot(bot)


if __name__ == "__main__":
    main()
