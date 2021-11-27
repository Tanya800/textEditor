from datetime import datetime

'''
    Классс Коммит - отвечает за создание и обработку одного коммита 
    Реализует функционал:
        - создание коммита
        - вывести все показатели коммита
        - вернуться к предыдущему коммиту
        - отобразить в какой ветке находится тот или иной коммит
'''


class Commit():

    def __init__(self, index=0, name='', snapshot='', branch='', parent=''):
        self.index = index
        self.name = name
        self.snapshot = snapshot
        self.branch = branch
        self.date = str(datetime.now())[:19]
        self.parent = parent

    def __eq__(self, other):
        res = True
        if self.index != other.index:
            res = False
        elif self.name != other.name:
            res = False
        elif self.date != other.date:
            res = False
        elif self.branch != other.branch:
            res = False
        elif self.parent != other.parent:
            res = False
        return res

    def setCommit(self, commit):
        self.index = commit.index
        self.name = commit.name
        self.snapshot = commit.snapshot
        self.branch = commit.branch
        self.date = commit.date
        self.parent = commit.parent

    def getIndex(self):
        return self.index

    def getName(self):
        return self.name

    def getInfo(self):
        return str(self.index) + " commit named " + self.name + " in " + self.date

    def getSnapshot(self):
        return self.snapshot

    def getParent(self):
        return self.parent

    def getAll(self):
        return {
            'index': self.index,
            'name': self.name,
            'snapshot': self.snapshot,
            'branch': self.branch,
            'date': self.date,
            'parent': self.parent,
        }
