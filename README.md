# Synthetic release integration fixture

Disposable dummy software for bounded release integration tests. This is not a
Bumpkin product release and contains no Bumpkin implementation or provider setup.
Tags, releases, review comments and artifacts are synthetic test data.

Run the tiny standard-library test suite:

```sh
PYTHONPATH=src python3 -m unittest discover -s tests -v
```

The build workflow produces a small ZIP and evidence for an exact source SHA.
The approval workflow records an environment review and probes its job token's
permissions. It does not execute the private release engine or publish software.
Build artifacts have one-day retention. No model services, caches or secrets are
configured in these workflows.
