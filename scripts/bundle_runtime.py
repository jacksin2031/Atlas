"""Build-time only: assemble hash-locked CPython and first-party stdlib hosts."""
from pathlib import Path
import hashlib
import json
import shutil
import subprocess
import tempfile
import urllib.request
import zipfile

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / "apps/atlas-desktop/src-tauri/resources/runtime"


def bundle() -> None:
    lock = json.loads((ROOT / "scripts/runtime-lock.json").read_text())
    with tempfile.TemporaryDirectory(prefix="atlas-runtime-build-") as temporary:
        stage = Path(temporary)
        archive = stage / "python.zip"
        with urllib.request.urlopen(lock["url"], timeout=120) as response:
            archive.write_bytes(response.read())
        if hashlib.sha256(archive.read_bytes()).hexdigest() != lock["sha256"]:
            raise RuntimeError("CPython archive SHA-256 mismatch; refusing to package")
        runtime = stage / "runtime"
        runtime.mkdir()
        with zipfile.ZipFile(archive) as source:
            for item in source.infolist():
                if Path(item.filename).name != item.filename:
                    raise RuntimeError("Unexpected embedded interpreter archive layout")
            source.extractall(runtime)
        modules = runtime / "modules"
        modules.mkdir()
        packages = {
            "atlas_workflow": ROOT / "src",
            "atlas_input": ROOT / "src",
            "atlas_automation": ROOT / "src",
            "atlas_ai": ROOT / "packages/ai/src",
            "atlas_vision": ROOT / "packages/vision/src",
            "atlas_knowledge": ROOT / "packages/knowledge/src",
        }
        for name, directory in packages.items():
            shutil.copytree(directory / name, modules / name,
                            ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "*.pyo"))
        # ._pth disables registry, PYTHONPATH, user site and working-directory imports.
        (runtime / "python313._pth").write_text("python313.zip\n.\nmodules\n", encoding="ascii")
        shutil.copy2(ROOT / "LICENSE", runtime / "ATLAS-LICENSE.txt")
        shutil.copy2(ROOT / "scripts/runtime-lock.json", runtime / "runtime-lock.json")
        subprocess.run([str(runtime / "python.exe"), "-I", "-B", "-c",
                        "import atlas_workflow.host, atlas_ai.host, atlas_vision, atlas_knowledge; "
                        "import ctypes, ssl, sqlite3; print('Bundled runtime imports PASS')"],
                       cwd=temporary, check=True)
        # Only replace this known generated resource subtree, never user files.
        if DEST.exists():
            if DEST.is_symlink() or DEST.resolve() != DEST.absolute():
                raise RuntimeError("Unsafe generated runtime destination")
            shutil.rmtree(DEST)
        DEST.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(runtime, DEST)
    print(f"Runtime assembled: {lock['version']} {lock['target']}")


if __name__ == "__main__":
    bundle()
