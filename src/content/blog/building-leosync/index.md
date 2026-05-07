---
title: "Building LeoSync: end-to-end encrypted file sync, the hard parts"
date: "2026-05-07"
readingTime: "8 min read"
summary: "Notes from building a Dropbox alternative — relay-mediated sync, file identity that survives renames, event coalescing, X25519 key exchange, and 35 scenario suites' worth of edge cases."
tags:
  - Go
  - Distributed Systems
  - Encryption
---

LeoSync started as a question: how hard is it, really, to build a Dropbox replacement that I'd trust with my own files? After a year of evenings and weekends, the answer is "harder than I expected, but tractable." This post is a tour of the parts that surprised me.

## Architecture in one paragraph

Three components: a desktop daemon (`leosyncd`) on each machine that owns all sync state, a relay server that brokers everything, and a thin CLI/GUI that talks to the daemon over a Unix socket. Devices never connect to each other directly — the relay holds state for offline peers and brokers X25519 key exchange for end-to-end encryption.

## Folder identity, not folder path

The first naive design tracks files by their absolute path. That breaks the moment two devices want different local paths for the same logical folder — `~/Documents` on one machine, `D:\Sync\Docs` on another. So files are tracked by a stable `FileIdentityID`, scoped under a folder ID like `documents`. A rename chain `A → B → C` arrives at peers as a single rename `A → C`, not three separate events.

## Event coalescing

A naive implementation uploads on every filesystem event. In practice, saving a file in VS Code can fire 5–15 events in a hundred milliseconds. Coalescing happens in two places:

- **Client-side, before upload.** `create + delete` collapses to nothing. `create + modify + modify + ...` becomes one upload of the latest content.
- **Server-side, before delivery.** A thousand changes on one file while a peer is offline produce one notification, not a thousand.

Without this, the system would melt under any real workload.

## End-to-end encryption without losing your mind

Files are encrypted client-side with a per-vault symmetric key. The relay never sees plaintext content. New devices request access via X25519 ECDH, and an existing approved device wraps the vault key for them. Paths and metadata stay plaintext because making them encrypted breaks every useful UX (search, the dashboard, "what's syncing right now").

## What broke in testing

Thirty-five scenario suites — the ones that mattered most:

- **Network partition mid-upload** — partial uploads need to resume from where they died, not restart.
- **SIGKILL the daemon during a download** — on next startup, the orphan sweep has to distinguish "in-flight" from "abandoned" or it deletes files that are about to land.
- **Repeated crash loops** — never lose acknowledged events, never replay them.
- **Unicode filename normalization** — macOS stores NFD, Linux stores NFC. The same filename round-trips through three normalizations between two devices.
- **Path traversal** — "innocent" sync events that try to write outside the sync root.

## What's next

Cross-platform interop testing (macOS ↔ Windows is the gap), single-relay reliability hardening, and `.msi` / `.dmg` / `.deb` native installers. Multi-relay failover comes after the single-relay setup is bulletproof.
