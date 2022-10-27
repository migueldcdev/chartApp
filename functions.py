from os import path

import pandas as pd
from pandas_ods_reader import read_ods

from tkinter import filedialog
import customtkinter as ctk

import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

import seaborn as sns


global current_df
global df_column_headers

df_sample =  pd.DataFrame(data={'Example graphic': ['a', 'b', 'c', 'd'], '':[1, 5, 3, 1]})

current_df = df_sample
df_column_headers = []


def get_file_extension(file):
    file_extension = path.splitext(file.name)
    return file_extension[1]


def file_data_to_df(file):
    file_extension = get_file_extension(file)

    if file_extension == ".csv":
        data = pd.read_csv(file.name)     

    if file_extension == ".ods":
        data = read_ods(file.name)        

    if file_extension == ".xls" or file_extension == ".xlsx":
        data = pd.read_excel(file.name)

    return data


def open_file(data_frame, canvas, panel):
    
    global current_df
    global df_column_headers    

    file = filedialog.askopenfile(
        mode="r",
        initialdir="/home/pi/Documents",
        filetypes=[
            ("CSV files", "*.csv"),
            ("Excel files", ".xlsx .xls"),
            ("ODF Spreadsheet", ".ods"),
        ],
    )

    current_df = file_data_to_df(file)
    df_column_headers = get_df_column_headers(current_df)    
    
    panel.update_combos()
    data_frame.add_df(current_df)    
    canvas.create_new_figure()


def get_df_column_headers(df):

    return list(df.columns.values)


def collect_figure_params(panel):    
    params = []   
    params.append(panel.radio_var.get())
    params.append(panel.x_axis_var.get())
    params.append(panel.y_axis_var.get())
    params.append(panel.hue_var.get())
    params.append(panel.checkbox_rotate_x_labels_var.get())
    params.append(panel.theme_var.get())
    
    return params


def plt_set_style(param):    
    styles = ['default', 'bmh', 'Solarize_Light2', 'dark_background', 'seaborn-v0_8-paper', 'grayscale']
    plt.style.use(styles[0])

    if(param == "Default"):
        plt.style.use(styles[0])

    if(param == "BMH"):
        plt.style.use(styles[1])

    if(param == "Solarize"):
        plt.style.use(styles[2])

    if(param == "Dark"):
        plt.style.use(styles[3])    

    if(param == "Pastel"):
        plt.style.use(styles[4])  

    if(param == "Grayscale"):
       plt.style.use(styles[5]) 


def create_figure(canvas):
    figure = Figure(figsize=(8, 7))
    ax = figure.subplots()
    
    try:
        sns.barplot(data=current_df, ax=ax, x=current_df.columns[0], y=current_df.columns[1])
    except TypeError:
        canvas.error_type_error()       
    
    return figure


def destroy_figure(frame):
    for widgets in frame.winfo_children():        
        widgets.destroy()


def create_canvas(frame, figure):
    canvas = FigureCanvasTkAgg(figure, master=frame)
    canvas.get_tk_widget().pack()  

    return canvas


def create_toolbar(canvas):
    toolbar = NavigationToolbar2Tk(canvas)
    toolbar.update()

    return toolbar


def update_x_axis(frame):
    axis_combo = ctk.CTkComboBox(frame, variable=frame.x_axis_var, values= df_column_headers, state="readonly", fg_color="gray85")   
    axis_combo.set(df_column_headers[0])

    return axis_combo


def update_y_axis(frame):
    axis_combo = ctk.CTkComboBox(frame, variable=frame.y_axis_var, values= df_column_headers, state="readonly", fg_color="gray85")
    axis_combo.set(df_column_headers[1])

    return axis_combo


def update_hue_selector(frame):
    df_col = df_column_headers    
    df_col.insert(0, "None")
    hue_selector = ctk.CTkComboBox(frame, variable=frame.hue_var, values= df_col ,state="readonly", fg_color="gray85")
    hue_selector.set("None")

    return hue_selector


def apply_changes(canvas, panel):
    params = collect_figure_params(panel)    
    plt_set_style(params[5])    
    canvas.update_figure(panel)


def create_figure_with_params(panel):  
    
    params = collect_figure_params(panel)  
    
    figure = Figure(figsize=(8, 7), constrained_layout=True)
    ax = figure.subplots()
    
    if(params[4]):
        ax.tick_params(axis='x', rotation=90)

    if(params[0] ==1):
        if(params[3] == 'None' or params[3] == ''):
            sns.barplot(data=current_df, ax=ax, x=params[1], y=params[2])
        else:
            sns.barplot(data=current_df, ax=ax, x=params[1], y=params[2], hue=params[3])       
        
    if(params[0] == 2):
        if(params[3] == 'None' or params[3] == ''):
            sns.histplot(data=current_df, ax=ax, x=params[1], y=params[2])   
        else:
            sns.histplot(data=current_df, ax=ax, x=params[1], y=params[2], hue=params[3])
    
    if(params[0] == 3):
        if(params[3] == 'None' or params[3] == ''):
            sns.scatterplot(data=current_df, ax=ax, x=params[1], y=params[2])
        else:        
            sns.scatterplot(data=current_df, ax=ax, x=params[1], y=params[2], hue=params[3])
    
    if(params[0] == 4):
        try:
            sns.regplot(data=current_df, ax=ax, x=params[1], y=params[2]) 
        except:
            panel.error_regplot()    
    
    if(params[0] == 5):
        if(params[3] == 'None' or params[3] == ''):
            sns.lineplot(data=current_df, ax=ax, x=params[1], y=params[2])
        else: 
            sns.lineplot(data=current_df, ax=ax, x=params[1], y=params[2], hue=params[3])
    
    return figure
   
    