import os
import difflib
from PySide6.QtGui import QTextCursor, QColor, QTextCharFormat
from PySide6.QtWidgets import QWidget, QHBoxLayout

from app.widgets.code_editor import CodeEditor
from app.widgets.pygments_highlighter import PygmentsHighlighter
from app.app_logger import logger



class CodeCompareWidget(QWidget):
    """
    Widget for code comparison.
    """

    def __init__(self, user_code: str, ai_code: str, parent=None):
        super().__init__(parent)

        # Инициализация редакторов кода
        self.left_text_edit = CodeEditor()
        self.right_text_edit = CodeEditor()

        # Установка начального текста
        self.left_text_edit.setPlainText(user_code)
        self.right_text_edit.setPlainText(ai_code)

        # Создание компоновки и добавление виджетов
        self.layout = QHBoxLayout()
        self.layout.addWidget(self.left_text_edit)
        self.layout.addWidget(self.right_text_edit)
        self.setLayout(self.layout)

        # Применение подсветки синтаксиса
        self.highlighter_old = PygmentsHighlighter(self.left_text_edit.document())
        self.highlighter_new = PygmentsHighlighter(self.right_text_edit.document())

        # Установка размера окна
        self.setFixedSize(1000, 600)

        # Установка темной темы
        self.__set_dark_theme()

        # Автоматическая подсветка различий
        self.highlight_differences()

    def __set_dark_theme(self):
        """
        Sets the dark theme.
        """
        stylesheet_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'resources', 'styles.qss')
        try:
            with open(stylesheet_path, "r") as file:
                self.setStyleSheet(file.read())
        except FileNotFoundError:
            logger.error(f"File not found: {stylesheet_path}")

    def highlight_differences(self):
        """
        Highlights the differences in the code.
        """
        # Получаем строки кода из обоих редакторов
        left_text = self.left_text_edit.toPlainText().split('\n')
        right_text = self.right_text_edit.toPlainText().split('\n')

        # Создаем matcher для поиска различий
        matcher = difflib.SequenceMatcher(None, left_text, right_text)

        # Формат подсветки различий
        highlight_format = QTextCharFormat()
        highlight_format.setBackground(QColor("green"))

        # Очистка предыдущих выделений
        self.__clear_highlight(self.left_text_edit)
        self.__clear_highlight(self.right_text_edit)

        # Обработка различий и подсветка
        for tag, i1, i2, j1, j2 in matcher.get_opcodes():
            if tag in ('replace', 'delete'):
                self.__highlight_lines(self.left_text_edit, i1, i2, highlight_format)
            if tag in ('replace', 'insert'):
                self.__highlight_lines(self.right_text_edit, j1, j2, highlight_format)

    def __clear_highlight(self, text_edit):
        """
        Clears the highlight in the specified editor.
        """
        cursor = QTextCursor(text_edit.document())
        cursor.select(QTextCursor.Document)
        cursor.setCharFormat(QTextCharFormat())

    def __highlight_lines(self, text_edit, start, end, format):
        """
        Highlights the specified lines in the specified editor.
        """
        cursor = QTextCursor(text_edit.document())
        for line in range(start, end):
            block = cursor.document().findBlockByNumber(line)
            if block.isValid():
                cursor.setPosition(block.position())
                cursor.movePosition(QTextCursor.EndOfBlock, QTextCursor.KeepAnchor)
                cursor.mergeCharFormat(format)




