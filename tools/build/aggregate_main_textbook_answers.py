import json
import re
from pathlib import Path

BASE = Path('/home/ubuntu/minna_pdf_analysis')
OUT = BASE / 'minna_n5_main_textbook_answers.json'
EXTRACT = BASE / 'page_extractions'
A_EXTRACT = BASE / 'renshuu_a_extractions'


def as_records(data, inherited_lesson=None, inherited_section=None):
    records = []
    if isinstance(data, list):
        for x in data:
            records.extend(as_records(x, inherited_lesson, inherited_section))
        return records
    if not isinstance(data, dict):
        return records

    lesson = inherited_lesson
    raw_lesson = data.get('lesson')
    if isinstance(raw_lesson, int):
        lesson = raw_lesson
    elif isinstance(raw_lesson, str):
        nums = re.findall(r'\d+', raw_lesson)
        if len(nums) == 1:
            lesson = int(nums[0])

    for key in data:
        m = re.fullmatch(r'lesson[_ -]?(\d+)', str(key), re.I)
        if m:
            records.extend(as_records(data[key], int(m.group(1)), inherited_section))

    if 'answer' in data and any(k in data for k in ('question','number','item','exercise_number','mode','audio_script','visual_description')):
        rec = dict(data)
        rec['_lesson'] = lesson
        rec['_section_context'] = inherited_section
        records.append(rec)
        return records

    for key, value in data.items():
        if str(key).lower() in ('lesson','source_page','page_notes','meta','title','book','book_en','source','note','usage','audio_map_note','caution'):
            continue
        section = inherited_section
        if key in ('practice_b','練習B'):
            section = '練習B'
        elif key in ('practice_c','練習C'):
            section = '練習C'
        elif key in ('problems','mondai'):
            section = 'Mondai'
        elif key in ('answers','items','entries','records','textbook_answers'):
            section = inherited_section
        records.extend(as_records(value, lesson, section))
    return records


def source_page(path):
    nums = [int(x) for x in re.findall(r'\d+', path.stem)]
    if path.name.startswith('mondai-') and len(nums) >= 2:
        return nums[:2]
    if path.name.startswith('renshuu_bc-') and nums:
        return nums[:1]
    return []


def lesson_from_file(path, kind):
    nums = [int(x) for x in re.findall(r'\d+', path.stem)]
    if kind == 'mondai' and nums:
        return (nums[0] - 4) // 2 + 1
    return None


def section_name(raw, context, question, exercise=None):
    s = str(raw or context or exercise or '')
    q = str(question or '')
    if '練習B' in s or 'practice_b' in s or '練習B' in q:
        return 'renshuu_b'
    if '練習C' in s or 'practice_c' in s or '練習C' in q:
        return 'renshuu_c'
    return 'mondai'


def clean_number(rec, question):
    for key in ('exercise_number','number','item'):
        if rec.get(key) not in (None, ''):
            return str(rec[key]).strip()
    q = str(question or '')
    m = re.search(r'練習[BC]\s*(\d+(?:[.、-]\s*\d+)?|例\d*)', q)
    if not m:
        m = re.search(r'^(\d+(?:[.、-]\s*\d+)?|例\d*)', q)
    return m.group(1).replace('、','.') if m else ''


def clean_item(rec, file_lesson, file_kind, page):
    question = rec.get('question')
    if question is None:
        question = ''
    if isinstance(question, (dict,list)):
        question = json.dumps(question, ensure_ascii=False)
    question = str(question).strip()
    answer = rec.get('answer','')
    if isinstance(answer, (dict,list)):
        answer = json.dumps(answer, ensure_ascii=False)
    answer = str(answer).strip()
    mode = str(rec.get('mode') or '').lower()
    audio_script = str(rec.get('audio_script') or '').strip()
    visual = str(rec.get('visual_description') or '').strip()
    if audio_script and mode in ('','text','unknown'):
        mode = 'audio'
    if visual and mode in ('','text','unknown'):
        mode = 'visual'
    if not mode:
        mode = 'text'
    lesson = rec.get('_lesson') or file_lesson
    if lesson is None:
        lm = re.search(r'第\s*(\d+)\s*課', question)
        if lm: lesson = int(lm.group(1))
    if lesson is not None:
        try: lesson = int(lesson)
        except Exception: lesson = None
    section = section_name(rec.get('section'), rec.get('_section_context'), question, rec.get('exercise'))
    if re.fullmatch(r'第\s*\d+\s*課\s*練習[BC]\s*\d+(?:[.、-]\s*\d+)?', question):
        question = ''
    if file_kind == 'mondai':
        section = 'mondai'
    return {
        'lesson': lesson,
        'section': section,
        'item': clean_number(rec, question),
        'question': question,
        'answer': answer,
        'mode': mode,
        'choices': rec.get('choices') if isinstance(rec.get('choices'), list) else [],
        'audio_script': audio_script or None,
        'visual_description': visual or None,
        'source_pages': page,
        'source': 'supplied_answer_key_pdf',
        'notes': str(rec.get('notes') or '').strip() or None,
        'confidence': str(rec.get('confidence') or 'medium'),
    }


