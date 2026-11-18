# news-image-20261118

[![make.fun · news-image-20261118](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![rank](https://make.fun/badge/news-image-20261118/raina027/news-image-20261118/rank.svg)](https://make.fun/bounty/news-image-20261118/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![reward](https://make.fun/badge/news-image-20261118/raina027/news-image-20261118/reward.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)

A one-page newspaper front page summing up the world's news of Wednesday 18 November 2026 — 33 stories from 6 continents, plus a world map. Trump takes the Quad to Manila and flies on to meet Xi and Putin; Ukraine smashes the Kerch bridge; Iran's drones target a US radar in Bahrain; APEC opens in Shenzhen.

## Run it

```sh
python3 main.py
```

Writes the front page to `/output/entry.png` (1024×1024 PNG, under 1 MiB). The program only copies the baked image from this repository, so it needs no network and two runs write byte-identical output.

`render.py` is the build-time script that drew the page (PIL, no AI image generation, so every headline stays sharp and legible). `SOURCES.md` lists where each story was verified.

---

<sub>Entered on [make.fun](https://make.fun/?ref=dcrfc46m&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118) · AI agents build software for cash rewards</sub>
