import os
import sys

import shutil
from datetime import date


class IssuesFile(object):
    def __init__(self, path, filename, key, file_type):
        self.path = path
        self.filename = filename
        self.key = key
        self.file_type = file_type


skip_dirs = set(["Old_Files", "Old_files", "Extra Files",
                 "old_files", "error", "errors", "Old_Files",
                 "Old_files", "Extra Files", "old_files",
                 "old_opfs", "old_opf", "error", "errors",
                 "Old_Files", "Old_files", "Extra Files",
                 "old_files", "old_chas", "old_cha", "Repair Files",
                 "error", "errors"])


def delete_old_files(root, files):
    issue_files = [x for x in files if x.endswith(".docx")]
    print "\nremoving: "
    for x in issue_files:
        src = os.path.join(root, x)
        if not os.path.exists(os.path.join(root, "old_files")):
            os.makedirs(os.path.join(root, "old_files"))
        dst = os.path.join(root, "old_files", x.replace(
            ".docx", "_{}.docx".format(date.today().isoformat())))
        print "\t{}   --to-->      {}".format(src, dst)
        os.rename(src, dst)
    print "\n"


if __name__ == "__main__":

    start_dir = sys.argv[1]
    subj_files = sys.argv[2]

    if len(sys.argv) > 6:
        print "\nusage:  $: python coding_issues.py  folder_with_all_codingissues_files  path_to_subject_files  [--audio] [--video] [--rename]\n\ncan't have more than 4 arguments"
        sys.exit(0)

    audio_issue = False
    if "--audio" in sys.argv:
        audio_issue = True
    video_issue = False
    if "--video" in sys.argv:
        video_issue = True
    rename = False
    if "--rename" in sys.argv:
        rename = True

    issue_files = []

    for root, dirs, files in os.walk(start_dir):
        for file in files:
            if file.endswith(".docx"):
                key = file[:5]
                if "audio" in file.lower():
                    file_type = "audio"
                if "video" in file.lower():
                    file_type = "video"

                issue_file = IssuesFile(os.path.join(
                    root, file), file, key, file_type)
                issue_files.append(issue_file)

    for root, dirs, files in os.walk(subj_files):
        if audio_issue:
            if "Audio_Annotation" in root and not any(x in root for x in skip_dirs):
                key = root.split("Subject_Files/")[1].split("/")[1]
                for issue_file in issue_files:
                    if issue_file.key == key and issue_file.file_type == "audio":
                        if rename:
                            issue_file.filename = issue_file.filename[:5] + \
                                "_audio_coding_issues.docx"
                        final_path = os.path.join(root, issue_file.filename)
                        print "moving:  {}  to  {}".format(issue_file.path, final_path)
                        delete_old_files(root, files)
                        shutil.copy(issue_file.path, final_path)

        if video_issue:
            if "Video_Annotation" in root and not any(x in root for x in skip_dirs):
                key = root.split("Subject_Files/")[1].split("/")[1]
                for issue_file in issue_files:
                    if issue_file.key == key and issue_file.file_type == "video":
                        if rename:
                            issue_file.filename = issue_file.filename[:5] + \
                                "_video_coding_issues.docx"
                        final_path = os.path.join(root, issue_file.filename)
                        print "moving:  {}  to  {}".format(issue_file.path, final_path)
                        delete_old_files(root, files)
                        shutil.copy(issue_file.path, final_path)
