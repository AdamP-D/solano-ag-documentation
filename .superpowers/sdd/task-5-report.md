# Task 5 Report: build_site.py

## Test Command

```
cd "C:/Projects/Solano/Ag/Documentation" && "C:/Program Files/ArcGIS/Pro/bin/Python/envs/arcgispro-py3/python.exe" tooling/tests/test_build_site.py
```

## Full Test Output

```
C:\Projects\Solano\Ag\Documentation\tooling\tests\test_build_site.py:11: ResourceWarning: unclosed file
<_io.TextIOWrapper name='...\knowledge-base.md' mode='w' encoding='utf-8'>
  open(os.path.join(c, "knowledge-base.md"), "w", encoding="utf-8").write(
ResourceWarning: Enable tracemalloc to get the object allocation traceback
C:\Projects\Solano\Ag\Documentation\tooling\tests\test_build_site.py:13: ResourceWarning: unclosed file
<_io.TextIOWrapper name='...\requirements.md' mode='w' encoding='utf-8'>
  open(os.path.join(c, "requirements.md"), "w", encoding="utf-8").write(
ResourceWarning: Enable tracemalloc to get the object allocation traceback
C:\Projects\Solano\Ag\Documentation\tooling\tests\test_build_site.py:26: ResourceWarning: unclosed file
<_io.TextIOWrapper name='...\search-index.json' mode='r' encoding='utf-8'>
  idx = json.load(open(os.path.join(self.out, "search-index.json"), encoding="utf-8"))
ResourceWarning: Enable tracemalloc to get the object allocation traceback
C:\Projects\Solano\Ag\Documentation\tooling\tests\test_build_site.py:28: ResourceWarning: unclosed file
<_io.TextIOWrapper name='...\index.html' mode='r' encoding='utf-8'>
  html = open(os.path.join(self.out, "index.html"), encoding="utf-8").read()
ResourceWarning: Enable tracemalloc to get the object allocation traceback
..
----------------------------------------------------------------------
Ran 2 tests in 0.083s
OK
```

**Result: 2 tests passed, 0 failures.**

Note: ResourceWarnings are from unclosed file handles in the brief's exact test setUp code (not in build_site.py). The build_site.py implementation uses context managers (with open(...)) as required. These warnings do not affect test results.

## Commit Hash

4d47e38

## Files Created

- `tooling/build_site.py` — static site generator (discover, build, APP_TITLES, DOC_TITLES)
- `tooling/tests/test_build_site.py` — unittest (TestBuildSite with 2 tests)

---

## Fix Run — 2026-07-01

### Changes Applied
- Fix 1 (resource safety): context managers already present; no change needed.
- Fix 2 (search quality): removed `-` from `[#*`|>_-]+` regex in `_plain_text` → `[#*`|>_]+` so hyphenated terms survive into the search index.

### Test Command
```
cd "/c/Projects/Solano/Ag/Documentation" && "/c/Program Files/ArcGIS/Pro/bin/Python/envs/arcgispro-py3/python.exe" tooling/tests/test_build_site.py
```

### Test Output
```
----------------------------------------------------------------------
Ran 2 tests in 0.020s
OK
```

**Result: 2 tests passed, 0 failures.**

### Commit Hash
f59961e
