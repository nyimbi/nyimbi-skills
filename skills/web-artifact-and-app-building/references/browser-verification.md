# Browser Verification with Playwright

Verification detail for step 6 of the [SKILL.md](../SKILL.md) workflow. Scripts and
examples live in `../scripts/webapp-testing/`. This is the verification half of web
artifact building: an artifact that has not been rendered and clicked is a proposal,
not a deliverable.

**Black-box rule:** run scripts with `--help` first and invoke them directly. Do not
read `with_server.py` (or any large helper) into context — use it as a command.

## Approach selection

```
task → static HTML file?
        yes → read the file to find selectors → write Playwright script against file://
              (fails or selectors stale → fall through to dynamic flow)
        no  → server already running?
                no  → start it with with_server.py, then run the script
                yes → reconnaissance-then-action (below)
```

## Serve then test

```bash
# single server
python scripts/webapp-testing/with_server.py --server "npm run dev" --port 5173 \
  -- python verify.py

# backend + frontend together
python scripts/webapp-testing/with_server.py \
  --server "cd backend && python server.py" --port 3000 \
  --server "cd frontend && npm run dev" --port 5173 \
  -- python verify.py
```

The helper polls each port until ready (30s default, `--timeout` to change), runs your
command, then tears the servers down. Your script therefore contains **only** Playwright
logic — no startup, no sleep loops, no cleanup.

## The script skeleton

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto('http://localhost:5173')
    page.wait_for_load_state('networkidle')   # CRITICAL: let JS settle first
    # ... verification logic ...
    browser.close()
```

## Reconnaissance-then-action

Never act on guessed selectors in a dynamic app:

1. `page.screenshot(path='/tmp/inspect.png', full_page=True)` and `page.content()`
2. Enumerate candidates — `page.locator('button').all()`
3. Identify stable selectors (`role=`, `text=`, id, CSS)
4. Act on the discovered selectors, then re-screenshot to confirm the change

**The classic failure:** inspecting the DOM before `networkidle` on a dynamic app and
concluding the component is missing when it simply has not mounted.

## What to verify for an artifact

| Check | How |
|---|---|
| Renders with no console errors | capture console output during the run |
| Primary flow works | click through the main interaction — not just page load |
| Bundle loads standalone | open the delivered `bundle.html` over `file://`, no dev server |
| Responsive | set a mobile viewport, screenshot, look for clipping |
| Keyboard/focus | Tab through interactive controls; focus ring visible |
| Visual result | full-page screenshot reviewed as an image — a picture beats re-reading the DOM |

Always close the browser; prefer `sync_playwright()`; add explicit waits
(`wait_for_selector`, `wait_for_timeout`) where `networkidle` is not enough.

## Runnable examples

- `../scripts/webapp-testing/examples/element_discovery.py` — finding buttons, links,
  and inputs on a rendered page
- `../scripts/webapp-testing/examples/static_html_automation.py` — driving a local HTML
  file over `file://`
- `../scripts/webapp-testing/examples/console_logging.py` — capturing console logs
  during automation (use this for the no-console-errors gate)
