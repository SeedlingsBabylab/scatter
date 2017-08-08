import shutil
import os
import sys

ignore_dirs = ['old_files', "Old Files", "Old_Files", "Extra Files"]


def get_subj_month(path):
    split_path = path.split("Home_Visit")
    base = os.path.basename(split_path[0][:-1])
    return base

def walk_sf(sf, bl_files, bl_root):
    for root, dirs, files in os.walk(sf):
        if "{}_Analysis".format(av.title()) in root and not any(x in root for x in ignore_dirs):
            sub_mon = get_subj_month(root)
            new_bl = next((x for x in bl_files if x.startswith(sub_mon)), None)
            if new_bl:
                new_path = os.path.join(root, "{}_{}_sparse_code.csv".format(sub_mon, av))
                shutil.copy(os.path.join(bl_root, new_bl),
                            new_path)
                print "copied: {} to --->  {}".format(new_bl, new_path)



if __name__ == "__main__":

    input_dir = sys.argv[1]
    sf = sys.argv[2]
    av = sys.argv[3]

    bl_files = []

    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if file.endswith(".csv"):
                bl_files.append(file)

    walk_sf(sf, bl_files, input_dir)