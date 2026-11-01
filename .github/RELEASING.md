# Release automation

## Preview packages

Each push to a pull request branch in this repository builds and tests one wheel. A separate
default-branch workflow validates that the artifact is named `graftql` and has a PEP 440
development version ending in `.dev<workflow-run-id>` before publishing it.

Fork pull requests are intentionally excluded from publishing. They continue to run the normal CI
workflow without receiving package-publishing permissions.

One-time repository setup:

1. Create a GitHub environment named `pypi-prerelease`. It does not need secrets.
2. In the `graftql` project settings on PyPI, add a GitHub Actions trusted publisher with:
   - Owner: `lorrod`
   - Repository: `graftql`
   - Workflow: `preview-publish.yml`
   - Environment: `pypi-prerelease`

Do not add a PyPI API token to GitHub. Both stable and preview publishing use short-lived OIDC
credentials.

The exact installation command is written to the preview workflow summary. Normal
`pip install graftql` ignores development releases; testing a preview requires an exact version,
for example:

```bash
pip install "graftql==2.0.5.dev123456"
```

## Stable packages

Every pull request merged into `main` increments the patch component of the latest stable tag,
builds and tests that version, creates an annotated tag, and publishes the package through the
existing `pypi` environment. The release workflow is serialized so concurrent merges cannot
allocate the same tag. Direct pushes to `main` do not create releases.
