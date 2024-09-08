from PySide6.QtCore import QSize
from PySide6.QtWidgets import QWidget


class LineNumberArea(QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.text_edit = editor

    def sizeHint(self):
        return QSize(self.text_edit.line_number_area_width(), 0)

    def paintEvent(self, event):
        self.text_edit.line_number_area_paint_event(event)