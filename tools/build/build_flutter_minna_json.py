import json
from pathlib import Path

BASE=Path('/home/ubuntu/minna_pdf_analysis')
source=json.loads((BASE/'minna_n5_main_textbook_answers.json').read_text(encoding='utf-8'))
out={'meta':dict(source['meta'], format='flutter_minna_answer_tree', note='Nested adapter for the existing MinnaData lesson renderer. Use the canonical JSON for item-level audio, source pages, confidence, and visual fields.'),'lessons':[]}
for lesson in source['lessons']:
    sections=[]
    for sec in lesson['sections']:
        if sec['section'] not in ('renshuu_b','renshuu_c','mondai'):
            continue
        nodes=[]
        for item in sec['items']:
            label=item.get('question') or item.get('item') or '—'
            if item.get('question') and item.get('item'):
                label=f"{item['item']} — {item['question']}"
            nodes.append({'question':label,'items':[{'item':'answer','answer':item.get('answer','')}], 'mode':item.get('mode'), 'audio_script':item.get('audio_script'), 'visual_description':item.get('visual_description'), 'source_pages':item.get('source_pages')})
        sections.append({'section':sec['section'],'items':nodes,'audioAsset':lesson['default_mondai_audio'] if sec['section']=='mondai' else None})
    out['lessons'].append({'lesson':str(lesson['lesson']),'lesson_ja':f"第{lesson['lesson']}課",'sections':sections})
(BASE/'main_textbook_answers_flutter_adapter.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('wrote adapter lessons=',len(out['lessons']))
