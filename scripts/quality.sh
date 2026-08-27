#!/usr/bin/env bash
set -euo pipefail

test -s LICENSE

uv sync --locked --group dev

uv run ruff check tools tests scripts/platform-package-smoke.py
uv run pytest
uv run desys-corpus-inventory --check
uv run desys-corpus-bundle --check
uv run desys-metadata-validate --config tools/desys_indexer.yaml --max-warnings 127
uv run desys-build-index --dry-run
uv run desys-build-index
uv run desys-check-indexes

repository_root="$(pwd)"
temporary_directory="$(mktemp -d)"
trap 'rm -rf "$temporary_directory"' EXIT

uv build --sdist --no-build-isolation --out-dir "$temporary_directory/dist"
sdists=("$temporary_directory"/dist/*.tar.gz)
test "${#sdists[@]}" -eq 1
uv build --wheel --no-build-isolation --out-dir "$temporary_directory/dist" "${sdists[0]}"
uv venv --python 3.12 "$temporary_directory/venv"

wheels=("$temporary_directory"/dist/*.whl)
test "${#wheels[@]}" -eq 1

uv run python - "${wheels[0]}" <<'PY'
import hashlib
import stat
import sys
import zipfile

import yaml

prefix = "tools/reference_corpus_data/"
with zipfile.ZipFile(sys.argv[1]) as wheel:
    names = {item.filename for item in wheel.infolist() if item.filename.startswith(prefix)}
    bundle_bytes = wheel.read(f"{prefix}bundle.yaml")
    bundle = yaml.safe_load(bundle_bytes)
    entries = bundle["entries"]
    expected = {
        f"{prefix}__init__.py",
        f"{prefix}bundle.yaml",
        f"{prefix}compatibility.yaml",
        f"{prefix}contracts/compatibility-1.0.0.schema.json",
        f"{prefix}contracts/consumer-manifest-1.1.0.schema.json",
        f"{prefix}contracts/reference-bundle-1.1.0.schema.json",
        *(f"{prefix}corpus-files/{entry['target']}" for entry in entries),
    }
    assert len(entries) + 6 == len(expected), "Corpus bundle contains duplicate targets."
    assert names == expected, f"Wheel corpus resources differ: missing={sorted(expected - names)}, extra={sorted(names - expected)}"

    descriptor = {
        key: bundle[key]
        for key in (
            "bundle_schema",
            "inventory_schema",
            "corpus_version",
            "release_tag",
            "source_commit",
            "entries",
        )
    }
    descriptor_bytes = yaml.safe_dump(
        descriptor,
        sort_keys=False,
        allow_unicode=False,
        width=120,
    ).encode("utf-8")
    descriptor_checksum = f"sha256:{hashlib.sha256(descriptor_bytes).hexdigest()}"
    assert descriptor_checksum == bundle["bundle_checksum"], "Wheel bundle descriptor checksum differs."

    for entry in entries:
        member = f"{prefix}corpus-files/{entry['target']}"
        checksum = f"sha256:{hashlib.sha256(wheel.read(member)).hexdigest()}"
        assert checksum == entry["checksum"], f"Wheel corpus checksum differs: {member}"
    for name in expected:
        mode = stat.S_IMODE(wheel.getinfo(name).external_attr >> 16)
        assert mode & 0o111 == 0, f"Wheel corpus resource is executable: {name}"
PY

uv export \
  --locked \
  --no-dev \
  --no-emit-project \
  --format requirements.txt \
  --output-file "$temporary_directory/runtime-requirements.txt"

uv pip install \
  --python "$temporary_directory/venv/bin/python" \
  --require-hashes \
  --requirements "$temporary_directory/runtime-requirements.txt"
uv pip install \
  --python "$temporary_directory/venv/bin/python" \
  --no-deps \
  "${wheels[0]}"

(
  cd "$temporary_directory"
  "$temporary_directory/venv/bin/python" -c \
    "import tools.build_corpus_inventory, tools.desys_metadata, tools.desys_indexer, tools.build_index, tools.init_project, tools.validate_metadata"
  "$temporary_directory/venv/bin/desys-project-init" --version
  "$temporary_directory/venv/bin/desys-metadata-validate" \
    --root "$repository_root" \
    --config "$repository_root/tools/desys_indexer.yaml" \
    --max-warnings 127
  "$temporary_directory/venv/bin/desys-build-index" \
    --dry-run \
    --config "$repository_root/tools/desys_indexer.yaml"
  "$temporary_directory/venv/bin/desys-check-indexes" \
    --output "$repository_root/skills/generated"
  "$temporary_directory/venv/bin/desys-metadata-migrate" \
    --root "$repository_root"

  consumer_repository="$temporary_directory/consumer"
  mkdir "$consumer_repository"
  git init --quiet "$consumer_repository"
  printf '[project]\nname = "consumer"\nversion = "1.0.0"\nrequires-python = ">=3.14"\n' \
    > "$consumer_repository/pyproject.toml"
  printf 'consumer-owned-lockfile\n' > "$consumer_repository/uv.lock"
  mkdir "$consumer_repository/.venv"
  printf 'consumer-owned-environment\n' > "$consumer_repository/.venv/marker"
  cp "$consumer_repository/pyproject.toml" "$temporary_directory/expected-pyproject.toml"
  cp "$consumer_repository/uv.lock" "$temporary_directory/expected-uv.lock"
  mkdir -p "$consumer_repository/tools/vendor"
  cp "${wheels[0]}" "$consumer_repository/tools/vendor/"
  consumer_source="tools/vendor/$(basename "${wheels[0]}")"
  "$temporary_directory/venv/bin/desys-project-init" \
    --root "$consumer_repository" \
    --desys-source "$consumer_source" \
    --dry-run
  "$temporary_directory/venv/bin/desys-project-init" \
    --root "$consumer_repository" \
    --desys-source "$consumer_source"
  "$temporary_directory/venv/bin/desys-project-init" \
    --root "$consumer_repository" \
    --desys-source "$consumer_source"
  test ! -e "$consumer_repository/docs/desys/corpus-manifest.yaml"
  test ! -e "$consumer_repository/docs/desys/reference"
  "$temporary_directory/venv/bin/desys-project-init" \
    --root "$consumer_repository" \
    --desys-source "$consumer_source" \
    --with-reference-corpus \
    --dry-run
  "$temporary_directory/venv/bin/desys-project-init" \
    --root "$consumer_repository" \
    --desys-source "$consumer_source" \
    --with-reference-corpus
  "$temporary_directory/venv/bin/desys-project-init" \
    --root "$consumer_repository" \
    --desys-source "$consumer_source" \
    --with-reference-corpus
  test -s "$consumer_repository/docs/desys/LICENSE"
  test -s "$consumer_repository/docs/desys/THIRD_PARTY_NOTICES.md"
  test -s "$consumer_repository/docs/desys/corpus-manifest.yaml"
  "$temporary_directory/venv/bin/python" -c \
    'import sys, yaml; data = yaml.safe_load(open(sys.argv[1], encoding="utf-8")); assert data["manifest_schema"] == "1.1.0"; assert data["release_tag"] == "v0.2.0-alpha.1"; assert data["source_commit"] == "1ba18c126dc9adf035f64c0ca6eda75186e73b60"; assert len(data["entries"]) == 41' \
    "$consumer_repository/docs/desys/corpus-manifest.yaml"
  bash "$consumer_repository/scripts/desys-docs-quality.sh"
  "$temporary_directory/venv/bin/python" -c \
    'import json, sys; data = json.load(open(sys.argv[1], encoding="utf-8")); assert len(data["documents"]) == 24; assert all(item["path"].startswith("docs/desys/reference/") for item in data["documents"])' \
    "$consumer_repository/docs/generated/search-index.json"
  cmp "$consumer_repository/pyproject.toml" "$temporary_directory/expected-pyproject.toml"
  cmp "$consumer_repository/uv.lock" "$temporary_directory/expected-uv.lock"
  test "$(< "$consumer_repository/.venv/marker")" = "consumer-owned-environment"
)
