# Original Japanese N5 Companion Dataset

This package contains an independently written 25-lesson Japanese N5 companion dataset. It is organized with familiar beginner section labels—`bunkei`, `reibun`, `kaiwa`, `renshuu.a`, `renshuu.b`, `renshuu.c`, `mondai`, and `listening`—so an application can provide a consistent lesson interface.

The JSON is not an official *Minna no Nihongo* answer book. It does not reproduce the textbook's exact exercises, dialogues, answer key, or publisher audio. All practice material, answers, and listening scripts were written as original companion content.

## Suggested app model

Render `lessons` as the primary navigation. Use `grammar` and `vocabulary` for study cards, `bunkei` and `reibun` for examples, `kaiwa.lines` for dialogue view, and the three `renshuu` arrays for progressive practice. In quiz mode, hide `answer`, `explanation`, and `translation` until the learner submits a response.

Every listening item includes an original Japanese `script`, `script_reading`, and `translation`. The app can send `script` to a Japanese text-to-speech service or record it as audio. Each listening question includes an `answer` and an explanation. The `audio_ref` field in a Mondai listening item points to the corresponding listening item ID.

For `short_answer` questions, treat the listed answer as one natural model answer. A production app should normalize whitespace and punctuation and may maintain an accepted-answer array for variants. Multiple-choice questions can be graded by exact comparison to `answer`.

## Files

| File | Purpose |
|---|---|
| `minna_n5_original_companion.json` | Main app-ready dataset containing 25 lessons and answer keys. |
| `minna_n5_original_schema.md` | Field-level schema and content-policy description. |
| `minna_n5_original_companion_README.md` | Import and rendering guidance. |
