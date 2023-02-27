from argparse import ArgumentParser, Action
from prepare_files import get_directory
import os
from progress_bar import progress_bar
import pandas as pd
from rich import print
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import calendar

class ValidateMonth(Action):
    def __call__(self, parser, namespace, values, option_string=None):
        if values == 'all':
            values = list(range(1, 13))
            setattr(namespace, self.dest, values)
            return
        if int(values) not in range(1, 13):
            parser.error(f"Please enter a valid month. Got: {values}")
        values = [int(values)]
        setattr(namespace, self.dest, values)

################## New ValidateYear#####################
class ValidateYear(Action):
    def __call__(self, parser, namespace, values, option_string=None):
        if values == 'all':
            values = list(range(2000, 2030))
            setattr(namespace, self.dest, values)
            return
        if int(values) not in range(2013, 2030):
            parser.error(f"Please enter a valid Year. Got: {values}")   
        setattr(namespace, self.dest, int(values))
        setattr(namespace, 'year', int(values))  # add year as instance variable
###################################################################################          


class ValidateFile(Action):
    def __call__(self, parser, namespace, values, option_string=None):
        output_folder = get_directory('output')
        files = []
        if 'all' in values:
            for file_name in os.listdir(output_folder):
                file = os.path.join(output_folder, file_name)
                path, file_extension = os.path.splitext(file)
                if file_extension == '.txt' and os.path.isfile(file):
                    files.append(file)
        else:
            for value in values:
                file_name, file_extension = os.path.splitext(value)
                file_name = file_name + '.txt'
                file = os.path.join(output_folder, file_name)
                if not os.path.isfile(file):
                    parser.error(f"Cannot find file {file_name} in output folder. Is it spelled correctly?")
                files.append(file)
        setattr(namespace, self.dest, files)


def get_plot_folder(plot_base_folder, name):
    path = os.path.join(plot_base_folder, name)
    # create folder if it does not exist
    exists = os.path.exists(path)
    if not exists:
        print(f"[bold green]{name}[/] directory does not exist. Creating directory...")
        os.makedirs(path)
    return path


class Plotter:
    def __init__(self, files, months, is_plot_years, singlyear=None):
        self.files = files
        self.months = months
        self.is_plot_years = is_plot_years
        self.singlyear = singlyear # Add new instance variable
        self.plot_folder = get_directory('plots')
        self.current_df = None
        self.current_file_name = None
        self.current_plot_folder = None
        self.progress, self.task_transform_file, self.task_plot_all, self.task_plot_months, self.task_plot_year\
            = [None] * 5
        self.task_plot_singlyear = None # Add new progress task for the plot_years method

    def reset_progress_bars(self):
        self.progress.remove_task(self.task_transform_file)
        self.progress.remove_task(self.task_plot_all)
        if self.task_plot_months is not None:
            self.progress.remove_task(self.task_plot_months)
        if self.task_plot_year is not None:
            self.progress.remove_task(self.task_plot_year)
        if self.task_plot_singlyear is not None:
            self.progress.remove_task(self.task_plot_singlyear)    

    def run(self):
        with progress_bar() as self.progress:
            task_progress_file = self.progress.add_task("[red]Plotting files...", total=len(self.files))
            for index, file in enumerate(self.files):
                self.current_file_name, file_extension = os.path.splitext(os.path.basename(file))
                self.current_df = pd.read_csv(str(file), sep="\t", skiprows=4,
                                              dtype={'YY': str, 'MM': str, 'DD': str, 'HH': str})

                self.transform_time()
                self.current_plot_folder = get_plot_folder(self.plot_folder, self.current_file_name)
                self.plot_all()
                self.plot_months()

                if self.is_plot_years and self.singlyear is None:
                    self.plot_years()
                elif self.is_plot_years and self.singlyear is not None:
                    self.plot_singlyear() # Call new plot_singlyear() method

                self.progress.update(task_progress_file, advance=1)
                self.reset_progress_bars()

    def transform_time(self):
        #output_folder = r"C:\Users\annak\OneDrive\Documents\Master\Masterarbeit\GitHubMasterSkripts\MasterSkript\transform\output"
        # create a new task for transforming the time column
        self.task_transform_file = self.progress.add_task(f"[green]Preparing file {self.current_file_name}...",
                                                          total=self.current_df.shape[0] + 1)
        time_cols = self.current_df.apply(self.transform_time_row, axis=1)
        time_cols.columns = ['datetime']
        self.current_df = time_cols.join(self.current_df)
        # set the new pandas timestamp as index
        self.current_df.set_index('datetime', inplace=True, drop=False)
                # complete the progress
        self.progress.update(self.task_transform_file, advance=1)
        # # Save transformed dataframe as CSV
        # csv_file_name = f"{self.current_file_name}_transformed.csv"
        # self.current_df.to_csv(os.path.join(output_folder, csv_file_name), index=False)
        # print(self.current_df)


    def transform_time_row(self, row):
        # generate a pandas timestamp
        month = row['MM']
        minute = row['MM.1']
        timestamp = [pd.Timestamp(f'{row.YY}{month.zfill(2)}{row.DD.zfill(2)} {row.HH.zfill(2)}:{minute.zfill(2)}:00')]
        # create a pandas series
        series = pd.Series(timestamp)
        # progress the progress bar to the next step
        self.progress.update(self.task_transform_file, advance=1)
        return series

    def plot_all(self):
        self.task_plot_all = self.progress.add_task(f"[green]Plotting full graph...", total=1)
        file_name = self.current_file_name + '_total'
        fig, ax = plt.subplots(figsize=(15, 7))
        ax.plot(self.current_df.datetime, self.current_df.Stat1)
        plt.title(f'{self.current_file_name} Full Time Frame')
        plt.xlabel("Timeframe")
        plt.ylabel("Value")
        locator = mdates.AutoDateLocator()
        ax.xaxis.set_major_formatter(mdates.ConciseDateFormatter(locator))
        plt.savefig(os.path.join(self.current_plot_folder, file_name))
        self.progress.update(self.task_plot_all, advance=1)

    ############### Original#######################
    def plot_months(self):
        if self.months is None:
            return
        self.task_plot_months = self.progress.add_task(f"[green]Plotting months graph...", total=len(self.months))
        for month in self.months:
            file_name = self.current_file_name + '_month_' + calendar.month_name[month]
            month_df = self.current_df[self.current_df.index.month == month]
            piv = pd.pivot_table(month_df, index=['DD'], columns=['YY'], values=['Stat1'], sort=False)
            piv.plot(figsize=(15, 7))
            plt.title(f'{self.current_file_name} Yearly in Month {calendar.month_name[month]}')
            plt.xlabel("Day of the Month")
            plt.ylabel("Value")
            plt.savefig(os.path.join(self.current_plot_folder, file_name))
            self.progress.update(self.task_plot_months, advance=1)
    ####################################################
    
    # ######### NEW ##############
    # def plot_monthstest(self):
    #     if self.months is None:
    #         return
    #     self.task_plot_monthstest = self.progress.add_task(f"[green]Plotting month graph...", total=len(self.months))
    #     for month in self.months:
    #         file_name = self.current_file_name + '_month_' + calendar.month_name[month]
    #         month_df = self.current_df[self.current_df.index.month == month]
            ## if self.year is not None:
            ##     month_df = month_df[month_df.index.year == self.year]
    #         piv = pd.pivot_table(month_df, index=['DD'], columns=['YY'], values=['Stat1'], sort=False)
    #         piv.plot(figsize=(15, 7))
    #         #if self.year is not None:
    #         #    plt.title(f'{self.current_file_name} in {calendar.month_name[month]} {self.year}')
    #         #else:
    #         #    plt.title(f'{self.current_file_name} Yearly in Month {calendar.month_name[month]}')
    #         plt.xlabel("Day of the Month")
    #         plt.ylabel("Value")
    #         plt.savefig(os.path.join(self.current_plot_folder, file_name))
    #         self.progress.update(self.task_plot_months, advance=1)    
            
