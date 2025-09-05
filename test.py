import os, re

root = "./"  # 프로젝트 루트 경로

imports = set()
pattern = re.compile(r'^(?:from|import)\s+([a-zA-Z0-9_]+)')

for subdir, _, files in os.walk(root):
    for file in files:
        if file.endswith(".py"):
            path = os.path.join(subdir, file)
            try:
                with open(path, "r", encoding="utf-8") as f:
                    for line in f:
                        m = pattern.match(line.strip())
                        if m:
                            imports.add(m.group(1))
            except Exception as e:
                print(f"⚠️ {path} 건너뜀 ({e})")

for pkg in sorted(imports):
    print(pkg)