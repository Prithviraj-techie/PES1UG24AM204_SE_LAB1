# Lab 5: Static Code Analysis

## Student Details
- **Repository:** PES1UG24AM204_SE_LAB1
- **Module Under Review:** `radio_schedule.py`

---

## 1. Objective
To enhance Python code quality, security, and style by utilizing static analysis tools (**Bandit**, **Flake8**, and **Pylint**) to detect and rectify common programming issues in the assigned script.

---

## 2. Issue Tracking & Resolution Table

| Issue | Tool | Type | Line(s) (Before) | Description | Fix Approach |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **SQL Injection (B608)** | Bandit | Vulnerability (Medium/High) | 18, 41 | Dynamic f-string SQL query construction (`f"INSERT INTO slots ... VALUES ('{show}', ...)"` and `f"DELETE ... WHERE id = {slot_id}"`) allows arbitrary SQL injection. | Replaced f-strings with parameterized SQL statements using `?` placeholders and tuple parameters (`(show, host, start_hour, minutes)`). |
| **Insecure Assertion (B101)** | Bandit | Vulnerability / Bug | 13 | `assert 0 <= start_hour <= 23` can be disabled at runtime when Python is run with optimizations (`-O` flag), bypassing range checks. | Replaced `assert` with explicit control flow: `if not 0 <= start_hour <= 23: raise ValueError(...)`. |
| **Broad Exception & Silent Pass (B110 / W0702 / E722)** | Bandit / Pylint / Flake8 | Bug / Security | 56-57 | Bare `except:` catching `BaseException` and silently suppressing unexpected errors with `pass`. | Removed bare `except` and structured error handling with `try...finally` to ensure the SQLite connection is always closed cleanly. |
| **Mutable Default Argument (W0102)** | Pylint | Bug / Logic Defect | 9 | `def add_slot(..., logs=[])` binds `logs` at function definition time, causing list state to persist and leak across subsequent method calls. | Removed `logs=[]` from the function signature (or default to `None` and instantiate locally if optional logging is needed). |
| **Unused Import (F401 / W0611)** | Flake8 / Pylint | Style / Code Smells | 2 | `import os` is imported at module level but never referenced anywhere in the script. | Removed `import os`. |
| **Line Length & Spacing (E501 / E225 / E226)** | Flake8 | PEP 8 Formatting | 7, 15, 28-31 | `CREATE TABLE` query line exceeded 79 chars (158 chars); missing whitespace around arithmetic and assignment operators (`start=start_hour*60`). | Split multiline SQL into a readable block; formatted arithmetic and assignments with PEP 8 compliant spaces (`start = start_hour * 60`). |
| **Missing Docstrings (C0114 / C0115 / C0116)** | Pylint | Convention / Quality | 1, 4, 5, 9, 23, 27, 35, 40, 45, 48 | Missing docstrings across module, class `RadioSchedule`, and all member/static methods, reducing initial Pylint score to **2.41/10**. | Added comprehensive, descriptive PEP 257 docstrings for module, class, and all methods, raising score to **10.00/10**. |

---

## 3. Static Analysis Metrics (Before vs. After)

| Tool | Before Report | Before Status | After Report | After Status |
| :--- | :--- | :--- | :--- | :--- |
| **Bandit** | `bandit_report_before.txt` | 4 issues (2 Medium, 2 Low) | `bandit_report.txt` | **0 issues identified** |
| **Flake8** | `flake8_report_before.txt` | 11 PEP 8 violations | `flake8_report.txt` | **0 errors (clean exit)** |
| **Pylint** | `pylint_report_before.txt` | **2.41 / 10.00** | `pylint_report.txt` | **10.00 / 10.00** |

---

## 4. Summary of 3 Git Commits

1. **Commit 1 (Bandit Fixes)**: `fix(security): resolve Bandit issues (SQL injection, assertions, bare except)`
   - Replaced dynamic SQL strings with parameterized queries (`?`).
   - Replaced assertions with `ValueError`.
   - Replaced bare `except: pass` with `finally` block for connection closing.
2. **Commit 2 (Flake8 Fixes)**: `style: fix Flake8 PEP 8 formatting, line length, and spacing issues`
   - Removed unused `import os`.
   - Broken long SQL strings into multiline statements (< 79 characters).
   - Formatted binary operators with appropriate whitespace.
   - Enforced 2 blank lines between classes and top-level functions.
3. **Commit 3 (Pylint Fixes)**: `refactor: fix Pylint issues, remove mutable defaults, add docstrings (score 10/10), and complete lab report`
   - Removed mutable default argument `logs=[]` in `add_slot`.
   - Added complete PEP 257 docstrings across module, class, and methods.
   - Achieved Pylint rating of 10.00/10.

---

## 5. Answers to Reflection Questions

### Question 1: What are the distinct roles of Pylint, Bandit, and Flake8, and why is a multi-tool approach necessary?
- **Flake8:** Fast, lightweight syntax and style checker enforcing PEP 8 guidelines (whitespace, line length, indentation, unused imports). It does not inspect logic or security.
- **Bandit:** AST-based security vulnerability scanner focusing on Common Weakness Enumerations (CWEs) such as SQL injection, hardcoded secrets, and dangerous library usage.
- **Pylint:** Deep code inspection tool evaluating design quality, logic bugs (such as mutable default arguments), documentation compliance, and cyclomatic complexity.
- **Necessity:** No individual tool provides complete static analysis coverage. Flake8 misses SQL vulnerabilities; Bandit ignores style and docstrings; Pylint benefits from Bandit's specialized security heuristics. Together they establish defense-in-depth for Python codebases.

### Question 2: Why are mutable default arguments (e.g., `logs=[]`) dangerous in Python, and how does static analysis detect them?
- In Python, default parameter values are evaluated **once at function definition time**, not upon each call.
- When a mutable data structure (`list`, `dict`) is used as a default, all calls sharing that default reference the exact same memory object. Any mutation (`logs.append(...)`) leaks across subsequent invocations, creating unintended side effects.
- Pylint detects this via AST rule `W0102` (`dangerous-default-value`). The standard fix is using `logs=None` and initializing inside the method if needed.

### Question 3: How does SQL injection manifest in application code, and why are parameterized queries the only safe resolution?
- SQL injection happens when user input is concatenated directly into SQL command strings (e.g., using Python f-strings). An attacker can inject syntax characters like `' OR '1'='1` or `; DROP TABLE ...` to alter query semantics.
- Parameterized queries (`execute(query, params)`) decouple the SQL code from untrusted data at the database driver protocol layer. The engine compiles the query template first, and parameters are passed strictly as data literals, neutralizing injection risks completely.

### Question 4: What are the comparative advantages and limitations of static analysis versus dynamic testing?
- **Advantages:** Instantaneous execution, no dependencies/mocking required, 100% path coverage, and early detection of security vulnerabilities and antipatterns before runtime.
- **Limitations:** Cannot detect dynamic business logic bugs (e.g., code runs cleanly but calculates the wrong schedule time) or environment-specific runtime issues. Dynamic unit and integration testing remain essential alongside static analysis.
