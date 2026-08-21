import json
from pathlib import Path

BASE=Path('/home/ubuntu/minna_pdf_analysis')
APP=Path('/home/ubuntu/repo_japanese_n5_app/android-app-flutter')
canonical=json.loads((BASE/'minna_n5_main_textbook_answers.json').read_text(encoding='utf-8'))
adapter=json.loads((BASE/'main_textbook_answers_flutter_adapter.json').read_text(encoding='utf-8'))
assert len(canonical['lessons']) == 25
assert len(adapter['lessons']) == 25
for lesson in adapter['lessons']:
    assert lesson['lesson']
    sections={s['section']:s for s in lesson['sections']}
    assert {'renshuu_b','renshuu_c','mondai'} <= set(sections)
    for sec in lesson['sections']:
        assert isinstance(sec['items'],list)
        if sec.get('audioAsset'):
            assert (APP/sec['audioAsset']).exists(), sec['audioAsset']
        for node in sec['items']:
            assert 'question' in node
            assert node['items'] and node['items'][0].get('answer','') != ''
print('canonical_json_valid=true')
print('adapter_json_valid=true')
print('lessons=',len(adapter['lessons']))
print('adapter_records=',sum(len(s['items']) for l in adapter['lessons'] for s in l['sections']))
print('audio_asset_paths_valid=true')
