import os
from tkinter import *
from tkinter import messagebox
from backend import *

#defining colours
base = "#C1E1C1"
white = "#ffffff"
blue = "#0FB5B5"
red = "#FF4500"
grey = "#777777"
orange = "#FFA400"
bold = 'bold'

def showDisplay(fetch):
    i = 1
    for item in fetch:
        display.insert(i, f" {item[0]} - {author(item[1])} - {genre(item[2])} - Shelf {item[3]}")
        if item[4] != 'NONE':
            display.itemconfig(i-1, fg=grey, selectforeground=grey)
        i += 1
    display.grid(row=2, column=1, rowspan=6, columnspan=3, pady=15, padx=10, sticky='e')
def clearDisplay():
    display.delete(0, 'end')
def showAll():
    fetch = searchByName('')
    clearDisplay()
    showDisplay(fetch)

window = Tk()
window.title("Library Management App")
window.configure(bg=base, border=5)
window.geometry("750x420")
icon = PhotoImage(file='icon.png') # Icon taken from flaticon.com
window.iconphoto(False, icon)

searchBy = StringVar(window)
searchBy.set('1. Book Name')
inputField = StringVar(window)

Label(window, text='Search:', bg=base, font=bold).grid(row=0,column=0, sticky='w', padx=43)
Label(window, text='by:', bg=base, font=bold).grid(row=0, column=3, sticky='w', padx=13)
Entry(window, textvariable=inputField, bg=white, width=45, font=bold).grid(row=1, column=0, columnspan=3)
OptionMenu(window, searchBy, '1. Book Name', '2. Author', '3. Genre').grid(row=1, column=3, sticky='w', padx=10)

display = Listbox(window, width=70, height=20, bg=white, activestyle='none', selectmode=BROWSE, selectbackground=orange)
showAll()

def show():
    if searchBy.get()[0] == '1':
        fetch = searchByName(inputField.get())
    if searchBy.get()[0] == '2':
        fetch = searchByAuthor(inputField.get())
    if searchBy.get()[0] == '3':
        fetch = searchByGenre(inputField.get())
    clearDisplay()
    showDisplay(fetch)

def addBook():
    addWindow = Toplevel()
    name, bAuthor, bGenre, shelf = StringVar(addWindow), StringVar(addWindow), StringVar(addWindow), StringVar(addWindow)
    addWindow.title("Add Book")
    addWindow.configure(bg=base, border=5)
    addWindow.geometry("350x150")
    Label(addWindow, text='Book Name: ', bg=base, font=bold).grid(row=0, column=0, padx=5, sticky='e')
    Label(addWindow, text='Author: ', bg=base, font=bold).grid(row=1, column=0, padx=5, sticky='e')
    Label(addWindow, text='Genre: ', bg=base, font=bold).grid(row=2, column=0, padx=5, sticky='e')
    Label(addWindow, text='Shelf: ', bg=base, font=bold).grid(row=3, column=0, padx=5, sticky='e')
    Entry(addWindow, textvariable=name, bg=white, width=20, font=bold).grid(row=0, column=1, sticky='w')
    Entry(addWindow, textvariable=bAuthor, bg=white, width=20, font=bold).grid(row=1, column=1, sticky='w')
    Entry(addWindow, textvariable=bGenre, bg=white, width=20, font=bold).grid(row=2, column=1, sticky='w')
    Entry(addWindow, textvariable=shelf, bg=white, width=20, font=bold).grid(row=3, column=1, sticky='w')
    def addButton(name, bAuthor, bGenre, shelf):
        name, bAuthor, bGenre, shelf = name.get(), bAuthor.get(), bGenre.get(), shelf.get()
        newBook(name, bAuthor, bGenre, shelf)
        showAll()
        addWindow.destroy()
    b = Button(addWindow, text='Add', width=10, command=lambda : addButton(name, bAuthor, bGenre, shelf))
    b.configure(bg=orange, font=bold)
    b.grid(row=4, column=1)

def rmBook():
    try:
        selection = display.curselection()[0]
    except:
        return
    name = display.get(selection)
    dash = name.index('-')
    deleteBook(name[1:dash-1])
    display.delete(selection)

def borrow():
    try:
        selection = display.curselection()[0]
    except:
        return
    name = display.get(selection)
    dash = name.index('-')
    borrowBook(name[1:dash-1], '')
    display.delete(selection)
    item = searchByName(name[1:dash-1])[0]
    display.insert(selection, f" {item[0]} - {author(item[1])} - {genre(item[2])} - Shelf {item[3]}")
    display.itemconfig(selection, fg=grey, selectforeground=grey)

def returnB():
    try:
        selection = display.curselection()[0]
    except:
        return
    name = display.get(selection)
    dash = name.index('-')
    returnBook(name[1:dash-1])
    display.delete(selection)
    item = searchByName(name[1:dash-1])[0]
    display.insert(selection, f" {item[0]} - {author(item[1])} - {genre(item[2])} - Shelf {item[3]}")

def deleteDB():
    if messagebox.askokcancel("Confirm", "This will delete every item from the database"):
        resetDB()
        clearDisplay()

b1 = Button(window, text="SEARCH", command=show)
b1.configure(bg=blue, font=bold)
b1.grid(row=2, column=0, pady=5, sticky='ne')

b2 = Button(window, text="Add Book", command=addBook)
b2.configure(bg=blue, font=bold)
b2.grid(row=3, column=0, pady=5, sticky='se')

b3 = Button(window, text="Remove Book", command=rmBook)
b3.configure(bg=blue, font=bold)
b3.grid(row=4, column=0, pady=5, sticky='ne')

b4 = Button(window, text="Borrow Book", command=borrow)
b4.configure(bg=blue, font=bold)
b4.grid(row=5, column=0, pady=5, sticky='se')

b5 = Button(window, text="Return Book", command=returnB)
b5.configure(bg=blue, font=bold)
b5.grid(row=6, column=0, pady=5, sticky='ne')

b6 = Button(window, text="Clear Database", command=deleteDB)
b6.configure(bg=red, fg = white, font=bold)
b6.grid(row=7, column=0, pady=5, sticky='sw')

window.mainloop()
sql.close()
