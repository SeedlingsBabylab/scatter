import os
import sys
from datetime import date

import shutil


class CHAFile(object):
    def __init__(self, path, filename, key):
        self.path = path
        self.filename = filename
        self.key = key

    def __str__(self):
        return(self.filename)



skip_dirs = ["Old_Files", "Old_files", "Extra Files", "old_files",
             "old_chas", "old_cha", "Repair Files", "error", "errors"]

rename_suffix = "_sparse_code.cha"


def delete_old_files(root, files):
    cha_files = [x for x in files if x.endswith(".cha")]
    print "\nremoving: "
    for x in cha_files:
        src = os.path.join(root, x)
        dst = os.path.join(root, "old_chas", x.replace(
            ".cha", "_{}.cha".format(date.today().isoformat())))
        print "\t{}   --to-->      {}".format(src, dst)
        if not os.path.isdir(os.path.join(root, "old_chas")):
            if os.path.exists(os.path.join(root, "old_chas")):
                os.remove(os.path.join(root, "old_chas"))
            os.makedirs(os.path.join(root, "old_chas"))
        os.rename(src, dst)
    print "\n"


if __name__ == "__main__":

    start_dir = sys.argv[1]
    path_file = sys.argv[2]

    if len(sys.argv) > 4:
        print "\nusage:  $: python cha.py  folder_with_all_cha_files [--rename]\n\ncan't have more than 2 arguments"
        print "cha_paths.txt should exist"
        sys.exit(0)

    rename = False
    if "--rename" in sys.argv:
        rename = True

    cha_files = []

    for root, dirs, files in os.walk(start_dir):
        for file in files:
            if file.endswith(".cha") and not "scrubbed" in file:
                print(root, file)
                cha_file = CHAFile(os.path.join(root, file), file, file[:5])
                cha_files.append(cha_file)

    with open(path_file) as f:
        paths = f.readlines()
        for path in paths:
            path = path.strip()
            if not path:
                continue
            files = os.listdir(path)
            key = path.split("Subject_Files/")[1].split("/")[1]
            for cha_file in cha_files:
                if cha_file.key == key:
                    if rename:
                        final_name = cha_file.filename[:5] + rename_suffix
                    else:
                        final_name = cha_file.filename
                    cha_filez = [x for x in os.listdir(path) if x.endswith(".cha")]
                    if len(cha_filez) != 1:
                        print(root)
                        print(cha_filez)
                        print "Error: more than one cha file"
                        print cha_filez
                        continue
                    else:
                        # os.remove(os.path.join(root, cha_filez[0]))
                        delete_old_files(path, files)
                    final_path = os.path.join(path, final_name)
                    print "moving:  {}  to  {}".format(cha_file.path, final_path)
                    shutil.copy(cha_file.path, final_path)


    # for root, dirs, files in os.walk(subj_files):
    #     if "Audio_Annotation" in root and not any(x in root for x in skip_dirs):
    #         key = root.split("Subject_Files/")[1].split("/")[1]
    #         for cha_file in cha_files:
    #             if cha_file.key == key:
    #                 if rename:
    #                     final_name = cha_file.filename[:5] + rename_suffix
    #                 else:
    #                     final_name = cha_file.filename
    #                 cha_filez = [x for x in files if x.endswith(".cha")]
    #                 if len(cha_filez) != 1:
    #                     print(root)
    #                     print(cha_filez)
    #                     print "Error: more than one cha file"
    #                     print cha_filez
    #                     continue
    #                     #raise Exception("\n\nmore than 1 cha file\n\n")
    #                 else:
    #                     # os.remove(os.path.join(root, cha_filez[0]))
    #                     delete_old_files(root, files)
    #                 final_path = os.path.join(root, final_name)
    #                 print "moving:  {}  to  {}".format(cha_file.path, final_path)
    #                 shutil.copy(cha_file.path, final_path)
