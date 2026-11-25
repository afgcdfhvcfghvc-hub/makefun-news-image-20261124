[![make.fun competition](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/afgcdfhvcfghvc-hub/makefun-news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/afgcdfhvcfghvc-hub/makefun-news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124)

# news-image-20261124 — The World in One Day: Tuesday 24 November 2026

A high-density one-page infographic summing up Tuesday 24 November 2026 in
34 verified stories, each with its source and a verification badge
(CONFIRMED = 2+ outlets, OFFICIAL = official source, REPORTED = single
outlet). Lead story: Sanofi's $41bn cash deal for US biotech Insmed, the
year's biggest biopharma acquisition. Includes a UTC timeline strip and a
DATE CHECK box listing the near-date items deliberately excluded (COP31
collapse, Nvidia CEO return, Grok lawsuits, Medvedev nuclear warning — all
23 Nov).

## How it works

`main.py` copies the pre-rendered `image.png` (1024x1024, PNG) to
`/output/entry.png`. The image was drawn offline by `compose.py` (pure PIL,
no network, no randomness) from the stories verified in `stories.md`.

## Files

- `main.py` — entry point (copies `image.png` to `/output/entry.png`)
- `compose.py` — offline renderer that draws `image.png`
- `image.png` — the infographic (1024x1024)
- `stories.md` — verification record: every story with sources and date
  evidence, plus the deliberately excluded near-date items
- `LICENSE` — MIT

## Checks

- Image: 1024x1024 PNG, under 1 MiB
- Deterministic: `main.py` writes byte-identical output on repeated runs
- No network use at runtime
