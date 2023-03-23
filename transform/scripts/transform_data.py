import pandas as pd
import os
import glob
from config_parser import get_config
from prepare_files import get_directory
from progress_bar import progress_bar


def get_file_name(file):
    # returns the file name without extension
    file_name = os.path.basename(file).split('.')[0]
    return file_name


def read_input_files(input_dir):
    # read all file names from the input folder
    csv_files = glob.glob(os.path.join(input_dir, "*.csv"))
    return csv_files


def transform_time_row(row, task, progress):
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
    progress.update(task, advance=1)
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
        self.progress = None

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
        with progress_bar() as self.progress:
            task_copy_file = self.progress.add_task(f'[red]Transforming file {self.file_name}',
                                                    total=self.df.shape[0]+1)
            # transform the timestamp
            self.transform_time(task_copy_file)
            # replace nan values
            self.replace_nan()
            # modify the value
            self.modify()
            # save transformed file to output folder
            self.save()
            # finish progress
            self.progress.update(task_copy_file, advance=1)

    def save(self):
        # get the new header in the required format
        self.df.columns = self.get_header()
        # generate the new filename based on the original file name and optionally the modifier, interval minutes, nan value identifier and replacement
        new_file_name = get_file_name(self.file_name)
        if self.config.get('modify_values') is True:
            new_file_name += f"_{self.config.get('modifier')}_{self.config.get('interval_minutes')}min"
        if self.config.get('replace_nan_values') is True:
            new_file_name += f"_nan-identifier-{self.config.get('nan_value_identifier')}_nan-replacement-{self.config.get('nan_value_replacement')}"
        new_file_name += ".txt"
        # save the df as txt file to the output folder with the new filename
        self.df.to_csv(os.path.join(self.output_dir, new_file_name), index=False, sep='\t')



    def transform_time(self, task):
        # apply the transform_time_row function to every row in the dataset
        time_cols = self.df.apply((lambda x: transform_time_row(x, task, self.progress)), axis=1)
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
### Original ####
    # def replace_nan(self):
    #     if self.config.get('replace_nan_values') is False:
    #         return
    #     replacement = self.config.get('nan_value_replacement') if isinstance(self.config.get('nan_value_replacement'),
    #                                                                          int) else float("NaN")
    #     identifier = self.config.get('nan_value_identifier')
    #     if identifier == '-':
    #         self.df['Stat1'] = self.df['Stat1'].apply(lambda x: x if x > 0 else replacement)
    #         return 
    #     self.df['Stat1'] = self.df['Stat1'].apply(lambda x: x if float(x) not in identifier else replacement)

###### Works fine with '-' and list of Int.  ##########
    # def replace_nan(self):
    #     if self.config.get('replace_nan_values') is False:
    #         return
    #     replacement = self.config.get('nan_value_replacement') if isinstance(self.config.get('nan_value_replacement'), int) else float("NaN")
    #     identifier = self.config.get('nan_value_identifier')
    #     if identifier == '-':
    #         self.df['Stat1'] = self.df['Stat1'].apply(lambda x: replacement if (isinstance(x, (int, float)) and x < 0) or x == '-' else x)
    #     else:
    #         ident_int = [i for i in identifier if isinstance(i, int) or (isinstance(i, str) and i.lstrip('-').isdigit())]
    #         ident_str = [i for i in identifier if isinstance(i, str) and not i.lstrip('-').isdigit()]
    #         self.df['Stat1'] = self.df['Stat1'].apply(lambda x: replacement if (isinstance(x, (int, float)) and x < 0 and '-' in identifier) or (x in ident_int) or (str(x) in ident_str) else x)


    def replace_nan(self):
        if self.config.get('replace_nan_values') is False:
            return
        replacement = self.config.get('nan_value_replacement') if isinstance(self.config.get('nan_value_replacement'), int) else float("NaN")
        identifier = self.config.get('nan_value_identifier')
        if isinstance(identifier, int):
            self.df['Stat1'] = self.df['Stat1'].apply(lambda x: replacement if x == identifier else x)
        elif isinstance(identifier, str):
            identifiers = [int(i) for i in identifier.split(',') if i.lstrip('-').isdigit()]
            if '-' in identifier:
                self.df['Stat1'] = self.df['Stat1'].apply(lambda x: replacement if (x in identifiers or x < 0) else x)
            else:
                self.df['Stat1'] = self.df['Stat1'].apply(lambda x: replacement if x in identifiers else x)


def main():
    Transformer().run()


if __name__ == "__main__":
    main()
