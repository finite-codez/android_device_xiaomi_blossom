import re
from collections import defaultdict

# Preference order for blobs (highest priority first)
PREFERENCE = ['product/', 'vendor/', 'system_ext/', 'system/']

def get_priority(blob_path):
    for i, prefix in enumerate(PREFERENCE):
        if blob_path.startswith(prefix):
            return i
    return len(PREFERENCE)  # lowest priority if no match

def parse_proprietary_files(file_path):
    blobs_map = defaultdict(list)  # key: filename, value: list of full paths

    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            # Remove optional colon with destination (e.g., src:path:dest)
            parts = line.split(':')
            blob_path = parts[0]

            # Normalize blob path to relative
            blob_path = blob_path.lstrip('/') 

            filename = blob_path.split('/')[-1]
            blobs_map[filename].append(blob_path)

    return blobs_map

def select_preferred_blobs(blobs_map):
    preferred_blobs = {}

    for filename, paths in blobs_map.items():
        # Sort paths by priority
        paths_sorted = sorted(paths, key=get_priority)
        # Pick the path with highest priority
        preferred_blobs[filename] = paths_sorted[0]

    return preferred_blobs

def main():
    proprietary_files_path = 'device/xiaomi/blossom/proprietary-files.txt'
    blobs_map = parse_proprietary_files(proprietary_files_path)
    preferred_blobs = select_preferred_blobs(blobs_map)

    # Print or write preferred blobs
    for filename, path in preferred_blobs.items():
        print(path)

if __name__ == "__main__":
    main()
