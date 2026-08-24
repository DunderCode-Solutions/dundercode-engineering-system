# Changelog

All notable changes to DESys are documented in this file.

## [0.1.0-alpha.2] - 2026-08-24

### Fixed

- Restored the complete MIT License text and copyright notice in `LICENSE`.
- Added a quality-gate check that prevents packaging when `LICENSE` is empty.

### Compatibility

- Runtime behavior and the consumer scaffold are unchanged from
  `v0.1.0-alpha.1`.
- Consumers should use `v0.1.0-alpha.2` because the previous release artifact
  carried an empty license file.

## [0.1.0-alpha.1] - 2026-08-21

### Added

- Canonical YAML metadata validation for DEKG documents.
- Deterministic documentation indexes, graph, navigation, aliases, and search
  artifacts.
- Isolated consumer tooling through Python 3.12 and `uvx`.
- Non-destructive `desys-project-init` scaffolding.
- Vendor-neutral `AGENTS.md` documentation instructions.
- Local and GitHub Actions documentation quality gates.
- Pytest coverage for metadata, indexing, packaging, and project initialization.
- Branch-independent consumer push workflows.
- Explicit schema v1 English-prose guidance and generated-artifact ignore notes.

### Validation

- Pilot A documentation scenarios and AI-agent regression scenarios.
- Pilot B populated-runtime, lockfile, application-test, and CI scenarios.
- Isolated wheel execution with cold and warm cache measurements.
- Governed baseline of 127 legacy warnings and zero metadata errors.
