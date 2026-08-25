"""Build the sdist-derived wheel and smoke-test it outside the checkout."""

from __future__ import annotations

import os
import subprocess
import tempfile
import tomllib
from pathlib import Path


def run(*command: str, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, cwd=cwd, check=True, text=True, capture_output=True)


def main() -> None:
    repository_root = Path.cwd().resolve()
    project = tomllib.loads((repository_root / "pyproject.toml").read_text(encoding="utf-8"))["project"]
    expected_version = project["version"]
    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        artifacts = root / "dist"
        run("uv", "build", "--sdist", "--no-build-isolation", "--out-dir", str(artifacts))
        sdists = tuple(artifacts.glob("*.tar.gz"))
        if len(sdists) != 1:
            raise RuntimeError(f"Expected one source distribution, found {len(sdists)}.")
        run(
            "uv",
            "build",
            "--wheel",
            "--no-build-isolation",
            "--out-dir",
            str(artifacts),
            str(sdists[0]),
        )
        wheels = tuple(artifacts.glob("*.whl"))
        if len(wheels) != 1:
            raise RuntimeError(f"Expected one wheel, found {len(wheels)}.")

        environment = root / "venv"
        run("uv", "venv", "--python", "3.12", str(environment))
        python = environment / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
        run("uv", "pip", "install", "--python", str(python), str(wheels[0]))
        probe = (
            "from importlib.metadata import version; "
            "from tools.corpus_resources import load_reference_bundle; "
            f"assert version({project['name']!r}) == {expected_version!r}; "
            "assert len(load_reference_bundle().entries) == 41"
        )
        run(str(python), "-c", probe, cwd=root)
        executable = environment / (
            "Scripts/desys-project-init.exe" if os.name == "nt" else "bin/desys-project-init"
        )
        result = run(str(executable), "--version", cwd=root)
        if result.stdout.strip() != f"desys-project-init {expected_version}":
            raise RuntimeError(f"Unexpected initializer version output: {result.stdout!r}")


if __name__ == "__main__":
    main()
