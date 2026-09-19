# Release process

The sole version source is `src/foresportia/_version.py`. Setuptools reads
`__version__` from that file for the distribution metadata through the dynamic
version configuration in `pyproject.toml`. Do not add a static project version.

For each release, in order:

1. Bump `__version__` in `src/foresportia/_version.py`.
2. Add the matching entry to `CHANGELOG.md`.
3. Commit the changes on `main`.
4. Install development dependencies and run `python -m pytest -q`.
5. Build with `python -m build` and run `python -m twine check dist/*`.
6. Validate the imported package version and the wheel and sdist metadata
   against the intended version. Confirm that version is absent from PyPI and
   the tag is absent from the remote.
7. Push the validated `main` commit without force, then create `v<version>`
   on that exact commit. Confirm `git rev-parse main` and
   `git rev-parse v<version>^{commit}` match.
8. Push only the new tag.
9. Wait for the publish workflow to pass and confirm the release on PyPI.

The publish workflow also refuses a tag that differs from `v` plus the
imported package version.
