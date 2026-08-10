#!/usr/bin/env bash
set -euo pipefail

uv sync --locked --group dev

uv run ruff check tools tests
uv run pytest
uv run desys-metadata-validate --max-warnings 127
uv run desys-build-index --dry-run
uv run desys-build-index
uv run desys-check-indexes

repository_root="$(pwd)"
temporary_directory="$(mktemp -d)"
trap 'rm -rf "$temporary_directory"' EXIT

uv build --no-build-isolation --out-dir "$temporary_directory/dist"
uv venv --python 3.12 "$temporary_directory/venv"

wheels=("$temporary_directory"/dist/*.whl)
test "${#wheels[@]}" -eq 1

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
    "import tools.desys_metadata, tools.desys_indexer, tools.build_index, tools.init_project, tools.validate_metadata"
  "$temporary_directory/venv/bin/desys-project-init" --version
  "$temporary_directory/venv/bin/desys-metadata-validate" \
    --root "$repository_root" \
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
  "$temporary_directory/venv/bin/desys-project-init" \
    --root "$consumer_repository" \
    --dry-run
  "$temporary_directory/venv/bin/desys-project-init" \
    --root "$consumer_repository"
  "$temporary_directory/venv/bin/desys-project-init" \
    --root "$consumer_repository"
)
