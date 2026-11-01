# Image Production — Enhancement and Export

Technique file for the production step of the [SKILL.md](../SKILL.md) workflow.
image-enhancer supplies **retouch and delivery**: taking an existing raster —
screenshot, photo, exported render — and making it fit its destination.

## Assess before enhancing

Record what you have and what the destination needs:

| Check | Ask |
|---|---|
| Resolution | enough pixels for the target (web, retina, slide, print)? |
| Sharpness | soft edges, camera blur, scaling artifacts? |
| Compression | JPEG ringing, banding, block noise? |
| Format | PNG for graphics and text, JPG for photographic size, target platform limits? |
| Colour | profile and bit depth appropriate to print or screen? |

Enhancement is for *existing* rasters. A design that must be sharper at a new size is
re-exported from its source (vector, canvas code, layered file) rather than upscaled —
upscaling interpolates, it does not recover detail.

## Enhance

- **Upscale** to the target dimension (2× for retina) with an edge-aware resampler, not
  naive bilinear interpolation.
- **Sharpen** edges conservatively; halos around text are worse than softness.
- **Reduce artifacts** first, sharpen second — sharpening amplifies compression noise.
- **Optimise** file size for the channel: PNG-8 where the palette is small, PNG-24 for
  gradients, JPG quality tuned to the visual tolerance.
- **Batch** a folder only when the images share a destination; assess each file.

Always keep the original: `name-original.*` beside `name-enhanced.*`.

## Export for the destination

| Destination | Minimum |
|---|---|
| Web / docs | 2× the displayed size, sRGB, compressed |
| Slide or large screen | match the deck's raster width, sRGB |
| Print | 300 DPI at final size, CMYK conversion by the print vendor |
| Social platform | the platform's prescribed dimensions, named explicitly |

For vector or code-drawn sources (poster from
[canvas-design.md](canvas-design.md), generative export from
[algorithmic-art.md](algorithmic-art.md)), re-render at the target size and only fall
back to upscaling when the source cannot be re-rendered.
