# Implementing Fuzz Testing In CICD With Aflplusplus

## API Reference

## Libraries Used
- **subprocess**: Execute AFL++ toolchain commands (afl-clang-fast, afl-fuzz, afl-cmin)
- **pathlib**: File system operations for corpus and crash management

## CLI Interface

```
python agent.py compile --source target.c --output target_fuzz [--compiler afl-clang-fast]
python agent.py fuzz --binary ./target_fuzz --input seeds/ --output findings/ [--duration 300]
python agent.py triage --binary ./target_fuzz --crashes-dir findings/default/crashes/
python agent.py stats --stats-file findings/default/fuzzer_stats
```

## Core Functions

### `compile_target(source_file, output_binary, compiler)`
Compiles target with AFL++ instrumentation. Sets `AFL_HARDEN=1` for memory sanitizers.

### `run_fuzzer(binary, input_dir, output_dir, duration_seconds, memory_limit)`
Runs `afl-fuzz` with headless mode (`AFL_NO_UI=1`), time-limited (`-V` flag).

**Environment Variables Set:**
| Variable | Value | Purpose |
|----------|-------|---------|
| `AFL_SKIP_CPUFREQ` | 1 | Skip CPU frequency check (CI/CD) |
| `AFL_NO_UI` | 1 | Headless mode for CI environments |
| `AFL_I_DONT_CARE_ABOUT_MISSING_CRASHES` | 1 | Continue on crash dir issues |

### `parse_fuzzer_stats(stats_file)`
Parses AFL++ `fuzzer_stats` file. Key metrics: `execs_per_sec`, `paths_total`, `saved_crashes`, `bitmap_cvg`.

### `triage_crashes(binary, crashes_dir)`
Re-runs crash inputs through the binary and classifies by signal (SIGSEGV, SIGABRT, etc.).

### `minimize_corpus(binary, input_dir, output_dir, timeout)`
Runs `afl-cmin` to remove redundant seeds from the corpus.

## AFL++ Commands Used

| Command | Purpose |
|---------|---------|
| `afl-clang-fast` | Compile with LLVM-based instrumentation |
| `afl-fuzz -i <in> -o <out> -- <binary>` | Main fuzzing loop |
| `afl-cmin -i <in> -o <out> -- <binary>` | Corpus minimization |
| `afl-tmin -i <crash> -o <min> -- <binary>` | Test case minimization |

## Dependencies
AFL++ must be installed: `apt install aflplusplus` or build from source.
```
pip install  # No Python packages needed beyond stdlib
```

---

## Standards and Controls

## NIST SP 800-53 Rev 5 Controls

| Control | Description | Fuzzing Alignment |
|---------|-------------|-------------------|
| SA-11(5) | Penetration Testing | Fuzz testing discovers vulnerabilities through automated input mutation |
| SA-11(8) | Dynamic Code Analysis | AFL++ provides runtime analysis with instrumented binaries |
| SI-10 | Information Input Validation | Fuzzing validates input handling robustness |
| SI-17 | Fail-Safe Procedures | Crash detection ensures failures are handled safely |

## OWASP Testing Guide v4.2

- **WSTG-INPV-07**: Testing for Input Validation --- AFL++ systematically tests boundary conditions
- **WSTG-ERRH-01**: Error Handling --- Crash analysis reveals improper error handling

## CWE Categories Commonly Found by Fuzzing

| CWE | Name | AFL++ Detection Method |
|-----|------|----------------------|
| CWE-120 | Buffer Overflow | ASan crash on out-of-bounds write |
| CWE-125 | Out-of-Bounds Read | ASan crash on invalid read |
| CWE-416 | Use After Free | ASan detects freed memory access |
| CWE-476 | NULL Pointer Dereference | SIGSEGV on null deref |
| CWE-190 | Integer Overflow | UBSan detects arithmetic overflow |
| CWE-787 | Out-of-Bounds Write | ASan detects heap/stack buffer overflow |
| CWE-400 | Uncontrolled Resource Consumption | Timeout detection for hangs |

## Fuzzing Maturity Levels

| Level | Description | CI Integration |
|-------|-------------|----------------|
| 1 Basic | Manual ad-hoc fuzzing | None |
| 2 Structured | Harness-based with corpus management | PR-triggered short runs |
| 3 Continuous | Nightly campaigns with crash tracking | Nightly + corpus caching |
| 4 Optimized | Multi-tool (AFL++, libFuzzer), crash dedup, coverage tracking | Full CI/CD integration with gating |

---

## Workflows

## Workflow 1: CI Pipeline Integration

```
Code pushed to branch
       |
Fuzzing harness compiled with afl-clang-fast + ASan
       |
Corpus restored from CI cache
       |
AFL++ runs in secondary mode for fixed duration
       |
[No crashes] --> Corpus updated in cache, pipeline passes
[Crashes found] --> Pipeline fails, crash artifacts uploaded
       |
Developer triages crashes
       |
Fix applied, re-run confirms no regression
```

## Workflow 2: Nightly Fuzzing Campaign

```
Scheduled nightly trigger (cron)
       |
Build instrumented binary + CmpLog binary
       |
Restore merged corpus from last run
       |
Launch parallel AFL++ instances (nproc count)
       |
Run for 4-8 hours
       |
Collect results from all instances
       |
afl-cmin merges and minimizes corpus
       |
Deduplicate crashes by stack hash
       |
New crashes create Jira/GitHub issues automatically
       |
Updated corpus cached for next run
```

## Workflow 3: Crash Triage and Fix

```
Crash file identified in findings/
       |
Reproduce crash with ASan-instrumented binary
       |
Capture ASan stack trace and error type
       |
Minimize crash input with afl-tmin
       |
Identify root cause from stack trace
       |
Develop fix and add crash input as regression test
       |
Verify fix by re-running AFL++ with crash input
       |
Update corpus to include edge case inputs
```

---

## Working Template

## Target Application

| Field | Value |
|-------|-------|
| Application Name | |
| Target Function | |
| Language | [ ] C [ ] C++ [ ] Other |
| Input Type | [ ] File [ ] Network [ ] Stdin |

## Fuzzing Configuration

| Parameter | Value |
|-----------|-------|
| Instrumentation | [ ] afl-clang-fast [ ] afl-gcc-fast [ ] QEMU |
| Sanitizer | [ ] ASan [ ] UBSan [ ] MSan [ ] TSan |
| Mode | [ ] Persistent [ ] Fork |
| CmpLog | [ ] Enabled [ ] Disabled |
| Timeout per exec | ms |
| CI run duration | minutes |
| Nightly duration | hours |

## Corpus Management

| Item | Location |
|------|----------|
| Seed corpus | |
| Minimized corpus | |
| CI cache key | |

## Crash Tracking

| Crash ID | CWE | Severity | Crash File | Stack Trace Summary | Fix Status |
|----------|-----|----------|------------|---------------------|------------|
| | | | | | |
