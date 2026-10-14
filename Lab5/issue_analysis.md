# Issue Analysis — Lab 5 Static Code Analysis

**Project:** `school_transport.py` (School Bus Transport Register)
**Tools:** Pylint 4.1.3 · Bandit 1.9.4 · Flake8 7.4.1 (Python 3.14)

> Note: The generic task template referenced `inventory_system.py`; the actual
> project file supplied by the lab repo (`SETAPESU26/L5_24_school_transport`)
> is `school_transport.py`. All findings below come from real runs of the three
> tools on that file. "Line(s)" refer to the **original** file
> (`school_transport_original.py`); the original reports are preserved as
> `*_report_original.txt`.

## Original findings summary

| Tool | Original result | Final result |
|------|-----------------|--------------|
| Pylint | **4.00/10** | **10.00/10** |
| Bandit | 1 High, 1 Medium, 2 Low | 0 High, 0 Medium, 3 Low (advisory) |
| Flake8 | 9 PEP8/style findings | 0 findings (clean) |

## Issue table

| Issue | Type/Tool | Line(s) | Description | Fix Approach | Status |
|-------|-----------|---------|-------------|--------------|--------|
| SQL injection via f-string | **Security** — Bandit **B608** (Medium) | 9 | `enrollRider` built the `INSERT` by interpolating `student`, `route`, `stop`, `fee` directly into the SQL string. Any value containing a quote could break out and inject SQL (CWE-89). | Replaced with a parameterised query using `?` placeholders: `conn.execute("INSERT ... VALUES (?, ?, ?, ?)", (student, route, stop, fee))`. Data is bound, never parsed as SQL. | **Fixed** |
| Command injection via `shell=True` | **Security** — Bandit **B602** (High), CWE-78 | 24 | `dispatchAlert` ran `subprocess.run("echo dispatching bus " + route, shell=True)`. The untrusted `route` was passed to a real shell, so a value like `R1; rm -rf /` would execute arbitrary commands. | Removed `shell=True` and switched to an argument list: `subprocess.run(["echo", "dispatching bus", route], check=False)`. No shell is spawned, so metacharacters in `route` are inert. | **Fixed** |
| Overly broad exception handler | **Code quality** — Pylint **W0702** / Flake8 **E722** | 30 | `feeCollected` used a bare `except:` that swallowed every exception (including `KeyboardInterrupt`/`SystemExit`) and silently returned `0`, hiding real failures. | Caught the specific `sqlite3.Error` and logged it with `logger.exception(...)` before returning `0`, so failures are visible and only the intended error class is handled. | **Fixed** |
| `assert` used for a runtime check | **Security/Reliability** — Bandit **B101** (Low), CWE-703 | 38 | `assert feeCollected("R1") == 3600` guards a business invariant, but asserts are stripped when Python runs optimised (`-O`), so the check silently disappears in production. | Replaced with an explicit `if ... != 3600: raise RuntimeError(...)`, which always executes regardless of optimisation flags. | **Fixed** |
| Unused function argument | **Code quality** — Pylint **W0613** | 13 | `routeRoster(route, driver)` accepted a `driver` parameter it never used (callers even passed `None`/`"Mr. Das"`). Dead parameter — confusing API. | Removed the `driver` parameter (`route_roster(route)`) and updated every call site. | **Fixed** |
| File opened without `with` / no encoding | **Code quality** — Pylint **R1732**, **W1514** | 18 | `exportRoster` used `open(...)`/`out.close()` manually; an exception mid-write would leak the file handle, and the text encoding was platform-dependent. | Used a context manager `with open(path, "w", encoding="utf-8") as out:` so the file is always closed and the encoding is explicit. | **Fixed** |
| Non-PEP8 function names (camelCase) | **Style** — Pylint **C0103**, Flake8 naming | 8,13,17,23,27 | Functions `enrollRider`, `routeRoster`, `exportRoster`, `dispatchAlert`, `feeCollected` used camelCase instead of PEP 8 `snake_case`. | Renamed to `enrol_rider`, `route_roster`, `export_roster`, `dispatch_alert`, `fee_collected` and updated all calls. | **Fixed** |
| Missing docstrings | **Style** — Pylint **C0114**, **C0116** | 1,8,13,17,23,27,34 | Module and every function lacked a docstring. | Added a module docstring and one-line docstrings for each function. | **Fixed** |
| Lines too long | **Style** — Pylint **C0301**, Flake8 **E501** | 5,9,14,29 | Several statements exceeded the line-length limit (up to 116 chars). | Wrapped long SQL/`CREATE` statements into implicit-concatenated literals and split call arguments across lines. | **Fixed** |
| Missing whitespace after commas | **Style** — Flake8 **E231** | 8 | `def enrollRider(student,route,stop,fee):` had no space after commas. | Reformatted the signature with spaces (part of the rename/reformat). | **Fixed** |
| Blank-line before top-level `def` | **Style** — Flake8 (E302 family) | 23 | Inconsistent blank lines between functions in the original. | Normalised to two blank lines between top-level definitions. | **Fixed** |
| `subprocess` import flagged | **Security (advisory)** — Bandit **B404** (Low) | 1 (now 9) | Bandit notes that importing `subprocess` *can* be risky. It is an informational blacklist, not an exploit. | **Kept** — the dispatch alert legitimately shells out to `echo`; the actual risk (B602) is removed. Removing `subprocess` would delete intended functionality just to silence a Low advisory. | **Remaining (justified)** |
| `subprocess` call + partial path | **Security (advisory)** — Bandit **B603**, **B607** (Low) | 50 | After the fix, Bandit still emits Low reminders: B603 "check untrusted input" and B607 "partial executable path" (`echo` has no directory). | **Kept** — these are inherent Low-severity notices for any safe `subprocess` use. `route` is passed as a single argv element (never reinterpreted by a shell), so it cannot inject commands. Hardcoding `/bin/echo` would be less portable for no real security gain. | **Remaining (justified)** |

## Result

Ten distinct genuine issues were fixed (4 of them security-relevant: B608, B602, B101 and the bare-except), clearing every **High** and **Medium** Bandit finding and reaching **Pylint 10.00/10** and a **clean Flake8** run, while the program still produces exactly the same output. The three remaining Bandit items are **Low** advisories tied to the legitimate, now-safe use of `subprocess`, explained above rather than suppressed.
