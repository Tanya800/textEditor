from datetime import datetime


class Commit():
    def __init__(self, index=0, name='', snapshot='', tree='', parent=''):
        self.index = index
        self.name = name
        self.snapshot = snapshot
        self.tree = tree
        self.date = str(datetime.now())[:19]
        self.parent = parent

    def setCommit(self, commit):
        self.index = commit.index
        self.name = commit.name
        self.snapshot = commit.snapshot
        self.tree = commit.tree
        self.date = commit.date
        self.parent = commit.parent

    def getAll(self):
        return {
            'index': self.index,
            'name': self.name,
            'snapshot': self.snapshot,
            'tree': self.tree,
            'date': self.date,
            'parent': self.parent,
        }
