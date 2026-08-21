# Minna no Nihongo Elementary I — Answer Data and Flutter Integration

This private repository contains organized JSON exports and Flutter integration files for **Minna no Nihongo Elementary I (Shokyu I), 2nd Edition**. The canonical answer dataset was produced from the user-supplied textbook and answer-key PDFs. The repository also contains the earlier original N5 companion dataset, a Flutter adapter, audio mappings, and reproducible build/validation tools.

## Repository layout

| Path | Purpose |
|---|---|
| `data/canonical/minna_n5_main_textbook_answers.json` | Canonical lesson-by-lesson answer dataset with questions, answers, modes, source pages, listening scripts where available, and audio references |
| `data/flutter/main_textbook_answers.json` | Compact nested adapter for the existing Flutter `MinnaBook` / `MinnaSection` / `MinnaNode` data model |
| `data/audio/audio_map.json` | Mapping for all 87 lesson audio tracks, including app asset paths and resource-pack paths |
| `data/original/minna_n5_original_companion.json` | Earlier independently written N5 companion dataset with original exercises and answers |
| `docs/main_textbook_answers_integration.md` | Flutter integration notes and known coverage gaps |
| `docs/original_companion_schema.md` | Schema for the original companion dataset |
| `patches/flutter_main_textbook.patch` | Patch that adds the main-textbook book card, loader, route, and app asset |
| `tools/build/` | Dataset and adapter generation scripts |
| `tools/validation/` | JSON and audio-path validation scripts |

## Canonical textbook-answer coverage

The canonical export contains records for 25 lessons and is intentionally answer-focused. It includes **Renshuu B, Renshuu C, and Mondai** records, including listening-mode records with answer-key scripts where those scripts were present in the supplied answer-key scans. It does not add grammar or vocabulary explanations.

The supplied answer-key materials do not provide a complete answer-key record set for **Bunkei, Reibun, Kaiwa, or Renshuu A**. Those sections are represented explicitly in the canonical metadata rather than being fabricated. Lesson 25 Renshuu C is also marked as unavailable because it was not visible in the supplied appendix material.

The extraction currently contains 1,618 answer records: 741 Renshuu B records, 143 Renshuu C records, and 734 Mondai records. These counts should be treated as extraction coverage metrics, not as publisher-certified exercise totals.

## Audio

The audio map links the user-provided listening resource pack to the existing Flutter app assets under `assets/audio/listening/`. The resource pack contains 87 MP3 files across Lessons 1–25, and all 87 files matched the app copies by SHA-256 during validation. The canonical records preserve the full lesson track list. A final lesson track is supplied as a default Mondai hint, but exact question-to-track boundaries should be manually confirmed against the user’s audio edition when a lesson contains multiple listening sections.

## Flutter integration

The patch adds `main_textbook_answers.json` to the app’s Minna data directory, adds `MinnaData.loadMainTextbook()`, routes the `main_textbook` book ID, and exposes a **Main Textbook Answers** card in the Minna hub. The app already registers `assets/data/minna/` and `assets/audio/listening/` in `pubspec.yaml`.

To apply the integration patch inside the Flutter project, run:

```bash
git apply patches/flutter_main_textbook.patch
```

Then ensure `data/flutter/main_textbook_answers.json` is copied to the app’s `assets/data/minna/main_textbook_answers.json`. Run Flutter analysis and tests on a machine with the Flutter SDK installed.

## Validation

The canonical and adapter JSON files parse successfully. The adapter contains 25 lessons and valid paths for all referenced audio assets. The sandbox used for preparation did not have the Flutter SDK, so Flutter static analysis must still be run locally after applying the patch.

## Provenance and rights

The main-textbook answer export is derived from user-supplied scans for personal study and application integration. The listening files remain subject to their original ownership and licensing terms. Do not redistribute textbook scans, publisher audio, or complete answer-key material outside the permissions applicable to your copy and intended use.

## References

1. [Minna no Nihongo listening resource directory](https://github.com/HosnainRafi/jlpt-n5-resource-pack/tree/main/minna-no-nihongo-listening)
2. [Japanese N5 Preparation Flutter app](https://github.com/HosnainRafi/Japanese-N5-preparation/tree/main/android-app-flutter)
3. [3A Corporation Minna no Nihongo resources](https://www.3anet.co.jp/np/en/resrcs/230020/)
