import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
import datetime as dt
import pytz

import pandas as pd
import pm4py
import visualizer
import algorithm
from pm4py.visualization.petri_net import visualizer
from pm4py.algo.decision_mining import algorithm as decision_mining

from pandastable import Table, TableModel

from os import listdir
from os.path import isfile, join

from tkinter import scrolledtext



# Received from her:
# df = pm4py.format_dataframe(df, case_id='case:concept:name', activity_key='concept:name', timestamp_key='time:timestamp')
# df['time:timestamp'] = pd.to_datetime(df['time:timestamp']).dt.tz_localize(None)
# filtered_log = pm4py.filter_time_range(df, "2016-01-09 00:00:00", "2016-02-18 23:59:59", mode='traces_contained')
# filtered_log.to_csv('/content/gdrive/MyDrive/Finalproject/bpi17-new/BPI17 filtertwomonth.csv',index=False)

class Calc:
    def __init__(self, csv_file):
        self.csv_file = csv_file

    def count(self, df_src, period, primary_key, event_value, new_count_col_name):

        #   Parameters:
        #    period: "By Day" or "By Month"
        #    primary_key:  subject column name, for example "bankerID"
        #    Note:  attribute_name:  for example "Loan Amount". doest participate in count()
        #    event_value:  it is in column case:concept. For example "disbursement"
        #    new_count_col_name

        pd.set_option('display.max_columns', None)
        print(df_src)

        # Filter row by banker id
        # df = df_src.loc[df_src['BankerID'] == banker_id]
        # df = df_src.copy()
        df = df_src

        pd.set_option('display.max_columns', None)
        print(df)

        # Using new_count_col_name as the column name and -1  for all its lines
        df[new_count_col_name] = -1
        print(df)

        for row_index in range(len(df)):
            if df.iloc[row_index][new_count_col_name] != -1:
                continue
            # banker_in_first_line = df.iloc[row_index]['BankerID']
            primary_key_in_first_line = df.iloc[row_index][primary_key]
            date_in_first_line = df.iloc[row_index]['time:timestamp']
            print("date_in_first_line: ", date_in_first_line)
            day_in_first_line = date_in_first_line[8:10]
            print("day_in_first_line: ", day_in_first_line)
            month_in_first_line = date_in_first_line[5:7]
            print("month_in_first_line: ", month_in_first_line)

            counter = 0
            day = day_in_first_line
            month = month_in_first_line

            for row_index2 in range(row_index, len(df)):
                # if df.iloc[row_index2]['BankerID'] == banker_in_first_line:
                if df.iloc[row_index2][primary_key] == primary_key_in_first_line:
                    date_in_line = df.iloc[row_index2]['time:timestamp']
                    day_in_line = date_in_line[8:10]
                    month_in_line = date_in_line[5:7]

                    if period == "By Day":
                        if day_in_line != day:
                            counter = 0
                            day = day_in_line
                    elif period == "By Month":
                        if month_in_line != month:
                            counter = 0
                            month = month_in_line

                    # if df.iloc[row_index2]['case:concept:name'] == case_concept:
                    if df.iloc[row_index2]["case:concept"] == event_value:
                        counter += 1
                    df.at[row_index2, new_count_col_name] = counter

        print("df to be saved in file " + self.csv_file + " is:")
        pd.set_option('display.max_columns', None)
        print(df)

        df.to_csv(self.csv_file, encoding='utf-8', index=False)

    # We want to sum loans that primary_key issues in one month
    def sum(self, df_src, period, primary_key, event_value, attribute_name, new_sum_col_name):
        #   Parameters:
        #    period: "By Day" or "By Month"
        #    primary_key:  subject column name, for example "bankerID"
        #    attribute_name:  this value should be summed, for example "Loan Amount"
        #    event_value:  it is in column "case:concept". For example "disbursement"
        #    new_sum_col_name: this new column should be created with the sum in each line

        # if not period == "per month":
        #     return

        pd.set_option('display.max_columns', None)
        print(df_src)

        # Filter row by banker id
        # df = df_src.loc[df_src['BankerID'] == banker_id]
        # df = df_src.copy()
        df = df_src

        pd.set_option('display.max_columns', None)
        print(df)

        # Using new_sum_col_name as the column name and -1  for all its lines
        df[new_sum_col_name] = -1
        print(df)

        for row_index in range(len(df)):
            if df.iloc[row_index][new_sum_col_name] != -1:
                continue
            subject_in_first_line = df.iloc[row_index][primary_key]
            date_in_first_line = df.iloc[row_index]['time:timestamp']
            print("date_in_first_line: ", date_in_first_line)
            day_in_first_line = date_in_first_line[8:10]
            print("day_in_first_line: ", day_in_first_line)
            month_in_first_line = date_in_first_line[5:7]
            print("month_in_first_line: ", month_in_first_line)

            the_sum = 0
            day = day_in_first_line
            month = month_in_first_line

            for row_index2 in range(row_index, len(df)):
                if df.iloc[row_index2][primary_key] == subject_in_first_line:
                    date_in_line = df.iloc[row_index2]['time:timestamp']
                    day_in_line = date_in_line[8:10]
                    month_in_line = date_in_line[5:7]

                    if period == "By Day":
                        if day_in_line != day:
                            the_sum = 0
                            day = day_in_line
                    elif period == "By Month":
                        if month_in_line != month:
                            the_sum = 0
                            month = month_in_line

                    if df.iloc[row_index2]["case:concept"] == event_value:
                        the_sum += df.iloc[row_index2][attribute_name]
                    df.at[row_index2, new_sum_col_name] = the_sum

        print("df to be saved in file " + self.csv_file + " is:")
        pd.set_option('display.max_columns', None)
        print(df)

        df.to_csv(self.csv_file, encoding='utf-8', index=False)

    # We want to average rates that a subject issues in one month
    def avg(self, df_src, period, primary_key, event_value, attribute_name, new_avg_col_name):
        #   Parameters:
        #    period: "By Day" or "By Month"
        #    primary_key:  subject column name, for example "bankerID"
        #    attribute_name:  this value should be summed, for example "Loan Amount"
        #    event_value:  it is in column "case:concept". For example "disbursement"
        #    new_sum_col_name: this new column should be created with the sum in each line

        pd.set_option('display.max_columns', None)
        print(df_src)

        # Filter row by banker id
        # df = df_src.loc[df_src['BankerID'] == banker_id]
        # df = df_src.copy()
        df = df_src

        pd.set_option('display.max_columns', None)
        print(df)

        # Using new_sum_col_name as the column name and -1  for all its lines
        df[new_avg_col_name] = -1
        print(df)

        for row_index in range(len(df)):
            if df.iloc[row_index][new_avg_col_name] != -1:
                continue
            subject_in_first_line = df.iloc[row_index][primary_key]
            date_in_first_line = df.iloc[row_index]['time:timestamp']
            print("date_in_first_line: ", date_in_first_line)
            day_in_first_line = date_in_first_line[8:10]
            print("day_in_first_line: ", day_in_first_line)
            month_in_first_line = date_in_first_line[5:7]
            print("month_in_first_line: ", month_in_first_line)

            count = 0
            the_sum = 0
            day = day_in_first_line
            month = month_in_first_line

            for row_index2 in range(row_index, len(df)):
                if df.iloc[row_index2][primary_key] == subject_in_first_line:
                    date_in_line = df.iloc[row_index2]['time:timestamp']
                    day_in_line = date_in_line[8:10]
                    month_in_line = date_in_line[5:7]

                    if period == "By Day":
                        if day_in_line != day:
                            count = 0
                            day = day_in_line
                    elif period == "By Month":
                        if month_in_line != month:
                            count = 0
                            month = month_in_line

                    if df.iloc[row_index2]["case:concept"] == event_value:
                        count += 1
                        the_sum += df.iloc[row_index2][attribute_name]
                    df.at[row_index2, new_avg_col_name] = the_sum / count if count > 0 else 0

        print("df to be saved in file " + self.csv_file + " is:")
        pd.set_option('display.max_columns', None)
        print(df)

        # dotPost = self.csv_file.rindex(".")
        # csvFileBeforeDot = self.csv_file[:dotPost]
        # new_file = csvFileBeforeDot + "-daily_loan_count.csv"
        # print("new file: " + new_file)
        # df.to_csv(new_file, encoding='utf-8', index=False)
        df.to_csv(self.csv_file, encoding='utf-8', index=False)


