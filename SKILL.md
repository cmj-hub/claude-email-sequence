---
name: lifecycle-email
description: "Draft a lifecycle email sequence as a welcome, delivery of the bargain, then nurture tied to the pain they showed, and score it with a local script. Use when someone already opted in (signup, lead magnet, trial, waitlist, demo request) and you need a welcome email, onboarding sequence, or nurture sequence that is not a generic drip. Not for cold outreach or re-engaging prospects who never opted in (use cold-email)."
models: ""
---

# Lifecycle email

Someone raised a hand. The sequence has three parts, in this order. Welcome them. Hand over the thing they opted in for. Then keep writing about the pain they already showed.

The build guide teaches a human. This pack teaches an agent.

## From brand-config.json

If `brand-config.json` sits at the project root, read it before drafting. Read only. This pack writes nothing to it.

- `psp.vocabulary` is the buyer's own words. Name the pain in those words, and repeat them in the nurture.
- `evp.primary` and `evp.outcome` say what the bargain delivers. The welcome can point at them; it does not pitch them.

The pain they showed on the form or in the reply still wins over the profile. If a block is missing, use what the user gives you and say which pack makes it: `/plugin install psp@gtm-operator-skills` or `/plugin install evp@gtm-operator-skills`. Do not invent vocabulary or an offer line.

## The three parts

1. Welcome. The first note after the opt-in. It names that they asked, and it starts the relationship. It is not an introduction to a stranger.
2. Bargain. Delivery of the thing they were promised: the checklist, the sample, the access. The bargain is the exchange, handed over.
3. Nurture. Later notes that stay on the pain they showed on the form or in the reply. The pain is in the words. A calendar of tips is not nurture.

## What the scorer refuses

The scorer refuses a generic drip and a cold email. A generic drip is a day-1, day-3, day-7 tip series, or a note that calls itself a generic drip. A cold email speaks to someone who never opted in, introduces a product to a stranger, or is labeled a cold email.

A welcome can be short. It still has to be for a person who opted in, and the nurture still has to name their pain.

## Checklist

Copy this list and tick it in order.

- [ ] 1. Name the pain they showed.
- [ ] 2. Fill the sequence shell: welcome, bargain, nurture.
- [ ] 3. Write the draft to `draft.json` and run `python3 ${CLAUDE_SKILL_DIR}/scripts/score.py --file draft.json`.
- [ ] 4. Fix every line the scorer prints under the verdict, then run it again.

Check again until the script exits 0. Show the user the three parts it prints.

## Reading a failure

The first line is the verdict. Each line under it names one gate and the field that tripped it. Fix them all before the next run.

| Line | Fix |
| --- | --- |
| `generic drip: <part> says "..."` | Drop the day-1/day-3/day-7 schedule or tip-series framing. Write to their pain, not the calendar. |
| `cold email: <part> says "..."` | They opted in. Stop introducing the product to a stranger; name what they asked for. |
| `missing: <fields>` | Fill every one of `pain`, `welcome`, `bargain`, `nurture` with text. |
| `pain mismatch` | Repeat the `pain` phrase inside `nurture`, in their words. Case, spacing, and end punctuation do not matter. |

Exit 0 passes. Exit 1 is refused or incomplete. Exit 2 means the input was not a readable JSON object.

Do not game the scorer by swapping a flagged phrase for a synonym. If the note is a drip or a cold email, rewrite it.

## Run

```
python3 ${CLAUDE_SKILL_DIR}/scripts/score.py --file ${CLAUDE_SKILL_DIR}/examples/lifecycle-good.json
python3 ${CLAUDE_SKILL_DIR}/scripts/score.py --file ${CLAUDE_SKILL_DIR}/examples/lifecycle-refused.json
```

Paths are relative to this skill's folder. In Claude Code that folder is `${CLAUDE_SKILL_DIR}`.

The good file exits 0 and prints the welcome, the bargain, and the nurture. The refused file exits 1 and lists each gate it failed. Add `--json` for one machine-readable result object, or pipe the draft with `--stdin`.

The JSON object has four strings: `pain`, `welcome`, `bargain`, and `nurture`. A broken JSON exits non-zero and does not echo the raw input.

Python 3 standard library only. No network. No send.

## Works with the suite

This is step 8 of the GTM operator suite (`/plugin marketplace add cmj-hub/gtm-operator-skills`).

- **Reads:** `psp.vocabulary` and `evp` from `brand-config.json`, if present.
- **Writes:** nothing outside the draft. It never touches another pack's keys.
- **Before this:** landing-page (`/landing-page:page`), when there is no opt-in page yet.
- **Not this:** cold outreach to people who never opted in goes to cold-email (`/cold-email:cold-email`). Re-engaging stalled cold prospects is `cold-email-nurture` in that pack.

If a companion pack is not installed, name it and its install line (`/plugin install <name>@gtm-operator-skills`); do not do its job inline.

## Example draft

```json
{
  "pain": "the trial dies after the first login",
  "welcome": "You asked for the trial checklist. This note starts there.",
  "bargain": "The checklist is the bargain. It is attached, the thing you opted in to receive.",
  "nurture": "The next note stays on the pain you showed: the trial dies after the first login."
}
```
