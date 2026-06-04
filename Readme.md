# my-skill

Agent skills loaded by Antigravity cli.

## Layout

Skills live under `skills/`.

Each skill is its own directory containing a `SKILL.md` (with YAML frontmatter — `name` and `description`) and any bundled scripts or reference files.

## Reference

### Engineering

- **[debug-mantra](./skills/debug-mantra/SKILL.md)** — Four-mantra debugging discipline: reproduce → trace the fail path → falsify the hypothesis → cross-reference every breadcrumb. Recites verbatim at session start, then applies in order before any fix.
- **[post-mortem](./skills/post-mortem/SKILL.md)** — Write the canonical engineering record of a fixed bug — root cause, mechanism, fix, validation, how it slipped through. Engineer-audience; refuses to draft without a reliable repro, known cause, and validated fix.
- **[scrutinize](./skills/scrutinize/SKILL.md)** — Outsider-perspective end-to-end review of a plan, PR, or code change. Questions intent (is there a simpler way?), traces the actual code path, and verifies the change does what it claims. Output is concise, actionable, with rationale.
- **[software-design](./skills/software-design/SKILL.md)** — Design software architectures and draft detailed design proposals with embedded Mermaid diagrams before writing any code. Follows a strict design-first approach with Fastify, MySQL, and WebSockets.

### Productivity

- **[management-talk](./skills/management-talk/SKILL.md)** — Rewrite engineer-to-engineer content for engineering-org leadership and shape it for the channel it's going to (JIRA, Slack, async standup, email, meeting talking-points).

## Setup & Scripts

To register these skills with your local Antigravity environment, you can link them using the provided setup scripts.

### Windows (PowerShell)

Run the following command in PowerShell:
```powershell
# To link all skills
.\scripts\link-skills.ps1

# To list all active skills
.\scripts\list-skills.ps1
```

### macOS / Linux / WSL (Bash)

Run the following command in your terminal:
```bash
# To link all skills
./scripts/link-skills.sh

# To list all active skills
./scripts/list-skills.sh
```