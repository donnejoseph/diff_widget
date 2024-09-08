from pygments.lexers import PythonLexer
from pygments.token import Token
from PySide6.QtGui import QColor, QSyntaxHighlighter, QTextCharFormat, QFont


class PygmentsHighlighter(QSyntaxHighlighter):
    def __init__(self, document):
        super().__init__(document)
        self.lexer = PythonLexer()

    def highlightBlock(self, text):
        tokens = list(self.lexer.get_tokens(text))
        index = 0
        for token_type, value in tokens:
            length = len(value)
            if token_type in Token.Keyword:
                self.setFormat(index, length, self.get_format(QColor("#ff79c6"), bold=True))
            elif token_type in Token.Name.Function:
                self.setFormat(index, length, self.get_format(QColor("#61afef")))
            elif token_type in Token.String:
                self.setFormat(index, length, self.get_format(QColor("#f1fa8c")))
            elif token_type in Token.Comment:
                self.setFormat(index, length, self.get_format(QColor("#6272a4"), italic=True))
            index += length

    def get_format(self, color, bold=False, italic=False):
        char_format = QTextCharFormat()
        char_format.setForeground(color)
        if bold:
            char_format.setFontWeight(QFont.Bold)
        if italic:
            char_format.setFontItalic(True)
        return char_format
