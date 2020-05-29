import os
from tkinter import Tk,ttk, PhotoImage, Menu, Frame, Text, Scrollbar, IntVar,GROOVE, \
    StringVar, BooleanVar, Button, END, Label, INSERT, Toplevel, Entry, Checkbutton
import tkinter.filedialog
import tkinter.messagebox

Program_Name = "QuickNotepad"
File_Name = None

root = Tk()
# Setting icon of root window
title_icon = PhotoImage(file='icons/Titleicon.png')
root.iconphoto(False, title_icon)
root.geometry('750x500')
root.minsize(750,500)
root.title(Program_Name)

#other functions
def Oncontentchanged(event=None):
    Updatelineno()
    Updatecursorinfobar()

def Showpopupmenu(event):
    popupmenu.tk_popup(event.x_root, event.y_root)

def Togglehighlight(event=None):
    if to_highlight_line.get():
        Tohighlightline()
    else:
        Undohighlight()

def Undohighlight():
    contenttext.tag_remove("active_line", 1.0, "end")

def Updatecursorinfobar(event=None):
    r, c = contenttext.index(INSERT).split('.')
    l_num, c_num = str(int(r)), str(int(c) + 1)
    infotext = "Line: {0} | Column: {1}".format(l_num, c_num)
    cursorbarinfo.config(text=infotext)


def Writetofile(file_name):
    try:
        content = contenttext.get(1.0, "end")
        with open(file_name, 'w') as file:
            file.write(content)
    except IOError:
        tkinter.messagebox.showwarning("Save", "Could not save the file.")

def Getlinenumbers():
    output = ''
    if show_line_no.get():
        row, col = contenttext.index("end").split('.')
        for i in range(1, int(row)):
            output += str(i) + '\n'
    return output


def Searchoutput(needle, if_ignore_case, content_text,
                 search_toplevel, search_box):
    content_text.tag_remove('match', '1.0', END)
    matches_found = 0
    if needle:
        start_pos = '1.0'
        while True:
            start_pos = content_text.search(needle, start_pos,
                            nocase=if_ignore_case, stopindex=END)
            if not start_pos:
                break
            end_pos = '{}+{}c'.format(start_pos, len(needle))
            content_text.tag_add('match', start_pos, end_pos)
            matches_found += 1
            start_pos = end_pos
        content_text.tag_config(
            'match', foreground='red', background='yellow')
    search_box.focus_set()
    search_toplevel.title('{} matches found'.format(matches_found))



#TODO filemenu command

def Newfile(event=None):
    root.title("Untitled")
    global File_Name
    File_Name = None
    contenttext.delete(1.0, END)
    Oncontentchanged()

def Openfile(event=None):
    inputfilename = tkinter.filedialog.askopenfilename(defaultextension=".txt",
                filetypes=[("All Files", "*.*"), ("Text Documents", "*.txt")])
    if inputfilename:
        global File_Name
        File_Name = inputfilename
        root.title('{}-{}'.format(os.path.basename(File_Name), Program_Name))
        contenttext.delete(1.0, END)
        with open(File_Name) as _file:
            contenttext.insert(1.0, _file.read())
        Oncontentchanged()

def Savefile(event=None):
    global File_Name
    if not File_Name:
        SaveAsfile()
    else:
        Writetofile(File_Name)
    return "break"

def SaveAsfile(event=None):
    inputfilename = tkinter.filedialog.asksaveasfilename(
        initialfile="Untitled",defaultextension=".txt",
        filetypes=[("All Files", "*.*"), ("Text Documents", "*.txt")])
    if inputfilename:
        global File_Name
        File_Name = inputfilename
        Writetofile(File_Name)
        root.title('{}-{}'.format(os.path.basename(File_Name), Program_Name))
    return "break"

def Exiteditor():
    if tkinter.messagebox.askokcancel("Quit?", "Are You Sure?"):
        root.destroy()
#

#TODO editmenu command

def Undo(event=None):
    print("undo executed")
    contenttext.event_generate(("<<Undo>>"))
    Oncontentchanged()

def Redo(event=None):
    contenttext.event_generate(("<<Redo>>"))
    Oncontentchanged()
    return "break"

def Cuttext():
    contenttext.event_generate("<<Cut>>")
    Oncontentchanged()
    return "break"

def Copytext():
    contenttext.event_generate("<<Copy>>")

def Pastetext():
    contenttext.event_generate("<<Paste>>")
    Oncontentchanged()
    return "break"

