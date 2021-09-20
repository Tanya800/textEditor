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
from Editor import *

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


def new_file():
	global FILE_NAME
	FILE_NAME = "Untitled"
	text.delete('1.0', tkinter.END)

def save_file():
	data = text.get('1.0', tkinter.END)
	out = open(FILE_NAME, 'w')
	out.write(data)
	out.close()

def save_stat():
	editor.setText(text.get('1.0', tkinter.END))
	caretaker.backup()


def Undo():
	caretaker.undo()
	moment = editor.createSnapshot()
	text.delete('1.0',END)
	text.insert(1.0,moment.get_text())

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


root = tkinter.Tk()
root.title("CDL Notepad v.0.1")

root.minsize(width=500, height=500)
root.maxsize(width=500, height=500)

text = tkinter.Text(root, width=400, height=400, wrap="word")
scrollb = Scrollbar(root, orient=VERTICAL, command=text.yview)
scrollb.pack(side="right", fill="y")
text.configure(yscrollcommand=scrollb.set)
text.pack()
menuBar = tkinter.Menu(root)
fileMenu = tkinter.Menu(menuBar)
fileMenu.add_command(label="New", command=new_file)
fileMenu.add_command(label="Open", command=open_file)
fileMenu.add_command(label="Save", command=save_stat)
fileMenu.add_command(label="Save as", command=save_as)

menuBar.add_cascade(label="File", menu=fileMenu)
menuBar.add_cascade(label="Info", command=info)
menuBar.add_cascade(label="Undo", command=Undo)
menuBar.add_cascade(label="Show states", command=show_states)
menuBar.add_cascade(label="Exit", command=root.quit)
root.config(menu=menuBar)

editor = Editor(text.get('1.0', tkinter.END))
caretaker = Caretaker(editor)
caretaker.backup()

root.mainloop()