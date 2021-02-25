from collections import defaultdict
from functools import partial


def new():
    return dict()


def size(frame):
    s = None
    for vs in frame.values():
        if s is None:
            s = len(vs)
        else:
            assert s == len(vs)
    if s is None:
        return 0
    return s


_key_missing = object()

# NOTE: this mutates
def _append(frame, x):
    s = size(frame)
    for k, v in x.items():
        if k not in frame:
            frame[k] = []
            for _ in range(s):
                frame[k].append(_key_missing)
        assert len(frame[k]) == s
        frame[k].append(v)
    for k in frame.keys():
        if len(frame[k]) != s + 1:
            assert k not in x
            frame[k].append(_key_missing)
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
        if v is _key_missing:
            continue
        res[k] = v
    return res


def index_op(ind):
    return lambda frame: index(frame, ind)


def to_dicts(frame):
    result = []
    for i in range(size(frame)):
        result.append(index(frame, i))
    return result


def copy(frame):
    return from_dicts(to_dicts(frame))


def append(f, d):
    f = copy(f)
    _append(f, d)
    return f


def slice_frame(frame, inds):
    result = new()
    for i in inds:
        _append(result, index(frame, i))
    return result


def slice_op(inds):
    return lambda frame: slice_frame(frame, inds)


def group_by(frame, fn):
    if isinstance(fn, str):
        k = fn
        fn = lambda x: x[k]
    key_to_vals = defaultdict(new)
    for i in range(size(frame)):
        val = index(frame, i)
        key = fn(val)
        _append(key_to_vals[key], val)
    result = new()
    for k, vals in key_to_vals.items():
        _append(result, dict(key=k, values=vals))
    return result


def group_by_op(fn):
    return lambda frame: group_by(frame, fn)


def sort_by(frame, fn):
    ds = to_dicts(frame)
    ds = sorted(ds, key=fn)
    return from_dicts(ds)


def sort_by_op(fn):
    return lambda frame: sort_by(frame, fn)


def map_frame(frame, fn):
    result = new()
    for i in range(size(frame)):
        mapped = fn(index(frame, i))
        _append(result, mapped)
    return result


def map_op(fn):
    return lambda frame: map_frame(frame, fn)


def compute_key(frame, k, fn):
    result = new()
    for i in range(size(frame)):
        d = index(frame, i)
        v = fn(d)
        d[k] = v
        _append(result, d)
    return result


def compute_key_op(k, fn):
    return lambda frame: compute_key(frame, k, fn)


map = map_frame
slice = slice_frame
