from pygments.lexers import PythonLexer
from pygments.token import Token
from PySide6.QtGui import QColor, QSyntaxHighlighter, QTextCharFormat, QFont, QPaintDevice


class PygmentsHighlighter(QSyntaxHighlighter):
    """
    A syntax highlighter using Pygments for Python code.
    """

    def __init__(self, document: QPaintDevice) -> None:
        """
        Initializes the syntax highlighter for the given document.

        :param document: The document to apply syntax highlighting to.
        """
        super().__init__(document)
        self.lexer: PythonLexer = PythonLexer()

    def highlightBlock(self, text: str) -> None:
        """
        Highlights the given text block by applying syntax highlighting rules.

        :param text: The text block to highlight.
        """
        tokens: list[tuple[Token, str]] = list(self.lexer.get_tokens(text))
        index: int = 0

        for token_type, value in tokens:
            length: int = len(value)
            if token_type in Token.Keyword:
                self.setFormat(index, length, self.get_format(QColor("#ff79c6"), bold=True))
            elif token_type in Token.Name.Function:
                self.setFormat(index, length, self.get_format(QColor("#61afef")))
            elif token_type in Token.String:
                self.setFormat(index, length, self.get_format(QColor("#f1fa8c")))
            elif token_type in Token.Comment:
                self.setFormat(index, length, self.get_format(QColor("#6272a4"), italic=True))
            index += length

    def get_format(self, color: QColor, bold: bool = False, italic: bool = False) -> QTextCharFormat:
        """
        Returns a text format with the specified color, boldness, and italicization.

        :param color: The color to use for the text.
        :param bold: Whether the text should be bold.
        :param italic: Whether the text should be italic.
        :return: QTextCharFormat object with the desired formatting.
        """
        char_format: QTextCharFormat = QTextCharFormat()
        char_format.setForeground(color)
        if bold:
            char_format.setFontWeight(QFont.Bold)
        if italic:
            char_format.setFontItalic(True)
        return char_format

