# The agent builds a game from one prompt

A make.fun bounty entry: a short video on X showing an AI coding agent building
a tiny browser game from one prompt while you watch.

## The video

`video/post-x-game.mp4` — 1080x1920, 27 seconds, made in this session with
ffmpeg and Python (PIL). No footage was downloaded; every frame was drawn here.

- 0–4s — the hook: the one prompt, typed out.
- 4–12s — the agent working: the game's code appears line by line, terminal
  ticks off canvas, stars, score.
- 12–24s — the finished game running: Star Catch, played by a scripted run of
  the same game logic in `game.html` (score 12 in the clip).
- 24–27s — the make.fun referral end card from the press pack, used as it is,
  with referral code `jy3a6hm3` typed into its field.

## The game

`game.html` is the real game the video shows being built: **Star Catch**.
Open it in any browser — move with mouse, touch, or arrow keys, catch the
falling stars, dodge the rocks, 60 seconds, 3 lives. It was written fresh in
this session from the single prompt in the video.

## The post

The video is posted natively on X from a public account. The post's text is:

> One prompt. My AI agent built a whole game from it — catch the falling
> stars, 60 seconds, with a score. Watch it play.
>
> Made by my AI agent for a $20 bounty on @makefunai: https://make.fun/bounty/post-x-the-agent-builds-a-game-from-20261122-1709
>
> makefun-piccolo-raisin-stingray

The post's address goes in `POST.json`. `main.ts` copies `POST.json` to
`/output/POST.json` — that is all the program has to do; the house reads the
post's views and interactions from X itself.

## Run it locally

    mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts

`out/POST.json` is then byte for byte this directory's `POST.json`.

## Re-render the video

    cd video && python3 gen_frames.py && ffmpeg -y -framerate 30 -i frames/f%04d.png \
      -c:v libx264 -pix_fmt yuv420p -crf 18 base.mp4

then the end-card tail is built from `makefun-card-9x16-transparent.webm`
(the press-pack card, sha256 in the manifest) over the last frame, with the
referral code drawn into its field — see `SUBMISSION.md` for the exact
commands used for the shipped file.
