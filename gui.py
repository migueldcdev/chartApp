import tkinter as tk
import customtkinter  as ctk

from functions import  open_file, create_figure, collect_figure_params, create_figure_with_params,  destroy_figure, create_canvas, create_toolbar, update_x_axis, update_y_axis, update_hue_selector, apply_changes


class App(ctk.CTk):
    def __init__(self):        
        ctk.CTk.__init__(self)
        
        self.title("ChartApp")
        self.configure(fg_color="black")

        container = ctk.CTkFrame(self, fg_color="black")
        container.grid()        

        frame = MainPage(container, self)
        frame.grid(padx=50, pady=75)
        frame.tkraise()        

        self.mainloop()
    
class MainPage(ctk.CTkFrame):
    def __init__(self, parent, container):
        ctk.CTkFrame.__init__(self, parent)

        self.configure(fg_color="gray25")
        self.rowconfigure(20)
        self.columnconfigure(20)
        
        open_file_button = ctk.CTkButton(self, text="Open file", text_color="white", border_width=2, border_color="white", fg_color="grey25", hover_color="gray55", command=lambda: open_file(data_frame, canvas, panel))
        open_file_button.grid(column=0, row=0, pady="30")

        data_frame = DataFrame(self)        
        data_frame.grid(column=0, row=1, columnspan=5, rowspan=5)
        
        canvas = Canvas(self)
        canvas.grid(column=5,row=0, columnspan=5,rowspan=5) 

        panel = Panel(self)
        panel.grid(column=0, row=2, rowspan=1, columnspan=5, padx=20)       
        
        apply_changes_button = ctk.CTkButton(self, text="Apply changes", fg_color="green2", text_color="white", hover_color="green3", command=lambda: apply_changes(canvas, panel))
        apply_changes_button.grid(column=0, row=3, pady=30)
        

class DataFrame(ctk.CTkFrame):    
    def __init__(self, container):
        ctk.CTkFrame.__init__(self, container) 
        self.configure(fg_color="gray25", padx=100)
        self.text = tk.Text(container, bg="black", fg="green2")                
        self.text.insert("1.0", "Start by clicking the button file on top of the window and opening a Csv, Excel or LibreOffice Calc document")
        self.text.configure(state="disabled", padx=10, pady=5, wrap="none")       
        self.text.grid(padx=50)        
        

    def add_df(self, df):        
        self.text.configure(state="normal")
        self.text.delete("1.0", tk.END)
        self.text.insert("1.0", df.to_string())
        self.text.configure(state="disabled")
        self.text.grid()


class Canvas(ctk.CTkFrame):
    def __init__(self, container):
        tk.Frame.__init__(self,container, bg="gray25")        
        self.configure(padx=100, pady=40)              
        self.figure = create_figure(self)
        self.canvas = create_canvas(self, self.figure)
        self.toolbar = create_toolbar(self.canvas)        
    
    def create_new_figure(self):        
        destroy_figure(self)               
        self.figure = create_figure(self)        
        self.canvas = create_canvas(self, self.figure)
        self.toolbar = create_toolbar(self.canvas)

    def update_figure(self, panel):
        destroy_figure(self)
        
        try:
            self.figure = create_figure_with_params(panel)   
        except:
            tk.messagebox.showerror('Data error', 'You may need to open a new file')
        
        self.canvas = create_canvas(self, self.figure)
        self.toolbar = create_toolbar(self.canvas) 

    def error_type_error(self):
        tk.messagebox.showerror('Parameters error', 'At least one of the columns must be numeric')  


