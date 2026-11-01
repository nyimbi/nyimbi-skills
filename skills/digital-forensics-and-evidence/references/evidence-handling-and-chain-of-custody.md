# Evidence Handling and Chain of Custody

Purpose: the binding procedural rules that apply to every acquisition
this skill performs, regardless of media, platform, or tool.

## Rules that bind every acquisition

1. **Authority first.** No collection without written authorization
   naming systems, data categories, and date range. Open a legal hold
   before anything is deleted, reimaged, or returned to a user.
2. **Originals are sealed.** Write-block (hardware preferred; verified
   software acceptable — check the read-only flag, do not assume it).
   Every analysis runs on a verified copy. If the original must be
   imaged live, document why hardware blocking was impossible.
3. **Hash at every boundary.** SHA-256 of the source before imaging,
   of the image, and of the source after imaging — all three must
   match. Hash every parser input and output that will be cited.
4. **Volatile before stable.** Capture memory, network state, and
   running processes before shutdown or imaging. For the in-flight
   collection sequence during an active incident, see
   ../security-incident-response-and-soc/references/collecting-volatile-evidence-from-compromised-host.md.
5. **Custody never has a gap.** Every transfer of possession is
   recorded at the time it happens, not reconstructed later.
6. **Timestamps are declared.** Record timezone and clock offset for
   every source; normalize to UTC in the timeline and note skew.

## Chain-of-custody log (required fields)

| Field | Content |
|---|---|
| Item ID | Unique exhibit reference (case-scoped) |
| Description | Media/device/image, make, model, serial |
| Source | Location and system the item came from |
| Collected by / when (UTC) | Person and timestamp |
| Method | Tool + exact options (e.g., `dcfldd sha256=... hashwindow=1G`) |
| Write protection | Hardware blocker or software method, verification result |
| Hash | Algorithm + value; verification status |
| Storage | Sealed location or path, access controls |
| Transfers | Time, from, to, reason — for every hand-off |
| Analysis copies | Derived copies made, with their hashes |

## Platform-specific additions

| Evidence class | Extra requirements |
|---|---|
| Live disk / removable media | Confirm device identity (serial) before imaging; re-hash source after |
| Memory | Record acquisition tool and OS build; keep the dump read-only; symbol/ISF pack version recorded |
| Cloud | Snapshot or export before isolation where possible; log the API calls used — the audit log is itself evidence; account for multi-region and ephemeral resources ([performing-cloud-forensics-investigation](performing-cloud-forensics-investigation.md)) |
| Container / host | Capture image digest, layer history, and runtime state; export logs before teardown ([analyzing-docker-container-forensics](analyzing-docker-container-forensics.md)) |
| Mobile | Isolate immediately (Faraday/airplane mode) against remote wipe; photograph and record lock state before acquisition ([performing-mobile-device-forensics-with-cellebrite](performing-mobile-device-forensics-with-cellebrite.md)) |
| Remote / SaaS | Use API export plus local sync-client artifacts; record export scope, pagination completeness, and account ([performing-cloud-storage-forensic-acquisition](performing-cloud-storage-forensic-acquisition.md)) |

## Jurisdiction and privacy checks

- Confirm data residency and cross-border transfer limits before
  pulling cloud or SaaS evidence into the case store.
- Minimize irrelevant personal data; segregate and restrict access
  (need-to-know) once collected.
- Insider and HR matters: legal sign-off before covert collection;
  preserve before the subject's departure date.

## Pre-delivery checklist

- [ ] Authorization and legal hold on file, scope matches what was taken
- [ ] Write protection verified and recorded
- [ ] Source/image/source hashes match and are logged
- [ ] Custody log complete with no time gaps
- [ ] Analysis performed on copies only; originals untouched
- [ ] Timezone and clock skew recorded for every source
- [ ] Every cited finding traces to an item in the evidence index
