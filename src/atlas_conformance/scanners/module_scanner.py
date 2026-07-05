from __future__ import annotations

import ast
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True, slots=True)
class ModuleImport:
    source_module: str
    target_module: str
    is_internal: bool
    line_number: int


@dataclass(frozen=True, slots=True)
class ModuleInfo:
    name: str
    path: str
    is_package: bool
    imports: tuple[ModuleImport, ...] = ()
    exports: tuple[str, ...] = ()
    classes: tuple[str, ...] = ()
    functions: tuple[str, ...] = ()


class ModuleScanner:
    def __init__(self, src_root: str | Path) -> None:
        self._src_root = Path(src_root)

    def find_packages(self) -> list[Path]:
        pkgs: list[Path] = []
        if not self._src_root.exists():
            return pkgs
        for init_file in sorted(self._src_root.rglob("__init__.py")):
            pkg_dir = init_file.parent
            if pkg_dir.name == "__pycache__":
                continue
            pkgs.append(pkg_dir)
        return pkgs

    def parse_python_file(self, path: Path) -> ModuleInfo:
        text = path.read_text(encoding="utf-8")
        try:
            tree = ast.parse(text, filename=str(path))
        except SyntaxError:
            return ModuleInfo(name=path.stem, path=str(path), is_package=False)

        imports: list[ModuleImport] = []
        classes: list[str] = []
        functions: list[str] = []
        exports: list[str] = []

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                classes.append(node.name)
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                if node.name.startswith("_"):
                    continue
                functions.append(node.name)
            if isinstance(node, ast.ImportFrom):
                module = node.module or ""
                for alias in node.names:
                    is_internal = not module.startswith(("os.", "sys.", "typing.", "dataclasses.",
                                                         "enum.", "pathlib.", "hashlib.",
                                                         "json.", "datetime.", "abc.",
                                                         "unittest.", "pytest.", "re."))
                    imports.append(ModuleImport(
                        source_module=path.stem,
                        target_module=f"{module}.{alias.name}" if module else alias.name,
                        is_internal=is_internal,
                        line_number=node.lineno,
                    ))

        for node in ast.iter_child_nodes(tree):
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name) and target.id == "__all__":
                        if isinstance(node.value, (ast.List, ast.Tuple)):
                            for elt in node.value.elts:
                                if isinstance(elt, ast.Constant):
                                    exports.append(elt.value)

        is_package = (path.name == "__init__.py")

        return ModuleInfo(
            name=path.stem,
            path=str(path),
            is_package=is_package,
            imports=tuple(imports),
            exports=tuple(exports),
            classes=tuple(classes),
            functions=tuple(functions),
        )

    def scan(self) -> list[ModuleInfo]:
        pkgs = self.find_packages()
        infos: list[ModuleInfo] = []
        for pkg in pkgs:
            for py_file in sorted(pkg.rglob("*.py")):
                if py_file.name == "__pycache__":
                    continue
                if "__pycache__" in str(py_file):
                    continue
                try:
                    info = self.parse_python_file(py_file)
                    if info.imports:
                        infos.append(info)
                except Exception:
                    pass
        return infos

    def build_dependency_graph(self) -> dict[str, set[str]]:
        graph: dict[str, set[str]] = {}
        for info in self.scan():
            src = info.path.split("/")[-2] if "/" in info.path else info.name
            graph.setdefault(src, set())
            for imp in info.imports:
                if imp.is_internal:
                    target = imp.target_module.split(".")[0]
                    graph[src].add(target)
        return graph
