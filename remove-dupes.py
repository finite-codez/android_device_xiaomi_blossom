import os
from collections import defaultdict

FILE_PATH = "proprietary-files.txt"

# Load all blob entries
with open(FILE_PATH, "r", encoding="utf-8") as f:
    lines = f.readlines()

so_map = defaultdict(list)

# Collect .so entries by basename
for idx, line in enumerate(lines):
    line = line.strip()
    if not line or line.startswith("#"):
        continue
    path = line.split(":")[0]
    if path.endswith(".so"):
        so_map[os.path.basename(path)].append((idx, line))

# Find conflicts
conflicts = {k: v for k, v in so_map.items() if len(v) > 1}

if not conflicts:
    print("✅ No conflicting .so blobs found.")
else:
    print("⚠️ Found conflicting .so blobs:")
    for blob, entries in conflicts.items():
        print(f"\n🔁 {blob} appears in multiple locations:")
        for idx, entry in entries:
            print(f"  - Line {idx+1}: {entry}")

    # Optional: auto-comment all but the first
    confirm = input("\nComment out duplicates? [y/N]: ").lower()
    if confirm == "y":
        for blob, entries in conflicts.items():
            for idx, line in entries[1:]:
                lines[idx] = f"# {line}  # auto-disabled due to conflict\n"
        with open(FILE_PATH, "w", encoding="utf-8") as f:
            f.writelines(lines)
        print("✅ Conflicting entries commented out.")
