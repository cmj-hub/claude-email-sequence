<p align="center">
  <img src="./assets/lockup.png" width="880" alt="Email sequence skill for Claude Code. An email sequence is the series of emails after someone raises their hand.">
</p>

# Email sequence skill for Claude Code

An email sequence is the series of emails after someone raises their hand.

The sample starts with the trial checklist they asked for.

The good draft passes. A generic drip fails the score.

<p align="center">
  <img src="./assets/demo.gif" alt="Email sequence skill — welcome, bargain, and nurture pass; a generic drip fails" width="100%">
</p>

The build guide teaches a human. The pack teaches an agent.

## Install

This pack is the files in this repository. Open the tree on the host you already run. There is no remote installer.

The scorer is Python in this repo. Host paths are on the [Skill packs catalog](https://jaymountconsulting.com/skills).

## What you walk out with in 15 minutes

Artifact: `examples/lifecycle-good.json`.

```
python3 scripts/score.py --file examples/lifecycle-good.json
python3 scripts/score.py --file examples/lifecycle-refused.json
```

The good draft exits 0 and prints three notes. Each note has a subject, a time, and a body: welcome, then the bargain, then nurture. The refused draft exits 1. Then drop in yours.

## What this pack will not do

It will not send the email. It does not write a generic drip. It will not write a cold email.

## Does this include a newsletter?

One issue can sit inside the sequence. A newsletter product is not a separate pack.

## Does this send the sequence?

No. It scores the draft. Your email tool sends it.

## On the site

- [Email sequence pack](https://jaymountconsulting.com/skills/claude-email-sequence) — this pack's page
- [Skill packs catalog](https://jaymountconsulting.com/skills) — install paths + every pack

## Free, no signup

[All free tools](https://jaymountconsulting.com/prototypes)

## Free, by email

[**Growth Audit**](https://jaymountconsulting.com/growth-audit) — architecture gaps in the GTM you already run. Free written report.

[**Friday Signal**](https://jaymountconsulting.com/newsletter/signal) — one Friday GTM read. No pitch in it.

## Next

Previous: [Cold email](https://github.com/cmj-hub/claude-cold-email)

Next: [Sales prospecting](https://github.com/cmj-hub/claude-prospect-list)

## License

MIT. No paid APIs. Python 3 standard library only.
