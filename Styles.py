class Styles:
    def __init__(self, tags=[], size=6, font='Times'):
        """Constructor"""
        self.tags = tags
        self.size = size
        self.font = font
        print(f"Styles: My initial font is: {self.font}")

    def setFont(self,font):
        self.font=font

    def setSize(self,size):
        self.size=size

    def setTags(self,tags):
        self.tags=tags

    def addTags(self,tag):
        self.tags.append(tag)

class Tag:
    def __init__(self, index_start, index_end ,size,weight,slant, font='Times'):
        self.index_start = index_start
        self.index_end = index_end
        self.size = size
        self.weight = weight
        self.slant = slant
        self.font = font

    def getStart(self):
        return self.index_start

    def getEnd(self):
        return self.index_end

    def setStart(self,index):
        self.index_start=index

    def setEnd(self,index):
        self.index_end=index