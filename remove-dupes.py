import os

# Define priority order (lower index = higher priority)
PREFERENCE = ['product/', 'vendor/', 'system_ext/', 'system/']

def get_priority(path):
    for i, prefix in enumerate(PREFERENCE):
        if path.startswith(prefix):
            return i
    return len(PREFERENCE)

def main():
    input_file = 'proprietary-files.txt'
    if not os.path.exists(input_file):
        print("File not found.")
        return

    lines = []
    blob_map = {}

    with open(input_file, 'r') as f:
        for i, line in enumerate(f):
            original_line = line.rstrip('\n')
            stripped = original_line.strip()
            if not stripped or stripped.startswith('#'):
                lines.append((i, original_line, None))  # (index, line, key=None)
                continue

            src = stripped.split(':')[0].lstrip('/')
            name = os.path.basename(src)

            # Store line data and reference
            if name not in blob_map:
                blob_map[name] = []
            blob_map[name].append((i, original_line, src))

            lines.append((i, original_line, name))

    # Determine which paths to keep
    keep_index_set = set()
    for name, entries in blob_map.items():
        if len(entries) == 1:
            keep_index_set.add(entries[0][0])
        else:
            # Sort by priority
            best = sorted(entries, key=lambda x: get_priority(x[2]))[0]
            keep_index_set.add(best[0])

    # Rewrite the file with excess lines commented
    with open(input_file, 'w') as f:
        for i, line, key in lines:
            if key is None or i in keep_index_set:
                f.write(line + '\n')
            else:
                f.write(f'# {line}\n')

    print("✅ Conflicts resolved and extra lines commented out.")

if __name__ == "__main__":
    main()
