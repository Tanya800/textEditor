'''
    Классс Ветка - отвечает за сохранение последовательности коммитов в единой ветке
    Реализует функционал:
        - отображение всех коммитов
        - установление указателя на выбранный коммит
        - отображение коммита, на который выставлен указатель
        - сохранение ветки
        - установление ветки
        - обновить ветки для добавления нового коммита в конец последовательности
'''
import pickle


class Branch:

    def __init__(self, name='', size=0, head=0, commits=[]):
        self.name = name
        self.size = size
        self.head = head  # ИНДЕКС КОММИТА В МАССИВЕ КОММИТОВ
        self.commits = commits
        if self.name != '':
            print(f"Branch was created: {self.name}")

    def getName(self):
        return self.name

    def getCommits(self):
        return self.commits

    def getSize(self):
        return self.size

    def getHead(self):
        return self.commits[self.head]

    def getIndexCommit(self, commit):
        commits = self.getCommits()
        for i in range(len(commits)):
            if commits[i].getName() == commit:
                return i
        return -1

    def setSize(self, size):
        self.size = size

    def setHead(self, index):
        self.head = index

    def appendCommits(self, commit):
        self.commits.append(commit)

    def addCommit(self, commit):
        self.appendCommits(commit)
        self.setHead(self.size)
        self.size += 1

    ''' МЕТОДЫ ДЛЯ РАБОТЫ СO СЧИТЫВАНИЕМ ВЕТКИ ИЗ ФАЙЛА'''

    def saveBranch(self, fileName):
        out = open(fileName, 'wb')
        pickle.dump(self, out)
        out.close()
        print('Branch was saved: {}'.format(self.name))

    def getBranch(self, fileName):

        try:
            out = open(fileName, 'rb')
            newBranch = pickle.load(out)
            out.close()
        except EOFError:
            return -1
        except FileNotFoundError:
            out = open(fileName, 'wb+')
            out.close()
            return -2

        self.name = newBranch.name
        self.size = newBranch.size
        self.head = newBranch.head
        self.commits = newBranch.commits
        # print('Branch was read: {}'.format(self.name))
        return 1
