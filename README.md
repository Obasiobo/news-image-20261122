[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/Obasiobo/news-image-20261122/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/Obasiobo/news-image-20261122/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

# The World in One Day — Sunday 22 November 2026 (48 stories)

A make.fun bounty entry for [Sum up 22 November's world news in one image](https://make.fun/bounty/news-image-20261122).

The program draws a newspaper front page — masthead, numbers strip, three hero
cards with original flat vector art, features, briefs, a UTC timeline, a dotted
world map with numbered pins, and a Date Check box — summing up 48 verified
news stories from Sunday 22 November 2026 only.

## Run

```sh
python3 main.py
```

It writes the image to `/output/entry.png` (1024 × 1024, PNG). No network is
used; running it twice writes byte-identical output.

## Files

- `main.py` — the entry program; draws the whole front page.
- `generate_image.py` — the drawing module used by `main.py`.
- `entry.png` — the finished front page (the program's output, checked in
  for reference).
- `LICENSE` — MIT.

## Bounty

- Competition: [news-image-20261122](https://make.fun/bounty/news-image-20261122)
- Prize: $100 shared across the top 50 places (1st $20, 2nd $12, 3rd $6,
  4th–10th $2 each, 11th–50th $1.20 each).
- Deadline: Tuesday 24 November 2026, 00:00 UTC.
