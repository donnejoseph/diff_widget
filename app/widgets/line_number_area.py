from PySide6.QtCore import QSize
from PySide6.QtGui import QPaintEvent
from PySide6.QtWidgets import QWidget


class LineNumberArea(QWidget):
    """
    A widget to display line numbers for a code editor.
    """

    def __init__(self, editor: QWidget) -> None:
        """
        Initializes the LineNumberArea with a reference to the code editor.

        :param editor: The code editor widget to which the line number area is attached.
        """
        super().__init__(editor)
        self.text_edit: QWidget = editor

    def sizeHint(self) -> QSize:
        """
        Provides the recommended size for the line number area.

        :return: QSize object representing the suggested size.
        """
        # Ленивый импорт
        from app.widgets.code_editor import CodeEditor
        if isinstance(self.text_edit, CodeEditor):
            return QSize(self.text_edit.line_number_area_width(), 0)
        return QSize(0, 0)

    def paintEvent(self, event: QPaintEvent) -> None:
        """
        Handles the paint event for the line number area.

        :param event: The paint event object.
        """
        # Ленивый импорт
        from app.widgets.code_editor import CodeEditor
        if isinstance(self.text_edit, CodeEditor):
            self.text_edit.line_number_area_paint_event(event)
