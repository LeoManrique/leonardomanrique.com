# Leonardo Manrique - Portfolio

A personal portfolio website built with SvelteKit and TypeScript, featuring file-based routing and static site generation.

## Tech Stack

- SvelteKit (Svelte 5)
- TypeScript
- Vite
- adapter-static (SSG)
- Data-driven content (JSON)

## Pages

- `/` — Home, About, Qualification
- `/portfolio` — Portfolio (coming soon)

## Development

```bash
# Install dependencies
pnpm install

# Start dev server
pnpm dev

# Build for production
pnpm build

# Type check
pnpm check
```

## Deployment

Deploy with the Python script — it builds `dist/`, rsyncs it to the server
over SSH, and restarts the container that serves the site:

```bash
# One-time setup: copy the env template and fill in your server details
cp .env.example .env

# Build and deploy
python3 scripts/deploy.py

# Deploy the existing dist/ without rebuilding
python3 scripts/deploy.py --skip-build

# Preview the commands without running them
python3 scripts/deploy.py --dry-run
```

Configuration lives in `.env` (see `.env.example`). SSH auth is left to your
agent or `~/.ssh/config`; `SSH_USER` needs passwordless sudo to take ownership
of the target and access to `docker`.
