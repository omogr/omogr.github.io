import argparse
import json
import sys
import os

def join_rewrite(path):
    with open("block_sum.html", 'r', encoding='utf-8') as f:
        block_content = f.read()
    block_content = [ts.strip() for ts in block_content.split('\n')]
    all_blocks = []
    header = None
    body = []
    for ts in block_content:
        
        if ts.startswith("<p>|title "):
            if header is not None:
                assert header
                assert body
                tb = {
                    "header":header,
                    "body":body
                }
                #qq = (header, body)
                all_blocks.append(tb)
            assert ts.endswith("</p>")
            header = ts[10:-4]
            header = header.strip()
            body = []
            continue
        ts = ts.strip()
        if ts:
            body.append(ts)

    if header is not None:
        assert header
        assert body
        tb = {
            "header":header,
            "body":body
        }
        #qq = (header, body)
        all_blocks.append(tb)

    # os.makedirs("block", exist_ok=True)
    return 
    titles = {}

    main = []    
    for index, (header, body) in enumerate(all_blocks):
        block_num = index + 1
        key = "%d"%block_num
        titles[key] = header
        output_file = "block/r%02d.html"%block_num
    
        with open(output_file, 'w', encoding='utf-8') as fout:
            print('\n'.join(body), file=fout)
        
    with open("titles.json", 'w', encoding='utf-8') as fout:
        print(json.dumps(titles, ensure_ascii=False, indent=2), file=fout)


if __name__ == '__main__':
    # Парсинг аргументов командной строки
    #parser = argparse.ArgumentParser(description="Объединяем в формате json")
    #parser.add_argument('utterence_json_file', help="Путь к входному propmt_file")
    #parser.add_argument('content_json_file', help="Путь к входному json_data_file")
    #parser.add_argument('output_file', help="Путь к выходному файлу")
    #args = parser.parse_args()
    

    #output_file = 'art.json'
    #content_json_file = "../data/content.json"
    #utterence_json_file = "../data/speaker_utterance.json"
    join_rewrite()
    