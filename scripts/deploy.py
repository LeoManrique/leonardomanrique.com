#!/usr/bin/env python3
"""Build the site and deploy it to the nginx server over SSH.

Assumes ssh connects to SSH_HOST non-interactively (agent or ~/.ssh/config)
and that SSH_USER can take ownership of the target (sudo chown) and run docker.
Reads configuration from .env at the repo root. See .env.example.

Usage:
    python3 scripts/deploy.py
    python3 scripts/deploy.py --skip-build
    python3 scripts/deploy.py --no-backup
    python3 scripts/deploy.py --dry-run
"""

from __future__ import annotations

import argparse
import os
import shlex
import shutil
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DIST_DIR = REPO_ROOT / "dist"
ENV_FILE = REPO_ROOT / ".env"

# Deliberately SSH_-prefixed: zsh defines HOST and USERNAME as special parameters
# bound to the local machine/user and exports them, which would silently shadow
# whatever is in .env and deploy to the wrong target.
REQUIRED = ("SSH_HOST", "SSH_USER")


class DeployError(Exception):
    pass


def log(msg: str) -> None:
    print(f"\033[36m==>\033[0m {msg}", flush=True)


def load_env(path: Path) -> dict[str, str]:
    """Parse a .env file. Real environment variables take precedence."""
    values: dict[str, str] = {}
    if path.exists():
        for lineno, raw in enumerate(path.read_text().splitlines(), start=1):
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            if line.startswith("export "):
                line = line[len("export "):].lstrip()
            key, sep, value = line.partition("=")
            if not sep:
                raise DeployError(f"{path.name}:{lineno}: expected KEY=value, got {raw!r}")
            key = key.strip()
            value = value.strip()
            if len(value) >= 2 and value[0] == value[-1] and value[0] in ("'", '"'):
                value = value[1:-1]
            values[key] = value
    values.update({k: v for k, v in os.environ.items() if k in values or k in REQUIRED})
    return values


def require(env: dict[str, str], key: str) -> str:
    value = env.get(key, "").strip()
    if not value:
        raise DeployError(
            f"{key} is not set. Add it to {ENV_FILE.name} (copy .env.example to get started)."
        )
    return value


def run(cmd: list[str], *, cwd: Path | None = None, dry_run: bool = False) -> None:
    printable = " ".join(shlex.quote(c) for c in cmd)
    if dry_run:
        print(f"    \033[90m[dry-run]\033[0m {printable}")
        return
    print(f"    \033[90m$ {printable}\033[0m")
    result = subprocess.run(cmd, cwd=cwd)
    if result.returncode != 0:
        raise DeployError(f"command failed (exit {result.returncode}): {printable}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Deploy leonardomanrique.com to the server.")
    parser.add_argument("--skip-build", action="store_true", help="deploy the existing dist/ as-is")
    parser.add_argument("--dry-run", action="store_true", help="print commands without running them")
    parser.add_argument("--no-backup", action="store_true", help="skip backing up the current deploy")
    parser.add_argument("--no-restart", action="store_true", help="skip the container restart")
    args = parser.parse_args()

    try:
        env = load_env(ENV_FILE)
        host = require(env, "SSH_HOST")
        user = require(env, "SSH_USER")
        port = env.get("SSH_PORT", "").strip()
        target = env.get("TARGET", "").strip() or "/home/lux/apps/leonardomanrique"
        backup_dir = env.get("BACKUP_DIR", "").strip() or "/home/lux/backups"
        container = env.get("CONTAINER", "").strip() or "traefik"

        if not args.skip_build:
            log("Building project")
            pnpm = shutil.which("pnpm")
            if not pnpm:
                raise DeployError("pnpm not found on PATH")
            run([pnpm, "install"], cwd=REPO_ROOT, dry_run=args.dry_run)
            run([pnpm, "run", "build"], cwd=REPO_ROOT, dry_run=args.dry_run)

        if not args.dry_run and not DIST_DIR.is_dir():
            raise DeployError(f"{DIST_DIR} does not exist — run without --skip-build first.")

        # An unset SSH_PORT leaves the port to ~/.ssh/config rather than forcing 22.
        ssh_opts = ["-p", port] if port else []
        rsync_ssh = f"ssh -p {port}" if port else "ssh"

        rsync = shutil.which("rsync")
        if not rsync:
            raise DeployError("rsync not found on PATH (brew install rsync)")

        def ssh(script: str) -> None:
            run(["ssh", *ssh_opts, f"{user}@{host}", script], dry_run=args.dry_run)

        qtarget = shlex.quote(target)
        qbackup = shlex.quote(backup_dir)
        quser = shlex.quote(user)

        # Prepare: ensure the target exists, back it up, then hand it to the deploy
        # user so rsync can write (it is owned by the web user between deploys).
        log(f"Preparing {target} on {host}")
        prepare = ["set -e", f"mkdir -p {qtarget}"]
        if not args.no_backup:
            prepare.append(
                f'if [ -n "$(ls -A {qtarget} 2>/dev/null)" ]; then '
                f"mkdir -p {qbackup} && "
                f"sudo cp -r {qtarget} {qbackup}/leonardomanrique.backup.$(date +%Y%m%d_%H%M%S); fi"
            )
        prepare.append(f"sudo chown -R {quser}:{quser} {qtarget}")
        ssh("\n".join(prepare))

        # Trailing slash on the source copies dist's *contents* into target,
        # matching strip_components: 1 in the old workflow. --delete replaces the
        # old "remove old files, then copy" dance atomically per file.
        log(f"Syncing dist/ to {user}@{host}:{target}")
        run(
            [
                rsync,
                "-az",
                "--delete",
                "-e",
                rsync_ssh,
                f"{DIST_DIR}/",
                f"{user}@{host}:{target}/",
            ],
            dry_run=args.dry_run,
        )

        # nginx runs inside a container here, not on the host, so there is no
        # `nginx -s reload` to call — restart the container that serves the site,
        # matching anelyleo. rsync -a preserves world-readable perms, so the
        # container reads the files regardless of host ownership.
        if not args.no_restart:
            log(f"Restarting {container}")
            ssh(f"docker container restart {shlex.quote(container)}")

        log("\033[32mDeployed.\033[0m" if not args.dry_run else "Dry run complete.")
        return 0

    except DeployError as exc:
        print(f"\033[31merror:\033[0m {exc}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("\naborted", file=sys.stderr)
        return 130


if __name__ == "__main__":
    sys.exit(main())
