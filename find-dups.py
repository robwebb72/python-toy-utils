import argparse
import os


def collate_file_info(path, include_path):
    files_found = []
    path_len = 0 if include_path else len(path)
    for root, _, files in os.walk(path):
        for name in files:
            file_path = os.path.join(root, name)
            file_size = os.path.getsize(file_path)
            root_name = root[path_len:]
            files_found.append((name, file_size, root_name))
    return files_found


def create_duplicate_lists(files):
    collated_files = {}
    for file in files:
        file_details = (file[0], file[1])
        if file_details in collated_files:
            record = collated_files[file_details]
            record.append(file[2])
        else:
            collated_files[file_details] = [file[2]]
    return collated_files


def process_args():
    parser = argparse.ArgumentParser(
        description="find possible duplicate files\n"
        )
    parser.add_argument(
        "-o", "--output_file",  help="the file for output"
    )
    parser.add_argument(
        "folder_list", nargs="*", help="the folders to search for duplicates"
    )
    return parser.parse_args()


def create_csv_row(file_key, file_list):
    dir_list = ", ".join(f'"{item}"' for item in file_list)
    return f'"{file_key[0]}", "{file_key[1]}", {dir_list}'


def write_duplicates(filename, dups):
    f = open(filename, "w")
    for file_key, file_list in dups.items():
        if len(file_list) > 1:
            f.write(create_csv_row(file_key, file_list)+ "\n")
    f.close()


def print_duplicates(dups):
    for file_key, file_list in dups.items():
        if len(file_list) > 1:
            print(create_csv_row(file_key, file_list))


if __name__ == "__main__":
    args = process_args()
    files = []
    include_root_name = len(args.folder_list) > 1
    for folder in args.folder_list:
        files.extend(collate_file_info(folder, include_root_name))

    dups = create_duplicate_lists(files)
    if args.output_file is None:
        print_duplicates(dups)
    else:
        write_duplicates(args.output_file.strip(), dups)

    print("...done")
