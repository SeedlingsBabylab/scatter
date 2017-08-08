import shutil
import os
import sys

ignore_dirs = ['old_files', "Old Files", "Old_Files", "Extra Files", "old_opfs", "old opfs", "Old_Opfs"]


def get_subj_month(path):
    split_path = path.split("Home_Visit")
    base = os.path.basename(split_path[0][:-1])
    return base


def walk_sf(sf, opf_files, opf_root):
    for root, dirs, files in os.walk(sf):
        if "Video_Annotation" in root and not any(x in root for x in ignore_dirs):
            sub_mon = get_subj_month(root)
            new_opf = next((x for x in opf_files if x.startswith(sub_mon)), None)
            if new_opf:
                new_path = os.path.join(root, "{}_sparse_code.opf".format(sub_mon))
                shutil.copy(os.path.join(opf_root, new_opf),
                            new_path)
                print "copied: {} to --->  {}".format(new_opf, new_path)


def output_likelihood_func(bl_files, output):
    with open(output, "wb") as out:
        for file in bl_files:
            out.write(file)


if __name__ == "__main__":

    input_dir = sys.argv[1]
    sf = sys.argv[2]

    opf_files = []

    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if file.endswith(".opf"):
                opf_files.append(file)

    walk_sf(sf, opf_files, input_dir)