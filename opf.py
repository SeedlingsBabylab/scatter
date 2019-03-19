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
             "old_files", "old_opfs", "old_opf", "error", "errors"]
rename_suffix = "_sparse_code.opf"


def delete_old_files(root, files):
    opf_files = [x for x in files if x.endswith(".opf")]
    print "\nremoving: "
    for x in opf_files:
        src = os.path.join(root, x)
        dst = os.path.join(root, "old_opfs", x.replace(
            ".opf", "_{}.opf".format(date.today().isoformat())))
        print "\t{}   --to-->      {}".format(src, dst)
        if not os.path.isdir(os.path.join(root, "old_opfs")):
            if os.path.exists(os.path.join(root, "old_opfs")):
                os.remove(os.path.join(root, "old_opfs"))
            os.makedirs(os.path.join(root, "old_opfs"))
        os.rename(src, dst)
    print "\n"


if __name__ == "__main__":

    start_dir = sys.argv[1]

    if len(sys.argv) > 3:
        print "\nusage:  $: python opf.py  folder_with_all_opf_files  [--rename]\n\ncan't have more than 2 arguments"
        print "opf_paths.txt should exist"
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
                print(os.path.join(root, file))

    with open('path_files/opf_directories.txt') as f:
        paths = f.readlines()
        for path in paths:
            path = path.strip()
            if not path:
                continue
            files = os.listdir(path)
            key = path.split("Subject_Files/")[1].split("/")[1]
            for opf_file in opf_files:
                if opf_file.key == key:
                    if rename:
                        final_name = opf_file.filename[:5] + rename_suffix
                    else:
                        final_name = opf_file.filename
                    opf_filez = [x for x in os.listdir(path) if x.endswith(".opf")]
                    if len(opf_filez) != 1:
                        print(root)
                        print(opf_filez)
                        print "Error: more than one cha file"
                        print opf_filez
                        continue
                    else:
                        delete_old_files(path, files)
                        # x = opf_filez[0]
                        # src = os.path.join(path, x)
                        # dst = os.path.join(path, "old_opfs", x.replace(
                        #     ".opf", "_{}.opf".format(date.today().isoformat())))
                        # print "\t{}   --to-->      {}".format(src, dst)
                        # os.rename(src, dst)
                    final_path = os.path.join(path, final_name)
                    print "moving:  {}  to  {}".format(opf_file.path, final_path)
                    shutil.copy(opf_file.path, final_path)

    # for root, dirs, files in os.walk(subj_files):
    #     if "Video_Annotation" in root and not any(x in root for x in skip_dirs):
    #         key = root.split("Subject_Files/")[1].split("/")[1]
    #         for opf_file in opf_files:
    #             if opf_file.key == key:
    #                 if rename:
    #                     final_name = opf_file.filename[:5] + rename_suffix
    #                 opf_filez = [x for x in files if x.endswith(".opf")]
    #                 if len(opf_filez) != 1:
    #                     print(root)
    #                     print(opf_filez)
    #                     raise
    #                 else:
    #                     x = opf_filez[0]
    #                     src = os.path.join(root, x)
    #                     dst = os.path.join(root, "old_opfs", x.replace(
    #                         ".opf", "_{}.opf".format(date.today().isoformat())))
    #                     print "\t{}   --to-->      {}".format(src, dst)
    #                     os.rename(src, dst)
    #                     # os.remove(os.path.join(root, opf_filez[0]))
    #                 final_path = os.path.join(root, final_name)
    #                 print "moving:  {}  to  {}".format(opf_file.path, final_path)
    #                 shutil.copy(opf_file.path, final_path)
