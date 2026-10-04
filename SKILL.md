---
name: lifecycle-email
description: "Draft three opted-in notes: welcome, delivery of the bargain, then nurture tied to the pain they showed. Each note has a subject and a time. Use when someone already opted in, and when a generic drip or a cold email must be refused."
models: ""
---

# Lifecycle email

Someone raised a hand. The sequence is three notes, in this order. Welcome them. Hand over the thing they opted in for. Then keep writing about the pain they already showed.

The build guide teaches a human. This pack teaches an agent.

You walk out with three notes. Each note has a subject, a time, and a body. A stranger can write them from this file alone. This pack does not send them.

This pack does not add a paid product. If note 3 needs a next step, name Friday Signal or the Growth Audit. Do not add a checkout, a retainer, or a new offer.

## Inputs

- The pain, in the words they used on the form or in the reply.
- The thing they were promised. That thing is the bargain.
- The day they opted in.

Do not write to someone who never opted in. That is a cold email. This pack refuses it.

## The three notes

Note 1 is welcome. It is not an introduction to someone who did not ask.

Note 2 is the bargain. It hands over the thing. It does not swap in a different offer.

Note 3 is nurture. It stays on the pain they showed. A calendar of tips is not nurture.

## Keys

One JSON object. Every value is a string.

- `pain` — their words.
- `welcome_subject`, `welcome_when`, `welcome` — note 1.
- `bargain_subject`, `bargain_when`, `bargain` — note 2.
- `nurture_subject`, `nurture_when`, `nurture` — note 3.

The bodies stay named welcome, bargain, and nurture. Do not rename them.

## Decision rules

Welcome. The subject names what they asked for. The body says they asked, or that they opted in. `welcome_when` says they opt in, because this note goes the day they opt in. It is not a product introduction.

Bargain. The subject names the thing. The body delivers it. `bargain_when` contains the word next, because this note goes the next morning. Do not attach a different offer.

Nurture. The subject repeats the pain, the same words as `pain`. The body contains that same pain. `nurture_when` contains the word after, because this note goes after the bargain is in their hands.

The three bodies are three different notes. The three subjects are three different lines.

Timing. Write the day in words. If a time line uses a number, the line must contain the word example. Replace the number. Do not write a day-1, day-3, day-7 tip series. The scorer refuses "day 1", "day 3", "day 7", "tip series", and "generic drip".

Cold. The scorer refuses a draft that says cold email, never opted, stranger, introduce our, or first touch. Do not put those phrases in a good draft. A letter to someone who did not opt in is still the wrong job even if you avoid the phrases.

A welcome can be short. It still has to be for a person who opted in, and the nurture still has to name their pain.

## Procedure

1. Copy `pain` from their words. Do not improve it into a slogan.
2. Write note 1. Subject, then the day they opt in, then the body. The body says they asked. Say the next note will hand over the thing.
3. Write note 2 for the next morning. Subject names the thing. Body puts the thing in their hands. Say it is the bargain they opted in to receive.
4. Write note 3 for after that. Subject is the pain. Body stays on the pain and points at one step they can do with the thing they already have.
5. If you used a number in a time line, include the word example and replace the number before you send.
6. Save `draft.json`. From the repo root, run `python3 scripts/score.py --file draft.json`.

Exit 0 prints the pain and the three notes. Exit 1 prints one reason.

## Filled example

Example only. Replace every line. The hours and the mornings are example timing, not a send calendar you should keep. The pain is a sample pain. Replace it with the words they used.

Note 1. Subject: You asked for the trial checklist. When: the day they opt in.

You asked for the trial checklist. This note starts there. The checklist is the thing you asked for, and the next note hands it over.

Note 2. Subject: The checklist is attached. When: the next morning.

The checklist is the bargain. It is attached, the thing you opted in to receive. Work the first box on the trial you already have.

Note 3. Subject: The trial dies after the first login. When: after the bargain is in their hands.

The next note stays on the pain you showed: the trial dies after the first login. The step that dies is the step after the first login. Do that step once, from the checklist you already have.

```json
{
  "pain": "the trial dies after the first login",
  "welcome_subject": "You asked for the trial checklist",
  "welcome_when": "The day they opt in. Example timing, replace this: within 1 hour.",
  "welcome": "You asked for the trial checklist. This note starts there. The checklist is the thing you asked for, and the next note hands it over.",
  "bargain_subject": "The checklist is attached",
  "bargain_when": "The next morning. Example timing, replace this: 1 morning after the welcome.",
  "bargain": "The checklist is the bargain. It is attached, the thing you opted in to receive. Work the first box on the trial you already have.",
  "nurture_subject": "The trial dies after the first login",
  "nurture_when": "After the bargain is in their hands. Example timing, replace this: 2 mornings after the bargain.",
  "nurture": "The next note stays on the pain you showed: the trial dies after the first login. The step that dies is the step after the first login. Do that step once, from the checklist you already have."
}
```

## What exit 1 means

- `a generic drip and a cold email` — the draft is a tip series, a cold email, or the nurture body does not contain the pain.
- `draft is incomplete` — a string is blank.
- `the notes are not three` — two bodies are the same note.
- `subjects are not three notes` — two subjects match.
- `welcome is not for someone who opted in` — the welcome body does not say they asked or opted in.
- `nurture does not name the pain` — the third subject does not repeat `pain`.
- `timing is not three notes` — the welcome time does not say opt, the bargain time does not say next, or the nurture time does not say after.
- `timing number is not labeled example` — a time line has a digit and does not say example.

## Checklist

Copy this list and tick it in order.

- [ ] 1. Name the pain they showed. Put those words in `pain`, in `nurture_subject`, and in `nurture`.
- [ ] 2. Write three notes. Each gets a subject, a when, and a body: welcome, then bargain, then nurture.
- [ ] 3. From the repo root, run `python3 scripts/score.py --file draft.json`.

Check again until the script exits 0.

Go back to step 2 if step 3 fails.

## Run

```
python3 scripts/score.py --file examples/lifecycle-good.json
python3 scripts/score.py --file examples/lifecycle-refused.json
```

The good file exits 0 and prints the three notes. The refused file exits 1.

A broken JSON exits non-zero and does not echo the raw input.

Python 3 standard library only. No network. No send.
