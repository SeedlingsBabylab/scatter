import os
import sys
from datetime import date

import shutil


class OPFFile(object):
    def __init__(self, path, filename, key):
        self.path = path
        self.filename = filename
        self.key = key


skip_dirs = ["Old_Files", "Old_files", "Extra Files",
             "old_files", "old_opfs", "old_opf"]
rename_suffix = "_sparse_code.opf"


def delete_old_files(root, files):
    cha_files = [x for x in files if x.endswith(".cha")]
    print "\nremoving: "
    for x in cha_files:
        src = os.path.join(root, x)
        dst = os.path.join(root, "old_chas", x.replace(
            ".cha", "_{}.cha".format(date.today().isoformat())))
        print "\t{}   --to-->      {}".format(src, dst)
        if not os.path.isdir(os.path.join(root, "old_chas")):
            os.makedirs(os.path.join(root, "old_chas"))
        os.rename(src, dst)
    print "\n"


if __name__ == "__main__":

    start_dir = sys.argv[1]
    subj_files = sys.argv[2]

    if len(sys.argv) > 4:
        print "\nusage:  $: python opf.py  folder_with_all_opf_files  path_to_subject_files  [--rename]\n\ncan't have more than 3 arguments"
        sys.exit(0)

    rename = False
    if "--rename" in sys.argv:
        rename = True

    opf_files = []

    for root, dirs, files in os.walk(start_dir):
        for file in files:
            if file.endswith(".opf"):
                opf_file = OPFFile(os.path.join(root, file), file, file[:5])
                opf_files.append(opf_file)

    for root, dirs, files in os.walk(subj_files):
        if "Video_Annotation" in root and not any(x in root for x in skip_dirs):
            key = root.split("Subject_Files/")[1].split("/")[1]
            for opf_file in opf_files:
                if opf_file.key == key:
                    if rename:
                        final_name = opf_file.filename[:5] + rename_suffix
                    opf_filez = [x for x in files if x.endswith(".opf")]
                    if len(opf_filez) != 1:
                        print(root)
                        print(opf_filez)
                        raise
                    else:
                        x = opf_filez[0]
                        src = os.path.join(root, x)
                        dst = os.path.join(root, "old_opfs", x.replace(
                            ".opf", "_{}.opf".format(date.today().isoformat())))
                        print "\t{}   --to-->      {}".format(src, dst)
                        os.rename(src, dst)
                        # os.remove(os.path.join(root, opf_filez[0]))
                    final_path = os.path.join(root, final_name)
                    print "moving:  {}  to  {}".format(opf_file.path, final_path)
                    shutil.copy(opf_file.path, final_path)
