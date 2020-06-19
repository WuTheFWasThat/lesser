from collections import defaultdict


def new():
    return dict()


def size(f):
    s = None
    for vs in f.values():
        if s is None:
            s = len(vs)
        else:
            assert s == len(vs)
    if s is None:
        return 0
    return s


def append(frame, x):
    s = size(frame)
    for k, v in x.items():
        if k not in frame:
            frame[k] = []
            for _ in range(s):
                frame[k].append(None)
        assert len(frame[k]) == s
        frame[k].append(v)
    for k in frame.keys():
        if len(frame[k]) != s + 1:
            assert k not in x
            frame[k].append(None)
    return frame


def from_dicts(xs):
    result = new()
    for x in xs:
        append(result, x)
    return result


def index(frame, ind):
    res = dict()
    for k in frame:
        v = frame[k][ind]
        if v is None:
            continue
        res[k] = v
    return res


def to_dicts(frame):
    result = []
    for i in range(size(frame)):
        result.append(index(frame, i))
    return result


def slice(f, inds):
    result = new()
    for i in inds:
        append(result, index(f, i))
    return result


def group_by(f, fn):
    if isinstance(fn, str):
        k = fn
        fn = lambda x: x[k]
    key_to_vals = defaultdict(new)
    for i in range(size(f)):
        val = index(f, i)
        key = fn(val)
        append(key_to_vals[key], val)
    result = new()
    for k, vals in key_to_vals.items():
        append(result, dict(key=k, values=vals))
    return result
