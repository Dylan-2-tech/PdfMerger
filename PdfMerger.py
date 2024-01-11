
# Importing the glob library to search in directory
import glob

# Importing the sys library in order to know the operating system
import sys

# importing the PdfWriter module to write a pdf file
from PyPDF2 import PdfWriter

# importing the custom tkinter library
from customtkinter import CTk
from customtkinter import CTkLabel
from customtkinter import CTkButton
from customtkinter import CTkFrame
from customtkinter import CTkFont
from customtkinter import CTkEntry
from customtkinter import CTkScrollableFrame
from customtkinter import CTkScrollbar
from customtkinter import CTkOptionMenu
import customtkinter as ctk

# Importing tkinter library
from tkinter import filedialog
from tkinter import Listbox
from tkinter import StringVar

from random import randint


ctk.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"
  
# knowing on which operating system the software is running
sysPlatform = sys.platform
print("système",sysPlatform)

sys_directory = {
    "linux": "/",
    "win32": "\\",
    "darwin": "/"}

if sysPlatform in sys_directory.keys():
    separator = sys_directory[sysPlatform]
else:
    separator = "\\"
print("système de séparation de dossier:"+separator)


file_list = []
simplified_file_list = []


# Function that simplified the name of the file
def simplify_name(file_name):
    sep_name = file_name.split(separator)
    return sep_name[len(sep_name)-1]

def browseFiles():
    try:
        filename = filedialog.askopenfilename(initialdir = separator,
                                              title = "Select a file",
                                              filetypes = (("Pdf files",
                                                            "*.pdf*"),
                                                           ("All files",
                                                            "*.*")))
          
        file_list.append(filename)
        simplified_file_list.append(simplify_name(filename))
        varFile_list.set(simplified_file_list)
    except AttributeError:
        pass
    
# Function that delete the file selected in the listBox
def delete_file(event):
    try:
        file_list.pop(ListBox_File.curselection()[0])
        simplified_file_list.pop(ListBox_File.curselection()[0])
        varFile_list.set(simplified_file_list) # refresh the listBox
    except:
        INFOlabel.configure(text = "select a file to delete")

# function that switch two element by they're index in a list 
def switch(ListFile, i, o):
    temp_file = ListFile[i]
    ListFile[i] = ListFile[o]
    ListFile[o] = temp_file
    
        
def move_file_up(event):
    try:
        selected_file_index = ListBox_File.curselection()[0]
        next_selected_file_index = selected_file_index - 1
        if selected_file_index > 0:
            switch(file_list, selected_file_index, next_selected_file_index)
            switch(simplified_file_list, selected_file_index, next_selected_file_index)
            varFile_list.set(simplified_file_list)
            ListBox_File.select_set(next_selected_file_index)
            ListBox_File.activate(next_selected_file_index)

        elif selected_file_index == 0:
            INFOlabel.configure(text = "can't move up file")
    except:
        INFOlabel.configure(text = "click on a file")

def move_file_down(event):
    try:
        len_file_list = len(file_list)-1
        selected_file_index = ListBox_File.curselection()[0]
        next_selected_file_index = selected_file_index + 1
        if selected_file_index < len_file_list:
            switch(file_list, next_selected_file_index, selected_file_index)
            switch(simplified_file_list, next_selected_file_index, selected_file_index)
            varFile_list.set(simplified_file_list)
            ListBox_File.select_set(next_selected_file_index)
            ListBox_File.activate(next_selected_file_index)

            
        elif selected_file_index == len_file_list:
            INFOlabel.configure(text = "can't move down file")
    except:
        INFOlabel.configure(text = "click on a file")

#Function that append all pdf files in the listBox
def list_all_files():
    
    try:
        directory = filedialog.askdirectory(initialdir = "home/dylantech/projets/PdfMerger",
                                            title = "Select a directory")

        list_of_all_files = glob.glob(directory+separator+"*.pdf")
        for fileN in list_of_all_files:
            file_list.append(fileN)
            simplified_file_list.append(simplify_name(fileN))
        varFile_list.set(simplified_file_list)
    except TypeError:
        pass

# Function that merges pdf files from a list of files
def merge_files(fl):

    if len(simplified_file_list) > 0:

        directory = filedialog.askdirectory(initialdir = separator,
                                            title = "Select a directory")

        fileName = FileNameEntry.get()
        if fileName == "":
            INFOlabel.configure(text = "enter a file name")
        else:
            merger = PdfWriter()
            for pdf in fl:
                merger.append(pdf)
            
            merger.write(directory + separator + fileName + ".pdf")
            merger.close()
            INFOlabel.configure(text = "correctly merged")
        
    else:
        INFOlabel.configure(text = "no file to merge")


def clear_info_label():
    INFOlabel.configure(text = "")


def change_appearance_mode_event(new_appearance_mode: str):
    ctk.set_appearance_mode(new_appearance_mode)

    if new_appearance_mode == "Dark":
        ListBox_File.configure(bg = "grey", selectbackground = "lightgrey")
    elif new_appearance_mode == "Light":
        ListBox_File.configure(bg = "lightgrey", selectbackground = "grey")

    