def Findtext(event=None):
    searchtoplevel = Toplevel(root)
    toplevel_icon = PhotoImage(file='icons/Findtext.png')
    searchtoplevel.title('Find Text')
    searchtoplevel.iconphoto(False,toplevel_icon)
    searchtoplevel.transient(root)

    Label(searchtoplevel, text="Find All:").grid(row=0, column=0, sticky='e')

    search_entry_widget = Entry(searchtoplevel,relief=GROOVE, width=25)
    search_entry_widget.grid(row=0, column=1, padx=2, pady=2, sticky='we')
    search_entry_widget.focus_set()
    ignore_case_value = IntVar()
    Checkbutton(searchtoplevel, text='Ignore Case', variable=ignore_case_value).grid(
        row=1, column=1, sticky='e', padx=2, pady=2)
    Button(searchtoplevel, text="Find All",relief=GROOVE,
           command=lambda: Searchoutput(
               search_entry_widget.get(), ignore_case_value.get(),
               contenttext, searchtoplevel, search_entry_widget)
           ).grid(row=0, column=2, sticky='e' + 'w', padx=2, pady=2)

    def Closesearchwindow():
        contenttext.tag_remove('match', '1.0', END)
        searchtoplevel.destroy()

    searchtoplevel.protocol('WM_DELETE_WINDOW', Closesearchwindow)
    return "break"

def Selectalltext(event=None):
    contenttext.tag_add('sel', '1.0', 'end')
    return "break"


#TODO formatmenu command

def Changefonts(event=None):
    selected_font = font_choice.get()
    selected_font_size = font_size_choice.get()
    font_tupple = (selected_font,selected_font_size)
    contenttext.config(font=font_tupple)

#TODO viewmenu command
def Updatelineno(event=None):
    line_numbers = Getlinenumbers()
    linenumberbar.config(state='normal')
    linenumberbar.delete('1.0', 'end')
    linenumberbar.insert('1.0', line_numbers)
    linenumberbar.config(state='disabled')

def Showcursorinfobar():
    show_cursor_info_check = show_cursor_info.get()
    if show_cursor_info_check:
        cursorbarinfo.pack(expand='no', fill=None, side='right', anchor='se')
    else:
        cursorbarinfo.pack_forget()

def Tohighlightline(interval=100):
    contenttext.tag_remove("active_line", 1.0, "end")
    contenttext.tag_add("active_line", "insert linestart", "insert lineend+1c")
    contenttext.after(interval, Togglehighlight)

def Changethemes(event=None):
    selected_theme = theme_choice.get()
    fg_bg_colors = color_schemes.get(selected_theme)
    fg_color, bg_color = fg_bg_colors.split(".")
    contenttext.config(background=bg_color, fg=fg_color)


#TODO aboutmenu command

def Help():
    help_string1=" Help Guide: QuickNotepad \n From View menu you can change Theme,\n"
    help_string2=" Turn On/Off Line Numbers,Cursor Location,\n And Highlighting Current Line"

    tkinter.messagebox.showinfo("Help","{}{}".format(help_string1,help_string2))


def About():
    tkinter.messagebox.showinfo("About",
                                "{}{}".format(Program_Name,
                    "\nPython Tkinter GUI App \nDeveloped by @compactcoder"))


#TODO menubar icons SETUP

#filemenu images
new_file_icon = PhotoImage(file='icons/Newfile.png')
open_file_icon = PhotoImage(file='icons/Openfile.png')
save_file_icon = PhotoImage(file='icons/Savefile.png')
#editmenu images
undo_icon = PhotoImage(file='icons/Undo.png')
redo_icon = PhotoImage(file='icons/Redo.png')
cut_icon = PhotoImage(file='icons/Cuttext.png')
copy_icon = PhotoImage(file='icons/Copytext.png')
paste_icon = PhotoImage(file='icons/Pastetext.png')
findtext_icon = PhotoImage(file='icons/Findtext.png')

#mainmenubar setup
menubar = Menu(root)


#TODO filemenu GUI

filemenu = Menu(menubar, tearoff=0)

#filemenu adding commands
filemenu.add_command(label="New", accelerator="Ctrl+N", compound="left",
                     image=new_file_icon, underline=0, command=Newfile)
filemenu.add_command(label="Open", accelerator="Ctrl+O", compound="left",
                     image=open_file_icon, underline=0, command=Openfile)
