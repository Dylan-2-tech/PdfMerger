# Import the required libraries
from tkinter import *
from customtkinter import *

# Create an instance of tkinter frame or window
win=CTk()

# Set the size of the window
win.geometry("700x350")

# ctk fram
ctkframe = CTkFrame (win, fg_color = ("red"))
ctkframe.grid_propagate(0)
ctkframe.pack(fill = "both", expand = True)

label = CTkLabel (ctkframe, text = "gfsgse")
label.pack()

# Add a Listbox widget with number as the list items
listbox =Listbox(ctkframe)
listbox.insert(END,"C++", "Java", "Python", "Rust", "GoLang", "Ruby", "JavaScript", "C# ", "SQL", "Dart")
listbox.pack(side = "left", fill = "both", expand = True)

win.mainloop()