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
    def get_style(self) -> Style:
        pass


class Editor:
    def __init__(self, text='', style=Style()):
        """Constructor"""
        self.text = text
        self.style = style # объект типа Styles
        # print(f"Editor: My initial text is: {self.text}")

    def setText(self, text):
        self.text = text

    def setStyle(self, style):
        self.style = style

    def createSnapshot(self):
        return Snapshot(self, self.text, self.style)

    def restore(self, memento: Memento) -> None:
        """
        Восстанавливает состояние Создателя из объекта снимка.
        """
        self.text = memento.get_text()
        self.style = memento.get_style()
        # print(f"Originator: My text has changed to: {self.text}")


class Snapshot(Memento):
    editor = Editor()

    def __init__(self, editor, text, style):
        self.editor = editor
        self.text = text
        self.style = style
        self._date = str(datetime.now())[:19]

    def restore(self):
        self.editor.setText(self.text)
        self.editor.setStyle(self.style)

    def get_text(self):
        return self.text

    def get_name(self):
        return f"{self.text} / ({self._date})"

    def get_style(self):
        return self.style

    def get_date(self) -> str:
        return self._date


