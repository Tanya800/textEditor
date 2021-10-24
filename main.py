'''
*  https://coderlog.top
*  https://youtube.com/CoderLog
*  https://youtu.be/DDFHtTIPvZ0
'''

import tkinter
from tkinter import *
from tkinter.filedialog import asksaveasfile, askopenfile
from tkinter.messagebox import showerror
from tkinter import messagebox
from tkinter.messagebox import showinfo
import tkinter.font as tkFont
from tkinter import ttk
from Editor import *
from Commit import *
import pickle

FILE_NAME = tkinter.NONE


class Caretaker():
    """
    Опекун не зависит от класса Конкретного Снимка. Таким образом, он не имеет
    доступа к состоянию создателя, хранящемуся внутри снимка. Он работает со
    всеми снимками через базовый интерфейс Снимка.
    """

    def __init__(self, editor: Editor) -> None:
        self._mementos = []
        self._editor = editor

    def backup(self) -> None:
        print("\nCaretaker: Saving Editor's text...")
        self._mementos.append(self._editor.createSnapshot())

    def undo(self) -> None:
        if not len(self._mementos):
            return

        memento = self._mementos.pop()
        print(f"Caretaker: Restoring text to: {memento.get_name()}")
        try:
            self._editor.restore(memento)
        except Exception:
            self.undo()

    def show_history(self) -> None:
        print("Caretaker: Here's the list of mementos:")
        for memento in self._mementos:
            print(memento.get_name())

def commit():
	shapshot = editor.createSnapshot()
	current_commit = Commit(1,'name',shapshot,'parent','none')
	out = open(FILE_NAME, 'wb')
	pickle.dump(current_commit, out)
	out.close()

def show_last_commit():
	out = open(FILE_NAME, 'rb')
	last_commit = pickle.load(out)
	out.close()
	current_commit = Commit()
	current_commit.setCommit(last_commit)
	for inf in current_commit.getAll():
		print(inf)
	print(current_commit)

def new_file():
	global FILE_NAME
	FILE_NAME = "Untitled.txt"
	text.delete('1.0', tkinter.END)

def save_file():
	data = text.get('1.0', tkinter.END)
	out = open(FILE_NAME, 'w')
	out.write(data)
	out.close()

def save_stat():
	editor.setText(text.get('1.0', tkinter.END))
	caretaker.backup()
# добавить сохранение текущих параметров

def Undo():
	caretaker.undo()
	moment = editor.createSnapshot()
	text.delete('1.0',END)
	text.insert(1.0,moment.get_text())
# добавить востановление параметров
def show_states():
	caretaker.show_history()

def save_as():
	out = asksaveasfile(mode='w', defaultextension='txt')
	data = text.get('1.0', tkinter.END)
	try:
		out.write(data.rstrip())
	except Exception:
		showerror(title="Error", message="Saving file error")

def open_file():
	global FILE_NAME
	inp = askopenfile(mode="r")
	if inp is None:
		return
	FILE_NAME = inp.name
	data = inp.read()
	text.delete('1.0', tkinter.END)
	text.insert('1.0', data)

def info():
	messagebox.showinfo("Information", "CDL Notepad v.0.1\nby CoderLog\nhttps://coderlog.top")

def families_changed(event):
	text.configure(font=(families_cb.get()))
    # msg = f'You selected {families_cb.get()}!'
    # showinfo(title='Result', message=msg)

def click_bigger():
	curr_size = 14
	start_index = text.index(tkinter.SEL_FIRST)
	end_index = text.index(tkinter.SEL_LAST)
	fontExample = tkFont.Font(family=families_cb.get(), size=curr_size, weight="bold", slant="italic")
	print(text.get(start_index,end_index))
	text.tag_add('tag1',start_index,end_index)
	text.tag_config("tag1", font=fontExample)



def click_smaller():
	print(text.selection_get())
	curr_size = 11
	start_index = text.index(tkinter.SEL_FIRST)
	end_index = text.index(tkinter.SEL_LAST)
	fontExample = tkFont.Font(family=families_cb.get(), size=curr_size, weight="bold", slant="italic")
	print(text.get(start_index, end_index))
	text.tag_add('tag1', start_index, end_index)
	text.tag_config("tag1", font=fontExample)
	#showinfo(title='Result', message='Вы кликнули на стрелку низ')


root = tkinter.Tk()
root.title("CDL Notepad v.0.1")

root.minsize(width=500, height=500)
root.maxsize(width=500, height=500)

text = tkinter.Text(root, width=225, height=25,bg="white",
            fg='black', wrap=WORD)

scrollb = Scrollbar(root, orient=VERTICAL, command=text.yview)
scrollb.pack(side="right", fill="y")
text.configure(yscrollcommand=scrollb.set)

toolbar = Frame(root)
toolbar.pack(side=TOP, fill=X)


families = ("Times", "Courier", "Helvetica")
selected_fam = tkinter.StringVar()
families_cb = ttk.Combobox(toolbar, textvariable=selected_fam)

families_cb['values'] = families
families_cb['state'] = 'readonly'  # normal
families_cb.set(families[0])
families_cb.bind('<<ComboboxSelected>>', families_changed)
families_cb.pack(side=LEFT)

btn_bigger = Button(toolbar, text="A↑", background="#555", foreground="#ccc",
             command=click_bigger)
btn_bigger.pack(side=LEFT, padx=0, pady=0)

btn_smaller = Button(toolbar, text="A↓", background="#555", foreground="#ccc",
             command=click_smaller)
btn_smaller.pack(side=LEFT, padx=0, pady=0)



text.pack()
text.insert(END, '''\
blah blah blah Failed blah blah
blah blah blah Passed blah blah
blah blah blah Failed blah blah
blah blah blah Failed blah blah
''')



menuBar = tkinter.Menu(root)
fileMenu = tkinter.Menu(menuBar)
fileMenu.add_command(label="New", command=new_file)
fileMenu.add_command(label="Open", command=open_file)
fileMenu.add_command(label="Save", command=save_stat)
fileMenu.add_command(label="Save as", command=save_as)
fileMenu.add_command(label="Commit", command=commit)

menuBar.add_cascade(label="File", menu=fileMenu)
menuBar.add_cascade(label="Info", command=info)
menuBar.add_cascade(label="Undo", command=Undo)
menuBar.add_cascade(label="Show states", command=show_states)
menuBar.add_cascade(label="Show commit", command=show_last_commit)
menuBar.add_cascade(label="Exit", command=root.quit)

root.config(menu=menuBar)

editor = Editor(text.get('1.0', tkinter.END))
caretaker = Caretaker(editor)
caretaker.backup()

root.mainloop()