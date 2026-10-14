# Reflection — Lab 5 Static Code Analysis

### 1. What is static code analysis, and how does it differ from dynamic testing?

Static code analysis inspects the **source code itself** without executing the
program. Tools parse the code (often into an abstract syntax tree) and apply
rules to flag bugs, style violations, and security patterns. In this lab,
Pylint, Bandit and Flake8 all examined `school_transport.py` without the
register ever running.

Dynamic testing, by contrast, runs the program with inputs and observes its
behaviour at runtime (unit tests, integration tests, manual execution). It can
catch logic errors that only surface on a particular input path, but it can only
find problems in code that the tests actually reach. They are complementary:
static analysis finds problems across *all* code paths up front; dynamic testing
confirms the code behaves correctly on the paths you exercise. I used both here —
the three static tools to find the issues, and running the program before and
after to confirm behaviour was preserved.

### 2. What types of issues did Pylint, Bandit, and Flake8 identify?

- **Pylint** found a mix of correctness and convention issues on the original
  (score 4.00/10): a bare `except` (`W0702`), an unused `driver` argument
  (`W0613`), opening a file without `with` / encoding (`R1732`, `W1514`),
  camelCase function names that violate PEP 8 (`C0103`), missing module and
  function docstrings (`C0114`, `C0116`), and over-long lines (`C0301`).
- **Bandit** found the security problems: **B602** *High* — `shell=True` in
  `subprocess.run` (OS-command injection), **B608** *Medium* — an `INSERT`
  built by f-string (SQL injection), **B101** *Low* — `assert` used for a
  runtime check, plus **B404** *Low* — the `subprocess` import itself.
- **Flake8** found pure PEP 8 style issues: over-long lines (`E501`), missing
  whitespace after commas (`E231`), and the bare `except` (`E722`).

So the three tools covered different layers: Bandit = security, Flake8 = style,
Pylint = a blend of correctness and convention.

### 3. Which issues were the most important to fix, and why?

The **security findings mattered most**, because they could let an attacker run
arbitrary commands or manipulate the database — the kind of defect that a
functional test would never reveal on normal data.

- **B602 `shell=True` (High)** was the worst: `dispatch_alert(route)` concatenated
  user-controlled `route` into a shell command, so a value like `R1; rm -rf /`
  or ``R1`malicious` `` would execute directly. This is a real, exploitable
  command-injection vector (CWE-78).
- **B608 SQL injection (Medium)**: building the `INSERT` with an f-string means a
  name containing a single quote (a perfectly plausible student name like
  `O'Brien`) could break the statement or inject SQL (CWE-89).
- **The bare `except:` (W0702/E722)** was the most important *reliability* fix:
  it silently swallowed every error and returned `0`, so a database failure would
  masquerade as "no fees collected" instead of being reported.
- **`assert` for a business check (B101)** was subtle but real: optimised bytecode
  (`python -O`) strips asserts, so the fee-total check would quietly vanish in
  production.

### 4. How did the fixes improve the code's quality, security, readability, or maintainability?

- **Security:** parameterised queries (`?` placeholders) and an argv list without
  a shell eliminate both injection vectors — untrusted data is now *data*, never
  parsed as code. Replacing the assert with an explicit `raise` keeps the
  invariant enforced even under `-O`. Bandit went from 1 High + 1 Medium to
  0 High + 0 Medium.
- **Quality/reliability:** catching `sqlite3.Error` (instead of every exception)
  and logging it means real failures are surfaced rather than hidden, while
  still returning a safe default.
- **Readability/maintainability:** renaming to `snake_case`, adding module and
  function docstrings, wrapping long lines, and using `with open(...)` brought
  Pylint from 4.00/10 to 10.00/10 and Flake8 to a clean run. Removing the dead
  `driver` parameter made the roster function's contract honest. None of these
  changed what the program *does* — its output is byte-for-byte the same — they
  only made the code safer and clearer.

### 5. What limitations does static analysis have?

- **It cannot see runtime behaviour.** It does not know that
  `fee_collected("R1")` actually returns `3600`, or that the register's logic is
  correct — only dynamic testing confirms that.
- **False positives / noise.** Bandit's **B404** simply flags *importing*
  `subprocess`, and **B603**/*B607* remain even though my call is safe (no shell,
  single argv element). These are advisories, not defects; blindly "fixing" them
  would mean deleting intended functionality.
- **False negatives.** Static tools miss issues that depend on data flow,
  configuration, or environment (race conditions, memory growth, logic bugs) and
  cannot reason about every path.
- **Rule/toolkit dependence.** Flake8's default line-length (79) differs from
  Pylint's (100), so the same file scores differently per tool; coverage depends
  on the rules you enable. It enforces *conventions*, not *correctness*.

### 6. How can static analysis contribute to software quality in a development team?

Run in CI/CD, static analysis gives **fast, cheap, objective feedback on every
commit** — catching an injection or a bare `except` at review time rather than in
production, where such bugs are expensive and dangerous. It enforces a consistent
style automatically (naming, docstrings, line length), so code reviews focus on
logic instead of formatting, and new team members inherit house standards without
manual policing. Because tools like Bandit map findings to CWEs, they raise
developer security awareness over time. The key is **triage, not zero-warning
dogma**: team leads should treat findings as signals — fixing the High/Medium
security issues here, documenting the remaining Low advisories with justification
rather than suppressing them — and pair static analysis with dynamic tests and
review for real coverage.
