# Releasing

SciEng Formulary is published to PyPI as `sciengformulary` by the
[`release`](.github/workflows/release.yml) workflow, using PyPI Trusted Publishing
(GitHub OIDC). No PyPI API token is stored in the repository.

**Pushing a tag alone does not publish.** The workflow runs only when a GitHub Release
is *published*. Pushes to `main`, pull requests, and tag pushes never publish.

## Steps

1. Merge the formula and catalog work into `main`.
2. Confirm the `validate-catalog` check passes on `main`.
3. Confirm the `package-check` check passes on `main`.
4. Set the release version in `src/sciengformulary/__init__.py` (`__version__`, for
   example `0.1.0`). The build reads the version from there; CI never edits it.
5. Commit that change and merge it into `main`.
6. Tag the intended `main` commit with `vX.Y.Z` matching the version exactly (for
   example `v0.1.0`), and push the tag. Nothing is published yet.
7. On GitHub, create a release from that tag.
8. Review the release notes.
9. Click **Publish release**.
10. `release.yml` then:
    - checks that the tag has the form `vX.Y.Z` and equals the package version;
    - builds the sdist and wheel from the tagged commit;
    - runs `twine check --strict`;
    - installs the wheel into a clean environment and runs the smoke test and
      `python -m sciengformulary.validation`;
    - publishes exactly those verified files to PyPI from the `pypi` environment.

If any check fails, nothing is published. Fix the problem on `main`, then delete the
unpublished GitHub release and its tag and start again from step 4 (the tag must point
at the fixed commit).

## Never overwrite a version

PyPI does not allow a file for an existing version to be replaced, and this project
does not try to. If a version is published with a mistake, for example `0.1.0`, release
the correction under a new version such as `0.1.1`. Yanking the broken version on PyPI
is optional; deleting it does not free the version number for reuse.

## One-time setup (before the first release)

These are done by a maintainer in the web interfaces; nothing in the repository can do
them.

1. **PyPI.** In the PyPI account, add a *pending* Trusted Publisher (the project does
   not exist yet before the first upload):
   - PyPI project name: `sciengformulary`
   - Owner: `2ssunny`
   - Repository name: `sciengformulary`
   - Workflow name: `release.yml`
   - Environment name: `pypi`
2. **GitHub.** In the repository settings, create an environment named `pypi`.
   Optionally add required reviewers so a person approves each publish, and restrict
   it to tags matching `v*`.
3. **Branch protection.** After the workflows have run once, mark `validate-catalog`
   and `package-check` as required status checks for `main`.
