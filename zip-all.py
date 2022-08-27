import argparse
import os
from zipfile import ZipFile
import zipfile


def zip_file(path, file):
    (basename, extension) = os.path.splitext(file)
    if extension == ".zip":
        return
    file_zip = basename + ".zip"
    filepath = os.path.join(path, file)
    filepath_zip = os.path.join(path, file_zip)
    with ZipFile(filepath_zip, "w") as zip:
        print(f"zipping: {file}... ",end="")
        zip.write(filepath, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
        os.remove(filepath)
        print("done")


def collate_file_info(path):
    files_found = []
    for root, _, files in os.walk(path):
        for name in files:
            files_found.append((root, name))
    return files_found


def process_args():
    parser = argparse.ArgumentParser(description="apply action to files\n")
    parser.add_argument(
        "folder", help="the folder perform action on"
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = process_args()
    files = collate_file_info(args.folder)

    [zip_file(path, file) for (path, file) in files]

    print("FINISHED")
