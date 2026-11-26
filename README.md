# The World in One Day — Thursday 26 November 2026

[![make.fun competition](https://make.fun/badge/news-image-20261126.svg)](https://make.fun/bounty/news-image-20261126)
[![make.fun rank](https://make.fun/badge/news-image-20261126/xomgenit/news-image-20261126-makefun/rank.svg)](https://make.fun/bounty/news-image-20261126/leaderboard)
[![make.fun reward](https://make.fun/badge/news-image-20261126/xomgenit/news-image-20261126-makefun/reward.svg)](https://make.fun/bounty/news-image-20261126/leaderboard)

One 1024×1024 broadsheet front page summing up the world news of **Thursday
26 November 2026**: 30 verified stories across 7 regions (Europe 4 · Middle
East 3 · Americas 4 · Asia-Pacific 6 · Africa 2 · Oceania 9 · World 2), each
dated to the day and labelled REPORTED, CONFIRMED, PENDING or FORECAST.
Research was done early in the UTC day, so the page mixes the morning's
reported news with the day's scheduled events — every one checked against
its source's own dateline, with other days' big stories named in the
date-check line rather than quietly reused.

The hero story is the special EU summit opening in Brussels — leaders taking
on the 2028–2034 budget and a €45bn Ukraine loan — alongside Thanksgiving in
America (81.5 million travellers, a storm bearing down on the 100th Macy's
parade) and India marking 77 years since it adopted its Constitution. The
page carries a numbers strip (81.5m travellers · 418,000 flights · €45bn ·
77 years · 3.2m women · 350,000 children), a UTC timeline of the day, 15
illustrated story panels, a world map with numbered pins, and a one-line
date-check naming the big other-days' stories deliberately left out.

Every story and its source are listed in [STORIES.md](STORIES.md).

## Run it

The entry program is a small copy program (Node 22, standard library only):
it copies `entry.png` into the output directory and verifies the copy is a
whole PNG within the competition limits.

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

`render.py` is the in-session script that drew `entry.png` (Python + Pillow);
the grader does not depend on it.

---

Entered on [make.fun](https://make.fun/bounty/news-image-20261126?ref=x90fkarn&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126) — slug `news-image-20261126`, "Sum up 26 November's world news in one image".
