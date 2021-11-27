import tkinter.font as tkFont


class Style:
    def __init__(self, tags=[], font='Helvetica', size=16, bold="normal", cursive="roman"):
        """Constructor"""
        self.tags = tags
        self.size = size
        self.font = font
        self.bold = bold
        self.cursive = cursive
        # print(f"Styles: My initial font is: {self.font}")

    def setFont(self, font):

        old = self.font
        tags = self.tags
        index_tag = self.indexTagForUpdate('font',old)

        while index_tag!=-1:
            tags[index_tag].setFont(font)
            index_tag = self.indexTagForUpdate('font', old)

        self.tags = tags
        self.font = font

    def setSize(self, size):
        self.size = size

    def setBold(self, bold="bold"):
        self.bold = bold

    def setCursive(self, cursive="italic"):
        self.cursive = cursive

    def setTags(self, tags):
        self.tags = tags

    def getConfig(self):
        return {
            'font': self.font,
            'size': self.size,
            'bold': self.bold,
            'cursive': self.cursive
        }

    def getTags(self):
        return self.tags

    def getFont(self):
        return self.font

    def getSize(self):
        return self.size

    def getBold(self):
        return self.bold

    def getCursive(self):
        return self.cursive

    def addTag(self, tag):
        self.tags.append(tag)

    def searchTag(self, start_, end_, config, value):
        for i in range(len(self.tags)):
            if (self.tags[i].start_ == start_):
                if (self.tags[i].end_ == end_ and self.tags[i].getConfig()[config] == value):
                    return i
        return -1

    def findTag(self, start_, end_):
        for i in range(len(self.tags)):
            if (self.tags[i].start_ == start_):
                if self.tags[i].end_ == end_:
                    return i
        return -1

    def indexTagForUpdate(self,feature,old_value):

        for i in range(len(self.tags)):
            if self.tags[i].getConfig()[feature] == old_value:
                return i
        return -1


# ПРОВЕРКА ТЕГА НА УНИКАЛЬНОСТЬ. ТЕГ СОДЕРЖИТ ОДИН ОТЛИЧНЫЙ ПАРАМЕТР ИЛИ НЕСКОЛЬКО
    def tagIsUniqueWithoutOne(self, tag, feature):

        tag_conf = tag.getConfig()
        self_conf = self.getConfig()

        for ft in self_conf:
            if ft != feature and tag_conf[ft] != self_conf[ft]:
                return False
        return True

    def deleteTag(self, index):
        self.tags.pop(index)

    def updateTag(self, index, tag):
        self.tags[index] = tag


class Tag:
    def __init__(self, name="", start_=0, end_=0, font='Helvetica', size=16, bold="normal", cursive="roman"):
        """Constructor"""
        self.name = name
        self.start_ = start_
        self.end_ = end_
        self.size = size
        self.font = font
        self.bold = bold
        self.cursive = cursive
        # print(f"tag: My initial name is: {self.name}")

    def setFont(self, font):
        self.font = font

    def setSize(self, size):
        self.size = size

    def setBold(self, bold="bold"):
        self.bold = bold

    def setCursive(self, cursive="italic"):
        self.cursive = cursive

    def getConfig(self):
        return {
            'font': self.font,
            'size': self.size,
            'bold': self.bold,
            'cursive': self.cursive
        }

    def getName(self):
        return self.name

    def getStart(self):
        return self.start_

    def getEnd(self):
        return self.end_

    def getFamilies(self):
        return self.font

    def getSize(self):
        return self.size

    def getBold(self):
        return self.bold

    def getCursive(self):
        return self.cursive

    def getFont(self):
        return tkFont.Font(family=self.font, size=self.size, weight=self.bold, slant=self.cursive)
