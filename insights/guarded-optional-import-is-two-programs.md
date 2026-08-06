# A Guarded Optional Import Ships Two Programs, and You Test One

```python
try:
    import yaml
    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False
```

This reads as defensive, and it is. It is also a **fork**. From that line the module is two programs, and a test suite run on a machine that has the package exercises exactly one of them. The other ships to users and is never executed by anyone in a position to notice it is wrong.

## The Finding

Guarding an import guarantees the module will not crash without the dependency. It guarantees nothing about whether the module will be *correct* without it. Those are different properties, and the guard only delivers the first.

A concrete case. A frontmatter-validation hook parsed YAML with the library when present and fell back to a hand-rolled line parser when absent. The fallback matched any line containing a colon, regardless of indentation, and so produced a flat dictionary in which a nested key silently overwrote a top-level key of the same name. Given

```yaml
type: reference          # top level, valid
metadata:
  type: not-a-valid-type # nested
```

the fallback resolved `type` to the nested value, and the hook emitted **"Invalid type" about a file whose type was valid**. A false positive on correct input, in the configuration with the fewest dependencies, which is the configuration a new adopter is most likely to be in.

The correct precedence rule already existed in that module, in a documented helper, fully written. It was only ever called from the library path. **The two parsers disagreed about the schema they were both supposed to be reading, and only one of them was under test.**

## How It Surfaced

Not by review. By a continuous-integration runner that happened not to have the package installed, failing four tests months after the fallback shipped.

Before that run, the import had been inspected directly and judged safe. The reasoning was "it is guarded, therefore it cannot break." That statement is true about the *import* and false about the *behaviour*, and the distinction is invisible unless you deliberately go looking for it.

## The Rule

**Every optional dependency needs the suite run without it, not only with it.** In continuous integration that is a second job or a second run, and it costs about a minute.

The second run needs a guard step that proves the intended configuration is actually in effect. Uninstalling a package and then running the suite is not enough: if the uninstall silently fails, or a transitive dependency reinstalls it, the "without" run quietly becomes a duplicate of the "with" run and reports green for a path it never touched. Assert the absence, then run.

```yaml
- name: suite (minimal, no optional deps)
  run: |
    pip uninstall -y -q SomePackage || true
    python -c "
    try:
        import somepackage; raise SystemExit('present: this job must run without it')
    except ImportError:
        print('confirmed: absent, minimal configuration')"
    pytest -q
```

## Corollaries

- **When a fallback and a primary parse the same format, make them share the interpretation rule** rather than reimplementing it. Two implementations of one schema is two schemas, and they will diverge in the direction nobody is watching.
- **A test asserting behaviour that is documented as unavailable without the package should skip there, not fail.** A red suite would report a supported configuration as broken, which trains people to ignore it.
- Reproducing a missing package locally is possible with a `sys.meta_path` finder that raises on the name. Use `find_spec`; the older `find_module` API is ignored on modern Python and your blocker will silently do nothing, which is the second-order trap described in [A Gate That Cannot Fail Is Not a Gate](a-gate-that-cannot-fail-is-not-a-gate.md).

## The Broader Pattern

Any branch that only one environment can reach is untested by construction, not by oversight. Optional imports are the most common instance because the language makes them a two-line idiom, but the class also covers platform branches, feature flags read from the environment, and error paths that require a failure the suite never induces.

The general form: **a conditional whose condition is a property of the machine, rather than of the input, splits your program into as many programs as there are machines.** Test each one, or ship the ones you did not.

## Related

- [Running CI's Steps Locally Is Not Running CI](running-ci-steps-locally-is-not-running-ci.md), the same failure at the level of the environment rather than the branch
- [A Gate That Cannot Fail Is Not a Gate](a-gate-that-cannot-fail-is-not-a-gate.md), checks that pass while checking nothing
- [Rubber-Stamp Enforcement Gaps](rubber-stamp-enforcement.md), the output-versus-action version of the same confusion
