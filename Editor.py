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

    @abstractmethod
    def get_size(self) -> int:
        pass

    @abstractmethod
    def get_front(self) -> str:
        pass

class Editor:
    def __init__(self, text='', size=6, front='Times',selectionWidth=0):
        """Constructor"""
        self.text = text
        self.size = size
        self.front = front
        self.selectionWidth = selectionWidth
        print(f"Editor: My initial text is: {self.text}")

    def setText(self,text):
        self.text=text

    def setSize(self,size):
        self.size=size

    def setFront(self,front):
        self.front=front

    def createSnapshot(self):
        return Snapshot(self,self.text,self.size,self.front,self.selectionWidth)

    def restore(self, memento: Memento) -> None:
        """
        Восстанавливает состояние Создателя из объекта снимка.
        """
        self.text = memento.get_text()
        self.size = memento.get_size()
        self.front = memento.get_front()
        print(f"Originator: My text has changed to: {self.text}")


class Snapshot(Memento):
    editor = Editor()

    def __init__(self,editor,text,size,front,selectionWidth):
        self.editor=editor
        self.size = size
        self.front = front
        self.text=text
        self._date=str(datetime.now())[:19]
        self.selectionWidth=selectionWidth

    def restore(self):
        self.editor.setText(self.text)
        self.editor.setSize(self.size)
        self.editor.setFront(self.front)

    def get_text(self):
        return self.text

    def get_name(self):
        return f"{self.text} / ({self._date})"

    def get_size(self):
        return self.size

    def get_front(self):
        return self.front

    def get_date(self) -> str:
        return self._date