# Create the root window
window = CTk()
window.title('PDF Merger')
window.geometry("1000x500+450+200")
window.minsize(800, 500)


editColumn = CTkFrame (window, corner_radius = 10) 
selectColumn = CTkFrame (window, corner_radius = 10) 
mergeColumn = CTkFrame (window, corner_radius = 10) 

# Adding label to the three columns
selectColumnLabel = CTkLabel(selectColumn, text = "Select Files", font = CTkFont(size = 25))
editColumnLabel = CTkLabel(editColumn, text = "Edit Files", font = CTkFont(size = 25))
mergeColumnLabel = CTkLabel(mergeColumn, text = "Merge Files", font = CTkFont(size = 25))


INFOlabel = CTkLabel(editColumn, 
                            text = "", font = CTkFont(size = 25),
                            pady = 5)

selectOneFileBtn = CTkButton(selectColumn, 
                        text = "Ajouter un fichier", font = CTkFont(size = 20),
                        command = browseFiles)

selectDirBtn = CTkButton(selectColumn, text = "Ajouter par dossier", font = CTkFont(size = 20),
                        fg_color = "#711890", hover_color = ("#5A0976"),
                        command = list_all_files)


#list box scrollbar
yscrollbar = CTkScrollbar(editColumn)
xscrollbar = CTkScrollbar(editColumn, orientation = 'horizontal')
varFile_list = StringVar(value = file_list)
ListBox_File = Listbox(editColumn, yscrollcommand = yscrollbar.set, xscrollcommand = xscrollbar.set,
    activestyle = "underline", selectbackground = "lightgrey", bg = "grey", fg = "black",
    borderwidth = 0, highlightthickness = 1, listvariable = varFile_list,
    font = CTkFont(size = 17), highlightcolor = ("black"), highlightbackground = ("grey"))
yscrollbar.configure(command = ListBox_File.yview)
xscrollbar.configure(command = ListBox_File.xview)

FileNameEntry = CTkEntry(mergeColumn, width = 200, font = CTkFont(size = 20))

mergeBtn = CTkButton(mergeColumn,
                         text = "Fusionner les fichiers", font = CTkFont(size = 20),
                         command =lambda fl=file_list:merge_files(fl))
  
exitBtn = CTkButton(mergeColumn, 
                     text = "Quitter", font = CTkFont(size = 20),
                     command = window.destroy, fg_color = ("#DD2A2A"), hover_color = ("#B71212"))

appearanceOptionemenu = CTkOptionMenu(window, values=["Dark", "System", "Light"],
                                    command = change_appearance_mode_event)


selectColumn.grid(row = 0, column = 0, sticky = 'nsew', padx = (10, 0), pady = (10, 10))
editColumn.grid(row = 0, column = 1, rowspan = 2, sticky = 'nsew', padx = 10, pady = (10, 10))
mergeColumn.grid(row = 0, column = 2, rowspan = 2, sticky = 'nsew', padx = (0, 10), pady = (10, 10))

# Responsive columns
window.grid_rowconfigure(0, weight = 1)
window.grid_columnconfigure((0,2), weight = 1)  
window.grid_columnconfigure(1, weight = 3)

selectColumnLabel.grid(row = 0, column = 0, sticky = 'n', pady = 10)
editColumnLabel.pack(pady = 10)
mergeColumnLabel.grid(row = 0, column = 0, sticky = 'n', pady = 10)


# placing the explore button in the select column(first one) 
selectOneFileBtn.grid(row = 1, column = 0, pady = (40, 15))
selectDirBtn.grid(row = 2, column = 0)
appearanceOptionemenu.grid(row = 1, column = 0, sticky = "s", pady = (0, 10))

# Placing the list of files in the edit column (middle one)
INFOlabel.pack(side = "bottom", fill = 'x')
xscrollbar.pack(side = "bottom", fill = 'x')
ListBox_File.pack(side = "left", fill = "both", expand = True, pady = (10, 0))#.grid(row = 0, column = 0, sticky = 'nsew', pady = 10, padx = (10, 0))
yscrollbar.pack(side = "right", fill = 'y')


# Placing the merges buttons in the merge column (third one)
FileNameEntry.grid(row = 1, column = 0, pady = (40, 30))
mergeBtn.grid(row = 2, column = 0, pady = (0, 15))
exitBtn.grid(row = 3, column = 0)


# responsive columns grid
selectColumn.grid_columnconfigure(0, weight = 1)
mergeColumn.grid_columnconfigure(0, weight = 1)


# All the shortcuts
window.bind('<Shift-Up>', move_file_up)
window.bind('<Shift-Down>', move_file_down)
window.bind('<Shift-BackSpace>', delete_file)
window.bind('<Return>', sel)
# Let the window wait for any events
window.mainloop()
