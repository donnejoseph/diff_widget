import pytest
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QTextDocument, QColor, QTextCursor

from app.widgets.code_compare_widget import CodeCompareWidget


@pytest.fixture(scope='module')
def app():
    """Fixture to create a QApplication instance."""
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    return app


@pytest.fixture
def code_compare_widget(qtbot, app):
    """Fixture to create an instance of CodeCompareWidget for testing."""
    user_code = """def say_hello(name):
    name = name
    hello = 'hello '
    message = hello + name
    return message"""

    ai_code = """def say_hello(name):
    return f"hello {name}"""

    widget = CodeCompareWidget(user_code, ai_code)
    qtbot.addWidget(widget)
    return widget


def test_widget_initialization(code_compare_widget):
    """Test if the CodeCompareWidget initializes correctly."""
    assert code_compare_widget.left_text_edit.toPlainText() != ""
    assert code_compare_widget.right_text_edit.toPlainText() != ""


def test_correct_text_loaded(code_compare_widget):
    """Test if the correct text is loaded into the widget editors."""
    expected_user_code = """def say_hello(name):
    name = name
    hello = 'hello '
    message = hello + name
    return message"""

    expected_ai_code = """def say_hello(name):
    return f"hello {name}"""

    assert code_compare_widget.left_text_edit.toPlainText() == expected_user_code
    assert code_compare_widget.right_text_edit.toPlainText() == expected_ai_code


def test_highlight_differences(code_compare_widget):
    """Test if differences are highlighted correctly."""
    code_compare_widget.highlight_differences()

    left_document: QTextDocument = code_compare_widget.left_text_edit.document()
    right_document: QTextDocument = code_compare_widget.right_text_edit.document()

    # Check that some text has been highlighted in both documents
    assert left_document.toPlainText() != ""
    assert right_document.toPlainText() != ""

    # Improved way to check for highlighted text
    left_highlighted = False
    right_highlighted = False

    # Iterate through all text blocks in the left editor
    block = left_document.firstBlock()
    while block.isValid():
        cursor = QTextCursor(block)
        while not cursor.atBlockEnd():
            if cursor.charFormat().background().color() == QColor("green"):
                left_highlighted = True
                break
            cursor.movePosition(QTextCursor.NextCharacter)

        if left_highlighted:
            break
        block = block.next()

    # Iterate through all text blocks in the right editor
    block = right_document.firstBlock()
    while block.isValid():
        cursor = QTextCursor(block)
        while not cursor.atBlockEnd():
            if cursor.charFormat().background().color() == QColor("green"):
                right_highlighted = True
                break
            cursor.movePosition(QTextCursor.NextCharacter)

        if right_highlighted:
            break
        block = block.next()

    assert left_highlighted, "Expected highlighted differences in the left editor."
    assert right_highlighted, "Expected highlighted differences in the right editor."


def test_dark_theme_applied(code_compare_widget):
    """Test if the dark theme is applied properly."""
    # Update the expected stylesheet to match the actual one
    expected_stylesheet = """QWidget {
    background-color: #1e1f22;
}

QPlainTextEdit {
    background-color: #1e1e1e;
    color: #c5c8c6;
    font-family: 'Fira Code', Consolas, 'Courier New', monospace;
    font-size: 13pt;
    selection-background-color: #4e5b70;
}

QMenuBar {
    background-color: #2b2b2b;
    color: #ffffff;
    border: 1px solid #4e4e4e;
}

QMenuBar::item {
    background-color: #2b2b2b;
    color: #ffffff;
    padding: 4px 10px;
}

QMenuBar::item:selected {
    background-color: #3c3c3c;
}

QMenu {
    background-color: #2b2b2b;
    color: #ffffff;
    border: 1px solid #4e4e4e;
}

QMenu::item:selected {
    background-color: #3c3c3c;
}

QToolBar {
    background-color: #2b2b2b;
    border: 1px solid #4e4e4e;
}

QPushButton {
    background-color: #2b2b2b;
    color: #ffffff;
    border: 1px solid #4e4e4e;
}

QPushButton:hover {
    background-color: #3c3c3c;
}
"""
    assert code_compare_widget.styleSheet() == expected_stylesheet, "Dark theme stylesheet is not applied correctly."