filemenu.add_command(label="Save", accelerator="Ctrl+S", compound="left",
                     image=save_file_icon, underline=0, command=Savefile)
filemenu.add_command(label="SaveAs", accelerator="Ctrl+Shift+N",
                     underline=0, command=SaveAsfile)
filemenu.add_separator()
filemenu.add_command(label="Exit", accelerator="Alt+F4", underline=0,
                     command=Exiteditor)

menubar.add_cascade(label='File', menu=filemenu)


#TODO editmenu GUI

editmenu = Menu(menubar, tearoff=0)

#editmenu adding commands
editmenu.add_command(label="Undo", accelerator="Ctrl+Z", compound="left",
                     image=undo_icon, underline=0, command=Undo)
editmenu.add_command(label="Redo", accelerator="Ctrl+Y", compound="left",
                     image=redo_icon, underline=0, command=Redo)
editmenu.add_separator()
editmenu.add_command(label="Cut", accelerator="Ctrl+X", compound="left",
                     image=cut_icon, underline=0, command=Cuttext)
editmenu.add_command(label="Copy", accelerator="Ctrl+C", compound="left",
                     image=copy_icon, underline=0, command=Copytext)
editmenu.add_command(label="Paste", accelerator="Ctrl+V", compound="left",
                     image=paste_icon, underline=0, command=Pastetext)
editmenu.add_separator()
editmenu.add_command(label="Find", accelerator="Ctrl+F", compound="left",
                     image=findtext_icon, underline=1, command=Findtext)
editmenu.add_command(label="Select All", accelerator="Ctrl+A", compound="left",
                     underline=7, command=Selectalltext)

menubar.add_cascade(label='Edit', menu=editmenu)


#TODO formatmenu GUI

formatmenu = Menu(menubar,tearoff=0)

#format menu adding command
fontsmenu = Menu(formatmenu,tearoff=0)
formatmenu.add_cascade(label='Fonts',menu=fontsmenu)

fontlist=["Arial","Courier New","Comic Sans MS","Calibre","Fixedsys",
          "MS Sans Serif","MS Serif","Symbol", "System", "Times New Roman","Verdana"]
font_choice = StringVar()
font_choice.set('Arial')

for f in fontlist:
    fontsmenu.add_radiobutton(label=f, variable=font_choice,
                               command=Changefonts)

fontsizemenu = Menu(formatmenu,tearoff=0)
formatmenu.add_cascade(label='Font Size',menu=fontsizemenu)
fontsizelist = [i for i in range(101)]
font_size_choice = IntVar()
font_size_choice.set(14)

for f in fontsizelist:
    fontsizemenu.add_radiobutton(label=f, variable=font_size_choice,
                              command=Changefonts)

menubar.add_cascade(label='Format', menu=formatmenu)


#TODO viewmenu GUI

viewmenu = Menu(menubar, tearoff=0)

#viewmenu variables and adding commands
show_line_no = IntVar()
show_line_no.set(1)
viewmenu.add_checkbutton(label="Show Line Numbers", variable=show_line_no,
                         command=Updatelineno)

show_cursor_info = IntVar()
show_cursor_info.set(1)
viewmenu.add_checkbutton(label="Show Cursor Location at Bottom",
                         variable=show_cursor_info, command=Showcursorinfobar)

to_highlight_line = BooleanVar()
viewmenu.add_checkbutton(label="Highlight Current Line", onvalue=1, offvalue=0,
                         variable=to_highlight_line, command=Tohighlightline)

themesmenu = Menu(viewmenu, tearoff=0)
viewmenu.add_cascade(label="Themes", menu=themesmenu)
color_schemes = {
    'Day Light': '#000000.#FFFFFF',
    'Greygarious': '#83406A.#D1D4D1',
    'Aquamarine': '#5B8340.#D1E7E0',
    'Bold Beige': '#4B4620.#FFF0E1',
    'Cobalt Blue': '#ffffBB.#3333aa',
    'Olive Green': '#D1E7E0.#5B8340',
    'Night Mode': '#FFFFFF.#000000',
}
theme_choice = StringVar()
theme_choice.set('Day Light')

for t in sorted(color_schemes):
    themesmenu.add_radiobutton(label=t, variable=theme_choice,
                               command=Changethemes)

menubar.add_cascade(label='View', menu=viewmenu)


#TODO helpmenu GUI

helpmenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label='Help', menu=helpmenu)

