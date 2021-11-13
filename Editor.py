from datetime import datetime
from abc import ABC, abstractmethod
from Styles import *

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
    def get_styles(self) -> []:
        pass


class Editor:
    def __init__(self, text='', styles=Style()):
        """Constructor"""
        self.text = text
        self.styles = styles # объект типа Styles
        # print(f"Editor: My initial text is: {self.text}")

    def setText(self, text):
        self.text = text

    def setStyles(self, styles):
        self.styles = styles

    def createSnapshot(self):
        return Snapshot(self, self.text, self.styles)

    def restore(self, memento: Memento) -> None:
        """
        Восстанавливает состояние Создателя из объекта снимка.
        """
        self.text = memento.get_text()
        self.styles = memento.get_styles()
        print(f"Originator: My text has changed to: {self.text}")


class Snapshot(Memento):
    editor = Editor()

    def __init__(self, editor, text, styles=[]):
        self.editor = editor
        self.text = text
        self.styles = styles
        self._date = str(datetime.now())[:19]

    def restore(self):
        self.editor.saveTextStat(self.text)
        self.editor.setStyles(self.styles)

    def get_text(self):
        return self.text

    def get_name(self):
        return f"{self.text} / ({self._date})"

    def get_styles(self):
        return self.styles

    def get_date(self) -> str:
        return self._date


