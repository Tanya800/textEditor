'''
    Классс Ветка - отвечает за сохранение последовательности коммитов в единой ветке
    Реализует функционал:
        - отображение всех коммитов
        - установление указателя на выбранный коммит
        - отображение коммита, на который выставлен указатель ---------РЕАЛИЗОВАТь
        - сохранение ветки
        - установление ветки
        - обновить ветки для добавления нового коммита в конец последовательности
'''
import pickle


class Branch:

    def __init__(self, name='', head='', commits=[]):
        self.name = name
        self.head = head
        self.commits = commits
        print(f"Branch was created: {self.name}")

    def getCommits(self):
        return self.commits

    def getHead(self):
        return self.head

    def setHead(self, index):
        self.head = self.commits[index]

    def addCommit(self, commit):
        self.commits.append(commit)

    def updateBranch(self, commit):
        self.addCommit(self, commit)
        self.setHead(self, commit.index)

    def saveBranch(self, fileName):
        out = open(fileName, 'wb')
        pickle.dump(self, out)
        out.close()
        print('Branch was saved: {}'.format(self.name))

    def getBranch(self, fileName):
        out = open(fileName, 'rb')
        newBranch = pickle.load(out)
        out.close()

        self.name = newBranch.name
        self.head = newBranch.head
        self.commits = newBranch.commits
        print('Branch was read: {}'.format(self.name))
