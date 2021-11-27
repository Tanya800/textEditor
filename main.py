'''
Проект текстового редактора с системой контроля версий
    Функционал:
    -   Восстановление состояния по сохраненному коммиту
    -   Выбор ветки и выбор коммита
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
from Styles import *
import pickle
import time

BOLD = "bold"
CURSIVE = "italic"
FILE_NAME = tkinter.NONE

CURRENT_COMMIT = 0


FILE_PROJECT = ".vsc/text_editor.txt"

CURRENT_STYLE = Style()


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

    def len_moments(self):
        return len(self._mementos)

    def restart(self):
        self._mementos = []

    def updateStyle(self, style):
        print('editor update style')
        self._editor.setStyle(style)

    def updateText(self, text):
        print('editor update text')
        self._editor.setText(text)


def createdStyle(old):
    tags=[]
    for tag in old.getTags():
        new = Tag(tag.getName(),tag.getStart(),tag.getEnd(),tag.getFamilies(),tag.getSize(),tag.getBold(),tag.getCursive())
        tags.append(new)
    style = Style(tags,old.getFont(),old.getSize(),old.getBold(),old.getCursive())
    return style

# Добавление коммита в ветку
def commit():

    print(CURRENT_BRANCH.getSize())
    print(CURRENT_BRANCH.head)
    if (CURRENT_BRANCH.getSize() != 0) & ((CURRENT_BRANCH.getSize() - 1) != CURRENT_BRANCH.head):
        eg.msgbox("Следует создать новую ветку!", ok_button="OK")
        return

    preparingForCommit()

    name = eg.enterbox(msg='Введите название коммита', title='Фиксация изменений', default='commit_1')

    print(name)
    if name == None:
        return

    shops = editor.createSnapshot()

    last_index = CURRENT_BRANCH.getSize() - 1 if CURRENT_BRANCH.getSize() != 0 else 0
    parent = {
        'index': last_index,
        'branch': CURRENT_BRANCH.getName()
    }
    current_commit = Commit(CURRENT_BRANCH.getSize(), name, shops, CURRENT_BRANCH.getName(), parent)
    print('Стиль сохраняемого коммита', end=' : ')
    print(shops.get_style().getConfig())

    CURRENT_BRANCH.addCommit(current_commit)


def showAllStylesForCommits():

    commits = CURRENT_BRANCH.getCommits()
    for commit in commits:
        print(commit.getInfo() ,end=': ')
        style = commit.getSnapshot().get_style()
        print(style.getConfig())

        for tag in style.getTags():
            print(tag.getConfig())



# Сохранение коммитов в файле ветки
def push():
    CURRENT_BRANCH.saveBranch(FILE_CURRENT_BRANCH)

def reset():

    global CURRENT_BRANCH
    current_commit = CURRENT_BRANCH.getHead()
    parent = current_commit.getParent()
    # print(parent)

    parent_branch = parent['branch']
    parent_index = parent['index']

    if CURRENT_BRANCH.getName() == parent_branch:

        caretaker.restart()
        CURRENT_BRANCH.setHead(parent_index)
        print('Указатель сменен на коммит: ', CURRENT_BRANCH.getHead().getName())
        updateText(CURRENT_BRANCH.getHead())

    else:

        CURRENT_PROJECT.setCurrentBranch(parent_branch)
        FILE_CURRENT_BRANCH = CURRENT_PROJECT.getCurrentBranch()
        CURRENT_BRANCH = getBranch(FILE_CURRENT_BRANCH)
        # print("После выбора новой ветки FILE_CURRENT_BRANCH:", CURRENT_PROJECT.getCurrentBranch())
        print("CURRENT_BRANCH:", CURRENT_BRANCH.getName())

        updateText(CURRENT_BRANCH.getHead())


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


# Сохранение состояния текстового редактора через класс опекуна
def saveTextStat():
    print('saving state...')
    caretaker.updateText(text.get('1.0', tkinter.END))
    caretaker.updateStyle(createdStyle(CURRENT_STYLE))
    editor.setText(text.get('1.0', tkinter.END))
    editor.setStyle(createdStyle(CURRENT_STYLE))
    caretaker.backup()




def preparingForCommit():
    editor.setText(text.get('1.0', tkinter.END))
    editor.setStyle(createdStyle(CURRENT_STYLE))
    caretaker.restart()


def Undo():
    print('trying undo...')

    caretaker.undo()
    if caretaker.len_moments() == 0:
        return

    moment = editor.createSnapshot()
    changeTextEditor(moment)


def updateText(commit):

    snapshot = commit.getSnapshot()
    editor.restore(snapshot)
    changeTextEditor(snapshot)


def changeTextEditor(snapshot):
    newText = snapshot.get_text()

    text.delete('1.0', END)
    text.insert(1.0, newText)

    global CURRENT_STYLE
    new_style = createdStyle(snapshot.get_style())

    CURRENT_STYLE = new_style
    upStyles()


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


def getBranch(filename):
    branch = Branch()
    res = branch.getBranch(filename)

    global CURRENT_PROJECT

    if res == -1:
        # print('Файл пустой, создается новая ветка')
        return Branch(CURRENT_PROJECT.getBranchByFilename(filename))
    elif res == -2:
        # print('Файл не найден, создан новый')
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

    if name == None:
        return

    global CURRENT_BRANCH, CURRENT_PROJECT, FILE_CURRENT_BRANCH

    last_index = CURRENT_BRANCH.getSize() - 1 if CURRENT_BRANCH.getSize() != 0 else 0

    parent={
        'index': last_index,
        'branch': CURRENT_BRANCH.getName()
    }

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
    print()


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
    # print("После выбора новой ветки FILE_CURRENT_BRANCH:", CURRENT_PROJECT.getCurrentBranch())
    print("CURRENT_BRANCH:", CURRENT_BRANCH.getName())

    updateText(CURRENT_BRANCH.getHead())


# БЛОК СО СТИЛЯМИ -------------------------------------------------------------------------------

def upStyles():

    global CURRENT_STYLE

    for tag in text.tag_names():
        text.tag_remove(tag, "1.0", "end")

    new_font = tkFont.Font(family=CURRENT_STYLE.getFont(), size=CURRENT_STYLE.getSize(),
                           weight=CURRENT_STYLE.getBold(), slant=CURRENT_STYLE.getCursive())
    label1.config(text='Size :{}'.format(CURRENT_STYLE.getSize()))

    text.configure(font=new_font)

    tags = CURRENT_STYLE.getTags()

    for tag in tags:
        tag_font = tag.getFont()
        name_tag = tag.getName()
        text.tag_add(name_tag, tag.getStart(), tag.getEnd())
        text.tag_config(name_tag, font=tag_font)

    return


def families_changed(event):
    new_families = families_cb.get()

    CURRENT_STYLE.setFont(new_families)

    upStyles()

    # new_font = tkFont.Font(family=CURRENT_STYLE.getFont(), size=CURRENT_STYLE.getSize(),
    #                        weight=CURRENT_STYLE.getBold(), slant=CURRENT_STYLE.getCursive())
    #
    # text.configure(font=new_font)



def click_bigger():
    global CURRENT_STYLE
    current_size = CURRENT_STYLE.getSize()

    if current_size >= 62:
        return

    indexes = getPartOfText()

    if indexes == -1:

        CURRENT_STYLE.setSize(current_size + 2)

        font = tkFont.Font(family=CURRENT_STYLE.getFont(), size=CURRENT_STYLE.getSize(), weight=CURRENT_STYLE.getBold(),
                           slant=CURRENT_STYLE.getCursive())
        text.config(font=font)
        label1.config(text='Size :{}'.format(CURRENT_STYLE.getSize()))
        return

    start_index, end_index = indexes

    is_exist = CURRENT_STYLE.findTag(start_index, end_index)

    if is_exist != -1:

        print()
        tags = CURRENT_STYLE.getTags()
        current_tag = tags[is_exist]
        print('Тэг ' + current_tag.getName() + ' существует')

        current_size = current_tag.getSize()
        current_tag.setSize(current_size + 2)

        text.tag_remove(current_tag.getName(), "1.0", "end")

        text.tag_add(current_tag.getName(), current_tag.getStart(), current_tag.getEnd())
        text.tag_config(current_tag.getName(), font=current_tag.getFont())

        CURRENT_STYLE.updateTag(is_exist, current_tag)

    else:

        new_tag = Tag(start_index + end_index + 'bigger', start_index, end_index,CURRENT_STYLE.getFont(), CURRENT_STYLE.getSize()+2,
                      CURRENT_STYLE.getBold(),CURRENT_STYLE.getCursive())
        text.tag_add(new_tag.getName(), new_tag.getStart(), new_tag.getEnd())

        fontExample = new_tag.getFont()
        text.tag_config(new_tag.getName(), font= fontExample)

        CURRENT_STYLE.addTag(new_tag)


def click_smaller():
    global CURRENT_STYLE
    current_size = CURRENT_STYLE.getSize()
    if current_size <= 2:
        return

    indexes = getPartOfText()

    if indexes == -1:

        CURRENT_STYLE.setSize(current_size - 2)

        font = tkFont.Font(family=CURRENT_STYLE.getFont(), size=CURRENT_STYLE.getSize(), weight=CURRENT_STYLE.getBold(),
                           slant=CURRENT_STYLE.getCursive())
        text.config(font=font)
        label1.config(text='Size :{}'.format(CURRENT_STYLE.getSize()))
        return

    start_index, end_index = indexes

    is_exist = CURRENT_STYLE.findTag(start_index, end_index)

    if is_exist != -1:

        print()
        tags = CURRENT_STYLE.getTags()
        current_tag = tags[is_exist]
        print('Тэг ' + current_tag.getName() + ' существует')

        current_size = current_tag.getSize()

        print('Old size' + str(current_size))
        current_tag.setSize(current_size - 2)
        print('New size' + str(current_tag.getSize()))

        text.tag_remove(current_tag.getName(), "1.0", "end")

        text.tag_add(current_tag.getName(), current_tag.getStart(), current_tag.getEnd())
        text.tag_config(current_tag.getName(), font=current_tag.getFont())

        CURRENT_STYLE.updateTag(is_exist, current_tag)

    else:

        new_tag = Tag(start_index + end_index + 'smaller', start_index, end_index,CURRENT_STYLE.getFont(), CURRENT_STYLE.getSize() + 2,CURRENT_STYLE.getBold(),
                      CURRENT_STYLE.getCursive())

        text.tag_add(new_tag.getName(), new_tag.getStart(), new_tag.getEnd())

        fontExample = new_tag.getFont()

        text.tag_config(new_tag.getName(), font=fontExample)

        CURRENT_STYLE.addTag(new_tag)


def infoStyle(event):
    print("Current Style:")
    print("Families: " + CURRENT_STYLE.getFont())
    print("Size: ", str(CURRENT_STYLE.getSize()))
    print("Bold: " + CURRENT_STYLE.getBold())
    print("Cursive: " + CURRENT_STYLE.getCursive())


def infoTags(event):

    print(text.tag_names())
    tags = CURRENT_STYLE.getTags()
    for tag in tags:
        print(tag.getConfig())

def deleteAllTags():
    CURRENT_STYLE.setTags([])
    upStyles()


def click_bold():

    global CURRENT_STYLE
    indexes = getPartOfText()

    if indexes == -1:

        if CURRENT_STYLE.getBold() == BOLD:
            CURRENT_STYLE.setBold("normal")
        else:
            CURRENT_STYLE.setBold()

        font = tkFont.Font(family=CURRENT_STYLE.getFont(), size=CURRENT_STYLE.getSize(), weight=CURRENT_STYLE.getBold(),
                           slant=CURRENT_STYLE.getCursive())
        text.config(font=font)

    else:
        start_index, end_index = indexes

        is_exist = CURRENT_STYLE.findTag(start_index, end_index)

        if is_exist != -1:

            print()
            tags = CURRENT_STYLE.getTags()
            current_tag = tags[is_exist]
            print('Тэг ' + current_tag.getName() + ' существует')
            # text.tag_remove(current_tag.getName(), "1.0", "end")
            # CURRENT_STYLE.deleteTag(is_exist)

            if CURRENT_STYLE.tagIsUniqueWithoutOne(current_tag, BOLD):

                print('Полностью удаляем тэг')
                text.tag_remove(current_tag.getName(), "1.0", "end")
                CURRENT_STYLE.deleteTag(is_exist)
            else:

                if(current_tag.getBold() == BOLD):
                    current_tag.setBold("normal")
                else:
                    current_tag.setBold()
                text.tag_remove(current_tag.getName(), "1.0", "end")

                text.tag_add(current_tag.getName(), current_tag.getStart(),  current_tag.getEnd())
                text.tag_config(current_tag.getName(), font=current_tag.getFont())

                CURRENT_STYLE.updateTag(is_exist, current_tag)

        else:

            new_tag = Tag(start_index + end_index + 'bold', start_index, end_index, CURRENT_STYLE.getFont(),
                          CURRENT_STYLE.getSize(), BOLD, CURRENT_STYLE.getCursive())

            text.tag_add(new_tag.getName(), new_tag.getStart(), new_tag.getEnd())
            temp_font = new_tag.getFont()
            text.tag_config(new_tag.getName(), font=temp_font)

            CURRENT_STYLE.addTag(new_tag)


def getPartOfText():
    try:
        start_index = text.index(tkinter.SEL_FIRST)
        end_index = text.index(tkinter.SEL_LAST)
        return [start_index, end_index]
    except TclError:
        return -1


def click_cursive():
    global CURRENT_STYLE
    indexes = getPartOfText()

    if indexes == -1:


        if CURRENT_STYLE.getCursive() == CURSIVE:
            CURRENT_STYLE.setCursive("roman")
        else:
            CURRENT_STYLE.setCursive()

        config_style = CURRENT_STYLE.getConfig()
        font = tkFont.Font(family=config_style['font'], size=config_style['size'], weight=config_style['bold'],
                           slant=config_style['cursive'])

        text.config(font=font)

    else:

        start_index, end_index = indexes

        is_exist = CURRENT_STYLE.findTag(start_index, end_index)

        if is_exist != -1:
            print()

            tags = CURRENT_STYLE.getTags()
            current_tag = tags[is_exist]

            print('Тэг ' + current_tag.getName() + ' существует')

            if CURRENT_STYLE.tagIsUniqueWithoutOne(current_tag, 'cursive'):

                print('Полностью удаляем тэг')
                text.tag_remove(current_tag.getName(), "1.0", "end")
                CURRENT_STYLE.deleteTag(is_exist)
            else:

                if current_tag.getCursive() == CURSIVE:
                    current_tag.setCursive("roman")
                else:
                    current_tag.setCursive()

                text.tag_remove(current_tag.getName(), "1.0", "end")
                text.tag_add(current_tag.getName(), current_tag.getStart(), current_tag.getEnd())
                text.tag_config(current_tag.getName(), font=current_tag.getFont())

                CURRENT_STYLE.updateTag(is_exist, current_tag)

        else:

            stand_conf = CURRENT_STYLE.getConfig()
            new_tag = Tag(start_index + end_index + 'cursive', start_index, end_index, stand_conf['font'],
                          stand_conf['size'],stand_conf['bold'], CURSIVE)
            text.tag_add(new_tag.getName(), new_tag.getStart(), new_tag.getEnd())
            text.tag_config(new_tag.getName(), font=new_tag.getFont())

            CURRENT_STYLE.addTag(new_tag)


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
root.title("Text Editor v.1.2")

root.minsize(width=500, height=500)
root.maxsize(width=500, height=500)

text = tkinter.Text(root, width=225, height=27, bg="white",
                    fg='black', wrap=WORD)

scrollb = Scrollbar(root, orient=VERTICAL, command=text.yview)
scrollb.pack(side="right", fill="y")
text.configure(yscrollcommand=scrollb.set)

toolbar = Frame(root)
toolbar.pack(side=TOP, fill=X)
# "Arial" ,
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

btn_bold = Button(toolbar, text="B", background="#555", foreground="#ccc",
                  command=click_bold)
btn_bold.pack(side=LEFT, padx=0, pady=0)

btn_cursive = Button(toolbar, text="I", background="#555", foreground="#ccc",
                     command=click_cursive)
btn_cursive.pack(side=LEFT, padx=0, pady=0)

label1 = Label(toolbar, text="Size text: 16") # ИЗМЕНИТЬ ОТОБРАЖЕНИЕ ТЕКУЩЕГО РАЗМЕРА ТЕКСТА
label1.pack(side=LEFT, padx=0, pady=0)

text.pack()

menuBar = tkinter.Menu(root)
# fileMenu = tkinter.Menu(menuBar)
vcsMenu = tkinter.Menu(menuBar)
branchMenu = tkinter.Menu(menuBar)

# fileMenu.add_command(label="New", command=new_file)
# fileMenu.add_command(label="Open", command=open_file)
# fileMenu.add_command(label="Save", command=saveTextStat)
# fileMenu.add_command(label="Save as", command=save_as)

vcsMenu.add_command(label="Commit", command=commit)
vcsMenu.add_command(label="Push", command=push)
vcsMenu.add_command(label="Reset", command=reset)
vcsMenu.add_command(label="Checkout", command=checkout)
vcsMenu.add_command(label="Show commit", command=showCommits)

branchMenu.add_command(label="New", command=createBranch)
branchMenu.add_command(label="Change", command=changeBranch)
# Save
# branchMenu.add_command(label="Save branch", command=saveBranch)
# branchMenu.add_command(label="Get", command=getBranch)


menuBar.add_cascade(label="VCS", menu=vcsMenu)
menuBar.add_cascade(label="Branch", menu=branchMenu)
menuBar.add_cascade(label="Info", command=info)
menuBar.add_cascade(label="Save", command=saveTextStat)
menuBar.add_cascade(label="Undo", command=Undo)
# menuBar.add_cascade(label="shortSaving", command=shortSaving)
# menuBar.add_cascade(label="showShortSaving", command=showShortSaving)
# menuBar.add_cascade(label="Show states", command=show_states)
menuBar.add_cascade(label="Delete tag", command=deleteAllTags)
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

if (CURRENT_BRANCH.getSize() > 0):
    text.insert(END, CURRENT_BRANCH.getHead().getSnapshot().get_text())
    CURRENT_STYLE = CURRENT_BRANCH.getHead().getSnapshot().get_style()
else:
    CURRENT_STYLE = Style()

upStyles() # ОБНОВЛЕНИЕ СТИЛЯ ,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,

editor = Editor(text.get('1.0', tkinter.END), style=CURRENT_STYLE)

caretaker = Caretaker(editor)
caretaker.backup()

# Добавление команд на нажатие клавиатуры
# root.bind('<Control-s>', saveTextStat)
# root.bind('<Control-z>', Undo)
root.bind('<Control-q>', infoStyle)
root.bind('<Control-w>', infoTags)


root.protocol('WM_DELETE_WINDOW', exit)
root.mainloop()
