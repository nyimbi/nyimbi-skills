# The deploy contract — a page shipping beyond `file://`

A page that only works over `file://` is not delivered. The contract below was written from four
failure classes found on one live deploy (2026-11-01): a CSP refusing same-origin frames, inlined
`data:` fonts refused by `font-src`, a blank canvas that was a missing import, and a baked board
overridden by an empty live store. Each rule names its origin.

1. **Smoke the deployed URL, never the local file.** Build, deploy, then probe the live ingress:
   every referenced asset gets a `curl -s -o /dev/null -w "%{http_code} %{content_type} %{size_download}"`,
   then a headless-browser render of the *deployed* page (fresh user-data-dir = cold cache). A green
   local run proves nothing about the vhost. "Probe the live ingress, not the route function."
2. **CSP: self-embedding needs `frame-ancestors 'self'`.** A vhost's global `frame-ancestors 'none'`
   refuses even same-origin iframes — both engine wells rendered as broken documents on an otherwise
   200 page. Fix shape: two **mutually exclusive** matcher directives (`@artifacts path /artifacts/*`,
   `@strict not path /artifacts/*`), because two same-path CSP headers append rather than replace and
   the browser intersects both. Verify both page classes with `curl -I`.
3. **Inline assets declare their scheme.** Pages that inline fonts as `data:` URIs need
   `font-src … data:`; video needs `media-src` (or `default-src 'self'` covering it). Enumerate what
   the page actually fetches — document it in the page's head — and check every scheme against the
   policy, including Google Fonts (`style-src https://fonts.googleapis.com` + `font-src
   https://fonts.gstatic.com`). A silent font fallback looks like a font choice, not a policy.
4. **Baked vs live state: the empty-store override.** A page booting baked data that *also* fetches a
   live store must define precedence: live overrides only when non-empty (`if (live.length)`), or the
   live store blanks the whole board while the baked page still shows the card in its HTML — the
   "reads clean in source, renders empty to the visitor" split-brain. State in a comment which store
   wins on each path; the baked copy is never the display of record once a live store exists.
5. **Blank canvas = a pageerror.** The most likely cause is a missing import or an uncaught
   constructor, not a rendering quirk. Gate: zero `pageerror` on the deployed page at default params
   and on one press/run-through — probe console and `window.onerror` from the embed, not the tab.
   Check `<html data-errors>` too where the page supports it.
6. **Iframe bands are measured, not guessed.** An embedded page's own breakpoints do not shrink with
   the frame: between its phone cutoff (≤560) and its comfortable desktop band (~700+) the layout can
   compress into collisions (stats over buttons at ~575×524; clean at 570×800 and 555×524). Before
   embedding, screenshot the page at four widths × two heights, pick the band it is designed for, and
   pin the embed there — recording the geometry and the *reason* in a CSS comment on the host page.
7. **Fullscreen is a click-gated API.** `requestFullscreen()` from a user gesture; phones and app
   views refuse it — catch rejection and say so inline once ("full screen runs in a normal browser
   tab"), then leave it. Provide a `:fullscreen` stylesheet for the target: the aspect-ratio box must
   not fight `width:100%; height:100%`.
8. **Hash is the only routing.** Only a plain `#name` survives a shared link; never `#/path`,
   `#k=v`, query strings or `pushState` (a vhost `try_files` 404s deep paths, the claude.ai frame
   drops everything but `#name`). Read state from `?press=`/`?yaw=` style params **once at load, as
   verification inputs, never as history** — the param surface is the page's screenshot contract.
9. **Film/video elements: controls + poster + muted autoplay posture.** `preload="metadata"`,
   `poster` always (the first frame of a video element is the poster), sound only after a user
   gesture. Gate on the deployed page: `video.readyState === 4` after wait + poster resolves.
10. **The encoded artifact is the deliverable.** Never report a film from the raw capture; the
    encoder wrote the truth — re-sheet the final file and read that sheet.