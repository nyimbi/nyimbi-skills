# React Project Setup and Single-File Bundling

Operational detail for steps 3–5 of the [SKILL.md](../SKILL.md) workflow. Scripts live
in `../scripts/web-artifacts-builder/`. Run every script with `--help` or from the
documented invocation below; do not read their source into context unless
customisation is genuinely required.

## Scaffold — `init-artifact.sh`

```bash
bash scripts/web-artifacts-builder/init-artifact.sh <project-name>
cd <project-name>
pnpm dev
```

Requires Node 18+ (the script detects the major version, pins Vite `5.4.11` on Node 18,
uses latest on Node 20+, installs `pnpm` if missing, and handles macOS/Linux `sed`
differences). It creates a React 18 + TypeScript Vite project and then configures:

| Provided | Detail |
|---|---|
| Tailwind CSS 3.4.1 | `postcss.config.js`, `tailwind.config.js` with the shadcn token set, dark-mode `class` strategy |
| Design tokens | `src/index.css` with `--background`, `--primary`, `--radius` etc. for light and dark |
| Path alias | `@/*` in `tsconfig.json`, `tsconfig.app.json`, and `vite.config.ts` |
| Components | `shadcn-components.tar.gz` extracted into `src/` — 40+ components |
| Radix + friends | all Radix primitives, `sonner`, `cmdk`, `vaul`, `embla`, `react-day-picker`, `react-resizable-panels`, `react-hook-form`, `zod` |
| `components.json` | shadcn config for reference and future `shadcn add` calls |
| Bundler config | `.parcelrc` with tspaths resolution, added at bundle time |

**Dev loop:** `pnpm dev` (Vite HMR on the usual port) → edit `src/` → import
components as `import { Button } from '@/components/ui/button'`.

## Bundle — `bundle-artifact.sh`

```bash
bash scripts/web-artifacts-builder/bundle-artifact.sh
# → bundle.html
```

Preconditions: run from the project root; `package.json` and a root `index.html` must
exist. What it does:

1. Installs `parcel`, `@parcel/config-default`, `parcel-resolver-tspaths`, `html-inline`
2. Writes `.parcelrc` with the tspaths resolver if absent
3. Clears `dist/` and any previous `bundle.html`
4. `parcel build index.html --dist-dir dist --no-source-maps`
5. `html-inline dist/index.html > bundle.html`

`bundle.html` is fully self-contained — all JS, CSS, and assets inlined. It opens from
`file://`, drops into a chat as an artifact, and can be sent as a file. Confirm it
loads and runs before handing it over:
[browser-verification.md](browser-verification.md).

## Troubleshooting

| Symptom | Fix |
|---|---|
| `No package.json found` | run the script from the project root, not `scripts/` |
| `No index.html found in project root` | Vite's entry must be at root; don't move it into `src/` |
| Blank page in `bundle.html` | usually a runtime error — verify in a browser and read the console ([browser-verification.md](browser-verification.md)) |
| `@/` imports fail at bundle time | `.parcelrc` with `parcel-resolver-tspaths` is what resolves them; let the script write it |
| Asset missing after bundling | only assets reachable from the import graph are inlined — check the import, not the file |
| Port already in use on `pnpm dev` | stop the stale process or take the port Vite offers |

## When not to use these scripts

Static single-file artifacts and the p5.js viewer template need neither script — see
[architecture-selection.md](architecture-selection.md). Scripts are only for the
React branch.
