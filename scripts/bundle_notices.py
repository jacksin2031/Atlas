"""Collect locally installed dependency metadata and original notice texts.

This inventories declared licenses; it does not assess legal compatibility.
Run after installing locked frontend/Cargo dependencies, before Tauri bundling.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "apps/atlas-desktop"
DEST = APP / "src-tauri/resources/notices"


def license_files(directory: Path, explicit=None):
    files = set()
    for path in directory.iterdir():
        if re.match(r"^(licen[cs]e|unlicense|copying|notice|copyright|authors)([._-]|$)", path.name, re.I):
            if path.is_file():
                files.add(path)
            elif path.is_dir():
                files.update(p for p in path.rglob("*") if p.is_file())
        elif path.is_dir() and path.name.lower() == "licenses":
            files.update(p for p in path.rglob("*") if p.is_file())
    if explicit:
        path = directory / explicit
        if path.is_file():
            files.add(path)
    return sorted(files)


def collect(ecosystem, name, version, directory, license_value, source, repository, explicit=None):
    identifier = re.sub(r"[^a-zA-Z0-9._-]", "_", f"{name}-{version}")
    output = DEST / ecosystem / identifier
    texts = []
    for index, path in enumerate(license_files(directory, explicit)):
        output.mkdir(parents=True, exist_ok=True)
        target = output / f"{index:02d}-{path.name}"
        shutil.copyfile(path, target)
        texts.append({"original_file": str(path.relative_to(directory)) if path.is_relative_to(directory) else explicit,
                      "bundled_file": target.relative_to(DEST).as_posix(),
                      "sha256": hashlib.sha256(target.read_bytes()).hexdigest()})
    return {"ecosystem": ecosystem, "name": name, "version": version,
            "declared_license": license_value or "UNKNOWN", "source": source,
            "repository": repository, "license_texts": texts,
            "review_required": not license_value or not texts,
            "review_reasons": (["Unknown declared license"] if not license_value else []) +
                              (["No collected original license/notice text"] if not texts else [])}


def resolve_node(directory, name):
    for parent in [directory, *directory.parents]:
        candidate = parent / "node_modules" / name / "package.json"
        if candidate.is_file():
            return candidate.resolve()
    return None


def frontend():
    manifest = APP / "package.json"
    pending = [(manifest, False)]
    visited = set()
    packages = []
    unresolved = []
    while pending:
        path, include = pending.pop()
        if path in visited:
            continue
        visited.add(path)
        data = json.loads(path.read_text(encoding="utf-8"))
        if include:
            packages.append(collect("npm", data["name"], data["version"], path.parent,
                                    data.get("license") or data.get("licenses"),
                                    "locally installed npm package", data.get("repository")))
        dependencies = {**data.get("dependencies", {}), **data.get("optionalDependencies", {})}
        if include:
            dependencies.update(data.get("peerDependencies", {}))
        for name in dependencies:
            resolved = resolve_node(path.parent, name)
            if resolved:
                pending.append((resolved, True))
            else:
                optional = name in data.get("optionalDependencies", {}) or data.get("peerDependenciesMeta", {}).get(name, {}).get("optional", False)
                unresolved.append({"parent": data["name"] + "@" + data["version"], "dependency": name, "optional": optional})
    # pnpm may install more than one peer context of the same package/version.
    unique = {(p["name"], p["version"]): p for p in packages}
    unresolved = list({(item["parent"], item["dependency"]): item for item in unresolved}.values())
    return list(unique.values()), unresolved


def rust():
    command = ["cargo", "metadata", "--format-version", "1", "--locked", "--offline",
               "--filter-platform", "x86_64-pc-windows-msvc", "--manifest-path",
               str(APP / "src-tauri/Cargo.toml")]
    result = subprocess.run(command, cwd=ROOT, capture_output=True, encoding="utf-8")
    if result.returncode != 0:
        detail = (result.stderr or result.stdout).strip()
        raise RuntimeError(f"cargo metadata failed ({result.returncode}): {detail}")
    metadata = json.loads(result.stdout)
    nodes = {node["id"]: node for node in metadata["resolve"]["nodes"]}
    pending = [metadata["resolve"]["root"]]
    reachable = set()
    while pending:
        identifier = pending.pop()
        if identifier in reachable:
            continue
        reachable.add(identifier)
        pending.extend(dep["pkg"] for dep in nodes[identifier]["deps"])
    packages = []
    for package in metadata["packages"]:
        if package["id"] not in reachable or package["id"] == metadata["resolve"]["root"]:
            continue
        packages.append(collect("cargo", package["name"], package["version"],
                                Path(package["manifest_path"]).parent, package.get("license"),
                                package.get("source") or "local workspace package", package.get("repository"),
                                package.get("license_file")))
    return packages


def main():
    if DEST.exists():
        if DEST.is_symlink() or DEST.resolve() != DEST.absolute():
            raise RuntimeError("Unsafe generated notices destination")
        shutil.rmtree(DEST)
    DEST.mkdir(parents=True)
    npm, unresolved = frontend()
    cargo = rust()
    packages = sorted(npm + cargo, key=lambda item: (item["ecosystem"], item["name"], item["version"]))
    review = [f"{p['ecosystem']}:{p['name']}@{p['version']}" for p in packages if p["review_required"]]
    inventory = {"scope": "Installed frontend production dependency and peer closure; Cargo Windows resolved graph including build dependencies",
                 "generation_command": "python scripts/bundle_notices.py",
                 "legal_compatibility_assessed": False,
                 "python_license": "../runtime/LICENSE.txt (embedded CPython distribution; includes its bundled third-party notices)",
                 "atlas_license": "../runtime/ATLAS-LICENSE.txt",
                 "unresolved_frontend_dependencies": unresolved, "review_required": review, "packages": packages}
    (DEST / "inventory.json").write_text(json.dumps(inventory, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    summary = ("# Beta dependency notices\n\n"
               "Generated with `python scripts/bundle_notices.py`, using local installed packages and "
               "`cargo metadata --locked --offline --filter-platform x86_64-pc-windows-msvc`.\n\n"
               f"- Frontend: {len(npm)} unique name/version packages from production dependencies and their installed dependency/peer closure.\n"
               f"- Rust: {len(cargo)} packages in the reachable Windows resolved graph; includes build dependencies and may over-include crates not shipped as executable code.\n"
               f"- Original notice/license files copied: {sum(len(p['license_texts']) for p in packages)}.\n"
               "- Generated bundle: `apps/atlas-desktop/src-tauri/resources/notices/inventory.json` plus original license texts. "
               "The inventory preserves package name, version, declared license, source/repository, original filename and SHA-256.\n"
               "- CPython and its embedded dependency notices: `resources/runtime/LICENSE.txt`; Atlas: `resources/runtime/ATLAS-LICENSE.txt`.\n\n"
               "This is a metadata and text collection, not a legal compatibility assessment. "
               "Only top-level LICENSE/UNLICENSE/COPYING/NOTICE/COPYRIGHT/AUTHORS files, license directories and Cargo's declared license_file are collected; "
               "notices embedded solely in source files or other documentation may require separate review. "
               "Frontend development-only packages are excluded unless reachable as production peers. "
               "The collected installed npm graph is not proof of which modules Vite emits. "
               "Generated resources are ignored by Git and must be regenerated before packaging.\n\n"
               f"## Missing metadata or texts ({len(review)})\n\n" +
               ("\n".join(f"- `{p['ecosystem']}:{p['name']}@{p['version']}`: {', '.join(p['review_reasons'])}." for p in packages if p["review_required"]) if review else "None in the collected package inventory.") +
               f"\n\n## Unresolved frontend dependencies ({len(unresolved)})\n\n" +
               ("\n".join(f"- `{item['parent']}` → `{item['dependency']}` (optional: {item['optional']})." for item in unresolved) if unresolved else "None.") + "\n")
    (ROOT / "docs/beta/NOTICES.md").write_text(summary, encoding="utf-8")
    print(json.dumps({"npm": len(npm), "cargo": len(cargo), "license_files": sum(len(p['license_texts']) for p in packages),
                      "review_required": len(review), "unresolved_frontend": len(unresolved)}))


if __name__ == "__main__":
    main()
