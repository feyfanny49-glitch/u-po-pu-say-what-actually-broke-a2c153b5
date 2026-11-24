# Strategy — Say What Actually Broke (u-po-pu-say-what-actually-broke-a2c153b5)

## Exact deliverable

One text file written by the repository's root entrypoint: `/output/entry.txt`.
It must be UTF-8 text of 1..200 characters, more than whitespace, and a single
software error message. The contest is a judged-TEXT contest: there is no image,
no dashboard and no asset bundle. The judged artifact is the bytes of
`/output/entry.txt` and nothing else.

Chosen line (177 characters, no trailing newline):

"Your 2:30 a.m. job never ran. Daylight saving deleted that hour; we stored local time without a zone, so the scheduler obeyed a clock that doesn't exist. Reschedule it for 3:00."

## Scoring and judge criteria, in the judge's order

The house judge (superbot at high reasoning effort, z-ai/glm-5.3-flash) is
briefed as a veteran SRE with no patience for vague errors. It compares two
entries at a time, in both orders, and picks the one a user would remember and
repeat to a colleague. It weighs, most important first:

1. A single-line software error message, at most 200 characters, telling the
   brutal truth about what went wrong in a funny way; it loses to any error
   message on the subject.
2. Names the real failure in plain words, so the reader knows what broke and
   what to do next, instead of apologising in generalities.
3. Is funny on a single read, with a twist or an image a reader repeats out loud.
4. Keeps the joke to a single line inside the character limit, no padding and
   no throat clearing.
5. Would survive being pasted into a real product's error dialog without
   embarrassing the team.

Each game is two calls (both label orders); the winner of a call gets
0.5 + margin/10. Three fixed house texts anchor every heat; 3 Swiss rounds and
a top-10 playoff decide the final. Only the top 8 places are paid ($2 total).
A statistical tie never moves a place; exact ties go to playoff head-to-head,
then smaller byte size, then earlier receipt. An exact byte copy of a house
text or another entry earns no prize.

## Hard caps and rules

- Gate: `/output/entry.txt` must be valid UTF-8, 1..200 characters, not only
  whitespace. Invalid entries are never judged and take no prize.
- Sandbox: program/v1, 1 CPU, 512 MB, 64 pids, 60 s wall time, no network.
- Everything the entry runs must live in the repository at the submitted
  commit; no secrets, no network reads, no code from git history or outside.
- Runtime: python3.13 entrypoint at the repository root (`main.py`).
- The file must be written atomically (temp file in `/output` + `os.replace`).
- No trailing newline in the artifact; validate UTF-8 and the 200-char cap
  locally before committing.
- Keep the `makefun anchor` freshness commit and the LICENSE commit intact.
- Do not upload or submit anything in this task: study, build, commit only.

## Research feed and angle selection

Read the public feed (`/api/competitions/<slug>/submissions` on make.fun; the
page's Feed tab and web search/extract were checked too). Around 1,700 judged
entries cluster on a handful of subjects: disk full of disk-full logs, lost
saves/autosave, Friday deploys, out-of-memory with 47 tabs, backups that were
screenshots, expired certificates, sessions/passwords, duplicate charges, DNS,
and lying progress bars. Several are good, so a me-too line on any of those
subjects loses on criterion 1.

Keyword scans of the feed show zero entries about daylight saving, `2:30`,
wall-clock time, schedulers, locale/date-format ambiguity, or binary-float
money. The chosen angle is the spring-forward gap: a job scheduled at a local
time that daylight saving removes, with no time zone stored. It satisfies the
rubric in order:

1. One line, 177/200 characters, and a concrete failure: the job never ran.
2. Plain mechanism ("daylight saving deleted that hour", "stored local time
   without a zone") and a next step ("Reschedule it for 3:00").
3. A quotable twist/image: "the scheduler obeyed a clock that doesn't exist".
4. No preamble, no meta-commentary to the judge, no padding.
5. Reads like real product copy — an honest error plus a fix, not a rant.

## Concrete plan to maximise the score

1. Write this STRATEGY.md with the deliverable, ordered criteria, caps and the
   chosen line.
2. Write `main.py` first: an entrypoint that writes the exact text via a
   temporary file and `os.replace`, creating `/output` if needed.
3. In a separate later step, rewrite that same `main.py` with a real
   improvement: explicit local validation (UTF-8 round-trip, 1..200 chars,
   no CR/LF, non-whitespace), temp-file cleanup on failure, and stdout with
   char count, byte count and sha256 for auditability.
4. Run the entrypoint locally with an isolated output directory and check the
   artifact's UTF-8 validity, exact length, absence of trailing newline and
   atomic write behaviour.
5. Commit every work file with git after the second write; print the final
   commit sha. No submission, no upload.
