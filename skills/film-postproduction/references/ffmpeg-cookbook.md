# ffmpeg Cookbook

Verified against ffmpeg 9.0.2 on this machine. Paths are examples; keep the masters
untouched and write to a new file.

## Probe

```bash
ffprobe -v error -show_entries format=duration,size,bit_rate \
  -show_entries stream=codec_name,width,height,r_frame_rate,sample_rate,channels \
  -of json input.mp4
```

## Normalize then concat

Concat demuxer requires matching streams. Normalize each take first:

```bash
mkdir -p 04_gen/normalized
for f in 04_gen/shots/*/approved.mp4; do
  id=$(basename "$(dirname "$f")")
  ffmpeg -y -i "$f" \
    -vf "scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2,setsar=1,fps=24" \
    -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p \
    -c:a aac -b:a 192k -ar 48000 -ac 2 \
    "04_gen/normalized/${id}.mp4"
done
```

Write the list in edit order:

```bash
ls 04_gen/normalized/*.mp4 | sort > /tmp/concat.txt
# replace /tmp/concat.txt with an explicit, hand-ordered list
ffmpeg -y -f concat -safe 0 -i /tmp/concat.txt -c copy 05_post/rough-cut.mp4
```

If `-c copy` fails, re-encode:

```bash
ffmpeg -y -f concat -safe 0 -i /tmp/concat.txt \
  -c:v libx264 -crf 18 -preset slow -pix_fmt yuv420p \
  -c:a aac -b:a 256k -ar 48000 05_post/rough-cut.mp4
```

## Mux a mix onto picture

```bash
ffmpeg -y -i 05_post/picture-lock.mp4 -i 05_post/sound/mix.wav \
  -map 0:v:0 -map 1:a:0 -c:v copy -c:a aac -b:a 320k -ar 48000 -shortest \
  05_post/master.mp4
```

## Loudness

Measure:

```bash
ffmpeg -hide_banner -i 05_post/master.mp4 \
  -af loudnorm=I=-14:TP=-1:LRA=11:print_format=json -f null -
```

Apply the measured values (two-pass):

```bash
ffmpeg -y -i 05_post/master.mp4 \
  -af "loudnorm=I=-14:TP=-1:LRA=11:measured_I=<I>:measured_TP=<TP>:measured_LRA=<LRA>:measured_thresh=<thresh>:offset=<offset>:linear=true" \
  -c:v copy -c:a aac -b:a 320k 05_post/master_norm.mp4
```

## Captions

Burn in:

```bash
ffmpeg -y -i 05_post/master.mp4 \
  -vf "subtitles=05_post/deliver/captions.srt:force_style='FontName=Helvetica,FontSize=22,OutlineColour=&H80000000,BorderStyle=3,Outline=1,Shadow=0,MarginV=40'" \
  -c:a copy 05_post/deliver/final_captioned.mp4
```

Soft subtitles (preferred for platforms that support them):

```bash
ffmpeg -y -i 05_post/master.mp4 -i 05_post/deliver/captions.srt \
  -map 0 -map 1 -c copy -c:s mov_text -metadata:s:s:0 language=eng \
  05_post/deliver/final_softsubs.mp4
```

## Delivery encodes

H.264 1080p:

```bash
ffmpeg -y -i 05_post/master_norm.mp4 \
  -c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p -profile:v high -level 4.1 \
  -c:a aac -b:a 320k -ar 48000 -movflags +faststart \
  05_post/deliver/final_16x9_1080p.mp4
```

H.265:

```bash
ffmpeg -y -i 05_post/master_norm.mp4 \
  -c:v libx265 -preset slow -crf 20 -pix_fmt yuv420p -tag:v hvc1 \
  -c:a aac -b:a 320k -ar 48000 -movflags +faststart \
  05_post/deliver/final_16x9_1080p_hevc.mp4
```

ProRes archive:

```bash
ffmpeg -y -i 05_post/master_norm.mp4 \
  -c:v prores_ks -profile:v 3 -pix_fmt yuv422p10le \
  -c:a pcm_s24le 05_post/deliver/archive.mov
```

## Vertical master

If the film was framed 16:9 and a vertical version is required, crop deliberately:

```bash
ffmpeg -y -i 05_post/master_norm.mp4 \
  -vf "crop=ih*9/16:ih,scale=1080:1920,setsar=1" \
  -c:v libx264 -crf 18 -preset slow -c:a aac -b:a 320k \
  05_post/deliver/final_9x16_1080p.mp4
```

A crop is not native vertical. If vertical is a deliverable, frame it at shot plan.

## QC probes

Black frames:

```bash
ffmpeg -hide_banner -i final.mp4 -vf blackdetect=d=0.1:pix_th=0.10 -an -f null - 2>&1 | grep blackdetect
```

Freeze:

```bash
ffmpeg -hide_banner -i final.mp4 -vf freezedetect=n=0.001:d=0.5 -an -f null - 2>&1 | grep freeze
```

Scene cuts (for a contact sheet or an edit audit):

```bash
ffmpeg -hide_banner -i final.mp4 -vf "select='gt(scene,0.3)',showinfo" -an -f null - 2>&1 | grep showinfo
```

Contact sheet:

```bash
ffmpeg -y -i final.mp4 -vf "select='not(mod(n,48))',scale=320:-1,tile=5x4" -frames:v 1 contact.jpg
```

## Audio stems

Split a stereo mix only if it was built that way. Otherwise export stems from the editor,
not from the final mix.