def load_answer_records():
    all_records=[]
    for path in sorted(EXTRACT.glob('mondai-*.json')):
        try: data=json.loads(path.read_text(encoding='utf-8'))
        except Exception: continue
        for rec in as_records(data):
            all_records.append(clean_item(rec, lesson_from_file(path,'mondai'), 'mondai', source_page(path)))
    for path in sorted(EXTRACT.glob('renshuu_bc-*.json')):
        try: data=json.loads(path.read_text(encoding='utf-8'))
        except Exception: continue
        for rec in as_records(data):
            item=clean_item(rec, None, 'renshuu_bc', source_page(path))
            if item['lesson'] is not None:
                all_records.append(item)
    return all_records


def add_audio(item, audio_by_lesson):
    n=item.get('lesson')
    if not n or n not in audio_by_lesson:
        return item
    info=audio_by_lesson[n]
    item['audio_assets']=info['tracks']
    item['default_audio_asset']=info['default_mondai_audio'] if item['section']=='mondai' and item['mode'] in ('audio','mixed') else None
    item['audio_mapping']='lesson_track_list; default_mondai_audio points to the final official lesson track and should be manually confirmed when exact section-level alignment matters'
    return item


def main():
    audio=json.loads((BASE/'audio_map.json').read_text(encoding='utf-8'))
    audio_by_lesson={x['lesson']:x for x in audio['lessons']}
    records=load_answer_records()
    for rec in records:
        if rec.get('lesson') == 21 and rec.get('source_pages') == [44, 45] and rec.get('mode') in ('audio','mixed') and '7月に京都' in (rec.get('audio_script') or ''):
            rec.update({'item':'2.4','question':'祇園祭は有名です。','answer':'○','notes':'Visually recovered from the supplied answer-key continuation page.','confidence':'high'})
        if rec.get('lesson') == 24 and rec.get('source_pages') == [50, 51] and rec.get('mode') in ('audio','mixed') and '郵便局がありますか' in (rec.get('audio_script') or ''):
            rec.update({'item':'2.4','question':'女の人は郵便局の近くまで男の人といっしょに行ってあげます。','answer':'○','notes':'Visually recovered from the supplied answer-key continuation page.','confidence':'high'})
    lessons=[]
    for n in range(1,26):
        ls=[r for r in records if r.get('lesson')==n]
        sections=[]
        # Explicitly represent the requested sections whose answer key is not present in the supplied PDFs.
        sections.append({'section':'bunkei','status':'not_an_answer_section_in_supplied_answer_keys','source_pages':None,'items':[]})
        sections.append({'section':'reibun','status':'not_an_answer_section_in_supplied_answer_keys','source_pages':None,'items':[]})
        sections.append({'section':'kaiwa','status':'dialogue_text_not_answer_key','source_pages':None,'items':[]})
        sections.append({'section':'renshuu_a','status':'not_present_in_supplied_answer_key_pdf','source_page':'main textbook Renshuu A page varies by lesson','items':[]})
        for sec in ('renshuu_b','renshuu_c','mondai'):
            items=[add_audio(x,audio_by_lesson) for x in ls if x['section']==sec]
            items.sort(key=lambda x:(x.get('item',''),x.get('source_pages',[])))
            sections.append({'section':sec,'status':'extracted_from_supplied_answer_key','items':items})
        lessons.append({'lesson':n,'title':f'Minna no Nihongo Elementary I 2nd Edition — Lesson {n}','sections':sections,'audio_tracks':audio_by_lesson[n]['tracks'],'default_mondai_audio':audio_by_lesson[n]['default_mondai_audio']})
    out={
      'meta':{
        'dataset_id':'minna-no-nihongo-elementary-1-2nd-edition-main-textbook-answers',
        'book':'Minna no Nihongo Elementary I (Shokyu I), 2nd Edition Main Textbook',
        'scope':'Answer records only. Grammar and vocabulary datasets are intentionally omitted.',
        'source_documents':['user-supplied main textbook PDF','user-supplied answer-key PDF: feismo','user-supplied answer-key PDF: pdfcoffee answer key 2'],
        'audio_source':'User-provided jlpt-n5-resource-pack/minna-no-nihongo-listening and matching Flutter assets',
        'audio_note':'All lesson audio asset lists are included. The final lesson track is supplied as a default Mondai hint; exact track-to-question mapping should be checked against the audio edition.',
        'copyright_note':'This JSON is generated from user-supplied materials for personal/app integration. Respect publisher rights and repository licensing before public redistribution.'
      },
      'lessons':lessons,
      'coverage_summary':{
        'lessons':25,
        'sections_requested':['bunkei','reibun','kaiwa','renshuu_a','renshuu_b','renshuu_c','mondai'],
        'sections_with_extracted_answer_key_records':['renshuu_b','renshuu_c','mondai'],
        'sections_not_present_as_answer_key_records':['bunkei','reibun','kaiwa','renshuu_a'],
        'audio_tracks_verified':87
      }
    }
    OUT.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('lessons',len(lessons),'records',sum(len(s['items']) for l in lessons for s in l['sections']))
    print('mondai',sum(len(s['items']) for l in lessons for s in l['sections'] if s['section']=='mondai'))
    print('renshuu_b',sum(len(s['items']) for l in lessons for s in l['sections'] if s['section']=='renshuu_b'))
    print('renshuu_c',sum(len(s['items']) for l in lessons for s in l['sections'] if s['section']=='renshuu_c'))

if __name__=='__main__': main()
