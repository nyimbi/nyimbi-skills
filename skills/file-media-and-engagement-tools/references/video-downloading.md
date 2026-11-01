# Video Downloading

Purpose: fetch a single video (or just its audio) at a stated quality and
format, using `scripts/video-downloader.py`, which drives `yt-dlp`. This is the
media-capture track of `file-media-and-engagement-tools`.

## Command

```bash
python scripts/video-downloader.py "<url>" [options]
```

| Option | Values | Default | Meaning |
|---|---|---|---|
| `-q`, `--quality` | `best`, `1080p`, `720p`, `480p`, `360p`, `worst` | `best` | Resolution target |
| `-f`, `--format` | `mp4`, `webm`, `mkv` | `mp4` | Container for video downloads |
| `-a`, `--audio-only` | flag | off | Audio only, extracted as MP3 |
| `-o`, `--output` | directory path | current working directory | Where the file lands |

Examples:

```bash
python scripts/video-downloader.py "https://www.youtube.com/watch?v=VIDEO_ID"
python scripts/video-downloader.py "URL" -q 720p
python scripts/video-downloader.py "URL" -a
python scripts/video-downloader.py "URL" -q 720p -f webm -o /path/to/directory
```

Confirm with the user which of quality / format / audio-only / destination they
want before running anything other than a default fetch.

## Behaviour of the underlying tool

`yt-dlp` is installed automatically if missing, fetches video metadata first,
picks the best available streams matching the request, and merges separate
video and audio streams when the source ships them apart (which is why a
`best` download is not always instant).

- Filename is generated from the video title; collisions with an existing file
  need a decision (overwrite, rename, or new directory)
- Playlists are skipped by default — this skill downloads one video per URL
- Higher quality takes longer and more disk; check free space before a long `best` fetch

## Verify before reporting success

1. The command exited zero and reported the output path
2. The file exists and is non-zero in size
3. For video: it opens and plays; audio/video are both present (merged correctly)
4. For `-a`: the output is an MP3 of usable bitrate, not a silent or truncated file
5. Size, duration, and format are quoted in the summary

If the URL is unavailable, region-locked, private, or a playlist, report that
verbatim instead of reporting a partial file as success.

## Quality gates for this track

- URL, quality, format, audio-only, and destination confirmed before the download
- Output path reported back exactly as written to disk
- File existence and non-zero size verified before calling it done
- Failures (deleted video, login required, region block) quoted, not paraphrased away
- Downloads limited to what the user asked for — one video, no playlists, no bulk grabs
