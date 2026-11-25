# Mole Review

Reviewed 2026-11-02: <https://github.com/tw93/mole>, GPL-3.0, 73k+ stars, macOS 12+.

Mole is a mature open-source CLI (`mo`) for deep cleaning, uninstalling apps, optimizing
services, analyzing disk usage, purging project artifacts, and live status. The review
was behavioural: no GPL code was copied into this MIT-licensed bundle. The ideas below
are reimplemented independently.

## What Mole does well

- **Dry-run first** for every destructive command.
- **Path validation** and protection of shared/system-owned locations; refuses when it
  cannot prove an item is safe.
- **Process guards**: skips caches of running apps, Xcode, simulators, and active
  project builds.
- **Whitelist** (`~/.config/mole/whitelist`) for caches and optimization rules; stops if
  the whitelist cannot be read.
- **Operation log** with history (`mo history`), so every deletion has a record.
- **Trash routing** for uninstall/analyze/slim; clean/purge/installer delete permanently
  after confirmation.
- **Project artifact purge** with registered roots, `CACHEDIR.TAG`, git-tracked checks,
  and cloud-sync exclusions.
- **Installer cleanup** and **app leftover** detection with installed-app inventory.
- **System optimization** as explicit tasks: DNS refresh, QuickLook cache, Spotlight
  reindex, periodic maintenance, with skip reasons.
- **Disk analyzer** and **status dashboard**: large files, directory drill-down, CPU,
  memory, disk I/O, network.

## What this skill adopted

- Read-only audit and explicit plan before any change.
- Per-category apply, dry-run default, `--yes` confirmation.
- Whitelist at `~/.config/mac-maintenance/whitelist`.
- Process guards for Xcode, Simulator, and Docker.
- Project artifact purge under registered roots only.
- Installer and old-Downloads quarantine.
- Operation log at `~/.mac-maintenance/changes.log`.
- Backup before power-setting changes.
- Human-readable report with sizes, risk, and skip reasons.

## What this skill rejected

- **GPL code**: incompatible with this bundle's MIT licensing; no source copied.
- **`mo uninstall`**: app removal plus leftovers is powerful but too broad for an
  always-available maintenance skill; it needs a dedicated uninstall workflow.
- **`mo slim`**: stripping Intel slices from universal apps can break Rosetta, code
  signatures, and updates. Not a routine maintenance action.
- **Automatic DNS flush / Spotlight reindex / periodic scripts**: low value, brief
  disruption, and often used as a placebo. Manual-only in this skill.
- **System cache cleaning with sudo**: risk outweighs the space.
- **Permanent deletion as the default**: this skill quarantines user files.
- **Force-empty Trash by default**: `trash-empty` exists but is explicit and irreversible.
- **`docker system prune -a --volumes`**: can delete images and data volumes; this skill
  uses `docker system prune -f` only.
- **`sudo purge`**: rejected as a memory routine.

## Licensing note

Mole is GPL-3.0. This skill is an independent implementation of maintenance concepts and
does not include Mole code, scripts, templates, or assets. If Mole itself is installed,
use `mo clean --dry-run` and review its output; it is a separate tool with its own
licence and safety model.
