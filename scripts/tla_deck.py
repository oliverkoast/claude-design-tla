"""Build a TLA-branded session deck from a JSON spec.

Usage: python scripts/tla_deck.py examples/2026-10-27-session-3.json out.pptx

Each slide in the spec names a layout and fills its slots. Slides are cloned
from templates/tla-session-template.pptx, so fonts, colors and spacing match
the house style exactly. Use "|" inside a value for a line break.
"""
import copy, json, os, sys
from pptx import Presentation

A = '{http://schemas.openxmlformats.org/drawingml/2006/main}'
HERE = os.path.dirname(os.path.abspath(__file__))
TEMPLATE = os.path.join(HERE, '..', 'templates', 'tla-session-template.pptx')

# layout name -> (template slide index, slot name -> shape index, footer label idx, footer page idx)
LAYOUTS = {
    'title': (0, {'word1': 0, 'word2': 1, 'word3': 2, 'client': 3, 'date': 4, 'topics': 8}, 6, 7),
    'rows4': (1, {'title': 0, 'l1': 1, 'v1': 5, 'l2': 6, 'v2': 7, 'l3': 8, 'v3': 9, 'l4': 10, 'v4': 11}, 3, 4),
    'rows6': (2, {'title': 0, 'subtitle': 12, 'note': 17, 'l1': 1, 'v1': 5, 'l2': 6, 'v2': 7, 'l3': 8, 'v3': 9,
                  'l4': 10, 'v4': 11, 'l5': 13, 'v5': 14, 'l6': 15, 'v6': 16}, 3, 4),
    'big4': (3, {'title': 0, 'subtitle': 1, 'w1': 3, 'v1': 4, 'w2': 6, 'v2': 7, 'w3': 9, 'v3': 10,
                 'w4': 12, 'v4': 13, 'note': 15}, 17, 18),
    'numbered4': (4, {'title': 0, 'subtitle': 1, 'l1': 2, 'v1': 3, 'l2': 5, 'v2': 6, 'l3': 8, 'v3': 9,
                      'l4': 12, 'v4': 13, 'note': 14}, 16, 17),
    'columns4': (5, {'title': 0, 'h1': 2, 'b1': 3, 'h2': 5, 'b2': 6, 'h3': 8, 'b3': 9, 'h4': 11, 'b4': 12,
                     'note': 14}, 16, 17),
    'rows4quote': (7, {'title': 0, 'l1': 1, 'v1': 5, 'l2': 6, 'v2': 7, 'l3': 8, 'v3': 9, 'l4': 10, 'v4': 11,
                       'quote': 12}, 3, 4),
}


def set_text(shape, text):
    ps = [q._p for q in shape.text_frame.paragraphs]
    first = next(q for q in ps if q.findall(A + 'r'))
    for q in ps:
        if q is not first:
            q.getparent().remove(q)
    runs = first.findall(A + 'r')
    for el in list(first):
        if el.tag == A + 'br' or (el.tag == A + 'r' and el is not runs[0]):
            first.remove(el)
    lines = [l.strip() for l in text.upper().split('|')]
    tmpl = copy.deepcopy(first)
    first.findall(A + 'r')[0].find(A + 't').text = lines[0]
    prev = first
    for line in lines[1:]:
        p = copy.deepcopy(tmpl)
        p.findall(A + 'r')[0].find(A + 't').text = line
        prev.addnext(p)
        prev = p


def build(spec, out):
    prs = Presentation(TEMPLATE)
    originals = list(prs.slides)
    n = len(spec['slides'])
    for i, s in enumerate(spec['slides'], 1):
        idx, slots, foot_l, foot_n = LAYOUTS[s['layout']]
        src = originals[idx]
        new = prs.slides.add_slide(src.slide_layout)
        for sh in list(new.shapes):
            sh._element.getparent().remove(sh._element)
        if src._element.cSld.bg is not None:
            new._element.cSld.insert(0, copy.deepcopy(src._element.cSld.bg))
        for sh in src.shapes:
            new.shapes._spTree.append(copy.deepcopy(sh._element))
        shapes = list(new.shapes)
        for key, val in s.items():
            if key in slots:
                set_text(shapes[slots[key]], val)
        set_text(shapes[foot_l], 'TLA / ' + s.get('footer', s.get('title', 'SESSION')))
        set_text(shapes[foot_n], f'ARCFORMA AI INC.      {i:02d} / {n:02d}')
    ids = prs.slides._sldIdLst
    for sid in list(ids)[:len(originals)]:
        prs.part.drop_rel(sid.rId)
        ids.remove(sid)
    prs.save(out)


if __name__ == '__main__':
    build(json.load(open(sys.argv[1])), sys.argv[2])
