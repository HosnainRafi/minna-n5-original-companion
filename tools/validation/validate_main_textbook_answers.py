import json
from pathlib import Path
from collections import Counter

path = Path('/home/ubuntu/minna_pdf_analysis/minna_n5_main_textbook_answers.json')
data = json.loads(path.read_text(encoding='utf-8'))
assert len(data['lessons']) == 25
required = {'bunkei','reibun','kaiwa','renshuu_a','renshuu_b','renshuu_c','mondai'}
errors=[]
report=[]
for lesson in data['lessons']:
    n=lesson['lesson']
    sections={s['section']:s for s in lesson['sections']}
    missing=required-set(sections)
    if missing: errors.append(f'lesson {n} missing sections {sorted(missing)}')
    tracks=lesson.get('audio_tracks',[])
    if not tracks: errors.append(f'lesson {n} has no audio tracks')
    for sec in ('renshuu_b','renshuu_c','mondai'):
        items=sections[sec]['items']
        null_lessons=[i for i in items if i.get('lesson') != n]
        if null_lessons: errors.append(f'lesson {n} {sec} contains mismatched lesson fields: {len(null_lessons)}')
        missing_answer=[i for i in items if not isinstance(i.get('answer'),str) or not i.get('answer')]
        if missing_answer: errors.append(f'lesson {n} {sec} has {len(missing_answer)} missing answers')
        audio_items=[i for i in items if i.get('mode') in ('audio','mixed') or i.get('audio_script')]
        bad_audio=[i for i in audio_items if sec == 'mondai' and not i.get('default_audio_asset')]
        if bad_audio: errors.append(f'lesson {n} {sec} has {len(bad_audio)} audio items without asset')
        keys=[(i.get('item'),i.get('question'),i.get('answer')) for i in items]
        dup=sum(v-1 for v in Counter(keys).values() if v>1)
        report.append((n,sec,len(items),len(audio_items),dup))
print('json_valid=true')
print('lessons=',len(data['lessons']))
print('audio_tracks=',data['coverage_summary']['audio_tracks_verified'])
print('records=',sum(x[2] for x in report))
print('errors=',len(errors))
for row in report: print('coverage',*row)
for e in errors: print('ERROR',e)
if errors: raise SystemExit(1)
