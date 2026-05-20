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

I was also inspired by how OneDrive and iCloud can synchornize changes that the user has done offline, and even provide an visual feeback of which files will be sent for sync when back online. This didn't seem like a straight forward implementation but also not impossible as I already worked on systems data integrations, assuming failures or unreliable connections.

## The stack

When I started the development of the project all the stack was completely different. I wanted to keep this development simple, so I went for the "easiest" technology I didn't even know so much about but was excited to learn more of: Python. I researched about the current status of Python for this kind of tools. For the file watcher it seemed to have quite mature libraries that handled the OS APIs in a stable way. Plus I found out about FastAPI, which apparently increased significantly the speed of Python processing the necessary data to act as an HTTP server.

The main problem I had with Python was it being interpreted and non-typed. I don't know if it's skill issue or what, but I quickly realized that this project had quite some edge cases to take care about, and I didn't want the code to be something I also had to worry about. However I didn't want to fully rewrite yet since the File Watcher was working quite well.

However the decision to stop using Python was not even caused by Python, but by Electron. I chose Electron as my UI to see the Python service working, and it was not a fun thing to do. Having to further mantain that codebase, and the fact that the RAM consumption and binary size felt not right, made me finally decide to change stack.

The next candidate for the job was Go. It really seemed to fix all the issues I had: compiled language, typed, simple enough, and also had one main advantage: Wails. Wails is an Electron alernative that uses Golang as a "backend" language for a desktop app, and automatically binds those types to Typescript, it just felt like the perfect tool to work on the desktop-side sync engine while also providing a user-friendly UI to configure and monitor what is being synched. For the Relay server I migrated from FastAPI to Gin Framework, which was later easily dropped in favor of standard Go http library.

`` in progress...``