class Panel(ctk.CTkFrame):
    def __init__(self, container):        
        ctk.CTkFrame.__init__(self,container)
        
        self.configure(fg_color="gray25")
        #vars
        self.radio_var = tk.IntVar(value=1)
        self.x_axis_var = tk.StringVar()
        self.y_axis_var = tk.StringVar()
        self.hue_var = tk.StringVar()
        self.checkbox_rotate_x_labels_var = tk.BooleanVar(False)
        self.theme_var = tk.StringVar(value="Default")

        #radio buttons for selecting graphic type
        graphic_type_label = ctk.CTkLabel(self, text="Graphic type:", text_color="gray65")        
        radio_bar = ctk.CTkRadioButton(self, text="Bar chart", variable=self.radio_var, value=1, fg_color="green2",hover_color="green3", border_color="white",text_color="white", command= lambda: self.get_params())
        radio_line = ctk.CTkRadioButton(self, text="Histogram plot", variable=self.radio_var, value=2, fg_color="green2",hover_color="green3", border_color="white",text_color="white", command= lambda: self.get_params())
        radio_scatter = ctk.CTkRadioButton(self, text="Scatter plot", variable=self.radio_var, value=3, fg_color="green2",hover_color="green3", border_color="white",text_color="white", command= lambda: self.get_params())
        radio_regression = ctk.CTkRadioButton(self, text="Regression plot", variable=self.radio_var, value=4, fg_color="green2",hover_color="green3", border_color="white",text_color="white", command= lambda: self.get_params())
        radio_hist= ctk.CTkRadioButton(self, text="Line chart", variable=self.radio_var, value=5, fg_color="green2",hover_color="green3", border_color="white",text_color="white", command=lambda: self.get_params())
        
        graphic_type_label.grid(row=0, column=0, pady=20)
        radio_bar.grid(row=1, column=0)
        radio_line.grid(row=1, column=1)
        radio_scatter.grid(row=1, column=2)
        radio_regression.grid(row=1, column=3)
        radio_hist.grid(row=1, column=4)
        

        #axis X Combobox selector
        x_axis_var_label = ctk.CTkLabel(self, text="X axis value:", text_color="gray65") 
        self.x_axis_combo = ctk.CTkComboBox(self, variable=self.x_axis_var, values= [],state="disabled")
        x_axis_var_label.grid(row=2, column=0, pady=30)
        self.x_axis_combo.grid(row=2, column=1,padx=15)
        

        #axis Y Combobox selector
        y_axis_var_label = ctk.CTkLabel(self, text="Y axis value:", text_color="gray65") 
        self.y_axis_combo = ctk.CTkComboBox(self, variable=self.y_axis_var, values= [],state="disabled")
        y_axis_var_label.grid(row=2, column=2, pady=30)
        self.y_axis_combo.grid(row=2, column=3)        

        #combo hue selector
        hue_selector_label = ctk.CTkLabel(self, text="Hue selector:", text_color="gray65") 
        self.hue_selector_combo = ctk.CTkComboBox(self, variable=self.hue_var, values= [],state="disabled")
        
        hue_selector_label.grid(row=3, column=2)
        self.hue_selector_combo.grid(row=3, column=3)

        #checkbox rotate x axis labels selector
        self.checkbox_rotate_x_labels = ctk.CTkCheckBox(self, text="Rotate X labels", variable=self.checkbox_rotate_x_labels_var,fg_color="green2",hover_color="green3", border_color="white",text_color="white",command= lambda: self.get_params())
        self.checkbox_rotate_x_labels.grid(row=4, column=0, padx=50, pady=20)

        #graphic theme combo selector   
        theme_selector_label = ctk.CTkLabel(self, text="Theme:", text_color="gray65")      
        self.theme_values = ["Default", "BMH", "Solarize", "Dark", "Pastel", "Grayscale"]
        self.theme_selector_combo = ctk.CTkComboBox(self, variable=self.theme_var, values=self.theme_values, state="readonly", fg_color="gray85")
        self.theme_selector_combo.bind('<<ComboboxSelected>>', lambda x: self.get_params())
        theme_selector_label.grid(row=3, column=0)
        self.theme_selector_combo.grid(row=3, column=1)


    def update_combos(self):       
        
        self.x_axis_combo.destroy()
        self.y_axis_combo.destroy()
        self.hue_selector_combo.destroy()
        
        self.x_axis_combo = update_x_axis(self)
        self.y_axis_combo = update_y_axis(self)
        self.hue_selector_combo = update_hue_selector(self)
        
        self.x_axis_combo.bind('<<ComboboxSelected>>', lambda x: self.get_params()) 
        self.y_axis_combo.bind('<<ComboboxSelected>>', lambda x: self.get_params()) 
        self.hue_selector_combo.bind('<<ComboboxSelected>>', lambda x: self.get_params())
        
        
        self.x_axis_combo.grid(row=2, column=1, padx=15)        
        self.y_axis_combo.grid(row=2, column=3, padx=15)
        self.hue_selector_combo.grid(row=3, column=3)  
         
    def get_params(self):
        collect_figure_params(self)   

    def error_regplot(self):
        tk.messagebox.showerror('Parameters error', 'Regression plot X axis and Y axis must be numeric')

       



