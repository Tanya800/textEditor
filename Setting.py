'''
Класс по управлению проектом
Хранит в себе все ветки текущего проекта в файле проекта

'''

DEFAULT_BRANCHES = {
    'current': '.vsc/master.txt',
    'master': '.vsc/master.txt'
}


class Project:

    def __init__(self, name='', date='', branches=[]):
        self.name = name
        self.date = date
        self.branches = branches


    def getInfo(self):
        return "Project " + self.name + "was created " + self.date

    def getBranches(self):
        return self.branches

    def getFilenameBranch(self, nameBranch):
        return self.branches[nameBranch]

    def getCurrentBranch(self):
        return self.branches['current']

    def setCurrentBranch(self, name):
        self.branches['current'] = self.getFilenameBranch(name)

    def addBranch(self, name, filename):
        self.branches[name] = filename