################## ORIGINAL##########################
    # def plot_years(self):
    #     if self.is_plot_years is False:
    #         return
    #     self.task_plot_year = self.progress.add_task(f"[green]Plotting years graph...", total=1)
    #     self.current_df['doy'] = self.current_df.index.dayofyear
    #     file_name = self.current_file_name + '_years'
    #     piv = pd.pivot_table(self.current_df, index=['doy'], columns=['YY'], values=['Stat1'])
    #     piv.plot(figsize=(15, 7))
    #     plt.title(f'{self.current_file_name} Each Year')
    #     plt.xlabel("Day of the Year")
    #     plt.ylabel("Value")
    #     plt.savefig(os.path.join(self.current_plot_folder, file_name))
    #     self.progress.update(self.task_plot_year, advance=1)
#######################################################

    def plot_years(self):
        self.task_plot_year = self.progress.add_task(f"[green]Plotting years graph...", total=1)
        self.current_df['doy'] = self.current_df.index.dayofyear
        file_name = self.current_file_name + '_years'
        piv = pd.pivot_table(self.current_df, index=['doy'], columns=['YY'], values=['Stat1'])
        piv.plot(figsize=(15, 7))
        plt.xlabel("Day of the Year")
        plt.ylabel("Value")
        plt.title(f'{self.current_file_name} Each Year')
        plt.savefig(os.path.join(self.current_plot_folder, file_name))
        self.progress.update(self.task_plot_year, advance=1)



    def plot_singlyear(self):
        self.task_plot_singlyear = self.progress.add_task(f"[green]Plotting year {self.singlyear[0]} graph...", total=1)
        self.current_df['doy'] = self.current_df.index.dayofyear
        year = self.singlyear[0]
        file_name = self.current_file_name + f'_{year}'
        year_df = self.current_df[self.current_df.index.year == year]
        piv = pd.pivot_table(year_df, index=['doy'], columns=['YY'], values=['Stat1'])
        piv.plot(figsize=(15, 7))
        plt.xlabel     


def main():
    parser = ArgumentParser()
    parser.add_argument("-f", "--files", nargs='+', dest="files", help="Specify the name(s) of the txt file(s) in the "
                                                                       "output folder you want to plot. Use 'all' for "
                                                                       "all files in output folder.",
                        metavar="FILE", action=ValidateFile, required=True)
    parser.add_argument("-y", "--years", dest="years", help="Plot each year in a graph.", action='store_true')
    parser.add_argument("-yr", "--singlyear", dest="singlyear", help="Specify a singl year you want to plot",
                         metavar="YEAR", action=ValidateYear, type=int)
    parser.add_argument("-m", "--months", dest="months", help="Plot the specified month of each year in a "
                                                              "graph. Use numbers from 1-12 to specify the month or "
                                                              "'all' for all months.",
                        metavar="MONTH", action=ValidateMonth)
    args = parser.parse_args()
    plotter = Plotter(files=args.files, months=args.months, is_plot_years=args.years)
    plotter.singlyear = [args.singlyear] if args.singlyear else None
    plotter.run()

if __name__ == "__main__":
    main()
