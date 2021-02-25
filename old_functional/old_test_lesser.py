import pytest

import lesser as lpd


def test_simple():
    dicts = [
        dict(x=1, y=2),
        dict(x=2, z=3),
    ]
    f = lpd.from_dicts(dicts)
    assert lpd.to_dicts(f) == dicts

    new = dict(x=2, y=2)
    assert lpd.size(f) == 2
    f = lpd.append(f, new)
    assert lpd.size(f) == 3
    assert lpd.to_dicts(f) == dicts + [new]
    grouped = lpd.group_by(f, 'x')
    assert lpd.size(grouped) == 2
    assert lpd.index(grouped, 0)['key'] == 1
    assert lpd.index(grouped, 0)['values'] == lpd.from_dicts([dicts[0]])
    assert lpd.index(grouped, 1)['key'] == 2
    assert lpd.index(grouped, 1)['values'] == lpd.from_dicts([dicts[1], new])

    assert lpd.slice(f, [0, 2]) == lpd.from_dicts([dicts[0], new])
