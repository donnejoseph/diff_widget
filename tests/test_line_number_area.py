import pytest
from PySide6.QtCore import QSize
from PySide6.QtWidgets import QApplication, QWidget

from app.widgets.line_number_area import LineNumberArea


@pytest.fixture(scope='module')
def app():
    """Fixture to create a QApplication instance."""
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    return app


@pytest.fixture
def mock_editor(qtbot, app):
    """Fixture to create a mock editor widget for testing."""
    editor = QWidget()

    # Define mock methods that return expected values
    def line_number_area_width():
        return 50

    def line_number_area_paint_event(event):
        pass

    # Attach mock methods to the editor object
    editor.line_number_area_width = line_number_area_width
    editor.line_number_area_paint_event = line_number_area_paint_event

    qtbot.addWidget(editor)
    return editor


@pytest.fixture
def line_number_area(mock_editor, qtbot):
    """Fixture to create an instance of LineNumberArea for testing."""
    area = LineNumberArea(mock_editor)
    qtbot.addWidget(area)
    return area


def test_initialization(line_number_area, mock_editor):
    """Test if the LineNumberArea initializes correctly with the editor reference."""
    assert line_number_area.text_edit == mock_editor


def test_size_hint(line_number_area):
    """Test if the sizeHint method returns the correct size."""
    expected_size = QSize(0, 0)
    assert line_number_area.sizeHint() == expected_size
