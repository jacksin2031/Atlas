import os, sys, json, base64, ast

BASE = r"E:\資料夾\桌面\Atlas\packages\vision\src\atlas_vision"
TESTS_BASE = r"E:\資料夾\桌面\Atlas\packages\vision\tests"

def wf(rel, content, base=BASE):
    path = os.path.join(base, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        f.write(content.encode("utf-8"))
    print(f"  wrote {rel}")
    return True

print("Generator ready")
