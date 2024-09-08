from typing import Optional
from PySide6.QtGui import QColor, QPainter, Qt, QTextCursor, QTextCharFormat
from PySide6.QtCore import QRect, QEvent
from PySide6.QtWidgets import QPlainTextEdit, QTextEdit

from app.widgets.line_number_area import LineNumberArea


class CodeEditor(QPlainTextEdit):
    """
    Code editor class with line numbers and current line highlighting.
    """

    def __init__(self, parent: Optional[QPlainTextEdit] = None) -> None:
        super(CodeEditor, self).__init__(parent)
        self.line_number_area: LineNumberArea = LineNumberArea(self)
        self.blockCountChanged.connect(self.update_line_number_area_width)
        self.updateRequest.connect(self.update_line_number_area)
        self.cursorPositionChanged.connect(self.highlight_current_line)
        self.update_line_number_area_width(0)

    def line_number_area_width(self) -> int:
        """
        Returns the width of the line number area.
        """
        digits: int = 1
        max_block: int = max(1, self.blockCount())
        while max_block >= 10:
            max_block //= 10
            digits += 1
        space: int = 3 + self.fontMetrics().horizontalAdvance('9') * digits
        return space

    def update_line_number_area_width(self, _: int) -> None:
        """
        Updates the width of the line number area.
        """
        self.setViewportMargins(self.line_number_area_width(), 0, 0, 0)

    def update_line_number_area(self, rect: QRect, dy: int) -> None:
        """
        Updates the line number area.
        """
        if dy:
            self.line_number_area.scroll(0, dy)
        else:
            self.line_number_area.update(0, rect.y(), self.line_number_area.width(), rect.height())

        if rect.contains(self.viewport().rect()):
            self.update_line_number_area_width(0)

    def resizeEvent(self, event: QEvent) -> None:
        """
        Handles the resize event of the editor.
        """
        super(CodeEditor, self).resizeEvent(event)
        cr: QRect = self.contentsRect()
        self.line_number_area.setGeometry(QRect(cr.left(), cr.top(), self.line_number_area_width(), cr.height()))

    def line_number_area_paint_event(self, event: QEvent) -> None:
        """
        Paints the line number area.
        """
        painter: QPainter = QPainter(self.line_number_area)
        painter.fillRect(event.rect(), QColor("#2b2b2b"))

        block = self.firstVisibleBlock()
        block_number: int = block.blockNumber()
        top: int = int(self.blockBoundingGeometry(block).translated(self.contentOffset()).top())
        bottom: int = top + int(self.blockBoundingRect(block).height())

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number: str = str(block_number + 1)
                painter.setPen(QColor("#d3d3d3"))
                painter.drawText(0, top, self.line_number_area.width(), self.fontMetrics().height(),
                                 Qt.AlignRight, number)

            block = block.next()
            top = bottom
            bottom = top + int(self.blockBoundingRect(block).height())
            block_number += 1

    def highlight_current_line(self) -> None:
        """
        Highlights the current line where the cursor is located.
        """
        extra_selections = []

        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection()
            line_color = QColor("#3c3c3c")
            selection.format.setBackground(line_color)
            selection.format.setProperty(QTextCharFormat.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extra_selections.append(selection)

        self.setExtraSelections(extra_selections)
