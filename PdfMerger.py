
# Importing the glob library to search in directory
import glob

# Importing the sys library in order to know the operating system
import sys

# importing the PdfWriter module to write a pdf file
from PyPDF2 import PdfWriter

# importing the custom tkinter library
import customtkinter as ctk
from customtkinter import CTkLabel
from customtkinter import CTkButton
from customtkinter import CTkFrame
from customtkinter import CTkFont
from customtkinter import CTkEntry

# Importing tkinter library
from tkinter import filedialog
from tkinter import Listbox
from tkinter import StringVar
  
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
                                              title = "Choisissez un fichier",
                                              filetypes = (("fichier pdf",
                                                            "*.pdf*"),
                                                           ("tout les fichiers",
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
        label_INFO.configure(text = "Vous devez séléctionner un fichier pour le supprimer")

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
            
            label_INFO.configure(text = "fichier déplacer de 1 cran supérieur")
        elif selected_file_index == 0:
            label_INFO.configure(text = "Le fichier ne peut pas monter plus que ça")
    except:
        label_INFO.configure(text = "Vous devez séléctionner un fichier pour le remonter")

def move_file_down(event):
    try:
        len_file_list = len(file_list)-1
        selected_file_index = ListBox_File.curselection()[0]
        next_selected_file_index = selected_file_index + 1
        if selected_file_index < len_file_list:
            switch(file_list, selected_file_index, next_selected_file_index)
            switch(simplified_file_list, selected_file_index, next_selected_file_index)
            varFile_list.set(simplified_file_list)
            
        elif selected_file_index == len_file_list:
            label_INFO.configure(text = "Le fichier ne peut pas descendre plus que ça")
    except:
        label_INFO.configure(text = "Vous devez séléctionner un fichier pour le remonter")

#Function that append all pdf files in the listBox
def list_all_files():
    
    try:
        directory = filedialog.askdirectory(initialdir = "home/dylantech/projets/PdfMerger",
                                            title = "Choisissez un dossier")

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
                                            title = "Choisissez un dossier")

        fileName = File_Name_Entry.get()
        if fileName == "":
            label_INFO.configure(text = "Veuillez entrer un nom de fichier")
        else:
            merger = PdfWriter()
            for pdf in fl:
                merger.append(pdf)
            
            merger.write(directory + separator + fileName + ".pdf")
            merger.close()
            label_INFO.configure(text = "correctly merged")
        
    else:
        label_INFO.configure(text = "Aucun fichier à fusionné")
    
    
# Create the root window
window = ctk.CTk()
  
# Set window title
window.title('PDF Merger')
  
# Set window size
window.geometry("700x450")
window.minsize(600,400)


#Set window background color
window.config(background = "grey")
  

label_INFO = CTkLabel(window, 
                            text = "", font = CTkFont(size = 25),
                            width = 100, height = 4, 
                            text_color = ("black"),
                            fg_color = "grey")

button_explore = CTkButton(window, 
                        text = "Ajouter un fichier",
                        command = browseFiles)

File_Name_Entry = CTkEntry(window)

button_merge = CTkButton(window,
                         text = "Fusionner les fichiers",
                         command =lambda fl=file_list:merge_files(fl))
  
button_exit = CTkButton(window, 
                     text = "Quitter",
                     command = window.destroy)

button_list_all_files = CTkButton(window, text = "Ajouter par dossier",
                        fg_color = "purple",
                        command = list_all_files)

varFile_list = StringVar(value = file_list)
ListBox_File = Listbox(window, width = 60, height = 20,
    activestyle = "none", selectbackground = "grey", bg = "lightgrey", fg = "black",
    borderwidth = 0, highlightthickness=0, listvariable = varFile_list)
  
label_INFO.grid(column = 2, row = 4)
button_explore.grid(column = 1, row = 1)
button_list_all_files.grid(column = 1, row = 2)
File_Name_Entry.grid(column = 3, row = 1)
button_merge.grid(column = 3, row = 2)
ListBox_File.grid(column = 2, row = 2, rowspan = 2)
button_exit.grid(column = 1,row = 3)

window.columnconfigure(1, weight = 1)
window.columnconfigure(2, weight = 2)
window.columnconfigure(3, weight = 1)

# All the shortcuts
window.bind('<Shift-Up>', move_file_up)
window.bind('<Shift-Down>', move_file_down)
window.bind('<BackSpace>', delete_file)
# Let the window wait for any events
window.mainloop()
