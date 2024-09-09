import os
import difflib
from typing import Optional

from PySide6.QtGui import QTextCursor, QColor, QTextCharFormat
from PySide6.QtWidgets import QWidget, QHBoxLayout

from app.widgets.code_editor import CodeEditor
from app.widgets.pygments_highlighter import PygmentsHighlighter
from app.app_logger import logger


class CodeCompareWidget(QWidget):
    """
    Widget for code comparison.
    """

    def __init__(self, user_code: str, ai_code: str, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)

        # Initialize code editors
        self.left_text_edit: CodeEditor = CodeEditor()
        self.right_text_edit: CodeEditor = CodeEditor()

        # Set initial text
        self.left_text_edit.setPlainText(user_code)
        self.right_text_edit.setPlainText(ai_code)

        # Create layout and add widgets
        self.layout: QHBoxLayout = QHBoxLayout()
        self.layout.addWidget(self.left_text_edit)
        self.layout.addWidget(self.right_text_edit)
        self.setLayout(self.layout)

        # Apply syntax highlighting
        self.highlighter_old: PygmentsHighlighter = PygmentsHighlighter(self.left_text_edit.document())
        self.highlighter_new: PygmentsHighlighter = PygmentsHighlighter(self.right_text_edit.document())

        # Set window size
        self.setMinimumSize(800, 600)
        self.showMaximized()

        # Set dark theme
        self.__set_dark_theme()

        # Automatically highlight differences
        self.highlight_differences()

    def __set_dark_theme(self) -> None:
        """
        Sets the dark theme.
        """
        stylesheet_path: str = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'resources', 'styles.qss')
        try:
            with open(stylesheet_path, "r") as file:
                self.setStyleSheet(file.read())
        except FileNotFoundError:
            logger.error(f"File not found: {stylesheet_path}")

    def highlight_differences(self) -> None:
        """
        Highlights the differences in the code.
        """
        # Get code lines from both editors
        left_text: list[str] = self.left_text_edit.toPlainText().split('\n')
        right_text: list[str] = self.right_text_edit.toPlainText().split('\n')

        # Create a matcher to find differences
        matcher: difflib.SequenceMatcher = difflib.SequenceMatcher(None, left_text, right_text)

        # Format for highlighting differences
        highlight_format: QTextCharFormat = QTextCharFormat()
        highlight_format.setBackground(QColor("green"))

        # Clear previous highlights
        self.__clear_highlight(self.left_text_edit)
        self.__clear_highlight(self.right_text_edit)

        # Process differences and apply highlighting
        for tag, i1, i2, j1, j2 in matcher.get_opcodes():
            if tag in ('replace', 'delete'):
                self.__highlight_lines(self.left_text_edit, i1, i2, highlight_format)
            if tag in ('replace', 'insert'):
                self.__highlight_lines(self.right_text_edit, j1, j2, highlight_format)

    def __clear_highlight(self, text_edit: CodeEditor) -> None:
        """
        Clears the highlight in the specified editor.
        """
        cursor: QTextCursor = QTextCursor(text_edit.document())
        cursor.select(QTextCursor.Document)
        cursor.setCharFormat(QTextCharFormat())

    def __highlight_lines(self, text_edit: CodeEditor, start: int, end: int, format: QTextCharFormat) -> None:
        """
        Highlights the specified lines in the specified editor.
        """
        cursor: QTextCursor = QTextCursor(text_edit.document())
        for line in range(start, end):
            block = cursor.document().findBlockByNumber(line)
            if block.isValid():
                cursor.setPosition(block.position())
                cursor.movePosition(QTextCursor.EndOfBlock, QTextCursor.KeepAnchor)
                cursor.mergeCharFormat(format)
