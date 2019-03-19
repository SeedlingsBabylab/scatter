import os
import sys
from sets import Set
import shutil
from datetime import date


class BLFile(object):
    def __init__(self, path, filename, key, bl_type):
        self.path = path
        self.filename = filename
        self.key = key
        self.bl_type = bl_type


skip_dirs = Set(["Old_Files", "Old_files",
             "Extra Files", "old_files", "error", "errors"])


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
    #subj_files = sys.argv[3]
    list_paths = sys.argv[2]

    if len(sys.argv) > 5:
        print "\nusage:  $: python scatterbl.py  folder_with_all_bl_files  list_paths.txt  [--audio] [--video] [--rename]\n\ncan't have more than 3 arguments"
        print "audiobl_paths.txt or videobl_paths.txt should exist"
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

            if file.endswith(".csv") and "wordmerged" in file:
                print(os.path.join(root, file))
                key = file[:5]
                to_use = False
                if "audio" in file or "audio" in dirs or "audio" in root \
                or "Audio" in file or "Audio" in dirs or "Audio" in root:
                # if audio_bl:
                    bl_type = "audio"
                    print("audio",file)
                    to_use = True
                elif "video" in file or "video" in dirs or "video" in root \
                or "Video" in file or "Video" in dirs or "Video" in root:
                    bl_type = "video"
                    print("video", file)
                    to_use = True
                else:
                    pass
                # if to_use:
                bl_file = BLFile(os.path.join(root, file), file, key, bl_type)
                bl_files.append(bl_file)

    if audio_bl:
        with open(list_paths) as f:
            paths = f.readlines()
    if video_bl:
        with open(list_paths) as f:
            paths = f.readlines()
    with open(list_paths) as f:
        paths = f.readlines()
        # print(len(paths))
        for path in paths:
            path = path.strip()
            if not path:
                continue
            files = os.listdir(path)
            if audio_bl:
                # print("audio")
                key = path.split("Subject_Files/")[1].split("/")[1]
                for bl_file in bl_files:
                    if bl_file.key == key and bl_file.bl_type == "audio":
                        if rename:
                            bl_file.filename = bl_file.filename[:5] + \
                                "_audio_sparse_code.csv"
                        final_path = os.path.join(path, bl_file.filename)
                        print "moving:  {}  to  {}".format(bl_file.path, final_path)
                        delete_old_files(path, files)
                        shutil.copy(bl_file.path, final_path)

            if video_bl:
                key = path.split("Subject_Files/")[1].split("/")[1]
                for bl_file in bl_files:
                    if bl_file.key == key and bl_file.bl_type == "video":
                        if rename:
                            bl_file.filename = bl_file.filename[:5] + \
                                "_video_sparse_code.csv"
                        final_path = os.path.join(path, bl_file.filename)
                        print "moving:  {}  to  {}".format(bl_file.path, final_path)
                        delete_old_files(path, files)
                        shutil.copy(bl_file.path, final_path)
