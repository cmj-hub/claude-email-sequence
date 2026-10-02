<p align="center">
  <img src="./assets/header.png" alt="Email sequence skill for Claude Code" width="100%">
</p>

# Email sequence skill for Claude Code

**An email sequence is the series of emails after someone raises their hand.**

You hold a welcome, delivery of the bargain, then nurture tied to the pain they showed.

The scorer refuses a generic drip and a cold email.

[![Claude Code Skill](https://img.shields.io/badge/Claude%20Code-Skill-blue)](https://claude.ai/claude-code)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
![No paid APIs](https://img.shields.io/badge/paid%20APIs-none-success)

<p align="center">
  <img src="./assets/demo.gif" alt="Email sequence skill — welcome, bargain, and nurture pass; a generic drip fails" width="100%">
</p>

The build guide teaches a human. This pack teaches an agent.

## Install

```bash
npx skills add cmj-hub/claude-email-sequence --all -g --full-depth
```

Installs into Claude Code, Cursor, Codex, Grok, Copilot, Windsurf, Cline, and OpenCode. The scorer is Python in this repo. It does not call a paid API.

## What you walk out with in 15 minutes

Artifact: `examples/lifecycle-good.json`.

```bash
python3 scripts/score.py --file examples/lifecycle-good.json
python3 scripts/score.py --file examples/lifecycle-refused.json
```

The good draft exits 0 and prints the welcome, the bargain, and the nurture. The refused draft exits 1. Then drop in yours.

## What this pack will not do

It will not send the email. It does not write a generic drip. It will not write a cold email.

## Does this include a newsletter?

One issue can sit inside the sequence. A newsletter product is not a separate pack.

## Does this send the sequence?

No. It scores the draft. Your email tool sends it.

## Companion packs

- [claude-psp](https://github.com/cmj-hub/claude-psp) — Ideal customer profile
- [claude-evp](https://github.com/cmj-hub/claude-evp) — Value proposition
- [claude-cold-email](https://github.com/cmj-hub/claude-cold-email) — Cold email
- [claude-founder-brand](https://github.com/cmj-hub/claude-founder-brand) — LinkedIn posts
- [claude-pricing](https://github.com/cmj-hub/claude-pricing) — Pricing strategy
- [claude-landing-page](https://github.com/cmj-hub/claude-landing-page) — Landing page
- [claude-geo](https://github.com/cmj-hub/claude-geo) — Generative engine optimization
- [claude-sales-offer](https://github.com/cmj-hub/claude-sales-offer) — Sales offer
- [claude-prospect-list](https://github.com/cmj-hub/claude-prospect-list) — Sales prospecting

## License

MIT. No paid APIs. Python 3 standard library only.
