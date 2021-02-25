import pytest

import lesser as lpd
import numpy as np


def test_simple():
    dicts = [
        dict(x=1, y=2),
        dict(x=2, z=3),
    ]
    f = lpd.from_dicts(dicts)
    assert lpd.to_dicts(f) == dicts

    new = dict(x=2, y=2)
    assert lpd.size(f) == 2
    f.append(new)
    assert lpd.size(f) == 3
    assert lpd.to_dicts(f) == dicts + [new]
    grouped = lpd.group_by(f, 'x')
    assert lpd.size(grouped) == 2
    assert lpd.index(grouped, 0)['key'] == 1
    assert lpd.index(grouped, 0)['values'] == lpd.from_dicts([dicts[0]])
    assert lpd.index(grouped, 1)['key'] == 2
    assert lpd.index(grouped, 1)['values'] == lpd.from_dicts([dicts[1], new])

    assert lpd.at(f, [0, 2]) == lpd.from_dicts([dicts[0], new])


def test_chain():
    frame = lpd.from_dicts([
      dict(name="Alice",   day=0, sleep_mins=500, reaction_time=60),
      dict(name="Alice",   day=1, sleep_mins=420, reaction_time=81),
      dict(name="Bob",     day=0, sleep_mins=540, reaction_time=62),
      dict(name="Bob",     day=1, sleep_mins=520, reaction_time=71),
      dict(name="Charles", day=0, sleep_mins=340, reaction_time=88),
      dict(name="Charles", day=1, sleep_mins=410, reaction_time=94),
    ])
    reactions_by_sleep = (
        frame.compute_key("sleep_hours", lambda x: x['sleep_mins'] // 60)
        # group_by makes a frame with key=[some computed key] and values=[a frame with all original items with that same computed key]
        .group_by("sleep_hours")
        .compute_key("sleep_hours", lambda x: x["key"])
        .compute_key(
            "average_reaction_time", lambda x: np.mean(x["values"]["reaction_time"])
        )
        .sort_by(lambda x: x["sleep_hours"])
    )

    assert reactions_by_sleep['sleep_hours'] == [5, 6, 7, 8, 9]
    assert reactions_by_sleep['average_reaction_time'] == [88, 94, 81, (60 + 71) / 2, 62]

