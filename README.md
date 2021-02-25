# Lesser :panda_face:

This is a tiny data manipulation library, very loosely based on pandas.
The core object is just a dict of lists (where each list has the same length).  We call this a frame.

It is not fast, but it is very simple.

## Usage

It's most easily understood by example!

```python
import lesser as lpd
import numpy as np
import toolz

frame = lpd.from_dicts([
  dict(name="Alice",   day=0, sleep_mins=500, reaction_time=60),
  dict(name="Alice",   day=1, sleep_mins=420, reaction_time=81),
  dict(name="Bob",     day=0, sleep_mins=540, reaction_time=62),
  dict(name="Bob",     day=1, sleep_mins=520, reaction_time=71),
  dict(name="Charles", day=0, sleep_mins=340, reaction_time=88),
  dict(name="Charles", day=1, sleep_mins=410, reaction_time=94),
])
reactions_by_sleep = toolz.pipe(
    frame,
    lpd.compute_key_op("sleep_hours", lambda x: x['sleep_mins'] // 60),
    # group_by makes a frame with key=[some computed key] and values=[a frame with all original items with that same computed key]
    lpd.group_by_op("sleep_hours"),
    lpd.compute_key_op("sleep_hours", lambda x: x["key"]),
    lpd.compute_key_op(
        "average_reaction_time", lambda x: np.mean(x["values"]["reaction_time"])
    ),
    lpd.sort_by_op(lambda x: x["sleep_hours"])
)

print(reactions_by_sleep)
import matplotlib.pyplot as plt
# A misleading chart
plt.plot(
    reactions_by_sleep["sleep_hours"],
    reactions_by_sleep["average_reaction_time"],
)
plt.show()
```

## Development

### Run tests

`pytest`
