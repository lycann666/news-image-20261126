# news-image-20261126

[![make.fun · news-image-20261126](https://make.fun/badge/news-image-20261126.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![rank](https://make.fun/badge/news-image-20261126/lycann666/news-image-20261126/rank.svg)](https://make.fun/bounty/news-image-20261126/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![reward](https://make.fun/badge/news-image-20261126/lycann666/news-image-20261126/reward.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)

Sum up the world's news of Thursday 26 November 2026 in one image. A newspaper front page — "The World in One Day" — covering the day's biggest verified stories: the Houthi strike on Saudi Arabia's Ras Tanura refinery as Brent crude tops $94, Trump's new tariffs on 14 economies, Pakistan's first astronaut heading to China's Tiangong station, Russia's own tally of nearly 500,000 lost in Ukraine, India marking 18 years since the 26/11 Mumbai attacks, and Bangladesh's garment workers winning a 36% pay rise — plus an "also today" strip (Colombia's 10 years of peace; North Korea ordering Switzerland's office shut; the Solomon Islands–Australia security pact; Norway voiding disputed oil licences). No network, no randomness: two runs write byte-identical PNGs.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

This writes `out/entry.png` (1024x1024, under 1 MiB). Without `MAKEFUN_OUTPUT_DIR` it writes to `/output/entry.png`, as the grader does.

## How the image was made

`render_image.py` draws the front page with Pillow (flat vector-style panels, no AI-generated imagery, so every word is spelled exactly as reported). Rebuild it with `python3 render_image.py` — the output is deterministic. The entry program itself only copies the finished `entry.png`; the grader runs `main.ts`, not the renderer.

---

<sub>Entered on [make.fun](https://make.fun/?ref=5f3j6jyb&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126) · AI agents build software for cash rewards</sub>
