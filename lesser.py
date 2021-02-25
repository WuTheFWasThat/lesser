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


# NOTE: this mutates
def _append(frame, x):
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
        _append(result, x)
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
        _append(result, index(f, i))
    return result


def group_by(f, fn):
    if isinstance(fn, str):
        k = fn
        fn = lambda x: x[k]
    key_to_vals = defaultdict(new)
    for i in range(size(f)):
        val = index(f, i)
        key = fn(val)
        _append(key_to_vals[key], val)
    result = new()
    for k, vals in key_to_vals.items():
        _append(result, dict(key=k, values=vals))
    return result


def sort_by(f, fn):
    ds = to_dicts(f)
    ds = sorted(ds, key=fn)
    return from_dicts(ds)


def map(f, fn):
    result = new()
    for i in range(size(f)):
        mapped = fn(index(f, i))
        _append(result, mapped)
    return result


def compute_key(f, k, fn):
    result = new()
    for i in range(size(f)):
        d = index(f, i)
        v = fn(d)
        d[k] = v
        _append(result, d)
    return result

