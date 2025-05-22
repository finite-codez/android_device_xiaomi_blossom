import os

# Priority of paths: earlier means more preferred
PREFERENCE = ['product/', 'vendor/', 'system_ext/', 'system/']

def get_priority(path):
    for i, prefix in enumerate(PREFERENCE):
        if path.startswith(prefix):
            return i
    return len(PREFERENCE)

def main():
    input_file = 'proprietary-files.txt'
    if not os.path.exists(input_file):
        print("❌ proprietary-files.txt not found.")
        return

    lines = []
    blob_map = {}

    # Step 1: Parse the file and build map
    with open(input_file, 'r') as f:
        for i, line in enumerate(f):
            original_line = line.rstrip('\n')
            stripped = original_line.strip()
            if not stripped or stripped.startswith('#'):
                lines.append((i, original_line, None))  # (index, line, blob name)
                continue

            src = stripped.split(':')[0].lstrip('/')
            name = os.path.basename(src)

            if name not in blob_map:
                blob_map[name] = []
            blob_map[name].append((i, original_line, src))

            lines.append((i, original_line, name))

    # Step 2: List conflicts
    print("\n🔍 Detected Conflicts:\n")
    to_comment = []
    for name, entries in blob_map.items():
        if len(entries) > 1:
            print(f"🧩 {name}:")
            sorted_entries = sorted(entries, key=lambda x: get_priority(x[2]))
            for idx, line, src in sorted_entries:
                prefix = "✅ KEEP" if (idx == sorted_entries[0][0]) else "❌ COMMENT"
                print(f"   {prefix}: {src}")
            print()

            to_comment.extend([idx for idx, _, _ in sorted_entries[1:]])

    if not to_comment:
        print("🎉 No conflicts found. You're all good!\n")
        return

    # Step 3: Confirm with user
    confirm = input("⚠️ Do you want to comment out the less preferred entries? [y/N]: ").strip().lower()
    if confirm != 'y':
        print("🚫 No changes made.")
        return

    # Step 4: Rewrite file with comments
    with open(input_file, 'w') as f:
        for i, line, key in lines:
            if key is None or i not in to_comment:
                f.write(line + '\n')
            else:
                f.write(f"# {line}\n")

    print("✅ Conflicts handled. Excess lines commented out.\n")

if __name__ == "__main__":
    main()
