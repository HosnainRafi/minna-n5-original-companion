# Original Japanese N5 Companion Dataset Schema

This dataset is an independently written study companion for Japanese N5 learners. It uses familiar pedagogical section labels for app organization, but it does not reproduce any textbook dialogue, exercise prompt, answer key, or publisher audio.

## Top-level JSON object

The JSON object contains `dataset` metadata and a `lessons` array. Metadata includes the dataset title, version, level, language fields, lesson count, section names, and a copyright note explaining that all examples, exercises, answer keys, and listening scripts are original.

## Lesson object

Each lesson contains `id`, `title`, `objectives`, `grammar`, `vocabulary`, `bunkei`, `reibun`, `kaiwa`, `renshuu`, `mondai`, and `listening`.

`grammar` is an array of objects containing `id`, `pattern`, `meaning`, `usage`, and an original example with Japanese, reading, English gloss, and translation.

`vocabulary` is an array of objects containing `word`, `reading`, `meaning`, `part_of_speech`, and an optional `notes` field.

`bunkei` contains original model sentences, each with `id`, `japanese`, `reading`, `translation`, and `grammar_refs`.

`reibun` contains original example exchanges or sentence pairs, each with `id`, `prompt`, `response`, `reading`, `translation`, and `grammar_refs`.

`kaiwa` contains an original short dialogue with `title`, `setting`, `lines`, and `comprehension_questions`. Each line has `speaker`, `japanese`, `reading`, and `translation`.

`renshuu` contains three arrays named `a`, `b`, and `c`. Each exercise has `id`, `type`, `prompt`, optional `choices`, `answer`, `explanation`, and `grammar_refs`. Exercise types include `fill_blank`, `transform`, `choose`, `order`, and `short_answer`.

`mondai` contains original review questions and answers. It may include `language`, `reading`, `listening`, and `production` items. Listening items reference an entry in the lesson's `listening` array and include a question, choices when applicable, the answer, and an explanation.

`listening` contains original audio-ready scripts. Each item has `id`, `title`, `script`, `script_reading`, `translation`, `questions`, and `tts_notes`. The `script` is suitable for text-to-speech generation. It is not a copy of textbook audio.

## Import guidance

All strings are UTF-8. Stable IDs use the form `l01-bunkei-01`, `l01-renshuu-a-01`, or `l01-mondai-listening-01`. An app can render Japanese and reading separately, hide `translation` in quiz mode, and compare normalized answers for exercises marked `short_answer`. Listening questions are designed to work with generated audio from the supplied original script.
