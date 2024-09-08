import pytest
from PySide6.QtGui import QColor, QPaintEvent, QTextCursor
from PySide6.QtCore import QRect
from PySide6.QtWidgets import QApplication

from app.widgets.code_editor import CodeEditor


@pytest.fixture(scope='module')
def app():
    """Fixture to create a QApplication instance."""
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    return app


@pytest.fixture
def code_editor(qtbot, app):
    """Fixture to create an instance of CodeEditor for testing."""
    editor = CodeEditor()
    qtbot.addWidget(editor)
    return editor


def test_initialization(code_editor):
    """Test if the CodeEditor initializes correctly."""
    assert code_editor.line_number_area is not None
    assert code_editor.line_number_area.parent() == code_editor


def test_line_number_area_width(code_editor):
    """Test the width calculation for the line number area."""
    code_editor.setPlainText("\n" * 10)
    assert code_editor.line_number_area_width() >= 4


def test_update_line_number_area_width(code_editor, qtbot):
    """Test if the line number area width is updated correctly."""
    initial_width = code_editor.line_number_area_width()
    code_editor.setPlainText("\n" * 100)
    qtbot.wait(100)
    updated_width = code_editor.line_number_area_width()
    assert updated_width > initial_width


def test_highlight_current_line(code_editor, qtbot):
    """Test if the current line is highlighted correctly."""
    code_editor.setPlainText("Line 1\nLine 2\nLine 3")
    code_editor.moveCursor(QTextCursor.End)
    qtbot.wait(100)  # Wait for the cursor position change
    selections = code_editor.extraSelections()
    assert len(selections) > 0
    assert selections[0].format.background().color() == QColor("#3c3c3c")


def test_line_number_area_paint_event(code_editor):
    """Test the painting of the line number area."""
    event = QPaintEvent(QRect(0, 0, 100, 100))
    code_editor.line_number_area_paint_event(event)
