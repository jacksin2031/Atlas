import os, sys

base = r"E:\u8cc7\u6599\u593e\u684c\u9762\Atlas\specs\plugin"

def write_rfc(filename, content):
    path = os.path.join(base, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Written: {filename} ({len(content)} bytes)")
