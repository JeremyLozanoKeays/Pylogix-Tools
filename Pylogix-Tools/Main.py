import tkinter as tk
from tkinter import ttk, simpledialog
import pylogix
import ast
import datetime
import xml.etree.cElementTree as et


class App(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self)

        # Make the app responsive
        for index in [0, 1, 2]:
            self.columnconfigure(index=index, weight=1)
            self.rowconfigure(index=index, weight=1)

        # Create value lists
        self.option_menu_list = ["", "OptionMenu", "Option 1", "Option 2"]
        self.processor_combo_list = ["0", "1", "2", "3", "4"]

        # Create control variables with defaults
        self.var_0 = tk.StringVar(value="10.10.100.1")
        self.var_1 = tk.StringVar(value="Tag_values.xml")
        self.var_2 = tk.StringVar(value="5000") # Connection Refresh Rate
        self.var_3 = tk.IntVar(value=2) # Connection Enabled status
        self.var_4 = tk.IntVar(value=0) # Processor Slot
        self.var_5 = tk.StringVar(value="Disabled") #Is an Emulator
        self.img_1 = tk.PhotoImage(file='Logo_Shadow_Cropped.png').subsample(2, 2)
        self.console = Console(5)
        self.console_last = tk.StringVar(value="") # Consle store to prevent reprints
        self.console_line_1 = tk.StringVar(value="Line 1 : Loading Saved Configuration")
        self.console_line_2 = tk.StringVar(value="Line 2 : ")
        self.console_line_3 = tk.StringVar(value="Line 3 : ")
        self.console_line_4 = tk.StringVar(value="Line 4 : ")
        self.console_line_5 = tk.StringVar(value="Line 5 : ")
        self.flag = 0

        # Create widgets :)
        self.setup_widgets()

    def setup_widgets(self):

#Left Column

        # Logo
        self.logo = ttk.Label(self, image = self.img_1 )
        self.logo.grid(row=0, column=0, padx=(20, 10), pady=(10, 20), sticky="nsew")

        # Seperator
        self.separator_c1 = ttk.Separator(self)
        self.separator_c1.grid(row=1, column=0, padx=(20, 10), pady=10, sticky="ew" )

        # Create a Frame for the Connection Radiobuttons
        self.radio_frame = ttk.LabelFrame(self, text="Connection", padding=(20, 10))
        self.radio_frame.grid(row=2, column=0, padx=(20, 10), pady=10, sticky="nsew")

        # Connection Radiobuttons
        self.radio_1 = ttk.Radiobutton(
            self.radio_frame, text="Enabled", variable=self.var_3, value=1
        )
        self.radio_1.grid(row=0, column=0, padx=5, pady=2, sticky="nsew")
        self.radio_2 = ttk.Radiobutton(
            self.radio_frame, text="Disabled", variable=self.var_3, value=2
        )
        self.radio_2.grid(row=1, column=0, padx=5, pady=2, sticky="nsew")
        self.radio_3 = ttk.Radiobutton(
            self.radio_frame, text="Read only", variable=self.var_3, value=3
        )
        self.radio_3.grid(row=3, column=0, padx=5, pady=2, sticky="nsew")


