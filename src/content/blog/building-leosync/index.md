---
title: "Building LeoSync: easy file sync, not so easy development"
date: "2026-05-07"
readingTime: "8 min read"
summary: "Notes from building a relay-mediated Syncthing alternative."
tags:
  - Go
  - Distributed Systems
  - Docker
---

This project started by the restrictions that some cloud sync services have, their poor privacy policy, and having a computer restricted to use SSH. The answer to this was of course building a Sync service myself. While starting the development of it I also discovered Syncthing, an open source alternative that could have done some of the job.

## My use case

I have recently accumulated some laptops and desktop PCs. Instead of selling them I have repurposed them: one desktop PC for development, one for gaming, one laptop for daily driver when abroad, one for experimenting. Plus I have my work laptop that is restricted from using SSH. Some of these devices also happen to have a dual boot option, so having a direct sync between those OS folders was not really an option.

My very initial requirement to have some files (or information) synched was when trying to plan my vacations both on my personal devices notes and my work PC. I had no way to access or transfer files in a seemless way, plus just having to turn on multiple devices at once was quite a distraction.

Later I also wanted a sync service that can keep my save files from Emulators synched between all my devices, so binary file sync was now also a requirement.

## My problem with Syncthing

Honestly I think Syncthing works perfectly for most people with my use case. I also I own a Raspberry Pi 5 and I have access to a VPS, so I could have used any of those as an always on node to sync my files to. But there was one use case that was not covered for me: offline work. What if I work on a plane or a train? What if I my server goes down? Thinking about debugging and manually sync those changes again was not something fun to think about.

``` From here it's just AI slop, ignore...``

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
