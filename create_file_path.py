import os
import sys

skip_dirs = ["Old_Files", "Old_files", "Extra Files", "old_files", "error", "errors"]

def create_file_path(subj_files_path, output_path, skip_dirs=skip_dirs, curr_case=None):
    # subj_files_path : path to Seedlings/Subject_Files/
    # output_path : path where the updated bl are
    # skip_dirs : dirs to not consider
    # curr_case : whether it is bl, opf, cha... not implemented yet

    audiobl_paths = open(output_path+"/audiobl_paths.txt", "w")
    videobl_paths = open(output_path+"/videobl_paths.txt", "w")

    for root, dirs, files in os.walk(subj_files_path):
        if not any(x in root for x in skip_dirs):

            if "Audio_Analysis" in root:
                print(root)
                audiobl_paths.write(root+"/\n")
            elif "Video_Analysis" in root:
                videobl_paths.write(root+"/\n")
    audiobl_paths.close()
    videobl_paths.close()


if __name__ == "__main__":
    subj_files_path = sys.argv[1]
    output_path = sys.argv[2]

    create_file_path(subj_files_path, output_path)