# Middle Column
        # Create a Frame for input widgets
        self.widgets_frame = ttk.LabelFrame(self, text="Configuration", padding=(0, 0, 0, 10))
        self.widgets_frame.grid(
            row=0, column=1, padx=10, pady=(30, 10), sticky="nsew", rowspan=3
        )
        self.widgets_frame.columnconfigure(index=0, weight=1)

        # IP address Entry Label
        self.ip_entry_label = ttk.Label(self.widgets_frame, text="IP Address")
        self.ip_entry_label.grid(row=0, column=0, padx=10, pady=(0, 2), sticky="ew")

        # IP addresss Entry
        self.ip_entry = ttk.Entry(self.widgets_frame, textvariable=self.var_0)
        self.ip_entry.grid(row=1, column=0, padx=20, pady=(0, 10), sticky="ew")

        # XML Source Entry Label
        self.xml_entry_label = ttk.Label(self.widgets_frame, text="XML Tag Source")
        self.xml_entry_label.grid(row=2, column=0, padx=10, pady=(0,2), sticky="ew")

        # XML Source Entry
        self.xml_entry = ttk.Entry(self.widgets_frame, textvariable=self.var_1)
        self.xml_entry.grid(row=3, column=0, padx=20, pady=(0, 10), sticky="ew")

        # Refresh Rate Entry Label
        self.refresh_entry_label = ttk.Label(self.widgets_frame, text="Refresh Rate (mS)")
        self.refresh_entry_label.grid(row=4, column=0, padx=10, pady=(0,2), sticky="ew")

        # Refresh Rate Entry
        self.refresh_entry = ttk.Entry(self.widgets_frame, textvariable=self.var_2)
        self.refresh_entry.grid(row=5, column=0, padx=20, pady=(0, 10), sticky="ew")

        # Processor combobox Label
        self.ip_entry_label = ttk.Label(self.widgets_frame, text="Processor Slot")
        self.ip_entry_label.grid(row=6, column=0, padx=10, pady=(0, 2), sticky="ew")

        # Processor combobox
        self.processor_entry = ttk.Combobox(
            self.widgets_frame, state="readonly", values=self.processor_combo_list
            )
        self.processor_entry.current(0)
        
        self.processor_entry.grid(row=7, column=0, padx=20, pady=(0,10), sticky="ew")

        # Is Emulator button Label
        self.emulator_entry_label = ttk.Label(self.widgets_frame, text="Emulate 5000")
        self.emulator_entry_label.grid(row=8, column=0, padx=10, pady=(0, 2), sticky="ew")

        # Is Emulator button
        self.emulator_switch = ttk.Checkbutton(
            self.widgets_frame, textvariable=self.var_5, style="Toggle.TButton"
            , variable=self.var_5, onvalue="Enabled", offvalue="Disabled"  # Var_5 updates display text

        )
        self.emulator_switch.grid(row=9, column=0, padx=20, pady=(0, 10), sticky="nsew")

        # Separator
        self.separator = ttk.Separator(self.widgets_frame)
        self.separator.grid(row=10, column=0, padx=10, pady=10, sticky="ew" , columnspan=4)

        # Save Changes button
        self.savebutton = ttk.Button(
            self.widgets_frame, text="Save Changes", style="Accent.TButton"
        )
        self.savebutton.grid(row=15, column=0, padx=10, pady=10, sticky="nsew" )
        self.savebutton['command'] = self.save_changes # Calls Save_Changes function on command

