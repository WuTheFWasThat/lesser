from collections import defaultdict
from functools import partial


def _validate(d):
    """
    Makes sure a dictionary is a valid frame
    - Requires each value in the dictionary is a list
    - Requires each of those lists has the same length
    """
    s = None
    ks = None
    for k, v in d.items():
        if not isinstance(v, list):
            raise Exception(f"value at key {k} is not a list")
        if s is None:
            s = len(v)
            ks = k
        elif len(v) != s:
            raise Exception(f"length mismatch at keys {k} and {ks}: {len(v)} vs {s}")
    return dict(
        # consider size to be zero if there is nothing
        size=s or 0
    )


_key_missing = object()


class Frame(dict):
    """
    Adds some methods to dict-of-list datastructures to support a pandas-like API
    """

    def __init__(self, **d):
        _validate(d)
        super().__init__(**d)

    def size(self):
        return _validate(self)['size']

    def append(self, x):
        # NOTE: this mutates
        s = self.size()
        for k, v in x.items():
            if k not in self:
                self[k] = []
                for _ in range(s):
                    self[k].append(_key_missing)
            assert len(self[k]) == s
            self[k].append(v)
        for k in self.keys():
            if len(self[k]) != s + 1:
                assert k not in x
                self[k].append(_key_missing)
        return self

    def index(self, ind):
        """
        Like iloc for a single integer
        """
        res = dict()
        for k in self:
            v = self[k][ind]
            if v is _key_missing:
                continue
            res[k] = v
        return res

    def to_dicts(self):
        result = []
        for i in range(self.size()):
            result.append(self.index(i))
        return result

    def clone(self):
        return from_dicts(self.to_dicts())

    def __add__(self, other):
        f = self.clone()
        for d in other.to_dicts():
            f.append(d)
        return f

    def at(self, inds):
        """
        Like iloc for a list of integers
        """
        result = Frame()
        for i in inds:
            result.append(self.index(i))
        return result

    def group_by(self, fn):
        """
        Returns a new frame with items with
        - key: the value being grouped by, return by fn
        - values: a Frame containing all the items in that group
        """
        if isinstance(fn, str):
            k = fn
            fn = lambda x: x[k]
        key_to_vals = defaultdict(Frame)
        for i in range(self.size()):
            val = self.index(i)
            key = fn(val)
            key_to_vals[key].append(val)
        result = Frame()
        for k, vals in key_to_vals.items():
            result.append(dict(key=k, values=vals))
        return result

    def sort_by(self, fn):
        ds = self.to_dicts()
        ds = sorted(ds, key=fn)
        return from_dicts(ds)

    def map(self, fn):
        result = Frame()
        for i in range(self.size()):
            mapped = fn(self.index(i))
            result.append(mapped)
        return result

    def filter(self, fn):
        result = Frame()
        for i in range(self.size()):
            d = self.index(i)
            if fn(d):
                result.append(d)
        return result

    def compute_key(self, k, fn):
        """
        Convenience method for adding a new key
        """
        def compute_key_fn(x):
            v = fn(x)
            x[k] = v
            return x
        return self.map(compute_key_fn)


def size(frame):
    return frame.size()


def from_dicts(xs):
    result = Frame()
    for x in xs:
        result.append(x)
    return result


def index(frame, ind):
    return frame.index(ind)


def to_dicts(frame):
    return frame.to_dicts()


def clone(frame):
    return frame.clone()


def concat(f1, f2):
    return f1 + f2


def at(frame, inds):
    return frame.at(inds)


def group_by(frame, fn):
    return frame.group_by(fn)


def sort_by(frame, fn):
    return frame.sort_by(fn)


def sort_by_op(fn):
    return lambda frame: sort_by(frame, fn)


def map(frame, fn):
    return frame.map(fn)


def filter(frame, fn):
    return frame.filter(fn)


def compute_key(frame, k, fn):
    return frame.compute_key(k, fn)
