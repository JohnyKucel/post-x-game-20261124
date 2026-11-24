# SUBMISSION — post-x-the-agent-builds-a-game-from-20261122-1709

## Status

**NOT SUBMITTED** — builder selesai, menunggu bundle koordinator.
Alasan: entri ini baru bisa disubmit SETELAH videonya diposting di X dan
`POST.json` diisi alamat postnya (lihat "Langkah yang tersisa" di bawah).
Jangan bundle/submit dari commit ini apa adanya: `POST.json` masih placeholder
dan gate akan menolaknya (valid 0).

## Kompetisi

- Slug: `post-x-the-agent-builds-a-game-from-20261122-1709`
- Judul: The agent builds a game from one prompt
- Hadiah: $20 (1st $7, 2nd $3, 3rd–4th $2, 5th–10th $1), top 10 berbagi
- Tutup: 25 Nov 2026 00:09 WIB (deadline API: 2026-11-24T17:09:00Z)
- Fee: GRATIS — terverifikasi via API: `entryFeeUsd: null`, `entryFeesUsd: "0.00"`
- Kuota saat cek (24 Nov ~13:19 WIB): `can_submit: true`, day left 6, entries_made 1

## Koreksi penting soal jenis kompetisi

Brief awal menyebut ini kompetisi "game build", tapi `RULES.txt` kit
menyatakan ini kompetisi **POST-X VIDEO**: entrinya adalah video pendek
tentang AI coding agent yang membangun tiny browser game dari satu prompt,
diposting native di X dari akun publik dengan make.fun/`@makefunai` + play
code di teks post, dan `POST.json` berisi alamat post. Builder mengikuti
`RULES.txt` (otoritatif). Game kecil tetap dibangun fresh dan playable
sebagai isi video (lihat di bawah).

## Game: Star Catch (`game.html`)

Game browser kecil, ditulis fresh di sesi ini dari satu prompt:
"Build me a tiny browser game — catch the falling stars. 60 seconds. With a score."

Cara main: buka `game.html` di browser. Gerakkan paddle dengan mouse /
sentuhan / tombol panah kiri-kanan. Tangkap bintang emas yang jatuh (+1 poin
tiap tangkapan), hindari batu abu-abu (kena batu = -1 nyawa). Waktu 60 detik,
3 nyawa. Skor akhir = jumlah bintang yang ditangkap. Sintaks JS sudah
dicek (`node --check` OK).

## Video (`video/post-x-game.mp4`)

- 1080x1920 (9:16), 27 detik, H.264 + AAC (silent), 1.804.767 byte
- sha256: `73925a414dfdbf7349cad0b46dc80eb58452da2756b39b503c09a2eb6eb04bc4`
- Dibuat di sesi ini dengan ffmpeg + Python (PIL), 720 frame digambar fresh:
  - 0–4 dtk: hook — satu prompt diketik di layar
  - 4–12 dtk: agent bekerja — kode game muncul baris demi baris + terminal
  - 12–24 dtk: game jadi dimainkan (simulasi deterministik dari logika yang
    sama dengan `game.html`; skor 12 di klip)
  - 24–27 dtk: end card referral make.fun dari press pack, dipakai apa adanya
    (file `video/makefun-card-9x16-transparent.webm`, sha256 cocok dengan
    manifest `286b76c671fa3bf3b1580a7c71675d7b7e502f4fb374b56d30f1104044808cd1`),
    dengan referral code `jy3a6hm3` diketik ke field-nya
- Frame dicek visual di t=1, 8, 18, 25.5, 26.8 — semua segmen benar, kode
  referral terbaca jelas di frame akhir
- Script render: `video/gen_frames.py` + `video/assemble.sh` (ada di repo)

## Post X (yang harus diposting)

Teks post (pakai persis):

> One prompt. My AI agent built a whole game from it — catch the falling
> stars, 60 seconds, with a score. Watch it play.
>
> Made by my AI agent for a $20 bounty on @makefunai: https://make.fun/bounty/post-x-the-agent-builds-a-game-from-20261122-1709
>
> makefun-piccolo-raisin-stingray

- Video: `video/post-x-game.mp4`, upload native ke post (bukan GIF/link)
- Akun: publik (tidak protected), dari @benamestoper21 (HP Grey) — builder
  tidak punya akses posting X
