import os
from argparse import ArgumentParser
from config_parser import generate_default_config
import shutil
from progress_bar import progress_bar
from chardet import detect
import re

CHUNK_SIZE = 1048576


def is_config_file(file):
    # check with regex if the file is a config file
    pattern = '_config.txt'
    a = re.search(pattern, file)
    if a is not None:
        return True
    return False


def get_directory(name):
    # get path to current working directory
    cwd = os.getcwd()
    # move one folder up, to get out of script folder
    dir_name = os.path.dirname(cwd)
    # get path to folder
    path = os.path.join(dir_name, name)
    # create folder if it does not exist
    exists = os.path.exists(path)
    if not exists:
        print(name + " directory does not exist. Creating directory...")
        os.makedirs(path)
    return path


def copy_raw_files(raw_dir, input_dir):
    with progress_bar() as progress:
        task_copy_file = progress.add_task("[red]Copying files...", total=len(os.listdir(raw_dir)))
        for file_name in os.listdir(raw_dir):
            # construct full file path
            source = os.path.join(raw_dir, file_name)
            path, file_extension = os.path.splitext(source)
            # only accept zrx and csv files
            if file_extension not in ['.zrx', '.csv'] or not os.path.isfile(source):
                progress.update(task_copy_file, advance=1)
                continue
            # get new file name and path
            destination = os.path.join(input_dir, file_name)
            # copy file to input folder
            shutil.copy(source, destination)
            progress.update(task_copy_file, advance=1)


def convert_to_csv(input_dir):
    # iterate over each file in input dir
    for file_name in os.listdir(input_dir):
        # get full path to file
        file = os.path.join(input_dir, file_name)
        if not os.path.isfile(file):
            continue
        # get the file extension
        path, file_extension = os.path.splitext(file)
        if file_extension == '.zrx':
            new_file = file.replace('.zrx', '.csv')
            # if file with same name already exists, remove it
            if os.path.exists(new_file):
                os.remove(new_file)
            os.rename(file, new_file)


# get file encoding type
def get_encoding_type(file):
    with open(file, 'rb') as f:
        rawdata = f.read(CHUNK_SIZE)
    return detect(rawdata)['encoding']


def read_in_chunks(file_object, chunk_size=1024):
    while True:
        data = file_object.read(chunk_size)
        if not data:
            break
        yield data


def convert_to_utf8(input_dir):
    with progress_bar() as progress:
        task_convert_file = progress.add_task("[red]Encoding to utf-8...", total=len(os.listdir(input_dir)))
        for file_name in os.listdir(input_dir):
            src_file = os.path.join(input_dir, file_name)
            path, file_extension = os.path.splitext(src_file)
            trg_file = path + "_utf" + file_extension
            if not os.path.isfile(src_file):
                progress.update(task_convert_file, advance=1)
                continue
            # get the encoding of the file
            from_codec = get_encoding_type(src_file)
            # skip converting config files and files that are already utf-8
            if from_codec == 'utf-8' or is_config_file(src_file):
                progress.update(task_convert_file, advance=1)
                continue
            try:
                with open(src_file, 'r', encoding=from_codec) as f, open(trg_file, 'w', encoding='utf-8') as e:
                    for piece in read_in_chunks(f):
                        e.write(piece)

                os.remove(src_file)  # remove old encoding file
                os.rename(trg_file, src_file)  # rename new encoding
                progress.update(task_convert_file, advance=1)
            except UnicodeDecodeError:
                print('Decode Error')
            except UnicodeEncodeError:
                print('Encode Error')


def generate_default_configs(input_dir, override):
    with progress_bar() as progress:
        task_default_config = progress.add_task("[red]Generating config files...", total=len(os.listdir(input_dir)))
        for file in os.listdir(input_dir):
            src_file = os.path.join(input_dir, file)
            file_name = os.path.splitext(os.path.basename(src_file))[0]
            config_file_name = file_name + "_config.txt"
            config_file = os.path.join(input_dir, config_file_name)
            # if file is a config file or if config file already exists and override flag is set to False, skip
            if (os.path.exists(config_file) and override is False) or is_config_file(src_file):
                progress.update(task_default_config, advance=1)
                continue
            generate_default_config(config_file)
            progress.update(task_default_config, advance=1)


def main():
    parser = ArgumentParser()
    # command line argument to set the source folder (where the raw files are located)
    parser.add_argument("-i", "--input", dest="raw_dir",
                        help="Specify the folder with the raw files to read.", metavar="DIR", required=True)
    # flag to determine if existing config files should be kept, defaults to false
    parser.add_argument("-o", "--override", dest="override",
                        help="Set this flag if you want to override existing config files", action='store_true')
    args = parser.parse_args()
    input_dir = get_directory("input")
    get_directory("output")
    # require a source folder
    copy_raw_files(args.raw_dir, input_dir)
    convert_to_csv(input_dir)
    convert_to_utf8(input_dir)
    generate_default_configs(input_dir, args.override)


if __name__ == "__main__":
    main()
