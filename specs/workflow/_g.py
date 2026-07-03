import os

DIR = 'E:\資料冊\桌面\Atlas\specs\workflow'
os.makedirs(DIR, exist_ok=True)
NL = chr(10)
TQ = chr(39) * 3
BT = chr(96) * 3

DEPS = [
    'RFC-0001 Runtime Overview',
    'RFC-0002 Runtime Lifecycle',
    'RFC-0003 Runtime Service Model',
    'RFC-0004 Runtime Scheduler',
    'RFC-0005 Runtime Event Bus',
    'RFC-0006 Runtime State Management',
    'RFC-1001 Common Event Model',
    'RFC-1002 Common State Model',
    'RFC-1003 Common Capability Model',
    'RFC-1004 Common Contract Model',
    'RFC-1005 Common Manifest Model',
    'RFC-1006 Common Error Model',
]

REL = {}
for _i, _n in [
    (301,'Overview'),
    (302,'Language'),
    (303,'Execution'),
    (304,'Runtime'),
    (305,'Lifecycle'),
    (306,'State'),
    (307,'Context'),
    (308,'Events'),
    (309,'Actions'),
    (310,'Conditions'),
    (311,'Triggers'),
    (312,'Scheduler'),
    (313,'Parallelism'),
    (314,'Error Handling'),
    (315,'Recovery'),
    (316,'Debugging'),
    (317,'Validation'),
    (318,'Versioning'),
    (319,'Security'),
    (320,'Performance'),
    (321,'Observability'),
    (322,'Extension'),
    (323,'Plugin Integration'),
    (324,'Storage'),
    (325,'AI'),
    (326,'Vision'),
    (327,'IPC'),
    (328,'Serialization'),
    (329,'Compatibility'),
    (330,'Compliance'),
]:
    REL[_i] = _n

def make_header(num, title):
    dl = NL.join('  - '+d for d in DEPS)
    rl = NL.join('  - RFC-%04d Workflow %s'%(k,v) for k,v in sorted(REL.items()))
    h = [
        '# RFC-%04d: %s'%(num, title),
        TQ,
        '## Header',
        TQ,
        BT,
        'RFC: RFC-%04d'%num,
        'Title: %s'%title,
        'Status: Proposed',
        'Version: 1.0.0',
        'Author: Atlas Specification Committee',
        'Created: 2026-07-01',
        'Depends On:',
        dl,
        'Supersedes: None',
        'Superseded By: None',
        'Category: Workflow',
        'Layer: Standard',
        'Normative: YES',
        'Audience: All Subsystem Teams',
        'ADR References:',
        '  - ADR-0012',
        'Constitution References:',
        '  - Section 1 (Workflow Philosophy)',
        'Related RFCs:',
        rl,
        'Target Release: 1.0.0',
        'Review Cycle: Specification Committee',
        'Compatibility: Compatible with Spec 1.x',
        'Last Updated: 2026-07-01',
        BT,
        TQ,
    ]
    return NL.join(h) + NL

def wf(name, content):
    path = os.path.join(DIR, name)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print('Wrote ' + name + ': ' + str(os.path.getsize(path)))

def tbl(headers, rows):
    r = []
    r.append('| ' + ' | '.join(headers) + ' |')
    r.append('| ' + ' | '.join('---' for _ in headers) + ' |')
    for row in rows:
        r.append('| ' + ' | '.join(str(c) for c in row) + ' |')
    return NL.join(r)

def mermaid(diagram):
    return '`mermaid' + NL + diagram + NL + '`'

print('Generator loaded OK')