#helpmenu adding command
helpmenu.add_command(label="Help", command=Help)
helpmenu.add_command(label="About", command=About)

#configure mainmenu
root.config(menu=menubar)


#TODO shortcutbar GUI

shortcutbar = Frame(root, height=25,borderwidth=0)
shortcutbar.pack(expand="no", fill="x")

icons = ['Newfile', 'Openfile', 'Savefile', 'Cuttext', 'Copytext',
         'Pastetext', 'Undo', 'Redo', 'Findtext']

for icon in icons:
    toolbar_icon = PhotoImage(file="icons/{}.png".format(icon))
    cmd = eval(icon)
    toolbar = Button(shortcutbar, image=toolbar_icon, command=cmd,relief=GROOVE)
    toolbar.image = toolbar_icon
    toolbar.pack(side='left')


#TODO font combobox

fontcomboboxlabel=ttk.Label(shortcutbar,text='          Select Fonts') #combobar label
fontcomboboxlabel.pack(side='left')

fontcombobox = ttk.Combobox(shortcutbar, width = 20, values=fontlist ,
                            textvariable = font_choice,state='readonly')
fontcombobox.pack(side='left')
fontcombobox.current(0)
fontcombobox.bind("<<ComboboxSelected>>", Changefonts)


#TODO fontsize combobox

fontsizecomboboxlabel = ttk.Label(shortcutbar,text='Font Size') #combobar label
fontsizecomboboxlabel.pack(side='left')

fontsizecombobox = ttk.Combobox(shortcutbar, width=5,values=fontsizelist,
                                textvariable=font_size_choice,state='readonly')
fontsizecombobox.pack(side='left')
fontsizecombobox.current(13)
fontsizecombobox.bind("<<ComboboxSelected>>",Changefonts)

#bottomframe for Cursor bar
bottomframe = Frame(root, height=25,borderwidth=0)
bottomframe.pack(side = 'bottom', fill="x")


#TODO linebar GUI

linenumberbar = Text(root, width=4, padx=0, takefocus=0, border=0,
                     background="#f0f0f0", state="disabled", wrap="word")
linenumberbar.pack(side="left",fill="y")


#TODO scrollbar GUI

scrollbar = Scrollbar(root)
scrollbar.pack(side='right', fill='both')


#TODO contentext GUI

contenttext = Text(root, wrap='word',yscrollcommand=scrollbar.set,
                   font=(font_choice.get(),font_size_choice.get()), undo=1)
contenttext.pack(expand='yes', fill='both')
#syncing scrollbar with textarea
scrollbar.config(command=contenttext.yview)


#TODO cursorbarinfo GUI

cursorbarinfo = Label(bottomframe, text='Line: 1 | Column: 1')
cursorbarinfo.pack(fill=None, side='right', anchor='se')


#TODO keybindings GUI

contenttext.bind('<KeyPress-F1>', Help)
contenttext.bind('<Control-N>', Newfile)
contenttext.bind('<Control-n>', Newfile)
contenttext.bind('<Control-O>', Openfile)
contenttext.bind('<Control-o>', Openfile)
contenttext.bind('<Control-S>', Savefile)
contenttext.bind('<Control-s>', Savefile)
contenttext.bind('<Control-f>', Findtext)
contenttext.bind('<Control-F>', Findtext)
contenttext.bind('<Control-A>', Selectalltext)
contenttext.bind('<Control-a>', Selectalltext)
contenttext.bind('<Control-y>', Redo)
contenttext.bind('<Control-Y>', Redo)
contenttext.bind('<Control-z>', Undo)
contenttext.bind('<Control-Z>', Undo)
contenttext.bind('<Any-KeyPress>', Oncontentchanged)
contenttext.bind('<Button-3>', Showpopupmenu)
contenttext.tag_configure('active_line', background='ivory2')


#TODO popupmenu config.

popupmenu = Menu(contenttext, tearoff=0)

popuplabellist=['Cut', 'Copy', 'Paste', 'Undo', 'Redo']
popupcmdlist = ['Cuttext', 'Copytext', 'Pastetext', 'Undo', 'Redo']

for i in range(5):
    cmd = eval(popupcmdlist[i])
    popupmenu.add_command(label=popuplabellist[i], compound="left", command=cmd)
popupmenu.add_separator()
popupmenu.add_command(label='Select All Text', command=Selectalltext)


contenttext.focus_set()
root.protocol('Wm_DELETE_WINDOW', Exiteditor)
root.mainloop()