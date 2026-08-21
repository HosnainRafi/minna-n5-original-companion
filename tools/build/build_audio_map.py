import json
from pathlib import Path

BASE = Path('/home/ubuntu/minna_pdf_analysis')
app_manifest = json.loads(Path('/home/ubuntu/repo_japanese_n5_app/android-app-flutter/assets/data/listening_lessons.json').read_text(encoding='utf-8'))
resource_index = json.loads(Path('/home/ubuntu/repo_resource_pack/minna-no-nihongo-listening/index.json').read_text(encoding='utf-8'))

out = {'lessons': []}
for lesson in app_manifest['lessons']:
    n = int(lesson['lesson'])
    tracks = []
    for track in lesson['tracks']:
        tracks.append({
            'track_number': track['track_number'],
            'filename': track['filename'],
            'duration_seconds': track['duration'],
            'app_asset': track['asset'],
            'resource_asset': f'minna-no-nihongo-listening/lesson-{n:02d}/{track["filename"]}',
        })
    out['lessons'].append({
        'lesson': n,
        'track_count': len(tracks),
        'tracks': tracks,
        'mondai_audio_policy': 'The last official track in this lesson is used as the default Mondai/listening audio reference. Keep the full track list for manual verification when a lesson contains multiple listening sections.',
        'default_mondai_audio': tracks[-1]['app_asset'] if tracks else None,
    })

(BASE / 'audio_map.json').write_text(json.dumps(out, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print('wrote', BASE / 'audio_map.json', 'lessons=', len(out['lessons']), 'tracks=', sum(x['track_count'] for x in out['lessons']))
