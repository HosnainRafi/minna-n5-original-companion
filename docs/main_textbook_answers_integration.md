# Minna no Nihongo Main Textbook Answers

This integration adds `assets/data/minna/main_textbook_answers.json`, a Flutter adapter generated from the supplied main textbook and answer-key PDFs. It is deliberately separate from the existing Standard Workbook and Listening Tasks 25 books.

## Included sections

The adapter includes the answer-key records available for Lessons 1–25 in **Renshuu B, Renshuu C, and Mondai**. Mondai records preserve question text, answers, listening mode, and the lesson-level default audio asset where supplied. The canonical export outside the Flutter asset directory additionally preserves `audio_script`, `visual_description`, source pages, choices, and confidence metadata.

The supplied answer-key PDFs do not provide a complete answer-key record set for Bunkei, Reibun, Kaiwa, or Renshuu A. These sections are therefore not fabricated in the adapter. Lesson 25 Renshuu C is also not visible in the supplied appendix page and remains an explicit coverage gap in the canonical JSON.

## Flutter changes

`MinnaData.loadMainTextbook()` loads the adapter and converts it to the existing nested `MinnaBook` / `MinnaSection` / `MinnaNode` model. `MinnaBookPage` routes the `main_textbook` book ID to that loader, and `MinnaHubPage` exposes a new **Main Textbook Answers** card.

The app already registers `assets/data/minna/` and `assets/audio/listening/` in `pubspec.yaml`. The 87 MP3 files referenced by this dataset already exist under `assets/audio/listening/` and match the user-provided resource-pack MP3s by SHA-256.

## Audio mapping

The canonical JSON retains the complete 3A track list for every lesson. For a Mondai record, `default_audio_asset` points to the final official lesson track as a lesson-level default. Because the supplied manifests do not expose exact question-to-track boundaries for every section, the full `audio_assets` list is retained for verification instead of pretending that every item has a precisely verified track.

## Validation

The canonical JSON and Flutter adapter both parse successfully. The adapter contains 25 lessons, 1,618 answer nodes, and valid paths for all referenced audio assets. Flutter SDK analysis could not be run in the sandbox because the Flutter executable is not installed; `git diff --check` and JSON/path validation passed.