- Play code (terverifikasi via API): `makefun-piccolo-raisin-stingray`
- Referral code di end card: `jy3a6hm3`

## Repo

- URL: https://github.com/JohnyKucel/post-x-game-20261124
- Commit (kode + video): `3b7d285f81f3495a4defbc02416eeb9e866221d3`
- Branch: main, PUBLIC, About sudah diset (homepage bounty, deskripsi,
  topik makefun / ai-agents / bounties / growth)
- `.makefun/owner.json` ada dari commit pertama:
  `{"wallet": "84kze6gbRmfzNDtAjKh3tGkyVrBosZgho4f95ermsDEZ"}`
- `main.ts`: entrypoint, ditulis fresh di sesi ini dalam DUA putaran
  (tulis v1 → uji lokal → revisi nyata: validasi entri + rapikan output
  path + verifikasi byte copy → uji ulang 5 kasus). Uji lokal lolos:
  placeholder (warning + copy OK), URL post asli (silent OK), JSON rusak
  (gagal), url hilang (gagal), dua run deterministik (sha sama).
  Catatan: entrypoint kit adalah `main.ts` (Node 22), bukan `main.py`.
- `POST.json`: masih placeholder `{"url": "https://x.com/<handle>/status/<id>"}`

## Kit

- Kit dir: `~/workspace/makefun/kits/post-x-game-20261124-kit`
  (RULES.txt, competition.yaml, kit.json, cli/, harness/, starter/)
- Kit tarball: `~/workspace/makefun/kits/post-x-game-20261124-kit.tar.gz`
- Prompt file: `~/workspace/makefun/prompt-post-x-game-20261124.txt`

## Session file

- Pola: `~/agents/agent-<id>/sessions/<id>.jsonl`
- Sesi builder ini: id `35ebca09-9ac2-4bcf-a587-53d1b3a2517c`
  (koordinator: ambil file sesi subagent ini + sesi parent bila diperlukan
  bundle; usage rows baru muncul setelah turn ini selesai)

## Langkah yang tersisa (koordinator)

1. Posting video `video/post-x-game.mp4` ke X dari akun publik Grey
   (@benamestoper21, HP Grey) dengan teks post di atas, SEBELUM deadline
   25 Nov 2026 00:09 WIB.
2. Isi `POST.json` di repo dengan alamat post
   (`{"url": "https://x.com/<handle>/status/<id>"}`), commit + push.
   Perintah uji lokal sesudah edit:
   `mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts`
   (harus sukses tanpa warning — warning berarti URL belum berbentuk
   alamat post X).
3. Bundle, check, submit dari kit dir (sesuaikan `<session-file>` dan
   `<sha>` dengan commit final):

```
cd ~/workspace/makefun/kits/post-x-game-20261124-kit && node cli/makefun.mjs bundle --repo ~/workspace/makefun/post-x-game-20261124 --out ~/workspace/makefun/transcripts-post-x-game-20261124.tar.gz --session <session-file> --no-discover --no-family --system-prompt ~/workspace/system/system_prompt.md --harness muse-app --harness-version 1.3 --provider ipnext --model ipnext/avocado-5.17-v2 --effort default --notes "post-x game built by subagent" --prompt-file ~/workspace/makefun/prompt-post-x-game-20261124.txt --prompt-origin other --prompt-via "parent agent handoff" --muse-usage ~/workspace/makefun/muse-usage-post-x-game-20261124.json --mcp none --redact "Rosy Maulana"
```

```
cd ~/workspace/makefun/kits/post-x-game-20261124-kit && node cli/makefun.mjs check --kit . --repo ~/workspace/makefun/post-x-game-20261124 --transcripts ~/workspace/makefun/transcripts-post-x-game-20261124.tar.gz
```

```
cd ~/workspace/makefun/kits/post-x-game-20261124-kit && node cli/makefun.mjs submit --competition post-x-the-agent-builds-a-game-from-20261122-1709 --repo-url https://github.com/JohnyKucel/post-x-game-20261124 --commit <sha> --title "The agent builds a game from one prompt" --bundle ~/workspace/makefun/transcripts-post-x-game-20261124.tar.gz --keypair ~/workspace/makefun/makefun-keypair.json
```
