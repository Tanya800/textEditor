'''
Проект текстового редактора с системой контроля версий
    Функционал:
    -   Восстановление состояния по сохраненному коммиту
    -   Выбор ветки и выбор коммита

    НЕ ИЗМЕНЯЕТСЯ СОДЕРЖИМОЕ ФАЙЛА ПРИ ИЗМЕНЕНИИ ВЕТКИ\КОМИТА
    НЕТ КНОПКИ ОТКАТИТЬСЯ
'''

import tkinter
from tkinter import *
from tkinter.filedialog import asksaveasfile, askopenfile
from tkinter.messagebox import showerror
from tkinter import messagebox
from tkinter.messagebox import showinfo
import tkinter.font as tkFont
import easygui as eg
from tkinter import ttk
from Editor import *
from Commit import *
from Branch import *
from Setting import *
import pickle
import time

FILE_NAME = tkinter.NONE

CURRENT_COMMIT = 0

# файл с названиями всех веток
FILE_PROJECT = ".vsc/text_editor.txt"


# файл с названиями всех коммитов(файла коммита) в ветке (в данном случае в ветке мастер)
# FILE_MAIN_BRANCH


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

    def restart(self):
        self._mementos = []


# Добавление коммита в ветку
def commit():
    print(CURRENT_BRANCH.getSize())
    print(CURRENT_BRANCH.head)
    if (CURRENT_BRANCH.getSize() != 0) & ((CURRENT_BRANCH.getSize()-1) != CURRENT_BRANCH.head):
        eg.msgbox("Следует создать новую ветку!", ok_button="OK")
        return

    preparingForCommit()

    name = eg.enterbox(msg='Введите название коммита', title='Фиксация изменений', default='commit_1')

    print(name)
    if name == None:
        return

    shapshot = editor.createSnapshot()
    print(shapshot.get_text())
    parent = CURRENT_BRANCH.getSize() - 1 if CURRENT_BRANCH.getSize() != 0 else 0

    current_commit = Commit(CURRENT_BRANCH.getSize(), name, shapshot, CURRENT_BRANCH.getName(), parent)

    CURRENT_BRANCH.addCommit(current_commit)


# Сохранение коммитов в файле ветки
def push():
    CURRENT_BRANCH.saveBranch(FILE_CURRENT_BRANCH)


# Загрузка коммита из файла
def showCommits():
    commits = CURRENT_BRANCH.getCommits()
    message = ''
    for commit in commits:
        message += commit.getInfo() + '\n'

    messagebox.showinfo("All commits", message)


# Выбрать коммит
def checkout():

    names = list()
    currentCommits = {}
    global CURRENT_BRANCH, FILE_CURRENT_BRANCH, CURRENT_PROJECT

    for commit in CURRENT_BRANCH.getCommits():
        names.append(commit.getName())
        currentCommits[commit.getName()] = commit.getIndex()

    out = eg.choicebox(msg="Выберете коммит: ", title="Выбрать коммит", choices=names)

    if (out == None):
        return
    else:
        print("Выбранный коммит: ", out)

    caretaker.restart()

    CURRENT_BRANCH.setHead(currentCommits[out])

    print('Указатель сменен на коммит: ', CURRENT_BRANCH.getHead().getName())

    updateText(CURRENT_BRANCH.getHead())



#
# def new_file():
#     global FILE_NAME
#     FILE_NAME = "Untitled.txt"
#     text.delete('1.0', tkinter.END)
#

# def save_file():
#     data = text.get('1.0', tkinter.END)
#     out = open(FILE_NAME, 'w')
#     out.write(data)
#     out.close()
#

# Сохранение состояния текстового редактора через класс опекуна
def saveTextStat(event=NONE):
    editor.setText(text.get('1.0', tkinter.END))
    caretaker.backup()

def preparingForCommit():
    editor.setText(text.get('1.0', tkinter.END))
    caretaker.restart()

# добавить сохранение текущих параметров

def Undo(event = NONE):
    caretaker.undo()
    moment = editor.createSnapshot()
    changeTextEditor(moment.get_text())


def updateText(commit):
    snapshot = commit.getSnapshot()
    editor.restore(snapshot)
    changeTextEditor(snapshot.get_text())

def changeTextEditor(newText):
    text.delete('1.0', END)
    text.insert(1.0, newText)


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
    messagebox.showinfo("Information", CURRENT_PROJECT.getInfo())


def saveBranch():
    commit = Commit(0, 'commit_first', editor.createSnapshot())
    commit2 = Commit(1, 'commit_second', editor.createSnapshot())
    master = Branch('master', '', [commit, commit2])
    master.setHead(1)
    master.saveBranch(FILE_CURRENT_BRANCH)


def getBranch(filename):
    branch = Branch()
    res = branch.getBranch(filename)

    global CURRENT_PROJECT

    if res == -1:
        print('Файл пустой, создается новая ветка')
        return Branch(CURRENT_PROJECT.getBranchByFilename(filename))
    elif res == -2:
        print('Файл не найден, создан новый')
        return Branch(CURRENT_PROJECT.getBranchByFilename(filename))

    return branch


def getProjectSetting():
    out = open(FILE_PROJECT, 'rb')
    try:
        project = pickle.load(out)
    except EOFError:
        project = Project('TextEditor', str(datetime.now())[:19], DEFAULT_BRANCHES)
    out.close()

    return project