#Right Column
        # Panedwindow
        self.paned = ttk.PanedWindow(self)
        self.paned.grid(row=0, column=2, pady=(35, 10), sticky="nsew", rowspan=3)

        # Pane #1
        self.pane_1 = ttk.Frame(self.paned, padding=5)
        self.paned.add(self.pane_1, weight=1)

        # Scrollbar
        self.scrollbar = ttk.Scrollbar(self.pane_1)
        self.scrollbar.pack(side="right", fill="y")

        # Treeview
        self.treeview = ttk.Treeview(
            self.pane_1,
            selectmode="browse",
            yscrollcommand=self.scrollbar.set,
            columns=(1, 2),
            height=10,
        )
        self.treeview.pack(expand=True, fill="both")
        self.scrollbar.config(command=self.treeview.yview)

        # Treeview columns
        self.treeview.column("#0", anchor="w", width=120)
        self.treeview.column(1, anchor="w", width=120)
        self.treeview.column(2, anchor="w", width=120)

        # Treeview headings
        self.treeview.heading("#0", text="Tag Name", anchor="center")
        self.treeview.heading(1, text="Value", anchor="center")
        self.treeview.heading(2, text="Data Type", anchor="center")

        # Define treeview data
        self.unpack_treeview()

        # Select and scroll
        self.treeview.selection_set(9)
        self.treeview.bind('<Double-1>', self.onDoubleClick)
        self.treeview.see(7)

        # Notebook, pane #2
        self.pane_2 = ttk.Frame(self.paned, padding=5)
        self.paned.add(self.pane_2, weight=3)

        # Notebook, pane #2
        self.notebook = ttk.Notebook(self.pane_2)
        self.notebook.pack(fill="both", expand=True)

        # Tab #1
        self.tab_1 = ttk.Frame(self.notebook)
        for index in [0, 1]:
            self.tab_1.columnconfigure(index=index, weight=1)
            self.tab_1.rowconfigure(index=index, weight=1)
        self.notebook.add(self.tab_1, text="Console")


        # Display Print Console date
        self.t1_label_1 = ttk.Label(self.tab_1, textvariable=self.console_line_1, justify="left",
            font=("-size", 8),
        )
        self.t1_label_1.grid(row=1, column=0, pady=(1, 0), columnspan=2, sticky="ew")

        self.t1_label_2 = ttk.Label(self.tab_1, textvariable=self.console_line_2, justify="left",
            font=("-size", 8),
        )
        self.t1_label_2.grid(row=2, column=0, pady=(1, 0), columnspan=2, sticky="ew")

        self.t1_label_3 = ttk.Label(self.tab_1, textvariable=self.console_line_3, justify="left",
            font=("-size", 8),
        )
        self.t1_label_3.grid(row=3, column=0, pady=(1, 0), columnspan=2, sticky="ew")

        self.t1_label_4 = ttk.Label(self.tab_1, textvariable=self.console_line_4, justify="left",
            font=("-size", 8),
        )
        self.t1_label_4.grid(row=4, column=0, pady=(1, 0), columnspan=2, sticky="ew")

        self.t1_label_5 = ttk.Label(self.tab_1, textvariable=self.console_line_5, justify="left",
            font=("-size", 8),
        )
        self.t1_label_5.grid(row=5, column=0, pady=(1, 1), columnspan=2, sticky="ew")



        # Tab #2
        self.tab_2 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_2, text="About")

        # Label
        self.t2_label_1 = ttk.Label(
            self.tab_2,
            text="Contact",
            justify="center",
            font=("-size", 12, "-weight", "bold"),
        )
        self.t2_label_1.grid(row=1, column=0, padx=0, pady=(10, 5), columnspan=2)

        # Label
        self.t2_label_2 = ttk.Label(
            self.tab_2,
            text="+1 (818) 538 6577\n+52 55 6083 5305",
            justify="center",
            font=("-size", 8, "-weight", "bold"),
        )
        self.t2_label_2.grid(row=2, column=0, padx=20, pady=2, columnspan=2)

 #Footer
        # Separator
        self.separator = ttk.Separator(self)
        self.separator.grid(row=10, column=0, padx=(20, 10), pady=10, sticky="ew" , columnspan=4)

        self.footleft = ttk.Label(
            self,
            text="© 2021 Avalae Automation. ",
            justify="center",
            font=("-size", 8, "-weight", "normal"),
        )
        self.footleft.grid(row=11, column=0, padx=(20, 10), pady=10, sticky="ew" , columnspan=2)

        self.footright = ttk.Label(
            self,
            text="By Jeremy Lozano-Keays ",
            justify="right",
            font=("-size", 8, "-weight", "normal"),
        )
        self.footright.grid(row=11, column=2, padx=(20, 10), pady=10, sticky="e" )

        # Sizegrip
        self.sizegrip = ttk.Sizegrip(self)
        self.sizegrip.grid(row=100, column=100, padx=(0, 3), pady=(0, 3))

    def onDoubleClick(self, event):
        ''' Executed, when a row is double-clicked. Opens 
        writeable string dialog above in the center of the treeview, so it is possible
        to modify the text '''

        # what row and column was clicked on
        rowid = self.treeview.identify_row(event.y)
        column = self.treeview.identify_column(event.x)
        columnint = int(column.strip('#'))
        

        # Store current row, text and values
        text = self.treeview.item(rowid, 'text')
        values = self.treeview.item(rowid, 'values')
        # Open changebox dialog and set new data into treeview
        if column == '#0':
            self.entryPopup = simpledialog.askstring('Change Value', "Current Tag Name: " + text, parent=self.treeview)
            if self.entryPopup != None:
                self.treeview.delete(rowid)
                self.treeview.insert('', index=(int(rowid)-1), iid=int(rowid), text=self.entryPopup , values=values)
        elif column == '#1':
            self.entryPopup = simpledialog.askstring('Change Value', "Current Value: " + values[0], parent=self.treeview)
            if self.entryPopup != None:
                values_new = (self.entryPopup, values[1])
                self.treeview.delete(rowid)
                self.treeview.insert('', index=(int(rowid)-1), iid=int(rowid), text=text, values=values_new)
        elif column == '#2':
            self.entryPopup = simpledialog.askstring('Change Value', "Current Data Type: " + values[1], parent=self.treeview)
            if self.entryPopup != None:
                values_new = (values[0], self.entryPopup)
                self.treeview.delete(rowid)
                self.treeview.insert('', index=(int(rowid)-1), iid=int(rowid), text=text, values=values_new)
                
    
    def plc_routine(self, initialize=False):
        if initialize:
            self.plc_initialize()
        
        # Use currently saved settings   
        self.PLC.IPAddress = self.plc_config['IP_Address']
        self.PLC.ProcessorSlot = self.plc_config['Processor_Slot']
        if self.plc_config['Is_Emulator'] == 'Enabled':
            self.PLC.ConnectionSize = 504
        else:
            self.PLC.ConnectionSize = 508
        # Connection is Enabled    
        if self.var_3.get() == 1:
            if self.flag != 1:
                self.console.insert('Connection set: Enabled')
                self.flag = 1
            write_data = self.bottle_treeview()            
            try:
                fail = False
                self.plc_status = self.PLC.Write(write_data)
                for i in self.plc_status:
                    if i.Status != 'Success':
                        fail = True
                if fail:
                    self.console.insert('Data failed to send, Check configuration')
                else:
                    self.console.insert('Data Write Successful')
            except:
                self.console.insert('Data failed to write, Check Data Types')
        # Connection is Disabled
        elif self.var_3.get() == 2:
            if self.flag != 2:
                self.console.insert('Connection set: Disabled')
                self.flag = 2
        # Connection is Read-Only
        elif self.var_3.get() == 3:
            if self.flag != 3:
                self.console.insert('Connection set: Read-Only')
                self.flag = 3
            read_data = self.bottle_treeview(readonly=True)
            try:
                fail = False
                self.plc_status = self.PLC.Read(read_data)
                self.repack_treeview(self.plc_status)
                for i in self.plc_status:
                    if i.Status != 'Success':
                        fail = True
                if fail:
                    self.console.insert('Data failed to read, Check configuration')
                else:
                    self.console.insert('Data Read Successful')
            except:
                self.console.insert('Data failed to send, Check Data Types')
        
        # LOOP CALL - After Delay call plc_routine again       
        root.after(self.plc_config["Refresh_Rate"], self.plc_routine)
    
    def plc_initialize(self):
        # Open Log file settings
        try:
            self.log_File = open("Log.txt", "a")
            self.log_File.close
        except:
            self.console.insert('No existing file Creating - log.txt')
            self.log_File = open("Log.txt", "a+") # Create a new file
            self.log_File.close
        
        # Open Configuration Settings and retrieve stored settings
        try:
            config_File = open("Config.txt", "r")
            config_Settings = config_File.read()
            config_File.close
            config_Settings = ast.literal_eval(config_Settings)
            # Update settings
            self.var_0.set(config_Settings['IP_Address']) # Set IP Address
            self.var_1.set(config_Settings['XML_Source']) # Set XML Filepath
            self.var_2.set(config_Settings['Refresh_Rate']) # Set Refresh Rate
            self.processor_entry.set(config_Settings['Processor_Slot']) # Processor Slot
            self.var_5.set(config_Settings['Is_Emulator']) # Set Is Emulator            
        except:
            self.console.insert('No existing file Creating - Config.txt')
            config_File = open("Config.txt", "a+") # Create a new file 
            config_File.close


        finally:
            self.save_changes()
            self.console.insert('Configuring PLC Settings')
            self.PLC = pylogix.PLC()


    def save_changes(self):
        # Write settings into PLC_Config
        self.plc_config = {
            "IP_Address" : self.var_0.get(),
            "XML_Source" : self.var_1.get(),
            "Refresh_Rate" : self.var_2.get(),
            "Connection_Status" : self.var_3.get(),
            "Processor_Slot" : int(self.processor_entry.get()) ,
            "Is_Emulator" : self.var_5.get(),
            }
        self.console.insert("Changes Saved")

        # Store settings as Config.txt
        config_File = open("Config.txt", "w")
        config_File.write(str(self.plc_config))
        config_File.close
        self.console.log(str(self.plc_config))
    
        
    def unpack_treeview(self):
        # Open XML containing File
        try:
            treeview_data = []
            data = []
            tree = et.parse(self.var_1.get())
            base = tree.getroot()
            for j in range(len(base.findall('Tag'))):
                for child in base[j]:
                     data.append(child.text)
                treeview_data.append(('', j+1, data[-3], (data[-2], data[-1])))           
        except:
            self.console.insert('Error opening - ' + self.var_1.get())
            treeview_data = [("", 1, "Tag_1", ("Sample", "String"))] # Use this as a template dat unpacking

        # Insert treeview data
        for item in treeview_data:
            self.treeview.insert(
                parent=item[0], index="end", iid=item[1], text=item[2], values=item[3]
            )
            if item[0] == "" or item[1] in {8, 21}:
                self.treeview.item(item[1], open=True)  # Open parents

    def repack_treeview(self, read_data):
        # Clear old tree
        for rowid in self.treeview.get_children():
            self.treeview.delete(rowid)
        # Create new rows
        for data, newid in zip(read_data, range(len(read_data))):
            if isinstance(data.Value, float):
                data.Value = round(data.Value, 4)
                data_type = "REAL"
            elif isinstance(data.Value, str):
                data_type = "STRING"
            else:
                data_type = "DINT"
            self.treeview.insert('', index="end", iid=int(newid), text=data.TagName, values=(data.Value, data_type))
        
    def bottle_treeview(self, readonly=False):
        # Bottle treeview data for PLC delivery
        x = 0
        tree_data =[]
        for x in self.treeview.get_children():  
            values = []
            skip = False
            # Retireves Value and Stats from Treeview
            for y in self.treeview.item(x,'values'):
                values.append(y)
            # Retrieves Value from Treeview 
            if not readonly:
                if values[1] == "STRING": # Builds the STRING, length is fixed at 25
                    tree_data.append(tuple([self.treeview.item(x,'text') + '.LEN', len(values[0])]))
                    values = [ord(c) for c in values[0]] + [0] * (25 - len(values[0]))
                    tree_data.append(tuple([self.treeview.item(x,'text') + '.DATA[0]', values]))
                    skip = True
                elif values[1] == "REAL": # Builds the REAL
                    values = [float(values[0])]
                else:
                    try:
                        values = [int(values[0])]
                    except ValueError:
                        return
                if not skip: # Skips append when STRING is selected.
                    tree_data.append(tuple([self.treeview.item(x,'text'), values[0]]))
            else:
                tree_data.append(self.treeview.item(x,'text'))
        return tree_data