class Win1(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack()

        self.df = None
        self.csv_file = ""
        self.is_filter_displayed = False

        self.win4 = None

        self.master.geometry("800x400")
        self.master.title('ISCF GUI')
        self.master.resizable(False, False)

        # lbl_name = tk.Label(self.master, text="name")
        # lbl_name.place(x=30, y=50)
        #
        # txt_name = tk.Entry(self.master).place(x=80, y=50)
        # btnOk = tk.Button(self.master, text="name",
        #              command = lambda: self.on_btn_ok_clicked(lbl_name)).place(x=30, y=120)

        self.TOP_Y = 50

        current_y = self.TOP_Y

        btn_open_csv = ttk.Button(
            self.master,
            text='Select CSV File',
            command=self.open_text_file
        ).place(x=30, y=self.TOP_Y)

        btn_open_win4 = ttk.Button(
            self.master,
            text='List of Saved Files',
            command=self.open_win4
        ).place(x=30, y=self.TOP_Y + 30)

        var1 = tk.IntVar()
        chkboxFilter = tk.Checkbutton(self.master, text='Filter', variable=var1, onvalue=1,
                                      offvalue=0, command=self.display_filter_widgets)
        chkboxFilter.place(x=30, y=self.TOP_Y + 80)

        self.lbl_start_date = tk.Label(self.master, text="Start date")
        self.lbl_start_date.place(x=30, y=self.TOP_Y + 120)
        self.txt_start_date = tk.Entry(self.master, width=40)
        self.txt_start_date.place(x=100, y=self.TOP_Y + 120)
        self.lbl_end_date = tk.Label(self.master, text="End date")
        self.lbl_end_date.place(x=30, y=self.TOP_Y + 50)
        self.txt_end_date = tk.Entry(self.master, width=40)
        self.txt_end_date.place(x=100, y=self.TOP_Y + 150)

        self.btn_save_filtered_csv = ttk.Button(
            self.master,
            text='Save Filtered CSV',
            command=self.on_btn_save_filtered_csv_clicked
        )
        self.btn_save_filtered_csv.place(x=400, y=self.TOP_Y + 150)

        self.lbl_start_date.place_forget()
        self.txt_start_date.place_forget()
        self.lbl_end_date.place_forget()
        self.txt_end_date.place_forget()
        self.btn_save_filtered_csv.place_forget()

        btn_open_csv = ttk.Button(
            self.master,
            text='Display CSV',
            command=self.on_btn_display_csv_clicked
        ).place(x=30, y=self.TOP_Y + 200)

        # self.button_new_win.configure(command=self.new_window)

        btn_continue = ttk.Button(
            self.master,
            text='Continue',
            command=self.on_btn_continue_clicked
        )
        btn_continue.place(x=30, y=self.TOP_Y + 250)

        btn_update_count = ttk.Button(
            self.master,
            text='Update Daily Count',
            command=self.on_btn_update_count_clicked
        )
        btn_update_count.place(x=30, y=self.TOP_Y + 280)

        btn_update_banker_sum = ttk.Button(
            self.master,
            text='Update Banker Loan Sum',
            command=self.on_btn_update_sum_banker_loans_clicked
        )
        btn_update_banker_sum.place(x=160, y=self.TOP_Y + 280)

        btn_update_customer_sum = ttk.Button(
            self.master,
            text='Update Customer Loan Sum',
            command=self.on_btn_update_sum_customer_loans_clicked
        )
        btn_update_customer_sum.place(x=310, y=self.TOP_Y + 280)

        btn_update_customer_sum = ttk.Button(
            self.master,
            text='Update Banker Monthly Rate',
            command=self.on_btn_update_average_rate_per_banker_clicked
        )
        btn_update_customer_sum.place(x=470, y=self.TOP_Y + 280)

    def open_win4(self):
        self.win4 = tk.Toplevel(self.master)
        self.app = Win4(self.win4, self.df)

    def display_filter_widgets(self):
        if self.is_filter_displayed:
            self.lbl_start_date.place_forget()
            self.txt_start_date.place_forget()
            self.lbl_end_date.place_forget()
            self.txt_end_date.place_forget()
            self.btn_save_filtered_csv.place_forget()
        else:
            self.lbl_start_date.place(x=30, y=self.TOP_Y + 120)
            self.txt_start_date.place(x=100, y=self.TOP_Y + 120)
            self.lbl_end_date.place(x=30, y=self.TOP_Y + 150)
            self.txt_end_date.place(x=100, y=self.TOP_Y + 150)
            self.btn_save_filtered_csv.place(x=400, y=self.TOP_Y + 150)

        self.is_filter_displayed = not self.is_filter_displayed

    def on_btn_update_count_clicked(self):
        # print("date in df: ", self.df.iloc[1]['time:timestamp'])
        # self.txt_end_date.insert(0, self.df.iloc[-1]['time:timestamp'])
        case_consept = "disbursement"
        period = "per day"
        new_count_col_name = "bankerCount"

        # We want to count how many loans that employee give in one day
        self.count(self.df, period, case_consept, new_count_col_name)

    def on_btn_update_sum_banker_loans_clicked(self):
        # print("date in df: ", self.df.iloc[1]['time:timestamp'])
        # self.txt_end_date.insert(0, self.df.iloc[-1]['time:timestamp'])
        primary_key = "BankerID"
        new_sum_col_name = "bankerSumLoans"
        case_consept = "disbursement"
        period = "per month"

        # The sum of all loans that particular customer is allowed to get in a month
        self.sum_1(self.df, period, case_consept, primary_key, new_sum_col_name)

    def on_btn_update_sum_customer_loans_clicked(self):
        # print("date in df: ", self.df.iloc[1]['time:timestamp'])
        # self.txt_end_date.insert(0, self.df.iloc[-1]['time:timestamp'])
        primary_key = "CustomerID"
        new_sum_col_name = "customerSumLoans"
        case_consept = "disbursement"
        period = "per month"

        # The sum of all loans that particular customer is allowed to get in a month
        self.sum_1(self.df, period, case_consept, primary_key, new_sum_col_name)

    def on_btn_update_average_rate_per_banker_clicked(self):
        # print("date in df: ", self.df.iloc[1]['time:timestamp'])
        # self.txt_end_date.insert(0, self.df.iloc[-1]['time:timestamp'])
        primary_key = "BankerID"
        new_avg_col_name = "bankerMonthlyAvgRate"
        case_consept = "disbursement"
        period = "per month"

        # The sum of all loans that particular customer is allowed to get in a month
        self.average_rate_per_subject_1(self.df, period, case_consept, primary_key, new_avg_col_name)

    # We want to count how many loans that employee give in one day
    def count_1(self, df_src, period, case_concept, new_count_col_name):
        # if not period == "per day":
        #    return

        pd.set_option('display.max_columns', None)
        print(df_src)

        # Filter row by banker id
        # df = df_src.loc[df_src['BankerID'] == banker_id]
        df = df_src.copy()

        pd.set_option('display.max_columns', None)
        print(df)

        # Using new_count_col_name as the column name and -1  for all its lines
        df[new_count_col_name] = -1
        print(df)

        for row_index in range(len(df)):
            if df.iloc[row_index][new_count_col_name] != -1:
                continue
            banker_in_first_line = df.iloc[row_index]['BankerID']
            date_in_first_line = df.iloc[row_index]['time:timestamp']
            print("date_in_first_line: ", date_in_first_line)

            day_in_first_line = date_in_first_line[8:10]
            print("day_in_first_line: ", day_in_first_line)
            month_in_first_line = date_in_first_line[5:7]
            print("month_in_first_line: ", month_in_first_line)

            # if period == "by day":
            # elif period == "by month":

            counter = 0
            day = day_in_first_line
            month = month_in_first_line

            for row_index2 in range(row_index, len(df)):
                if df.iloc[row_index2]['BankerID'] == banker_in_first_line:
                    date_in_line = df.iloc[row_index2]['time:timestamp']
                    day_in_line = date_in_line[8:10]
                    month_in_line = date_in_line[5:7]

                    if period == "by day":
                        if day_in_line != day:
                            counter = 0
                            day = day_in_line
                    elif period == "by month":
                        if month_in_line != month:
                            counter = 0
                            month = month_in_line

                    if df.iloc[row_index2]['case:concept:name'] == case_concept:
                        counter += 1
                    df.at[row_index2, new_count_col_name] = counter

        pd.set_option('display.max_columns', None)
        print(df)

        dotPost = self.csv_file.rindex(".")
        csvFileBeforeDot = self.csv_file[:dotPost]
        new_file = csvFileBeforeDot + "-daily_loan_count.csv"
        print("new file: " + new_file)
        df.to_csv(new_file, encoding='utf-8', index=False)

    # We want to sum how many loans that subject issues in one month
    def sum_1(self, df_src, period, case_concept, primary_key, new_sum_col_name):
        if not period == "per month":
            return

        pd.set_option('display.max_columns', None)
        print(df_src)

        # Filter row by banker id
        # df = df_src.loc[df_src['BankerID'] == banker_id]
        df = df_src.copy()

        pd.set_option('display.max_columns', None)
        print(df)

        # Using new_sum_col_name as the column name and -1  for all its lines
        df[new_sum_col_name] = -1
        print(df)

        for row_index in range(len(df)):
            if df.iloc[row_index][new_sum_col_name] != -1:
                continue
            subject_in_first_line = df.iloc[row_index][primary_key]
            date_in_first_line = df.iloc[row_index]['time:timestamp']
            print("date_in_first_line: ", date_in_first_line)
            month_in_first_line = date_in_first_line[5:7]
            print("month_in_first_line: ", month_in_first_line)

            sum = 0
            month = month_in_first_line

            for row_index2 in range(row_index, len(df)):
                if df.iloc[row_index2][primary_key] == subject_in_first_line:
                    date_in_line = df.iloc[row_index2]['time:timestamp']
                    month_in_line = date_in_line[5:7]
                    if month_in_line != month:
                        sum = 0
                        month = month_in_line

                    if df.iloc[row_index2]['case:concept:name'] == case_concept:
                        sum += df.iloc[row_index2]['Loan Amount']
                    df.at[row_index2, new_sum_col_name] = sum

        pd.set_option('display.max_columns', None)
        print(df)

        dotPost = self.csv_file.rindex(".")
        csvFileBeforeDot = self.csv_file[:dotPost]
        new_file = csvFileBeforeDot + "-" + primary_key + "-monthly_loan_sum.csv"
        print("new file: " + new_file)
        df.to_csv(new_file, encoding='utf-8', index=False)

    # We want to average rates that a subject issues in one month
    def average_rate_per_subject_1(self, df_src, period, case_concept, primary_key, new_avg_col_name):
        if not period == "per month":
            return

        pd.set_option('display.max_columns', None)
        print(df_src)

        # Filter row by banker id
        # df = df_src.loc[df_src['BankerID'] == banker_id]
        df = df_src.copy()

        pd.set_option('display.max_columns', None)
        print(df)

        # Using new_sum_col_name as the column name and -1  for all its lines
        df[new_avg_col_name] = -1
        print(df)

        for row_index in range(len(df)):
            if df.iloc[row_index][new_avg_col_name] != -1:
                continue
            subject_in_first_line = df.iloc[row_index][primary_key]
            date_in_first_line = df.iloc[row_index]['time:timestamp']
            print("date_in_first_line: ", date_in_first_line)
            month_in_first_line = date_in_first_line[5:7]
            print("month_in_first_line: ", month_in_first_line)

            count = 0
            sum = 0
            month = month_in_first_line

            for row_index2 in range(row_index, len(df)):
                if df.iloc[row_index2][primary_key] == subject_in_first_line:
                    date_in_line = df.iloc[row_index2]['time:timestamp']
                    month_in_line = date_in_line[5:7]
                    if month_in_line != month:
                        count = 0
                        sum = 0
                        month = month_in_line

                    if df.iloc[row_index2]['case:concept:name'] == case_concept:
                        count += 1
                        sum += df.iloc[row_index2]['Interest Rate']
                    df.at[row_index2, new_avg_col_name] = sum / count if count > 0 else 0

        pd.set_option('display.max_columns', None)
        print(df)

        dotPost = self.csv_file.rindex(".")
        csvFileBeforeDot = self.csv_file[:dotPost]
        new_file = csvFileBeforeDot + "-" + primary_key + "-monthly_avg_rate.csv"
        print("new file: " + new_file)
        df.to_csv(new_file, encoding='utf-8', index=False)

    def on_btn_save_filtered_csv_clicked(self):
        self.df = pm4py.format_dataframe(self.df,
                                         case_id='case:concept:name', activity_key='concept:name',
                                         timestamp_key='time:timestamp')
        # self.df['time:timestamp'] = pd.to_datetime(self.df['time:timestamp']).dt.tz_localize(None)

        start_date = self.txt_start_date.get()
        end_date = self.txt_end_date.get()

        print("start_date[19]: ", start_date[:19])

        filtered_log = pm4py.filter_time_range(self.df, start_date[:19],
                                               end_date[:19],
                                               mode='traces_contained')

        dotPost = self.csv_file.rindex(".")
        csvFileBeforeDot = self.csv_file[:dotPost]
        new_file = csvFileBeforeDot + "-2.csv"
        print("new file: " + new_file)
        filtered_log.to_csv(new_file, index=False)

    def on_btn_ok_clicked(self, lbl_name):
        lbl_name.config(text="hello")

    def on_btn_continue_clicked(self):
        self.win3 = tk.Toplevel(self.master)

        print("The df in win1 is")
        print(self.df)

        self.app = Win3(self.win3, self.df, self.csv_file)

    def on_btn_display_csv_clicked(self):
        self.new_window()

    def open_text_file(self):
        # file type
        filetypes = (
            ('CSV files', '*.csv'),
            ('All files', '*.*')
        )
        # show the open file dialog
        f = fd.askopenfile(filetypes=filetypes)
        print("file name: ", f.name)
        self.csv_file = f.name
        self.df = pd.read_csv(self.csv_file)

        print("date in df: ", self.df.iloc[1]['time:timestamp'])
        self.txt_start_date.delete(0, tk.END)
        self.txt_start_date.insert(0, self.df.iloc[1]['time:timestamp'])

        self.txt_end_date.delete(0, tk.END)
        self.txt_end_date.insert(0, self.df.iloc[-1]['time:timestamp'])

        # read the text file and show its content on the Text
        # Works great
        # lbl_screen.insert('1.0', f.readlines())

        # self.new_window()

    # Call back function
    def new_window(self):
        # self.df['time:timestamp'] = pd.to_datetime(self.df['time:timestamp'])
        # start_date = self.txt_start_date.get();
        # end_date = self.txt_end_date.get();
        ## self.df[(self.df['time:timestamp'] >= start_date) &
        ##         (self.df['time:timestamp'] =< '2014-07-23 09:00:00')]
        # self.df = self.df[(self.df['time:timestamp'] >= start_date) &
        #                  (self.df['time:timestamp'] <= end_date)]
        self.newWindow = tk.Toplevel(self.master)
        self.app = Win2(self.newWindow, self.df, self.csv_file)


class Win2(tk.Frame):
    # def __init__(self,master):
    #
    #     super().__init__(master)
    #     # self.pack()
    #     self.master.geometry("1200x800")
    #     self.master.title("window 2")
    #
    #     # take the data
    #     lst = [(1, 'Raj', 'Mumbai', 19),
    #            (2, 'Aaryan', 'Pune', 18),
    #            (3, 'Vaishnavi', 'Mumbai', 20),
    #            (4, 'Rachna', 'Mumbai', 21),
    #            (5, 'Shubham', 'Delhi', 21)]
    #
    #     # find total number of rows and
    #     # columns in list
    #     total_rows = len(lst)
    #     total_columns = len(lst[0])
    #     Table(self.master, total_rows, total_columns, lst)
    def __init__(self, master, df, csv_file):
        master.geometry('1200x400+200+100')
        master.title('CSV Table')
        f = tk.Frame(master)
        f.pack(fill=tk.BOTH, expand=1)
        # df = TableModel.getSampleData()
        # self.df = pd.read_csv(csv_file)
        self.df = df
        self.table = pt = Table(f, dataframe=self.df,
                                showtoolbar=True, showstatusbar=True)
        self.csv_file = csv_file
        pt.show()
        return

    def quit_window(self):
        self.master.destroy()


class Win3(tk.Frame):
    def __init__(self, master, df, csv_file):
        super().__init__(master)

        self.df = df
        self.master = master
        self.master.geometry("700x600")
        # self.master.title('Functions Screen')
        # self.master.resizable(False, False)
        self.csv_file = csv_file

        self.tab_parent = ttk.Notebook(master)
        tab1 = ttk.Frame(self.tab_parent)
        tab2 = ttk.Frame(self.tab_parent)
        tab3 = ttk.Frame(self.tab_parent)
        tab4 = ttk.Frame(self.tab_parent)
        self.tab_parent.add(tab1, text="Count")
        self.tab_parent.add(tab2, text="Sum")
        self.tab_parent.add(tab3, text="Avg")
        self.tab_parent.add(tab4, text="Diff time")

        self.tab_parent.pack(expand=1, fill='both')

        # ==== tab1 widgets ==================================

        # var = IntVar()
        # R1 = Radiobutton(root, text="Option 1", variable=var, value=1,
        #                  command=sel)

        self.selected_radio_button1 = tk.IntVar()
        self.selected_radio_button1.set(1)
        radiobutton1 = tk.Radiobutton(tab1, text='Single Parameter Version', variable=self.selected_radio_button1,
                                      value=1,
                                      command=self.on_tab1_radio_button_clicked)
        radiobutton1.place(x=30, y=50)

        radiobutton2 = tk.Radiobutton(tab1, text='Single Parameter & Condition', variable=self.selected_radio_button1,
                                      value=2,
                                      command=self.on_tab1_radio_button_clicked)
        radiobutton2.place(x=30, y=80)

        radiobutton3 = tk.Radiobutton(tab1, text='Single Parameter & Function', variable=self.selected_radio_button1,
                                      value=3,
                                      command=self.on_tab1_radio_button_clicked)
        radiobutton3.place(x=30, y=110)

        radiobutton4 = tk.Radiobutton(tab1, text='Two parameters version', variable=self.selected_radio_button1,
                                      value=4,
                                      command=self.on_tab1_radio_button_clicked)
        radiobutton4.place(x=30, y=140)

        radiobutton5 = tk.Radiobutton(tab1, text='Two parameters & Condition', variable=self.selected_radio_button1,
                                      value=5,
                                      command=self.on_tab1_radio_button_clicked)
        radiobutton5.place(x=30, y=170)

        radiobutton6 = tk.Radiobutton(tab1, text='Two parameters & Function', variable=self.selected_radio_button1,
                                      value=6,
                                      command=self.on_tab1_radio_button_clicked)
        radiobutton6.place(x=30, y=200)

        print("The df in win3 is")
        print(self.df.head())

        # ===== start - Right pane of tab1 ========

        self.lbl_primary_key = tk.Label(tab1, text="Primary Key")
        self.lbl_primary_key.place(x=420, y=50)

        self.var_primary_key1 = tk.StringVar()
        self.combobox_primary_key1 = ttk.Combobox(tab1, textvariable=self.var_primary_key1)
        self.combobox_primary_key1.place(x=500, y=50)
        # Populate combobox with the dataframe titles
        self.combobox_primary_key1['values'] = list(self.df.columns)
        self.combobox_primary_key1.current(2)
        # prevent typing a value
        self.combobox_primary_key1['state'] = 'readonly'

        #   var_primary_key1.get()  - selected value in combobox

        self.lbl_attribute = tk.Label(tab1, text="Attribute")
        self.lbl_attribute.place(x=420, y=80)

        self.var_attribute1 = tk.StringVar()
        self.combobox_attribute1 = ttk.Combobox(tab1, textvariable=self.var_attribute1)
        self.combobox_attribute1.place(x=500, y=80)
        # Populate combobox with the dataframe titles
        self.combobox_attribute1['values'] = list(self.df.columns)
        self.combobox_attribute1.current(3)
        # prevent typing a value
        self.combobox_attribute1['state'] = 'readonly'

        self.lbl_time_range = tk.Label(tab1, text="Time Range")
        self.lbl_time_range.place(x=420, y=110)

        self.var_time_range1 = tk.StringVar()
        self.combobox_time_range1 = ttk.Combobox(tab1, textvariable=self.var_time_range1)
        self.combobox_time_range1.place(x=500, y=110)
        # Populate combobox with the dataframe titles
        self.combobox_time_range1['values'] = ["By Day", "By Month"]
        self.combobox_time_range1.current(0)
        # prevent typing a value
        self.combobox_time_range1['state'] = 'readonly'

        # self.lbl_time_range = tk.Label(tab1, text="Time Range")
        # self.lbl_time_range.place(x=420, y=110)

        self.lbl_event_value = tk.Label(tab1, text="Event Value")
        self.lbl_event_value.place(x=420, y=140)

        self.var_event_value1 = tk.StringVar()
        self.combobox_event_value1 = ttk.Combobox(tab1, width=27, textvariable=self.var_event_value1)
        self.combobox_event_value1.place(x=500, y=140)
        # Populate combobox with the dataframe concept:name unique column values
        self.combobox_event_value1['values'] = list(set(self.df["case:concept"].tolist()))
        self.combobox_event_value1.current(5)
        # prevent typing a value
        self.combobox_event_value1['state'] = 'readonly'

        self.lbl_foreign_key = tk.Label(tab1, text="foreign_key")
        self.lbl_foreign_key.place(x=420, y=170)
        self.lbl_foreign_key.place_forget()

        self.var_foreign_key1 = tk.StringVar()
        self.combobox_foreign_key1 = ttk.Combobox(tab1, width=27, textvariable=self.var_foreign_key1)
        self.combobox_foreign_key1.place(x=500, y=170)
        self.combobox_foreign_key1.place_forget()
        # Populate combobox with the dataframe titles
        self.combobox_foreign_key1['values'] = list(self.df.columns)
        # prevent typing a value
        self.combobox_foreign_key1['state'] = 'readonly'

        self.lbl_function = tk.Label(tab1, text="Function")
        self.lbl_function.place(x=420, y=200)
        self.lbl_function.place_forget()

        self.var_function1 = tk.StringVar()
        self.combobox_function1 = ttk.Combobox(tab1, width=27, textvariable=self.var_function1)

        self.combobox_function1.place_forget()
        # Populate combobox with the dataframe concept:name unique column values
        self.combobox_function1['values'] = ["sum", "average", "count", "diff time"]
        # prevent typing a value
        self.combobox_function1['state'] = 'readonly'

        self.lbl_condition = tk.Label(tab1, text="Condition")
        self.lbl_condition.place(x=420, y=240)
        self.lbl_condition.place_forget()

        self.lbl_operator = tk.Label(tab1, text="Operator")
        self.lbl_operator.place(x=440, y=270)
        self.lbl_operator.place_forget()
        self.var_condition1 = tk.StringVar()
        self.combobox_condition1 = ttk.Combobox(tab1, textvariable=self.var_condition1)
        self.combobox_condition1.place(x=520, y=270)
        self.combobox_condition1.place_forget()
        # Populate combobox with the dataframe titles
        self.combobox_condition1['values'] = ["<", ">", "=", "!=", ">=", "<="]
        # prevent typing a value
        self.combobox_condition1['state'] = 'readonly'

        self.lbl_value = tk.Label(tab1, text="Value")
        self.lbl_value.place(x=440, y=300)
        self.lbl_value.place_forget()
        self.txt_value = tk.Entry(tab1, width=23)
        self.txt_value.place(x=520, y=300)
        self.txt_value.place_forget()

        # ======end - Right pane of tab1 ===============

        self.btn_add1 = ttk.Button(
            tab1,
            text='Add',
            command=self.on_tab1_btn_add
        )
        self.btn_add1.place(x=300, y=530)

        self.btn_next1 = ttk.Button(
            tab1,
            text='Next',
            command=self.on_btn_next
        ).place(x=380, y=530)

        # ====  tab2 widgets ==================================

        self.selected_radio_button2 = tk.IntVar()
        self.selected_radio_button2.set(1)
        radiobutton1b = tk.Radiobutton(tab2, text='Single Parameter Version', variable=self.selected_radio_button2,
                                       value=1,
                                       command=self.on_tab2_radio_button_clicked)
        radiobutton1b.place(x=30, y=50)

        radiobutton2b = tk.Radiobutton(tab2, text='Single Parameter & Condition', variable=self.selected_radio_button2,
                                       value=2,
                                       command=self.on_tab2_radio_button_clicked)
        radiobutton2b.place(x=30, y=80)

        radiobutton3b = tk.Radiobutton(tab2, text='Single Parameter & Function', variable=self.selected_radio_button2,
                                       value=3,
                                       command=self.on_tab2_radio_button_clicked)

        radiobutton3b.place(x=30, y=110)

        radiobutton4b = tk.Radiobutton(tab2, text='Two parameters version', variable=self.selected_radio_button2,
                                       value=4,
                                       command=self.on_tab2_radio_button_clicked)

        radiobutton4b.place(x=30, y=140)

        radiobutton5b = tk.Radiobutton(tab2, text='Two parameters & Condition', variable=self.selected_radio_button2,
                                       value=5,
                                       command=self.on_tab2_radio_button_clicked)

        radiobutton5b.place(x=30, y=170)

        radiobutton6b = tk.Radiobutton(tab2, text='Two parameters & Function', variable=self.selected_radio_button2,
                                       value=6,
                                       command=self.on_tab2_radio_button_clicked)

        radiobutton6b.place(x=30, y=200)

        # ===== start - Right pane of tab2 ========

        self.lbl_primary_key2 = tk.Label(tab2, text="Primary Key")
        self.lbl_primary_key2.place(x=420, y=50)

        self.var_primary_key2 = tk.StringVar()
        self.combobox_primary_key2 = ttk.Combobox(tab2, textvariable=self.var_primary_key2)
        self.combobox_primary_key2.place(x=500, y=50)
        # Populate combobox with the dataframe titles
        self.combobox_primary_key2['values'] = list(self.df.columns)
        self.combobox_primary_key2.current(2)
        # prevent typing a value
        self.combobox_primary_key2['state'] = 'readonly'

        #   var_primary_key1.get()  - selected value in combobox

        self.lbl_attribute2 = tk.Label(tab2, text="Attribute")
        self.lbl_attribute2.place(x=420, y=80)

        self.var_attribute2 = tk.StringVar()
        self.combobox_attribute2 = ttk.Combobox(tab2, textvariable=self.var_attribute2)
        self.combobox_attribute2.place(x=500, y=80)
        # Populate combobox with the dataframe titles
        self.combobox_attribute2['values'] = list(self.df.columns)
        self.combobox_attribute2.current(3)
        # prevent typing a value
        self.combobox_attribute2['state'] = 'readonly'

        self.lbl_time_range2 = tk.Label(tab2, text="Time Range")
        self.lbl_time_range2.place(x=420, y=110)

        self.var_time_range2 = tk.StringVar()
        self.combobox_time_range2 = ttk.Combobox(tab2, textvariable=self.var_time_range2)
        self.combobox_time_range2.place(x=500, y=110)
        # Populate combobox with the dataframe titles
        self.combobox_time_range2['values'] = ["By Day", "By Month"]
        self.combobox_time_range2.current(0)
        # prevent typing a value
        self.combobox_time_range2['state'] = 'readonly'

        # self.lbl_time_range = tk.Label(tab2, text="Time Range")
        # self.lbl_time_range.place(x=420, y=110)

        self.lbl_event_value2 = tk.Label(tab2, text="Event Value")
        self.lbl_event_value2.place(x=420, y=140)

        self.var_event_value2 = tk.StringVar()
        self.combobox_event_value2 = ttk.Combobox(tab2, width=27, textvariable=self.var_event_value2)
        self.combobox_event_value2.place(x=500, y=140)
        # Populate combobox with the dataframe concept:name unique column values
        self.combobox_event_value2['values'] = list(set(self.df["case:concept"].tolist()))
        self.combobox_event_value2.current(5)
        # prevent typing a value
        self.combobox_event_value2['state'] = 'readonly'

        self.lbl_foreign_key2 = tk.Label(tab2, text="foreign_key")
        self.lbl_foreign_key2.place(x=420, y=170)
        self.lbl_foreign_key2.place_forget()

        self.var_foreign_key2 = tk.StringVar()
        self.combobox_foreign_key2 = ttk.Combobox(tab2, width=27, textvariable=self.var_foreign_key2)
        self.combobox_foreign_key2.place(x=500, y=170)
        self.combobox_foreign_key2.place_forget()
        # Populate combobox with the dataframe titles
        self.combobox_foreign_key2['values'] = list(self.df.columns)
        # prevent typing a value
        self.combobox_foreign_key2['state'] = 'readonly'

        self.lbl_function2 = tk.Label(tab2, text="Function")
        self.lbl_function2.place(x=420, y=200)
        self.lbl_function2.place_forget()

        self.var_function2 = tk.StringVar()
        self.combobox_function2 = ttk.Combobox(tab2, width=27, textvariable=self.var_function2)

        self.combobox_function2.place_forget()
        # Populate combobox with the dataframe concept:name unique column values
        self.combobox_function2['values'] = ["sum", "average", "count", "diff time"]
        # prevent typing a value
        self.combobox_function2['state'] = 'readonly'

        self.lbl_condition2 = tk.Label(tab2, text="Condition")
        self.lbl_condition2.place(x=420, y=240)
        self.lbl_condition2.place_forget()

        self.lbl_operator2 = tk.Label(tab2, text="Operator")
        self.lbl_operator2.place(x=440, y=270)
        self.lbl_operator2.place_forget()
        self.var_condition2 = tk.StringVar()
        self.combobox_condition2 = ttk.Combobox(tab2, textvariable=self.var_condition2)
        self.combobox_condition2.place(x=520, y=270)
        self.combobox_condition2.place_forget()
        # Populate combobox with the dataframe titles
        self.combobox_condition2['values'] = ["<", ">", "=", "!=", ">=", "<="]
        # prevent typing a value
        self.combobox_condition2['state'] = 'readonly'

        self.lbl_value2 = tk.Label(tab2, text="Value")
        self.lbl_value2.place(x=440, y=300)
        self.lbl_value2.place_forget()
        self.txt_value2 = tk.Entry(tab2, width=23)
        self.txt_value2.place(x=520, y=300)
        self.txt_value2.place_forget()

        # ======end - Right pane of tab2 ===============

        btn_add2 = ttk.Button(
            tab2,
            text='Add',
            command=self.on_tab2_btn_add
        ).place(x=300, y=530)

        btn_next2 = ttk.Button(
            tab2,
            text='Next',
            # command = self.on_btn_next
        ).place(x=380, y=530)

        # ====  tab3 widgets ==================================

        self.selected_radio_button3 = tk.IntVar()
        self.selected_radio_button3.set(1)
        radiobutton1c = tk.Radiobutton(tab3, text='Single Parameter Version', variable=self.selected_radio_button3,
                                       value=1,
                                       command=self.on_tab3_radio_button_clicked)
        radiobutton1c.place(x=30, y=50)

        radiobutton2c = tk.Radiobutton(tab3, text='Single Parameter & Condition', variable=self.selected_radio_button3,
                                       value=2,
                                       command=self.on_tab3_radio_button_clicked)
        radiobutton2c.place(x=30, y=80)

        radiobutton3c = tk.Radiobutton(tab3, text='Single Parameter & Function', variable=self.selected_radio_button3,
                                       value=3,
                                       command=self.on_tab3_radio_button_clicked)

        radiobutton3c.place(x=30, y=110)

        radiobutton4c = tk.Radiobutton(tab3, text='Two parameters version', variable=self.selected_radio_button3,
                                       value=4,
                                       command=self.on_tab3_radio_button_clicked)

        radiobutton4c.place(x=30, y=140)

        radiobutton5c = tk.Radiobutton(tab3, text='Two parameters & Condition', variable=self.selected_radio_button3,
                                       value=5,
                                       command=self.on_tab3_radio_button_clicked)
        radiobutton5c.place(x=30, y=170)

        radiobutton6c = tk.Radiobutton(tab3, text='Two parameters & Function', variable=self.selected_radio_button3,
                                       value=6,
                                       command=self.on_tab3_radio_button_clicked)

        radiobutton6c.place(x=30, y=200)

        # ===== start - Right pane of tab3 ========

        self.lbl_primary_key3 = tk.Label(tab3, text="Primary Key")
        self.lbl_primary_key3.place(x=420, y=50)

        self.var_primary_key3 = tk.StringVar()
        self.combobox_primary_key3 = ttk.Combobox(tab3, textvariable=self.var_primary_key3)
        self.combobox_primary_key3.place(x=500, y=50)
        # Populate combobox with the dataframe titles
        self.combobox_primary_key3['values'] = list(self.df.columns)
        self.combobox_primary_key3.current(2)
        # prevent typing a value
        self.combobox_primary_key3['state'] = 'readonly'

        #   var_primary_key1.get()  - selected value in combobox

        self.lbl_attribute3 = tk.Label(tab3, text="Attribute")
        self.lbl_attribute3.place(x=420, y=80)

        self.var_attribute3 = tk.StringVar()
        self.combobox_attribute3 = ttk.Combobox(tab3, textvariable=self.var_attribute3)
        self.combobox_attribute3.place(x=500, y=80)
        # Populate combobox with the dataframe titles
        self.combobox_attribute3['values'] = list(self.df.columns)
        self.combobox_attribute3.current(3)
        # prevent typing a value
        self.combobox_attribute3['state'] = 'readonly'

        self.lbl_time_range3 = tk.Label(tab3, text="Time Range")
        self.lbl_time_range3.place(x=420, y=110)

        self.var_time_range3 = tk.StringVar()
        self.combobox_time_range3 = ttk.Combobox(tab3, textvariable=self.var_time_range3)
        self.combobox_time_range3.place(x=500, y=110)
        # Populate combobox with the dataframe titles
        self.combobox_time_range3['values'] = ["By Day", "By Month"]
        self.combobox_time_range3.current(0)
        # prevent typing a value
        self.combobox_time_range3['state'] = 'readonly'

        # self.lbl_time_range = tk.Label(tab3, text="Time Range")
        # self.lbl_time_range.place(x=420, y=110)

        self.lbl_event_value3 = tk.Label(tab3, text="Event Value")
        self.lbl_event_value3.place(x=420, y=140)

        self.var_event_value3 = tk.StringVar()
        self.combobox_event_value3 = ttk.Combobox(tab3, width=27, textvariable=self.var_event_value3)
        self.combobox_event_value3.place(x=500, y=140)
        # Populate combobox with the dataframe concept:name unique column values
        self.combobox_event_value3['values'] = list(set(self.df["case:concept"].tolist()))
        self.combobox_event_value3.current(5)
        # prevent typing a value
        self.combobox_event_value3['state'] = 'readonly'

        self.lbl_foreign_key3 = tk.Label(tab3, text="foreign_key")
        self.lbl_foreign_key3.place(x=420, y=170)
        self.lbl_foreign_key3.place_forget()

        self.var_foreign_key3 = tk.StringVar()
        self.combobox_foreign_key3 = ttk.Combobox(tab3, width=27, textvariable=self.var_foreign_key3)
        self.combobox_foreign_key3.place(x=500, y=170)
        self.combobox_foreign_key3.place_forget()
        # Populate combobox with the dataframe titles
        self.combobox_foreign_key3['values'] = list(self.df.columns)
        # prevent typing a value
        self.combobox_foreign_key3['state'] = 'readonly'

        self.lbl_function3 = tk.Label(tab3, text="Function")
        self.lbl_function3.place(x=420, y=200)
        self.lbl_function3.place_forget()

        self.var_function3 = tk.StringVar()
        self.combobox_function3 = ttk.Combobox(tab3, width=27, textvariable=self.var_function3)

        self.combobox_function3.place_forget()
        # Populate combobox with the dataframe concept:name unique column values
        self.combobox_function3['values'] = ["sum", "average", "count", "diff time"]
        # prevent typing a value
        self.combobox_function3['state'] = 'readonly'

        self.lbl_condition3 = tk.Label(tab3, text="Condition")
        self.lbl_condition3.place(x=420, y=240)
        self.lbl_condition3.place_forget()

        self.lbl_operator3 = tk.Label(tab3, text="Operator")
        self.lbl_operator3.place(x=440, y=270)
        self.lbl_operator3.place_forget()
        self.var_condition3 = tk.StringVar()
        self.combobox_condition3 = ttk.Combobox(tab3, textvariable=self.var_condition3)
        self.combobox_condition3.place(x=520, y=270)
        self.combobox_condition3.place_forget()
        # Populate combobox with the dataframe titles
        self.combobox_condition3['values'] = ["<", ">", "=", "!=", ">=", "<="]
        # prevent typing a value
        self.combobox_condition3['state'] = 'readonly'

        self.lbl_value3 = tk.Label(tab3, text="Value")
        self.lbl_value3.place(x=440, y=300)
        self.lbl_value3.place_forget()
        self.txt_value3 = tk.Entry(tab3, width=23)
        self.txt_value3.place(x=520, y=300)
        self.txt_value3.place_forget()

        # ======end - Right pane of tab3 ===============

        btn_add3 = ttk.Button(
            tab3,
            text='Add',
            command=self.on_tab3_btn_add
        ).place(x=300, y=530)

        btn_next3 = ttk.Button(
            tab3,
            text='Next',
            command=self.on_btn_next
        ).place(x=380, y=530)

    # This is the add button for the "count" tab
    def on_tab1_btn_add(self):

        print("Current tab is: ", self.tab_parent.index("current"))

        primary_key = self.var_primary_key1.get()
        attribute_name = self.var_attribute1.get()
        # case_consept = "disbursement"
        attribute_value = self.var_event_value1.get()
        # period = "per day"
        period = self.var_time_range1.get()

        event_value = self.var_event_value1.get()

        new_count_col_name = "None"
        if period == "By Day":
            new_count_col_name = "count " + attribute_name + " ByDay"
        elif period == "By Month":
            new_count_col_name = "count " + attribute_name + " ByMonth"

        # def count(self, df_src, period, primary_key, event_name, event_value, new_count_col_name):
        # We want to count how many loans that employee give in one day
        Calc(self.csv_file).count(self.df, period, primary_key, event_value, new_count_col_name)

    # This is the add button for the tab2 named "sum"
    def on_tab2_btn_add(self):

        print("Current tab is: ", self.tab_parent.index("current"))

        primary_key = self.var_primary_key2.get()
        attribute_name = self.var_attribute2.get()
        # case_consept = "disbursement"
        attribute_value = self.var_event_value2.get()
        # period = "per day"
        period = self.var_time_range2.get()

        event_value = self.var_event_value2.get()

        new_count_col_name = "None"
        if period == "By Day":
            new_sum_col_name = "sum " + attribute_name + " ByDay"
        elif period == "By Month":
            new_sum_col_name = "sum " + attribute_name + " ByMonth"

        # def count(self, df_src, period, primary_key, event_name, event_value, new_count_col_name):
        # We want to count how many loans that employee give in one day
        Calc(self.csv_file).sum(self.df, period, primary_key, event_value, attribute_name, new_sum_col_name)

    # This is the add button for the tab3 named "avg"
    def on_tab3_btn_add(self):

        print("Current tab is: ", self.tab_parent.index("current"))

        primary_key = self.var_primary_key3.get()
        attribute_name = self.var_attribute3.get()
        # period = "per day"
        period = self.var_time_range3.get()
        event_value = self.var_event_value3.get()

        new_count_col_name = "None"
        if period == "By Day":
            new_avg_col_name = "avg " + attribute_name + " ByDay"
        elif period == "By Month":
            new_avg_col_name = "avg " + attribute_name + " ByMonth"

        # def count(self, df_src, period, primary_key, event_name, event_value, new_count_col_name):
        # We want to count how many loans that employee give in one day
        Calc(self.csv_file).avg(self.df, period, primary_key, event_value, attribute_name, new_avg_col_name)

    def on_tab1_radio_button_clicked(self):
        print("radio button clicked: " + str(self.selected_radio_button1.get()))
        if self.selected_radio_button1.get() == 1:
            print("radio button 1 clicked")
            self.lbl_primary_key.place(x=420, y=50)
            # self.lbl_primary_key.place_forget()
            self.combobox_primary_key1.place(x=500, y=50)
            self.combobox_primary_key1.place(x=500, y=50)
            # self.combobox_primary_key1.place_forget()
            self.lbl_attribute.place(x=420, y=80)
            # self.lbl_attribute.place_forget()
            self.combobox_attribute1.place(x=500, y=80)
            # self.combobox_attribute1.place_forget()
            self.lbl_time_range.place(x=420, y=110)
            # self.lbl_time_range.place_forget()
            self.combobox_time_range1.place(x=500, y=110)
            # self.combobox_time_range1.place_forget()
            self.lbl_time_range.place(x=420, y=110)
            # self.lbl_time_range.place_forget()
            self.lbl_event_value.place(x=420, y=140)
            # self.lbl_event_value.place_forget()
            self.combobox_event_value1.place(x=500, y=140)
            # self.combobox_event_value1.place_forget()
            self.lbl_foreign_key.place(x=420, y=170)
            self.lbl_foreign_key.place_forget()
            self.combobox_foreign_key1.place(x=500, y=170)
            self.combobox_foreign_key1.place_forget()
            self.lbl_function.place(x=420, y=200)
            self.lbl_function.place_forget()
            self.combobox_function1.place(x=500, y=200)
            self.combobox_function1.place_forget()
            self.lbl_condition.place(x=420, y=240)
            self.lbl_condition.place_forget()
            self.combobox_condition1.place(x=520, y=270)
            self.combobox_condition1.place_forget()
            self.lbl_operator.place(x=440, y=270)
            self.lbl_operator.place_forget()
            self.lbl_value.place(x=440, y=300)
            self.lbl_value.place_forget()
            self.txt_value.place(x=520, y=300)
            self.txt_value.place_forget()

        if self.selected_radio_button1.get() == 2:
            print("radio button 2 clicked")
            self.lbl_primary_key.place(x=420, y=50)
            # self.lbl_primary_key.place_forget()
            self.combobox_primary_key1.place(x=500, y=50)
            # self.combobox_primary_key1.place_forget()
            self.lbl_attribute.place(x=420, y=80)
            # self.lbl_attribute.place_forget()
            self.combobox_attribute1.place(x=500, y=80)
            # self.combobox_attribute1.place_forget()
            self.lbl_time_range.place(x=420, y=110)
            # self.lbl_time_range.place_forget()
            self.combobox_time_range1.place(x=500, y=110)
            # self.combobox_time_range1.place_forget()
            self.lbl_time_range.place(x=420, y=110)
            # self.lbl_time_range.place_forget()
            self.lbl_event_value.place(x=420, y=140)
            # self.lbl_event_value.place_forget()
            self.combobox_event_value1.place(x=500, y=140)
            # self.combobox_event_value1.place_forget()
            self.lbl_foreign_key.place(x=420, y=170)
            self.lbl_foreign_key.place_forget()
            self.combobox_foreign_key1.place(x=500, y=170)
            self.combobox_foreign_key1.place_forget()
            self.lbl_function.place(x=420, y=200)
            self.lbl_function.place_forget()
            self.combobox_function1.place(x=500, y=200)
            self.combobox_function1.place_forget()
            self.lbl_condition.place(x=420, y=240)
            # self.lbl_condition.place_forget()
            self.combobox_condition1.place(x=520, y=270)
            # self.combobox_condition1.place_forget()
            self.lbl_operator.place(x=440, y=270)
            # self.lbl_operator.place_forget()
            self.lbl_value.place(x=440, y=300)
            # self.lbl_value.place_forget()
            self.txt_value.place(x=520, y=300)
            # self.txt_value.place_forget()

        if self.selected_radio_button1.get() == 3:
            print("radio button 3 clicked")
            self.lbl_primary_key.place(x=420, y=50)
            # self.lbl_primary_key.place_forget()
            self.combobox_primary_key1.place(x=500, y=50)
            # self.combobox_primary_key1.place_forget()
            self.lbl_attribute.place(x=420, y=80)
            # self.lbl_attribute.place_forget()
            self.combobox_attribute1.place(x=500, y=80)
            # self.combobox_attribute1.place_forget()
            self.lbl_time_range.place(x=420, y=110)
            # self.lbl_time_range.place_forget()
            self.combobox_time_range1.place(x=500, y=110)
            # self.combobox_time_range1.place_forget()
            self.lbl_time_range.place(x=420, y=110)
            # self.lbl_time_range.place_forget()
            self.lbl_event_value.place(x=420, y=140)
            # self.lbl_event_value.place_forget()
            self.combobox_event_value1.place(x=500, y=140)
            # self.combobox_event_value1.place_forget()
            self.lbl_foreign_key.place(x=420, y=170)
            self.lbl_foreign_key.place_forget()
            self.combobox_foreign_key1.place(x=500, y=170)
            self.combobox_foreign_key1.place_forget()
            self.lbl_function.place(x=420, y=200)
            # self.lbl_function.place_forget()
            self.combobox_function1.place(x=500, y=200)
            # self.combobox_function1.place_forget()
            self.lbl_condition.place(x=420, y=240)
            # self.lbl_condition.place_forget()
            self.combobox_condition1.place(x=520, y=270)
            # self.combobox_condition1.place_forget()
            self.lbl_operator.place(x=440, y=270)
            # self.lbl_operator.place_forget()
            self.lbl_value.place(x=440, y=300)
            # self.lbl_value.place_forget()
            self.txt_value.place(x=520, y=300)
            # self.txt_value.place_forget()

        if self.selected_radio_button1.get() == 4:
            print("radio button 4 clicked")
            self.lbl_primary_key.place(x=420, y=50)
            # self.lbl_primary_key.place_forget()
            self.combobox_primary_key1.place(x=500, y=50)
            # self.combobox_primary_key1.place_forget()
            self.lbl_attribute.place(x=420, y=80)
            # self.lbl_attribute.place_forget()
            self.combobox_attribute1.place(x=500, y=80)
            # self.combobox_attribute1.place_forget()
            self.lbl_time_range.place(x=420, y=110)
            # self.lbl_time_range.place_forget()
            self.combobox_time_range1.place(x=500, y=110)
            # self.combobox_time_range1.place_forget()
            self.lbl_time_range.place(x=420, y=110)
            # self.lbl_time_range.place_forget()
            self.lbl_event_value.place(x=420, y=140)
            # self.lbl_event_value.place_forget()
            self.combobox_event_value1.place(x=500, y=140)
            # self.combobox_event_value1.place_forget()
            self.lbl_foreign_key.place(x=420, y=170)
            # self.lbl_foreign_key.place_forget()
            self.combobox_foreign_key1.place(x=500, y=170)
            # self.combobox_foreign_key1.place_forget()
            self.lbl_function.place(x=420, y=200)
            self.lbl_function.place_forget()
            self.combobox_function1.place(x=500, y=200)
            self.combobox_function1.place_forget()
            self.lbl_condition.place(x=420, y=240)
            self.lbl_condition.place_forget()
            self.combobox_condition1.place(x=520, y=270)
            self.combobox_condition1.place_forget()
            self.lbl_operator.place(x=440, y=270)
            self.lbl_operator.place_forget()
            self.lbl_value.place(x=440, y=300)
            self.lbl_value.place_forget()
            self.txt_value.place(x=520, y=300)
            self.txt_value.place_forget()

        if self.selected_radio_button1.get() == 5:
            print("radio button 5 clicked")
            self.lbl_primary_key.place(x=420, y=50)
            # self.lbl_primary_key.place_forget()
            self.combobox_primary_key1.place(x=500, y=50)
            # self.combobox_primary_key1.place_forget()
            self.lbl_attribute.place(x=420, y=80)
            # self.lbl_attribute.place_forget()
            self.combobox_attribute1.place(x=500, y=80)
            # self.combobox_attribute1.place_forget()
            self.lbl_time_range.place(x=420, y=110)
            # self.lbl_time_range.place_forget()
            self.combobox_time_range1.place(x=500, y=110)
            # self.combobox_time_range1.place_forget()
            self.lbl_time_range.place(x=420, y=110)
            # self.lbl_time_range.place_forget()
            self.lbl_event_value.place(x=420, y=140)
            # self.lbl_event_value.place_forget()
            self.combobox_event_value1.place(x=500, y=140)
            # self.combobox_event_value1.place_forget()
            self.lbl_foreign_key.place(x=420, y=170)
            # self.lbl_foreign_key.place_forget()
            self.combobox_foreign_key1.place(x=500, y=170)
            # self.combobox_foreign_key1.place_forget()
            self.lbl_function.place(x=420, y=200)
            self.lbl_function.place_forget()
            self.combobox_function1.place(x=500, y=200)
            self.combobox_function1.place_forget()
            self.lbl_condition.place(x=420, y=240)
            # self.lbl_condition.place_forget()
            self.combobox_condition1.place(x=520, y=270)
            # self.combobox_condition1.place_forget()
            self.lbl_operator.place(x=440, y=270)
            # self.lbl_operator.place_forget()
            self.lbl_value.place(x=440, y=300)
            # self.lbl_value.place_forget()
            self.txt_value.place(x=520, y=300)
            # self.txt_value.place_forget()

        if self.selected_radio_button1.get() == 6:
            print("radio button 6 clicked")
            self.lbl_primary_key.place(x=420, y=50)
            # self.lbl_primary_key.place_forget()
            self.combobox_primary_key1.place(x=500, y=50)
            # self.combobox_primary_key1.place_forget()
            self.lbl_attribute.place(x=420, y=80)
            # self.lbl_attribute.place_forget()
            self.combobox_attribute1.place(x=500, y=80)
            # self.combobox_attribute1.place_forget()
            self.lbl_time_range.place(x=420, y=110)
            # self.lbl_time_range.place_forget()
            self.combobox_time_range1.place(x=500, y=110)
            # self.combobox_time_range1.place_forget()
            self.lbl_time_range.place(x=420, y=110)
            # self.lbl_time_range.place_forget()
            self.lbl_event_value.place(x=420, y=140)
            # self.lbl_event_value.place_forget()
            self.combobox_event_value1.place(x=500, y=140)
            # self.combobox_event_value1.place_forget()
            self.lbl_foreign_key.place(x=420, y=170)
            # self.lbl_foreign_key.place_forget()
            self.combobox_foreign_key1.place(x=500, y=170)
            # self.combobox_foreign_key1.place_forget()
            self.lbl_function.place(x=420, y=200)
            # self.lbl_function.place_forget()
            self.combobox_function1.place(x=500, y=200)
            # self.combobox_function1.place_forget()
            self.lbl_condition.place(x=420, y=240)
            # self.lbl_condition.place_forget()
            self.combobox_condition1.place(x=520, y=270)
            # self.combobox_condition1.place_forget()
            self.lbl_operator.place(x=440, y=270)
            # self.lbl_operator.place_forget()
            self.lbl_value.place(x=440, y=300)
            # self.lbl_value.place_forget()
            self.txt_value.place(x=520, y=300)
            # self.txt_value.place_forget()

    def on_tab2_radio_button_clicked(self):
        print("radio button clicked: " + str(self.selected_radio_button2.get()))
        if self.selected_radio_button2.get() == 1:
            print("radio button 1 clicked")
            self.lbl_primary_key2.place(x=420, y=50)
            # self.lbl_primary_key2.place_forget()
            self.combobox_primary_key2.place(x=500, y=50)
            # self.combobox_primary_key2.place_forget()
            self.lbl_attribute2.place(x=420, y=80)
            # self.lbl_attribute2.place_forget()
            self.combobox_attribute2.place(x=500, y=80)
            # self.combobox_attribute2.place_forget()
            self.lbl_time_range2.place(x=420, y=110)
            # self.lbl_time_range2.place_forget()
            self.combobox_time_range2.place(x=500, y=110)
            # self.combobox_time_range2.place_forget()
            self.lbl_time_range2.place(x=420, y=110)
            # self.lbl_time_range2.place_forget()
            self.lbl_event_value2.place(x=420, y=140)
            # self.lbl_event_value2.place_forget()
            self.combobox_event_value2.place(x=500, y=140)
            # self.combobox_event_value2.place_forget()
            self.lbl_foreign_key2.place(x=420, y=170)
            self.lbl_foreign_key2.place_forget()
            self.combobox_foreign_key2.place(x=500, y=170)
            self.combobox_foreign_key2.place_forget()
            self.lbl_function2.place(x=420, y=200)
            self.lbl_function2.place_forget()
            self.combobox_function2.place(x=500, y=200)
            self.combobox_function2.place_forget()
            self.lbl_condition2.place(x=420, y=240)
            self.lbl_condition2.place_forget()
            self.combobox_condition2.place(x=520, y=270)
            self.combobox_condition2.place_forget()
            self.lbl_operator2.place(x=440, y=270)
            self.lbl_operator2.place_forget()
            self.lbl_value2.place(x=440, y=300)
            self.lbl_value2.place_forget()
            self.txt_value2.place(x=520, y=300)
            self.txt_value2.place_forget()

        if self.selected_radio_button2.get() == 2:
            print("radio button 2 clicked")
            self.lbl_primary_key2.place(x=420, y=50)
            # self.lbl_primary_key2.place_forget()
            self.combobox_primary_key2.place(x=500, y=50)
            # self.combobox_primary_key2.place_forget()
            self.lbl_attribute2.place(x=420, y=80)
            # self.lbl_attribute2.place_forget()
            self.combobox_attribute2.place(x=500, y=80)
            # self.combobox_attribute2.place_forget()
            self.lbl_time_range2.place(x=420, y=110)
            # self.lbl_time_range2.place_forget()
            self.combobox_time_range2.place(x=500, y=110)
            # self.combobox_time_range2.place_forget()
            self.lbl_time_range2.place(x=420, y=110)
            # self.lbl_time_range2.place_forget()
            self.lbl_event_value2.place(x=420, y=140)
            # self.lbl_event_value2.place_forget()
            self.combobox_event_value2.place(x=500, y=140)
            # self.combobox_event_value2.place_forget()
            self.lbl_foreign_key2.place(x=420, y=170)
            self.lbl_foreign_key2.place_forget()
            self.combobox_foreign_key2.place(x=500, y=170)
            self.combobox_foreign_key2.place_forget()
            self.lbl_function2.place(x=420, y=200)
            self.lbl_function2.place_forget()
            self.combobox_function2.place(x=500, y=200)
            self.combobox_function2.place_forget()
            self.lbl_condition2.place(x=420, y=240)
            # self.lbl_condition2.place_forget()
            self.combobox_condition2.place(x=520, y=270)
            # self.combobox_condition2.place_forget()
            self.lbl_operator2.place(x=440, y=270)
            # self.lbl_operator2.place_forget()
            self.lbl_value2.place(x=440, y=300)
            # self.lbl_value2.place_forget()
            self.txt_value2.place(x=520, y=300)
            # self.txt_value2.place_forget()

        if self.selected_radio_button2.get() == 3:
            print("radio button 3 clicked")
            self.lbl_primary_key2.place(x=420, y=50)
            # self.lbl_primary_key2.place_forget()
            self.combobox_primary_key2.place(x=500, y=50)
            # self.combobox_primary_key2.place_forget()
            self.lbl_attribute2.place(x=420, y=80)
            # self.lbl_attribute2.place_forget()
            self.combobox_attribute2.place(x=500, y=80)
            # self.combobox_attribute2.place_forget()
            self.lbl_time_range2.place(x=420, y=110)
            # self.lbl_time_range2.place_forget()
            self.combobox_time_range2.place(x=500, y=110)
            # self.combobox_time_range2.place_forget()
            self.lbl_time_range2.place(x=420, y=110)
            # self.lbl_time_range2.place_forget()
            self.lbl_event_value2.place(x=420, y=140)
            # self.lbl_event_value2.place_forget()
            self.combobox_event_value2.place(x=500, y=140)
            # self.combobox_event_value2.place_forget()
            self.lbl_foreign_key2.place(x=420, y=170)
            self.lbl_foreign_key2.place_forget()
            self.combobox_foreign_key2.place(x=500, y=170)
            self.combobox_foreign_key2.place_forget()
            self.lbl_function2.place(x=420, y=200)
            # self.lbl_function2.place_forget()
            self.combobox_function2.place(x=500, y=200)
            # self.combobox_function2.place_forget()
            self.lbl_condition2.place(x=420, y=240)
            # self.lbl_condition2.place_forget()
            self.combobox_condition2.place(x=520, y=270)
            # self.combobox_condition2.place_forget()
            self.lbl_operator2.place(x=440, y=270)
            # self.lbl_operator2.place_forget()
            self.lbl_value2.place(x=440, y=300)
            # self.lbl_value2.place_forget()
            self.txt_value2.place(x=520, y=300)
            # self.txt_value2.place_forget()

        if self.selected_radio_button2.get() == 4:
            print("radio button 4 clicked")
            self.lbl_primary_key2.place(x=420, y=50)
            # self.lbl_primary_key2.place_forget()
            self.combobox_primary_key2.place(x=500, y=50)
            # self.combobox_primary_key2.place_forget()
            self.lbl_attribute2.place(x=420, y=80)
            # self.lbl_attribute2.place_forget()
            self.combobox_attribute2.place(x=500, y=80)
            # self.combobox_attribute2.place_forget()
            self.lbl_time_range2.place(x=420, y=110)
            # self.lbl_time_range2.place_forget()
            self.combobox_time_range2.place(x=500, y=110)
            # self.combobox_time_range2.place_forget()
            self.lbl_time_range2.place(x=420, y=110)
            # self.lbl_time_range2.place_forget()
            self.lbl_event_value2.place(x=420, y=140)
            # self.lbl_event_value2.place_forget()
            self.combobox_event_value2.place(x=500, y=140)
            # self.combobox_event_value2.place_forget()
            self.lbl_foreign_key2.place(x=420, y=170)
            # self.lbl_foreign_key2.place_forget()
            self.combobox_foreign_key2.place(x=500, y=170)
            # self.combobox_foreign_key2.place_forget()
            self.lbl_function2.place(x=420, y=200)
            self.lbl_function2.place_forget()
            self.combobox_function2.place(x=500, y=200)
            self.combobox_function2.place_forget()
            self.lbl_condition2.place(x=420, y=240)
            self.lbl_condition2.place_forget()
            self.combobox_condition2.place(x=520, y=270)
            self.combobox_condition2.place_forget()
            self.lbl_operator2.place(x=440, y=270)
            self.lbl_operator2.place_forget()
            self.lbl_value2.place(x=440, y=300)
            self.lbl_value2.place_forget()
            self.txt_value2.place(x=520, y=300)
            self.txt_value2.place_forget()

        if self.selected_radio_button2.get() == 5:
            print("radio button 5 clicked")
            self.lbl_primary_key2.place(x=420, y=50)
            # self.lbl_primary_key2.place_forget()
            self.combobox_primary_key2.place(x=500, y=50)
            # self.combobox_primary_key2.place_forget()
            self.lbl_attribute2.place(x=420, y=80)
            # self.lbl_attribute2.place_forget()
            self.combobox_attribute2.place(x=500, y=80)
            # self.combobox_attribute2.place_forget()
            self.lbl_time_range2.place(x=420, y=110)
            # self.lbl_time_range2.place_forget()
            self.combobox_time_range2.place(x=500, y=110)
            # self.combobox_time_range2.place_forget()
            self.lbl_time_range2.place(x=420, y=110)
            # self.lbl_time_range2.place_forget()
            self.lbl_event_value2.place(x=420, y=140)
            # self.lbl_event_value2.place_forget()
            self.combobox_event_value2.place(x=500, y=140)
            # self.combobox_event_value2.place_forget()
            self.lbl_foreign_key2.place(x=420, y=170)
            # self.lbl_foreign_key2.place_forget()
            self.combobox_foreign_key2.place(x=500, y=170)
            # self.combobox_foreign_key2.place_forget()
            self.lbl_function2.place(x=420, y=200)
            self.lbl_function2.place_forget()
            self.combobox_function2.place(x=500, y=200)
            self.combobox_function2.place_forget()
            self.lbl_condition2.place(x=420, y=240)
            # self.lbl_condition2.place_forget()
            self.combobox_condition2.place(x=520, y=270)
            # self.combobox_condition2.place_forget()
            self.lbl_operator2.place(x=440, y=270)
            # self.lbl_operator2.place_forget()
            self.lbl_value2.place(x=440, y=300)
            # self.lbl_value2.place_forget()
            self.txt_value2.place(x=520, y=300)
            # self.txt_value2.place_forget()

        if self.selected_radio_button2.get() == 6:
            print("radio button 6 clicked")
            self.lbl_primary_key2.place(x=420, y=50)
            # self.lbl_primary_key2.place_forget()
            self.combobox_primary_key2.place(x=500, y=50)
            # self.combobox_primary_key2.place_forget()
            self.lbl_attribute2.place(x=420, y=80)
            # self.lbl_attribute2.place_forget()
            self.combobox_attribute2.place(x=500, y=80)
            # self.combobox_attribute2.place_forget()
            self.lbl_time_range2.place(x=420, y=110)
            # self.lbl_time_range2.place_forget()
            self.combobox_time_range2.place(x=500, y=110)
            # self.combobox_time_range2.place_forget()
            self.lbl_time_range2.place(x=420, y=110)
            # self.lbl_time_range2.place_forget()
            self.lbl_event_value2.place(x=420, y=140)
            # self.lbl_event_value2.place_forget()
            self.combobox_event_value2.place(x=500, y=140)
            # self.combobox_event_value2.place_forget()
            self.lbl_foreign_key2.place(x=420, y=170)
            # self.lbl_foreign_key2.place_forget()
            self.combobox_foreign_key2.place(x=500, y=170)
            # self.combobox_foreign_key2.place_forget()
            self.lbl_function2.place(x=420, y=200)
            # self.lbl_function2.place_forget()
            self.combobox_function2.place(x=500, y=200)
            # self.combobox_function2.place_forget()
            self.lbl_condition2.place(x=420, y=240)
            # self.lbl_condition2.place_forget()
            self.combobox_condition2.place(x=520, y=270)
            # self.combobox_condition2.place_forget()
            self.lbl_operator2.place(x=440, y=270)
            # self.lbl_operator2.place_forget()
            self.lbl_value2.place(x=440, y=300)
            # self.lbl_value2.place_forget()
            self.txt_value2.place(x=520, y=300)
            # self.txt_value2.place_forget()

    def on_tab3_radio_button_clicked(self):
        print("radio button clicked: " + str(self.selected_radio_button3.get()))
        if self.selected_radio_button3.get() == 1:
            print("radio button 1 clicked")
            self.lbl_primary_key3.place(x=420, y=50)
            # self.lbl_primary_key3.place_forget()
            self.combobox_primary_key3.place(x=500, y=50)
            # self.combobox_primary_key3.place_forget()
            self.lbl_attribute3.place(x=420, y=80)
            # self.lbl_attribute3.place_forget()
            self.combobox_attribute3.place(x=500, y=80)
            # self.combobox_attribute3.place_forget()
            self.lbl_time_range3.place(x=420, y=110)
            # self.lbl_time_range3.place_forget()
            self.combobox_time_range3.place(x=500, y=110)
            # self.combobox_time_range3.place_forget()
            self.lbl_time_range3.place(x=420, y=110)
            # self.lbl_time_range3.place_forget()
            self.lbl_event_value3.place(x=420, y=140)
            # self.lbl_event_value3.place_forget()
            self.combobox_event_value3.place(x=500, y=140)
            # self.combobox_event_value3.place_forget()
            self.lbl_foreign_key3.place(x=420, y=170)
            self.lbl_foreign_key3.place_forget()
            self.combobox_foreign_key3.place(x=500, y=170)
            self.combobox_foreign_key3.place_forget()
            self.lbl_function3.place(x=420, y=200)
            self.lbl_function3.place_forget()
            self.combobox_function3.place(x=500, y=200)
            self.combobox_function3.place_forget()
            self.lbl_condition3.place(x=420, y=240)
            self.lbl_condition3.place_forget()
            self.combobox_condition3.place(x=520, y=270)
            self.combobox_condition3.place_forget()
            self.lbl_operator3.place(x=440, y=270)
            self.lbl_operator3.place_forget()
            self.lbl_value3.place(x=440, y=300)
            self.lbl_value3.place_forget()
            self.txt_value3.place(x=520, y=300)
            self.txt_value3.place_forget()

        if self.selected_radio_button3.get() == 2:
            print("radio button 2 clicked")
            self.lbl_primary_key3.place(x=420, y=50)
            # self.lbl_primary_key3.place_forget()
            self.combobox_primary_key3.place(x=500, y=50)
            # self.combobox_primary_key3.place_forget()
            self.lbl_attribute3.place(x=420, y=80)
            # self.lbl_attribute3.place_forget()
            self.combobox_attribute3.place(x=500, y=80)
            # self.combobox_attribute3.place_forget()
            self.lbl_time_range3.place(x=420, y=110)
            # self.lbl_time_range3.place_forget()
            self.combobox_time_range3.place(x=500, y=110)
            # self.combobox_time_range3.place_forget()
            self.lbl_time_range3.place(x=420, y=110)
            # self.lbl_time_range3.place_forget()
            self.lbl_event_value3.place(x=420, y=140)
            # self.lbl_event_value3.place_forget()
            self.combobox_event_value3.place(x=500, y=140)
            # self.combobox_event_value3.place_forget()
            self.lbl_foreign_key3.place(x=420, y=170)
            self.lbl_foreign_key3.place_forget()
            self.combobox_foreign_key3.place(x=500, y=170)
            self.combobox_foreign_key3.place_forget()
            self.lbl_function3.place(x=420, y=200)
            self.lbl_function3.place_forget()
            self.combobox_function3.place(x=500, y=200)
            self.combobox_function3.place_forget()
            self.lbl_condition3.place(x=420, y=240)
            # self.lbl_condition3.place_forget()
            self.combobox_condition3.place(x=520, y=270)
            # self.combobox_condition3.place_forget()
            self.lbl_operator3.place(x=440, y=270)
            # self.lbl_operator3.place_forget()
            self.lbl_value3.place(x=440, y=300)
            # self.lbl_value3.place_forget()
            self.txt_value3.place(x=520, y=300)
            # self.txt_value3.place_forget()

        if self.selected_radio_button3.get() == 3:
            print("radio button 3 clicked")
            self.lbl_primary_key3.place(x=420, y=50)
            # self.lbl_primary_key3.place_forget()
            self.combobox_primary_key3.place(x=500, y=50)
            # self.combobox_primary_key3.place_forget()
            self.lbl_attribute3.place(x=420, y=80)
            # self.lbl_attribute3.place_forget()
            self.combobox_attribute3.place(x=500, y=80)
            # self.combobox_attribute3.place_forget()
            self.lbl_time_range3.place(x=420, y=110)
            # self.lbl_time_range3.place_forget()
            self.combobox_time_range3.place(x=500, y=110)
            # self.combobox_time_range3.place_forget()
            self.lbl_time_range3.place(x=420, y=110)
            # self.lbl_time_range3.place_forget()
            self.lbl_event_value3.place(x=420, y=140)
            # self.lbl_event_value3.place_forget()
            self.combobox_event_value3.place(x=500, y=140)
            # self.combobox_event_value3.place_forget()
            self.lbl_foreign_key3.place(x=420, y=170)
            self.lbl_foreign_key3.place_forget()
            self.combobox_foreign_key3.place(x=500, y=170)
            self.combobox_foreign_key3.place_forget()
            self.lbl_function3.place(x=420, y=200)
            # self.lbl_function3.place_forget()
            self.combobox_function3.place(x=500, y=200)
            # self.combobox_function3.place_forget()
            self.lbl_condition3.place(x=420, y=240)
            # self.lbl_condition3.place_forget()
            self.combobox_condition3.place(x=520, y=270)
            # self.combobox_condition3.place_forget()
            self.lbl_operator3.place(x=440, y=270)
            # self.lbl_operator3.place_forget()
            self.lbl_value3.place(x=440, y=300)
            # self.lbl_value3.place_forget()
            self.txt_value3.place(x=520, y=300)
            # self.txt_value3.place_forget()

        if self.selected_radio_button3.get() == 4:
            print("radio button 4 clicked")
            self.lbl_primary_key3.place(x=420, y=50)
            # self.lbl_primary_key3.place_forget()
            self.combobox_primary_key3.place(x=500, y=50)
            # self.combobox_primary_key3.place_forget()
            self.lbl_attribute3.place(x=420, y=80)
            # self.lbl_attribute3.place_forget()
            self.combobox_attribute3.place(x=500, y=80)
            # self.combobox_attribute3.place_forget()
            self.lbl_time_range3.place(x=420, y=110)
            # self.lbl_time_range3.place_forget()
            self.combobox_time_range3.place(x=500, y=110)
            # self.combobox_time_range3.place_forget()
            self.lbl_time_range3.place(x=420, y=110)
            # self.lbl_time_range3.place_forget()
            self.lbl_event_value3.place(x=420, y=140)
            # self.lbl_event_value3.place_forget()
            self.combobox_event_value3.place(x=500, y=140)
            # self.combobox_event_value3.place_forget()
            self.lbl_foreign_key3.place(x=420, y=170)
            # self.lbl_foreign_key3.place_forget()
            self.combobox_foreign_key3.place(x=500, y=170)
            # self.combobox_foreign_key3.place_forget()
            self.lbl_function3.place(x=420, y=200)
            self.lbl_function3.place_forget()
            self.combobox_function3.place(x=500, y=200)
            self.combobox_function3.place_forget()
            self.lbl_condition3.place(x=420, y=240)
            self.lbl_condition3.place_forget()
            self.combobox_condition3.place(x=520, y=270)
            self.combobox_condition3.place_forget()
            self.lbl_operator3.place(x=440, y=270)
            self.lbl_operator3.place_forget()
            self.lbl_value3.place(x=440, y=300)
            self.lbl_value3.place_forget()
            self.txt_value3.place(x=520, y=300)
            self.txt_value3.place_forget()

        if self.selected_radio_button3.get() == 5:
            print("radio button 5 clicked")
            self.lbl_primary_key3.place(x=420, y=50)
            # self.lbl_primary_key3.place_forget()
            self.combobox_primary_key3.place(x=500, y=50)
            # self.combobox_primary_key3.place_forget()
            self.lbl_attribute3.place(x=420, y=80)
            # self.lbl_attribute3.place_forget()
            self.combobox_attribute3.place(x=500, y=80)
            # self.combobox_attribute3.place_forget()
            self.lbl_time_range3.place(x=420, y=110)
            # self.lbl_time_range3.place_forget()
            self.combobox_time_range3.place(x=500, y=110)
            # self.combobox_time_range3.place_forget()
            self.lbl_time_range3.place(x=420, y=110)
            # self.lbl_time_range3.place_forget()
            self.lbl_event_value3.place(x=420, y=140)
            # self.lbl_event_value3.place_forget()
            self.combobox_event_value3.place(x=500, y=140)
            # self.combobox_event_value3.place_forget()
            self.lbl_foreign_key3.place(x=420, y=170)
            # self.lbl_foreign_key3.place_forget()
            self.combobox_foreign_key3.place(x=500, y=170)
            # self.combobox_foreign_key3.place_forget()
            self.lbl_function3.place(x=420, y=200)
            self.lbl_function3.place_forget()
            self.combobox_function3.place(x=500, y=200)
            self.combobox_function3.place_forget()
            self.lbl_condition3.place(x=420, y=240)
            # self.lbl_condition3.place_forget()
            self.combobox_condition3.place(x=520, y=270)
            # self.combobox_condition3.place_forget()
            self.lbl_operator3.place(x=440, y=270)
            # self.lbl_operator3.place_forget()
            self.lbl_value3.place(x=440, y=300)
            # self.lbl_value3.place_forget()
            self.txt_value3.place(x=520, y=300)
            # self.txt_value3.place_forget()

        if self.selected_radio_button3.get() == 6:
            print("radio button 6 clicked")
            self.lbl_primary_key3.place(x=420, y=50)
            # self.lbl_primary_key3.place_forget()
            self.combobox_primary_key3.place(x=500, y=50)
            # self.combobox_primary_key3.place_forget()
            self.lbl_attribute3.place(x=420, y=80)
            # self.lbl_attribute3.place_forget()
            self.combobox_attribute3.place(x=500, y=80)
            # self.combobox_attribute3.place_forget()
            self.lbl_time_range3.place(x=420, y=110)
            # self.lbl_time_range3.place_forget()
            self.combobox_time_range3.place(x=500, y=110)
            # self.combobox_time_range3.place_forget()
            self.lbl_time_range3.place(x=420, y=110)
            # self.lbl_time_range3.place_forget()
            self.lbl_event_value3.place(x=420, y=140)
            # self.lbl_event_value3.place_forget()
            self.combobox_event_value3.place(x=500, y=140)
            # self.combobox_event_value3.place_forget()
            self.lbl_foreign_key3.place(x=420, y=170)
            # self.lbl_foreign_key3.place_forget()
            self.combobox_foreign_key3.place(x=500, y=170)
            # self.combobox_foreign_key3.place_forget()
            self.lbl_function3.place(x=420, y=200)
            # self.lbl_function3.place_forget()
            self.combobox_function3.place(x=500, y=200)
            # self.combobox_function3.place_forget()
            self.lbl_condition3.place(x=420, y=240)
            # self.lbl_condition3.place_forget()
            self.combobox_condition3.place(x=520, y=270)
            # self.combobox_condition3.place_forget()
            self.lbl_operator3.place(x=440, y=270)
            # self.lbl_operator3.place_forget()
            self.lbl_value3.place(x=440, y=300)
            # self.lbl_value3.place_forget()
            self.txt_value3.place(x=520, y=300)
            # self.txt_value3.place_forget()

    def on_btn_next(self):
        self.win_selectCaseId = tk.Toplevel(self.master)
        self.app_selectCaseId = Win5(self.win_selectCaseId, self.df, self.csv_file)


# screen to see all saved files
class Win4(tk.Frame):
    def __init__(self, master, df):
        super().__init__(master)

        self.df = df
        self.master = master
        self.master.geometry("700x400")
        # self.master.title('Functions Screen')
        # self.master.resizable(False, False)
        mypath = "c:/savedCsvFiles"
        onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

        listbox = Listbox(self.master, width=100)
        listbox.place(x=50, y=50)
        for name in onlyfiles:
            listbox.insert('end', name)


# Select caseIds for display graphs windows for them
class Win5(tk.Frame):
    def __init__(self, master, df, csv_file):
        super().__init__(master)
        self.pack()

        self.csv_file = csv_file
        self.df = df
        self.is_filter_displayed = False

        self.master.geometry("800x400")
        self.master.title('ISCF GUI - Select CaseId')
        self.master.resizable(False, False)

        lbl_name = tk.Label(self.master, text="Select one or more options")
        lbl_name.place(x=30, y=50)

        # Choosing selectmode as multiple
        # for selecting multiple options
        self.listbox_caseid = Listbox(self.master, selectmode="multiple")
        self.listbox_caseid.place(x=30, y=80)

        # Widget expands horizontally and
        # vertically by assigning both to
        # fill option
        # self.listbox_caseid.pack(expand=YES, fill="y")
        # self.listbox_caseid.pack()

        # self.list_caseid = ["aa", "bb", "cc", "dd"]
        self.list_caseid = list(self.df.columns)
        for item in range(len(self.list_caseid)):
            self.listbox_caseid.insert(END, self.list_caseid[item])
            # coloring alternative lines of listbox
            self.listbox_caseid.itemconfig(item, bg="yellow" if item % 2 == 0 else "cyan")

        btn_display_graphs = ttk.Button(
            self.master,
            text='Display Graphs',
            command=self.on_btn_display_graphs_clicked
        )
        btn_display_graphs.place(x=30, y=350)

    def on_btn_display_graphs_clicked(self):

        # get all selected indices from the listbox
        selected_indices = self.listbox_caseid.curselection()
        # get selected items
        selected_case_ids = ",".join([self.listbox_caseid.get(i) for i in selected_indices])
        msg = f'You selected: {selected_case_ids}'
        # showinfo(title='Information', message=msg)
        print(msg)
        self.graphsWindows = []
        self.apps = []
        for i in range(len(selected_indices)):
            self.graphsWindows.append(tk.Toplevel(self.master))
            case_id_index = selected_indices[i]
            case_id = self.listbox_caseid.get(case_id_index)
            self.apps.append(Win6(self.graphsWindows[i], self.df, self.csv_file, case_id))


class Win6(tk.Frame):
    def __init__(self, master, df, csv_file, case_id):
        super().__init__(master)

        self.df = df
        self.csv_file = csv_file
        self.case_id = case_id

        self.pack()

        self.csv_file = csv_file
        self.is_filter_displayed = False

        self.master.geometry("1200x800")
        self.master.title('ISCF GUI - Select CaseId')
        # self.master.resizable(False, False)
        # for scrolling vertically
        yscrollbar = Scrollbar(self.master)
        yscrollbar.pack(side=RIGHT, fill=Y)

        print("csv file before xes:" + self.csv_file)

        event_log = pd.read_csv(self.csv_file)

        print("event_log before converting to xes:")
        pd.set_option('display.max_columns', None)
        print(event_log)

        log_scv = pm4py.format_dataframe(event_log, case_id=self.case_id, activity_key='case:concept',
                                         timestamp_key='time:timestamp')

        dot_position = self.csv_file.rindex(".")
        csvFileBeforeDot = self.csv_file[:dot_position]
        new_xes_file = csvFileBeforeDot + " - " + self.case_id + ".xes"
        print("creating new xes file: " + new_xes_file)

        # Reading the xes file
        pm4py.write_xes(log_scv, new_xes_file)
        self.log = pm4py.read_xes(new_xes_file)

        self.net = None
        self.im = None
        self.fm = None


        lbl_graphs = tk.Label(self.master, text="Display Graphs by " + str(case_id) + ":")
        lbl_graphs.place(x=30, y=30)

        btn_name = tk.Button(self.master, text="Inductive Miner",
                             command=self.display_inductive_miner_graph)
        btn_name.place(x=250, y=25)

        # Display Graph for inductive miner
        self.net, self.im, self.fm = pm4py.discover_petri_net_inductive(self.log)
        gviz = visualizer.apply(self.net, self.im, self.fm,
                                parameters={visualizer.Variants.WO_DECORATION.value.Parameters.DEBUG: True})
        # visualizer.view(gviz)

        btn_name = tk.Button(self.master,
                             text="Instance spanning constraints",
                             command=self.display_spanning_constraints_graph)
        btn_name.place(x=370, y=25)

        # # Display Graph for spanning constraints
        self.net, self.im, self.fm = decision_mining.create_data_petri_nets_with_decisions(self.log, self.net, self.im, self.fm)
        gviz = visualizer.apply(self.net, self.im, self.fm,
                                parameters={visualizer.Variants.WO_DECORATION.value.Parameters.DEBUG: True})
        # visualizer.view(gviz)

        btn_name = tk.Label(self.master, text="Guards by " + str(case_id) + ":")
        btn_name.place(x=30, y=60)

        # # # Guards:
        # for t in self.net.transitions:
        #     if "guard" in t.properties:
        #         print("")
        #         print(t)
        #         print(t.properties["guard"])

        # # Guards:
        strGuards = ""
        for t in self.net.transitions:
            if "guard" in t.properties:
                strGuards += t
                strGuards += t.properties["guard"]
                strGuards += "\n"

        text_area_guards = scrolledtext.ScrolledText(self.master, wrap=tk.WORD,
                                              width=100, height=4,
                                              font=("Times New Roman", 15))
        text_area_guards.insert(END, strGuards)
        text_area_guards.place(x=30,y=90)



        lbl_name = tk.Label(self.master, text="Fitness by " + str(case_id) + ":")
        lbl_name.place(x=30, y=210)

        fitness = pm4py.fitness_alignments(self.log, self.net, self.im, self.fm)
        # print("the fitness is:", fitness)
        text_area_fitness = scrolledtext.ScrolledText(self.master, wrap=tk.WORD,
                                              width=100, height=4,
                                              font=("Times New Roman", 15))
        text_area_fitness.insert(END, fitness)
        text_area_fitness.place(x=30, y=240)



        lbl_name = tk.Label(self.master, text="Prec by " + str(case_id) + ":")
        lbl_name.place(x=30, y=360)

        # print("the precision is ", prec)
        # self.gen = generalization_evaluator.apply(self.log, self.net, self.im, self.fm)

        text_area_prec = scrolledtext.ScrolledText(self.master, wrap=tk.WORD,
                                              width=100, height=4,
                                              font=("Times New Roman", 15))
        text_area_prec.insert(END, "Here should be prec")
        text_area_prec.place(x=30,y=390)



        lbl_name = tk.Label(self.master, text="Gen by " + str(case_id) + ":")
        lbl_name.place(x=30, y=510)

        #self.gen = generalization_evaluator.apply(self.log, self.net, self.im, self.fm)
        # print("the generalization is ", gen)

        text_area_gen = scrolledtext.ScrolledText(self.master, wrap=tk.WORD,
                                              width=100, height=4,
                                              font=("Times New Roman", 15))
        text_area_gen.insert(END, "Here should be gen")
        text_area_gen.place(x=30,y=540)



        lbl_name = tk.Label(self.master, text="Simp by " + str(case_id) + ":")
        lbl_name.place(x=30, y=660)

        text_area_simp = scrolledtext.ScrolledText(self.master, wrap=tk.WORD,
                                              width=100, height=4,
                                              font=("Times New Roman", 15))
        text_area_simp.insert(END, "Here should be simp")
        text_area_simp.place(x=30,y=690)


        # simp = simplicity_evaluator.apply(net)
        # print("the simplicity is:", net)

        # # Guards:
        # for t in net.transitions:
        #     if "guard" in t.properties:
        #         print("")
        #         print(t)
        #         print(t.properties["guard"])
        #
        # fitness = pm4py.fitness_alignments(log, net, im, fm)
        # print("the fitness is:", fitness)
        # prec = pm4py.precision_alignments(log, net, im, fm)
        # print("the precision is ", prec)
        # gen = generalization_evaluator.apply(log, net, im, fm)
        # print("the generalization is ", gen)
        # simp = simplicity_evaluator.apply(net)
        # print("the simplicity is:", net)

    def display_inductive_miner_graph(self):
        # Display Graph for inductive miner
        self.net, self.im, self.fm = pm4py.discover_petri_net_inductive(self.log)
        gviz = visualizer.apply(self.net, self.im, self.fm,
                                parameters={visualizer.Variants.WO_DECORATION.value.Parameters.DEBUG: True})
        visualizer.view(gviz)

    def display_spanning_constraints_graph(self):
        # Display Graph for spanning constraints
        net, im, fm = decision_mining.create_data_petri_nets_with_decisions(self.log, self.net, self.im, self.fm)
        gviz = visualizer.apply(self.net, self.im, self.fm,
                                parameters={visualizer.Variants.WO_DECORATION.value.Parameters.DEBUG: True})
        visualizer.view(gviz)

def main():
    root = tk.Tk()
    app = Win1(master=root)  # Inherit
    app.mainloop()


if __name__ == "__main__":
    main()