def createBranch():
    name = eg.enterbox(msg='Введите название новой ветки', title='Создание новой ветки', default='branch_1')

    print(name)
    if name == None:
        return

    global CURRENT_BRANCH, CURRENT_PROJECT, FILE_CURRENT_BRANCH

    parent = CURRENT_BRANCH.getSize() - 1 if CURRENT_BRANCH.getSize() != 0 else 0

    preparingForCommit()

    shapshot = editor.createSnapshot()

    print("Текущая ветка проекта ", CURRENT_BRANCH.getName())

    CURRENT_BRANCH = Branch(name, 0, 0, [])
    print("Созданная ветка:  " + CURRENT_BRANCH.getName())

    CURRENT_PROJECT.addBranch(CURRENT_BRANCH.getName(), '.vsc/' + name + '.txt')
    CURRENT_PROJECT.setCurrentBranch(name)

    FILE_CURRENT_BRANCH = CURRENT_PROJECT.getFilenameBranch(name)

    current_commit = Commit(CURRENT_BRANCH.getSize(), 'init', shapshot, name, parent)
    CURRENT_BRANCH.addCommit(current_commit)

    print("Количество коммитов в ветке: ", len(CURRENT_BRANCH.getCommits()))


def changeBranch():
    names = list()
    global CURRENT_BRANCH, FILE_CURRENT_BRANCH, CURRENT_PROJECT

    for branch in CURRENT_PROJECT.getBranches():
        names.append(branch)
    out = eg.choicebox(msg="Выберете ветку: ", title="Ветки проекта", choices=names)

    if (out == None):
        return
    else:
        print("Выбрана ветка: ", out)

    CURRENT_PROJECT.setCurrentBranch(out)
    FILE_CURRENT_BRANCH = CURRENT_PROJECT.getCurrentBranch()
    CURRENT_BRANCH = getBranch(FILE_CURRENT_BRANCH)
    print("После выбора новой ветки FILE_CURRENT_BRANCH:", CURRENT_PROJECT.getCurrentBranch())
    print("CURRENT_BRANCH:", CURRENT_BRANCH.getName())


def families_changed(event):
    text.configure(font=(families_cb.get()))


# msg = f'You selected {families_cb.get()}!'
# showinfo(title='Result', message=msg)

def click_bigger():
    curr_size = 14
    start_index = text.index(tkinter.SEL_FIRST)
    end_index = text.index(tkinter.SEL_LAST)
    fontExample = tkFont.Font(family=families_cb.get(), size=curr_size, weight="bold", slant="italic")
    print(text.get(start_index, end_index))
    text.tag_add('tag1', start_index, end_index)
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

def backspace(event):
    print(text.index(SEL_LAST))
    print('backspace')

def uno(event):
    # print(text.index(SEL_LAST))
    print('uno')

def exit():
    global root
    print("Обрабатывается выход из приложения...")
    out = eg.ccbox(msg="Сохранить проект перед выходом?", choices=('Да', 'Нет'), title="Сохранение")

    if out == True:
        out = open(FILE_PROJECT, 'wb+')
        pickle.dump(CURRENT_PROJECT, out)
        out.close()
        print("Проект сохранен")
    root.quit()


# showinfo(title='Result', message='Вы кликнули на стрелку низ')


root = tkinter.Tk()
root.title("CDL Notepad v.0.1")

root.minsize(width=500, height=500)
root.maxsize(width=500, height=500)

text = tkinter.Text(root, width=225, height=27, bg="white",
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
# text.insert(END, '''\
# blah blah blah Failed blah blah
# blah blah blah Passed blah blah
# blah blah blah Failed blah blah
# blah blah blah Failed blah blah
# ''')

menuBar = tkinter.Menu(root)
fileMenu = tkinter.Menu(menuBar)
vcsMenu = tkinter.Menu(menuBar)
branchMenu = tkinter.Menu(menuBar)

# fileMenu.add_command(label="New", command=new_file)
# fileMenu.add_command(label="Open", command=open_file)
fileMenu.add_command(label="Save", command=saveTextStat)
# fileMenu.add_command(label="Save as", command=save_as)

vcsMenu.add_command(label="Commit", command=commit)
vcsMenu.add_command(label="Push", command=push)
vcsMenu.add_command(label="Checkout", command=checkout)
vcsMenu.add_command(label="Show commit", command=showCommits)

branchMenu.add_command(label="Create branch", command=createBranch)
branchMenu.add_command(label="Change branch", command=changeBranch)

branchMenu.add_command(label="Save", command=saveBranch)
# branchMenu.add_command(label="Get", command=getBranch)

menuBar.add_cascade(label="File", menu=fileMenu)
menuBar.add_cascade(label="VCS", menu=vcsMenu)
menuBar.add_cascade(label="Branch", menu=branchMenu)
menuBar.add_cascade(label="Info", command=info)
menuBar.add_cascade(label="Undo", command=Undo)
menuBar.add_cascade(label="Show states", command=show_states)

menuBar.add_cascade(label="Exit", command=exit)

root.config(menu=menuBar)



# ПРЕДВАРИТЕЛЬНАЯ НАСТРОЙКА ПРОЕКТА
CURRENT_PROJECT = getProjectSetting()
FILE_CURRENT_BRANCH = CURRENT_PROJECT.getCurrentBranch()
CURRENT_BRANCH = getBranch(FILE_CURRENT_BRANCH)
print()
print("Первоначальная настройка проекта завершена")
print("FILE_MAIN_BRANCH: ", FILE_CURRENT_BRANCH)
print("CURRENT_BRANCH: ", CURRENT_BRANCH.getName())
print()

text.insert(END,CURRENT_BRANCH.getHead().getSnapshot().get_text() )
editor = Editor(text.get('1.0', tkinter.END))
caretaker = Caretaker(editor)
caretaker.backup()

# time.sleep(5)

# Добавление команд на нажатие клавиатуры
root.bind('<Control-s>', saveTextStat)
root.bind('<Control-z>', Undo)
root.bind('<BackSpace>', backspace)
root.bind('<Control-a>', uno)

root.protocol('WM_DELETE_WINDOW', exit)
root.mainloop()
