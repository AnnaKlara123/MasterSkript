import pandas as pd
import os
import glob
from alive_progress import alive_bar
from config_parser import get_config
from prepare_files import get_directory


def get_file_name(file):
    # returns the file name without extension
    file_name = os.path.basename(file).split('.')[0]
    return file_name


def read_input_files(input_dir):
    # read all file names from the input folder
    csv_files = glob.glob(os.path.join(input_dir, "*.csv"))
    return csv_files


def transform_time_row(row, bar):
    # indices that separate each value in the timestamp column
    indices = [0, 4, 6, 8, 10, 12]
    # separate the timestamp column into parts
    parts = [str(row.timestamp)[i:j] for i, j in zip(indices, indices[1:])]
    # generate a pandas timestamp for resampling
    timestamp = [pd.Timestamp(f'{parts[0]}{parts[1]}{parts[2]} {parts[3]}:{parts[4]}:00')]
    # convert the string values to int
    values = [int(numeric_string) for numeric_string in parts]
    # merge the two arrays
    timestamp.extend(values)
    # create a pandas series
    series = pd.Series(timestamp)
    # progress the progress bar to the next step
    bar()
    return series


class Transformer:
    input_folder_name = "input"

    def __init__(self):
        self.input_dir = get_directory(self.input_folder_name)
        self.csv_files = read_input_files(self.input_dir)

    def run(self):
        # loop over the list of csv files
        for index, csv in enumerate(self.csv_files):
            # create a File object from each csv
            file = File(csv, index, total_files=len(self.csv_files))
            file.transform()


class File:
    output_folder_name = "output"

    def __init__(self, csv, index, total_files):
        self.csv = csv
        self.index = index
        self.total_files = total_files
        self.output_dir = get_directory(self.output_folder_name)
        self.path, self.file_name = os.path.split(csv)
        self.config = get_config(self.path, get_file_name(self.file_name))
        self.df = None

    def get_header(self):
        header = [["YY", "MM", "DD", "HH", "MM", "Stat1"],
                  ["YY", "MM", "DD", "HH", "MM", self.config.get('elevation')],
                  ["YY", "MM", "DD", "HH", "MM", self.config.get('latitude')],
                  ["YY", "MM", "DD", "HH", "MM", self.config.get('longitude')],
                  ["YY", "MM", "DD", "HH", "MM", "Stat1"]]
        return header

    def transform(self):
        # read the data from the csv
        self.df = pd.read_csv(self.csv, sep=' ', skiprows=self.config.get('skip_first_n'),
                              names=["timestamp", "Stat1"])
        # add a progress bar to view the current progress in the console
        with alive_bar(self.df.shape[0], dual_line=True,
                       title=f'Transforming file {self.index + 1}/{self.total_files}') as bar:
            # transform the timestamp
            self.transform_time(bar)
            # modify the value
            self.modify()
            # save transformed file to output folder
            self.save()

    def save(self):
        # get the new header in the required format
        self.df.columns = self.get_header()
        # save the df as txt file to the output folder
        self.df.to_csv(os.path.join(self.output_dir, get_file_name(self.file_name)+'.txt'), index=False, sep='\t')

    def transform_time(self, bar):
        # apply the transform_time_row function to every row in the dataset
        time_cols = self.df.apply((lambda x: transform_time_row(x, bar)), axis=1)
        # add headers to the new columns
        time_cols.columns = ['datetime', 'YY', 'MM', 'DD', 'HH', 'MN']
        # join the dataset with the new columns
        self.df = time_cols.join(self.df)
        # set the new pandas timestamp as index for resampling
        self.df.set_index('datetime', inplace=True)

    def modify(self):
        # if the modify flag in the config is set to False, remove the timestamp column and exit
        if self.config.get('modify_values') is False:
            self.df = self.df.drop('timestamp', axis=1)
            return
        # get the interval from the config
        interval = self.config.get('interval_minutes')
        # get the modifier from the config
        modifier = self.config.get('modifier')
        # resample the dataframe with the required interval and apply the modifier to the Stat1 column
        self.df = self.df.resample(f'{interval}T', label='right').agg({"YY": 'first',
                                                                       "MM": 'first',
                                                                       "DD": 'first',
                                                                       "HH": 'first',
                                                                       "MN": 'first',
                                                                       "Stat1": f'{modifier}'})


def main():
    Transformer().run()


if __name__ == "__main__":
    main()
