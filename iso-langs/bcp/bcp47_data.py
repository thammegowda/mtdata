from pathlib import Path
import csv

src_dir = Path(__file__).parent
ISO_3166_file = src_dir / 'iso3166.tsv'
ISO_15924_file = src_dir / 'iso15924.tsv'
ISO_639_3_file = src_dir / 'iso639_3.tsv'
IANA_tag_file = src_dir / 'language-subtag-registry'


def read_tsv(path: Path):
    assert path.exists(), f'file at {path} not found'
    with open(path, encoding='utf-8') as inp:
        yield from csv.reader(inp, delimiter='\t', quotechar=None)


def read_tsv_with_head(path: Path):
    rows = list(read_tsv(path))
    head, rows = rows[0], rows[1:]
    return head, rows


def load_country_codes():
    head, rows = read_tsv_with_head(ISO_3166_file)
    assert head[0] == 'English Name'
    assert head[2] == 'Alpha-2'

    def cleanup(name):
        return name.replace(' (the)', '')

    recs = [(r[2], cleanup(r[0]))for r in rows]
    return recs


def load_script_codes():
    head, rows = read_tsv_with_head(ISO_15924_file)
    assert head[0] == 'Code'
    assert head[2] == 'English Name'

    recs = [(r[0], r[2]) for r in rows]
    return recs


def load_language_codes():
    head, rows = read_tsv_with_head(ISO_639_3_file)
    assert head[0] == 'Id'
    assert head[3] == 'Part1'
    assert head[6] == 'Ref_Name'

    recs = [(r[0], r[3], r[6]) for r in rows]
    return recs


def parse_iana_tags(path: Path):

    def unwrap_lines(lines):
        """Some lines are wrapped; this mapper unwraps lines"""
        prev = ''
        wrap_prefix = '  '  # two spaces
        for i, line in enumerate(lines):
            if i == 0:
                prev = line
                continue
            if line.startswith(wrap_prefix):
                prev += ' ' + line.strip()
            else:
                yield prev
                prev = line
        if prev:
            yield prev

    def segment_recs(lines):
        marker = '%%'
        recs = []
        for line_num, line in enumerate(lines, start=1):
            line = line.strip()
            if line_num == 1 and 'File-Date:' in line:
                continue
            if line == marker:
                recs.append({})
            else:
                parts = line.split(":")
                assert len(parts) >= 2
                key = parts[0].strip()
                val = ':'.join(parts[1:]).strip()
                if key in recs[-1]:  # already exists
                    if not isinstance(recs[-1][key], list):
                        recs[-1][key] = [recs[-1][key]]
                    recs[-1][key].append(val)
                else:
                    recs[-1][key] = val
        return recs

    with open(path, encoding='utf-8') as lines:
        recs = segment_recs(unwrap_lines(lines))
    return recs


def load_iana_default_scripts():
    tags = parse_iana_tags(IANA_tag_file)
    scripts = []
    for tag in tags:
        if 'Suppress-Script' in tag:
            assert tag['Type'] == 'language', f'Error: {tag}'
            scripts.append([tag['Subtag'], tag['Suppress-Script'], tag['Description']])
    return scripts


def get_bcp47_data():
    return {
        'languages': load_language_codes(),
        'scripts': load_script_codes(),
        'countries': load_country_codes(),
        'default_scripts': load_iana_default_scripts()
    }


if __name__ == '__main__':
    import json
    data = get_bcp47_data()
    s = json.dumps(data, ensure_ascii=False)
    print(s.replace("],", "],\n  ").replace(": ", ":\n  ").replace('\n   "', '\n"'))
    #from pprint import pprint
    #pprint(data)

