import os, ast, subprocess

base = r"E:\資料夾\桌面\Atlas\packages\vision\src\atlas_vision"
tests_base = r"E:\資料夾\桌面\Atlas\packages\vision\tests"

# 1. Check all files parse
print("=== Parsing Check ===")
errors = []
for root, dirs, files in os.walk(base):
    for f in sorted(files):
        if f.endswith(".py"):
            path = os.path.join(root, f)
            try:
                ast.parse(open(path, encoding="utf-8").read())
            except SyntaxError as e:
                errors.append(f"{os.path.relpath(path, base)}: {e}")
for f in sorted(os.listdir(tests_base)):
    if f.endswith(".py"):
        path = os.path.join(tests_base, f)
        try:
            ast.parse(open(path, encoding="utf-8").read())
        except SyntaxError as e:
            errors.append(f"tests/{f}: {e}")

if errors:
    for e in errors: print(f"  FAIL: {e}")
else:
    print("  All files parse OK")

# 2. Check for TODOs
print("\n=== TODO Check ===")
todo_count = 0
for root, dirs, files in os.walk(base):
    for f in files:
        if f.endswith(".py"):
            path = os.path.join(root, f)
            content = open(path, encoding="utf-8").read()
            for line in content.split("\n"):
                stripped = line.strip()
                if "TODO" in stripped.upper() and not stripped.startswith("# TODO:"):
                    todo_count += 1
                    print(f"  TODO in {os.path.relpath(path, base)}: {stripped[:60]}")
print(f"  TODO count: {todo_count}")

# 3. Count modules
print("\n=== Module Count ===")
total_py = 0
for root, dirs, files in os.walk(base):
    total_py += len([f for f in files if f.endswith(".py")])
test_py = len([f for f in os.listdir(tests_base) if f.endswith(".py")])
print(f"  Source files: {total_py}")
print(f"  Test files: {test_py}")

# 4. Check no circular imports
print("\n=== Import Check ===")
import_errors = []
for root, dirs, files in os.walk(base):
    for f in files:
        if f.endswith(".py") and f != "__init__.py":
            path = os.path.join(root, f)
            content = open(path, encoding="utf-8").read()
            if "from .." in content or "from ." in content:
                import_errors.append(os.path.relpath(path, base))
if import_errors:
    print(f"  Relative imports found: {import_errors}")
else:
    print("  No relative imports (all absolute)")

# 5. Check platform independence
print("\n=== Platform Independence ===")
platform_refs = []
for root, dirs, files in os.walk(base):
    for f in files:
        if f.endswith(".py"):
            path = os.path.join(root, f)
            content = open(path, encoding="utf-8").read()
            for bad in ["opencv", "cv2", "torch", "tensorflow", "onnx", "cuda", "directx", "win32", "ctypes"]:
                if bad in content.lower():
                    platform_refs.append(f"{os.path.relpath(path, base)}: {bad}")
if platform_refs:
    for r in platform_refs: print(f"  FOUND: {r}")
else:
    print("  No platform-specific references found")

print("\n=== Validation Complete ===")
