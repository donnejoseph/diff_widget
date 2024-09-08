import pytest
from PySide6.QtGui import QTextDocument, QColor, QFont
from app.widgets.pygments_highlighter import PygmentsHighlighter


@pytest.fixture
def text_document():
    """Fixture to create a QTextDocument for testing."""
    return QTextDocument()


@pytest.fixture
def highlighter(text_document):
    """Fixture to create an instance of PygmentsHighlighter for testing."""
    return PygmentsHighlighter(text_document)


def test_initialization(highlighter, text_document):
    """Test if the PygmentsHighlighter initializes correctly with the document."""
    assert highlighter.document() == text_document


def test_highlight_keywords(highlighter):
    """Test if keywords are highlighted correctly."""
    highlighter.highlightBlock("def function():")
    char_format = highlighter.get_format(QColor("#ff79c6"), bold=True)
    assert char_format.fontWeight() == QFont.Bold
    assert char_format.foreground().color().name() == "#ff79c6"


def test_highlight_function_names(highlighter):
    """Test if function names are highlighted correctly."""
    highlighter.highlightBlock("def function():")
    char_format = highlighter.get_format(QColor("#61afef"))
    assert char_format.foreground().color().name() == "#61afef"


def test_highlight_strings(highlighter):
    """Test if strings are highlighted correctly."""
    highlighter.highlightBlock('print("Hello, World!")')
    char_format = highlighter.get_format(QColor("#f1fa8c"))
    assert char_format.foreground().color().name() == "#f1fa8c"


def test_highlight_comments(highlighter):
    """Test if comments are highlighted correctly."""
    highlighter.highlightBlock("# This is a comment")
    char_format = highlighter.get_format(QColor("#6272a4"), italic=True)
    assert char_format.fontItalic() is True
    assert char_format.foreground().color().name() == "#6272a4"


def test_get_format(highlighter):
    """Test if the get_format method returns the correct QTextCharFormat."""
    char_format = highlighter.get_format(QColor("#ff79c6"), bold=True, italic=True)
    assert char_format.foreground().color().name() == "#ff79c6"
    assert char_format.fontWeight() == QFont.Bold
    assert char_format.fontItalic() is True
