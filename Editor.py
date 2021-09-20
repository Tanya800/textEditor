from datetime import datetime
from abc import ABC, abstractmethod

class Memento(ABC):
    """
    Интерфейс Снимка предоставляет способ извлечения метаданных снимка, таких
    как дата создания или название. Однако он не раскрывает состояние Создателя.
    """

    @abstractmethod
    def get_name(self) -> str:
        pass

    @abstractmethod
    def get_date(self) -> str:
        pass

    @abstractmethod
    def get_text(self) -> str:
        pass


class Editor:
    def __init__(self, text='', curX=0, curY=0,selectionWidth=0):
        """Constructor"""
        self.text = text
        self.curX = curX
        self.curY = curY
        self.selectionWidth = selectionWidth
        print(f"Editor: My initial text is: {self.text}")

    def setText(self,text):
        self.text=text

    def setCursor(self,x,y):
        self.curX=x
        self.curY=y

    def createSnapshot(self):
        return Snapshot(self,self.text,self.curX,self.curY,self.selectionWidth)

    def restore(self, memento: Memento) -> None:
        """
        Восстанавливает состояние Создателя из объекта снимка.
        """
        self.text = memento.get_text()
        print(f"Originator: My text has changed to: {self.text}")


class Snapshot(Memento):
    editor = Editor()

    def __init__(self,editor,text,curX,curY,selectionWidth):
        self.editor=editor
        self.curX=curX
        self.curY=curY
        self.text=text
        self._date=str(datetime.now())[:19]
        self.selectionWidth=selectionWidth

    def restore(self):
        self.editor.setText(self.text)
        self.editor.setCursor(self.curX,self.curY)

    def get_text(self):
        return self.text

    def get_name(self):
        return f"{self.text} / ({self._date})"

    def get_date(self) -> str:
        return self._date

