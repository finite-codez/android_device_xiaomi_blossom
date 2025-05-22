import os

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

    with open(input_file, 'r') as f:
        for i, line in enumerate(f):
            original_line = line.rstrip('\n')
            stripped = original_line.strip()
            if not stripped or stripped.startswith('#'):
                lines.append((i, original_line, None))  # no blob name
                continue

            src = stripped.split(':')[0].lstrip('/')
            name = os.path.basename(src)

            if name not in blob_map:
                blob_map[name] = []
            blob_map[name].append((i, original_line, src))

            lines.append((i, original_line, name))

    # Find conflicts and decide which to keep
    to_comment = []
    print("\n🔍 Detected Conflicts:\n")
    for name, entries in blob_map.items():
        if len(entries) > 1:
            print(f"🧩 {name}:")
            # sort entries by priority
            sorted_entries = sorted(entries, key=lambda x: get_priority(x[2]))
            for idx, line, src in sorted_entries:
                prefix = "✅ KEEP" if (idx == sorted_entries[0][0]) else "❌ COMMENT"
                print(f"   {prefix}: {src}")
            print()
            # Collect indices except the first one to comment out
            to_comment.extend([idx for idx, _, _ in sorted_entries[1:]])

    if not to_comment:
        print("🎉 No conflicts found. You're all good!\n")
        return

    confirm = input("⚠️ Do you want to comment out the less preferred entries? [y/N]: ").strip().lower()
    if confirm != 'y':
        print("🚫 No changes made.")
        return

    # DEBUG: show indices to comment out
    print(f"📝 Commenting out {len(to_comment)} lines at indices: {sorted(to_comment)}")

    with open(input_file, 'w') as f:
        for i, line, key in lines:
            if i in to_comment:
                if not line.lstrip().startswith('#'):
                    f.write(f"# {line}\n")
                else:
                    # already commented
                    f.write(line + '\n')
            else:
                f.write(line + '\n')

    print("✅ Conflicts handled. Excess lines commented out.\n")

if __name__ == "__main__":
    main()
