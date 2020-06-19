import pytest

import lesser

def test_simple():
    dicts = [
        dict(x=1, y=2),
        dict(x=2, z=3),
    ]
    f = lesser.from_dicts(dicts)
    print(f)
    assert lesser.to_dicts(f) == dicts
