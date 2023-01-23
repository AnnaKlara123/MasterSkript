import pandas as pd
import os
import glob
from alive_progress import alive_bar


def get_directory(name):
    # get path to current working directory
    cwd = os.getcwd()
    # get path to folder
    path = os.path.join(cwd, name)
    # create folder if it does not exist
    exists = os.path.exists(path)
    if not exists:
        print(name + " directory does not exist. Creating directory...")
        os.makedirs(path)
    return path


def read_input_files(input_dir):
    # TODO call method to transform to csv
    # TODO call method to transform to utf-8
    # read all file names from the input folder
    csv_files = glob.glob(os.path.join(input_dir, "*.csv"))
    return csv_files


def transform_date(row, bar):
    indices = [0, 4, 6, 8, 10, 12]
    parts = [str(row.timestamp)[i:j] for i, j in zip(indices, indices[1:])]
    bar()
    return pd.Series([int(numeric_string) for numeric_string in parts])


def transform(dataframe, bar):
    time_cols = dataframe.apply((lambda x: transform_date(x, bar)), axis=1)
    time_cols.columns = ['YY', 'MM', 'DD', 'HH', 'MM']
    dataframe = dataframe.drop('timestamp', axis=1)
    return time_cols.join(dataframe)


def save(df, path, filename):
    head, tail = os.path.split(filename)
    # TODO which seperator should be used? Output as csv or txt?
    df.to_csv(os.path.join(path, tail))


def generate_output_files(csv_files, output_dir):
    # loop over the list of csv files
    for index, file in enumerate(csv_files):
        # read the csv file
        # TODO how to determine amount of skiprows?
        df = pd.read_csv(file, sep=' ', skiprows=10, names=["timestamp", "Stat1"])
        with alive_bar(df.shape[0], dual_line=True, title=f'Transforming file {index+1}/{len(csv_files)}') as bar:
            # transform the dataframe
            transformed = transform(df, bar)
            # save transformed file to output folder
            save(transformed, output_dir, file)


def main():
    input_dir = get_directory("input")
    output_dir = get_directory("output")
    csv_files = read_input_files(input_dir)
    generate_output_files(csv_files, output_dir)


if __name__ == "__main__":
    main()
