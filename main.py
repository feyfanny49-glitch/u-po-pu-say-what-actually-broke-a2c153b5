#!/usr/bin/env python3
"""Write this competition's single judged line to /output/entry.txt.

The artifact is one line of UTF-8 text, 1..200 characters, with no trailing
newline. It is created through a temporary file and os.replace so the judge
never sees a partially written entry.
"""

import hashlib
import os
import tempfile

ENTRY = (
    "Your 2:30 a.m. job never ran. Daylight saving deleted that hour; "
    "we stored local time without a zone, so the scheduler obeyed a clock "
    "that doesn't exist. Reschedule it for 3:00."
)

OUT_PATH = "/output/entry.txt"


def validate(text: str) -> bytes:
    """Return the exact bytes allowed by the gate, or raise ValueError."""
    if not 1 <= len(text) <= 200:
        raise ValueError(f"entry must be 1..200 characters, got {len(text)}")
    if not text.strip():
        raise ValueError("entry may not be only whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line with no newline bytes")
    payload = text.encode("utf-8")
    if payload.decode("utf-8") != text:
        raise ValueError("entry is not valid UTF-8")
    return payload


def main() -> None:
    payload = validate(ENTRY)
    outdir = os.path.dirname(OUT_PATH)
    os.makedirs(outdir, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix=".entry-", dir=outdir)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp, OUT_PATH)
    except BaseException:
        try:
            os.unlink(tmp)
        except FileNotFoundError:
            pass
        raise
    digest = hashlib.sha256(payload).hexdigest()
    print(
        f"wrote {OUT_PATH}: {len(ENTRY)} chars, {len(payload)} bytes, "
        f"sha256 {digest}"
    )


if __name__ == "__main__":
    main()