class Console:
    # Console FiFo
    def __init__(self, size = 10):
        self.items =[]
        self.size = size

    def is_empty(self):
        return self.items == []

    def insert(self, item):
        now = datetime.datetime.now()
        if app.console_last.get() != item :
            self.items.insert(0, now.strftime('%d-%m-%Y %H:%M:%S - ') + item)
            app.console_last.set(item)
        if len(self.items) > self.size:
            self.out()
        self.refresh()
        self.log(self.items[0])
            
    def out(self):
        return self.items.pop()

    def get(self, item = None):
        try:
            if item >= 0:
                return str(self.items[item])
            else:
                return str(self.items)
        except:
            return '.'

    def refresh(self):
        app.console_line_1.set("Line 1:" + self.get(0))
        app.console_line_2.set("Line 2:" + self.get(1))
        app.console_line_3.set("Line 3:" + self.get(2))
        app.console_line_4.set("Line 4:" + self.get(3))
        app.console_line_5.set("Line 5:" + self.get(4))

    def log(self, text):
        log_File = open("Log.txt", "a")
        log_File.write(text + '\n')
        log_File.close
                    

if __name__ == "__main__":
    root = tk.Tk()
    root.title("")

    # Simply set the theme
    root.tk.call("source", "azure.tcl")
    root.tk.call("set_theme", "dark")

    app = App(root)
    app.pack(fill="both", expand=True)

    # Set a minsize for the window, and place it in the middle
    root.update()
    root.minsize(root.winfo_width(), root.winfo_height())
    x_cordinate = int((root.winfo_screenwidth() / 2) - (root.winfo_width() / 2))
    y_cordinate = int((root.winfo_screenheight() / 2) - (root.winfo_height() / 2))
    root.geometry("+{}+{}".format(x_cordinate, y_cordinate-20))

    # Deplay application
    root.after(2000, app.plc_routine(True))
    root.mainloop()

    #sync test
