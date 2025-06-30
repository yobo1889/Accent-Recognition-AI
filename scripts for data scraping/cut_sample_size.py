import os
import shutil
from collections import defaultdict
from random import shuffle

SOURCE_DIR = 'voxforge_data'
DEST_DIR = 'balanced_voxforge_subset'
SAMPLES_PER_ACCENT = 200  

TARGET_ACCENTS = {
    'American English',
    'European English',
    'Canadian English'
}
# parse README to extract pronunciation dialect
def parse_readme(readme_path):

    dialect = None
    with open(readme_path, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            if 'Pronunciation dialect' in line:
                _, value = line.strip().split(':', 1)
                dialect = value.strip()
                break
    return dialect
# Traverse voxforge data and group paths by selected accent classes
def collect_accent_samples(data_dir):
   
    accent_dict = defaultdict(list)

    for root, dirs, files in os.walk(data_dir):
        if 'etc' in dirs:
            readme_path = os.path.join(root, 'etc', 'README')
            if os.path.exists(readme_path):
                accent = parse_readme(readme_path)
                if accent in TARGET_ACCENTS:
                    accent_dict[accent].append(root)

    return accent_dict
 #Copy balanced samples of the selected accents into a new directory
def create_balanced_subset(accent_dict, max_per_class, dest_dir):
   
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    for accent, paths in accent_dict.items():
        shuffle(paths)
        selected = paths[:max_per_class]
        accent_sanitized = accent.replace(" ", "_")

        for i, sample_path in enumerate(selected):
            new_dir_name = f"{accent_sanitized}_{i}"
            dest_path = os.path.join(dest_dir, new_dir_name)
            shutil.copytree(sample_path, dest_path)

        print(f"Copied {len(selected)} samples for accent: {accent}")

def main():
    accent_samples = collect_accent_samples(SOURCE_DIR)
    print("Available samples per target accent:")
    for accent in TARGET_ACCENTS:
        count = len(accent_samples.get(accent, []))
        print(f"{accent}: {count}")

    create_balanced_subset(accent_samples, SAMPLES_PER_ACCENT, DEST_DIR)

if __name__ == '__main__':
    main()
