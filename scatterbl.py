import os
import sys

import shutil
from datetime import date


class BLFile(object):
    def __init__(self, path, filename, key, bl_type):
        self.path = path
        self.filename = filename
        self.key = key
        self.bl_type = bl_type


skip_dirs = ["Old_Files", "Old_files", "Extra Files", "old_files"]


def delete_old_files(root, files):
    csv_files = [x for x in files if x.endswith(".csv")]
    print "\nremoving: "
    for x in csv_files:
        src = os.path.join(root, x)
        dst = os.path.join(root, "old_files", x.replace(
            ".csv", "_{}.csv".format(date.today().isoformat())))
        print "\t{}   --to-->      {}".format(src, dst)
        os.rename(src, dst)
    print "\n"


if __name__ == "__main__":

    start_dir = sys.argv[1]
    subj_files = sys.argv[2]

    if len(sys.argv) > 5:
        print "\nusage:  $: python scatterbl.py  folder_with_all_bl_files  path_to_subject_files  [--audio] [--video] [--rename]\n\ncan't have more than 3 arguments"
        sys.exit(0)

    audio_bl = False
    if "--audio" in sys.argv:
        audio_bl = True
    video_bl = False
    if "--video" in sys.argv:
        video_bl = True
    rename = False
    if "--rename" in sys.argv:
        rename = True

    bl_files = []

    for root, dirs, files in os.walk(start_dir):
        for file in files:
            if file.endswith(".csv"):
                key = file[:5]
                if "audio" in file:
                    bl_type = "audio"
                if "video" in file:
                    bl_type = "video"

                bl_file = BLFile(os.path.join(root, file), file, key, bl_type)
                bl_files.append(bl_file)

    for root, dirs, files in os.walk(subj_files):
        if audio_bl:
            if "Audio_Analysis" in root and not any(x in root for x in skip_dirs):
                key = root.split("Subject_Files/")[1].split("/")[1]
                for bl_file in bl_files:
                    if bl_file.key == key and bl_file.bl_type == "audio":
                        if rename:
                            bl_file.filename = bl_file.filename[:5] + \
                                "_audio_sparse_code.csv"
                        final_path = os.path.join(root, bl_file.filename)
                        print "moving:  {}  to  {}".format(bl_file.path, final_path)
                        delete_old_files(root, files)
                        shutil.copy(bl_file.path, final_path)

        if video_bl:
            if "Video_Analysis" in root and not any(x in root for x in skip_dirs):
                key = root.split("Subject_Files/")[1].split("/")[1]
                for bl_file in bl_files:
                    if bl_file.key == key and bl_file.bl_type == "video":
                        if rename:
                            bl_file.filename = bl_file.filename[:5] + \
                                "_video_sparse_code.csv"
                        final_path = os.path.join(root, bl_file.filename)
                        print "moving:  {}  to  {}".format(bl_file.path, final_path)
                        delete_old_files(root, files)
                        shutil.copy(bl_file.path, final_path)
